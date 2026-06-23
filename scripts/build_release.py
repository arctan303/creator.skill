#!/usr/bin/env python3
"""
build_release.py — 从 creator.skill 源仓库生成三套释放包。

产物：
  dist/creator.codex.zip   — Codex 工作空间初始化包
  dist/creator.claude.zip  — Claude Code 工作空间初始化包
  dist/creator-gateway.zip — 网关 Skill 安装包

用法：
  python scripts/build_release.py
"""

import os
import re
import shutil
import zipfile
from typing import List
from datetime import date
from pathlib import Path

# ── 路径 ──────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = REPO_ROOT / "dist"
SKILLS_SRC = REPO_ROOT / ".agents" / "skills"
GATEWAY_SRC = REPO_ROOT / "gateway"

# ── 中文命令名映射（skill-name → 命令文件名） ─────────────────────────
# 构建时从 openai.yaml 读取 description 和 prompt，此处仅定义命令文件名

COMMAND_NAMES = {
    "product-spec-builder": "需求",
    "design-brief-builder": "设计规范",
    "design-maker": "设计制图",
    "dev-planner": "开发计划",
    "dev-builder": "项目开发",
    "release-builder": "发布准备",
    "bug-fixer": "修复缺陷",
    "reviewer": "代码审查",
    "goal-writer": "Goal生成",
    "self-evolver": "自进化",
    "skill-builder": "技能构建",
}


# ── 工具函数 ──────────────────────────────────────────────────────────


def clean_dist():
    """清理并重建 dist 目录。"""
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)


def read_version() -> str:
    """从 VERSION 文件读取版本号，不存在时回退到当前日期。"""
    version_file = REPO_ROOT / "VERSION"
    if version_file.exists():
        return version_file.read_text(encoding="utf-8").strip()
    return date.today().strftime("%Y.%m.%d")


def parse_openai_yaml(yaml_path: Path) -> dict:
    """简易解析 openai.yaml，提取 display_name / short_description / default_prompt。

    文件格式固定，不引入 PyYAML 依赖。
    """
    result = {}
    text = yaml_path.read_text(encoding="utf-8")
    for line in text.splitlines():
        line = line.strip()
        for key in ("display_name", "short_description", "default_prompt"):
            if line.startswith(f"{key}:"):
                # 去掉 key: 前缀，去掉引号
                value = line[len(key) + 1 :].strip().strip('"').strip("'")
                result[key] = value
    return result


def convert_agents_to_claude(text: str) -> str:
    """将 AGENTS.md 内容转换为 CLAUDE.md 格式。

    替换规则（仅路径和 CLI 名称，不改动业务逻辑）：
    1. AGENTS.md → CLAUDE.md
    2. .agents/skills/ → .claude/skills/
    3. .codex/ → .claude/
    4. Codex → Claude Code（仅独立出现的 CLI 名称）
    """
    result = text

    # 先替换路径（顺序重要，避免二次替换）
    result = result.replace("AGENTS.md", "CLAUDE.md")
    result = result.replace(".agents/skills/", ".claude/skills/")
    result = result.replace(".codex/", ".claude/")

    # 替换 CLI 名称：仅匹配独立的 "Codex"（前面不是 . / 字母）
    result = re.sub(r"(?<!\.)(?<!/)(?<!\w)Codex(?!\w)", "Claude Code", result)

    return result


def generate_command_md(description: str, prompt: str) -> str:
    """生成一个 Claude Code slash command 的 md 文件内容。"""
    # 去掉 prompt 中的 $skill-name 格式（Codex 专属语法），替换为纯名称
    clean_prompt = re.sub(r"\$(\S+)", r"\1", prompt)
    return (
        f"---\n"
        f'description: "{description}"\n'
        f"---\n"
        f"\n"
        f"{clean_prompt}\n"
        f"\n"
        f"$ARGUMENTS\n"
    )


def zip_directory(source_dir: Path, zip_path: Path):
    """将目录内容打包成 zip，保留目录结构但不含顶层目录名。"""
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(source_dir.rglob("*")):
            if file_path.is_file():
                arcname = file_path.relative_to(source_dir)
                zf.write(file_path, arcname)


def discover_skills() -> List[str]:
    """自动发现所有 skill 目录（含 SKILL.md 的子目录）。"""
    skills = []
    for d in sorted(SKILLS_SRC.iterdir()):
        if d.is_dir() and (d / "SKILL.md").exists():
            skills.append(d.name)
    return skills


# ── 构建 Codex 包 ────────────────────────────────────────────────────


def build_codex(skills: List[str], version: str):
    """构建 creator.codex.zip。"""
    print("=== 构建 Codex 包 ===")
    stage = DIST_DIR / "stage-codex"
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)

    # 复制 AGENTS.md
    shutil.copy2(REPO_ROOT / "AGENTS.md", stage / "AGENTS.md")
    print("  ✓ AGENTS.md")

    # 复制 EVOLUTION.md
    shutil.copy2(REPO_ROOT / "EVOLUTION.md", stage / "EVOLUTION.md")
    print("  ✓ EVOLUTION.md")

    # 复制 .agents/skills/（完整目录）
    dest_skills = stage / ".agents" / "skills"
    for skill_name in skills:
        src = SKILLS_SRC / skill_name
        dst = dest_skills / skill_name
        shutil.copytree(src, dst)
    print(f"  ✓ .agents/skills/ ({len(skills)} skills)")

    # 写入 .version
    (stage / ".version").write_text(version, encoding="utf-8")
    print(f"  ✓ .version ({version})")

    # 打包
    zip_path = DIST_DIR / "creator.codex.zip"
    zip_directory(stage, zip_path)
    print(f"  ✓ 打包完成: {zip_path.name}")

    # 清理暂存
    shutil.rmtree(stage)


# ── 构建 Claude 包 ───────────────────────────────────────────────────


def build_claude(skills: List[str], version: str):
    """构建 creator.claude.zip。"""
    print("\n=== 构建 Claude 包 ===")
    stage = DIST_DIR / "stage-claude"
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)

    # 转换 AGENTS.md → CLAUDE.md
    agents_text = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    claude_text = convert_agents_to_claude(agents_text)
    (stage / "CLAUDE.md").write_text(claude_text, encoding="utf-8")
    print("  ✓ CLAUDE.md（已转换）")

    # 复制 EVOLUTION.md（也需要转换路径引用）
    evo_text = (REPO_ROOT / "EVOLUTION.md").read_text(encoding="utf-8")
    evo_claude = convert_agents_to_claude(evo_text)
    (stage / "EVOLUTION.md").write_text(evo_claude, encoding="utf-8")
    print("  ✓ EVOLUTION.md（已转换）")

    # 复制 skills 到 .claude/skills/（去除 agents/ 目录）
    dest_skills = stage / ".claude" / "skills"
    for skill_name in skills:
        src = SKILLS_SRC / skill_name
        dst = dest_skills / skill_name
        shutil.copytree(src, dst)
        # 删除 agents/ 目录（包含 openai.yaml，Claude Code 不使用）
        agents_dir = dst / "agents"
        if agents_dir.exists():
            shutil.rmtree(agents_dir)
    print(f"  ✓ .claude/skills/ ({len(skills)} skills, 已去除 openai.yaml)")

    # 从 openai.yaml 动态生成 .claude/commands/
    commands_dir = stage / ".claude" / "commands"
    commands_dir.mkdir(parents=True, exist_ok=True)
    cmd_count = 0
    for skill_name in skills:
        yaml_path = SKILLS_SRC / skill_name / "agents" / "openai.yaml"
        if not yaml_path.exists():
            continue
        cmd_name = COMMAND_NAMES.get(skill_name)
        if not cmd_name:
            print(f"  ⚠ 跳过 {skill_name}：未配置中文命令名")
            continue
        info = parse_openai_yaml(yaml_path)
        description = info.get("short_description", "")
        prompt = info.get("default_prompt", "")
        cmd_file = commands_dir / f"{cmd_name}.md"
        cmd_file.write_text(generate_command_md(description, prompt), encoding="utf-8")
        cmd_count += 1
    print(f"  ✓ .claude/commands/ ({cmd_count} commands)")

    # 预建 .claude/evolution/signals.md
    evo_dir = stage / ".claude" / "evolution"
    evo_dir.mkdir(parents=True, exist_ok=True)
    (evo_dir / "signals.md").write_text(
        "# 自进化信号\n\n暂无待处理信号。\n", encoding="utf-8"
    )
    print("  ✓ .claude/evolution/signals.md")

    # 写入 .version
    (stage / ".version").write_text(version, encoding="utf-8")
    print(f"  ✓ .version ({version})")

    # 打包
    zip_path = DIST_DIR / "creator.claude.zip"
    zip_directory(stage, zip_path)
    print(f"  ✓ 打包完成: {zip_path.name}")

    # 清理暂存
    shutil.rmtree(stage)


# ── 构建 Gateway 包 ──────────────────────────────────────────────────


def build_gateway():
    """构建 creator-gateway.zip。"""
    print("\n=== 构建 Gateway 包 ===")
    stage = DIST_DIR / "stage-gateway"
    if stage.exists():
        shutil.rmtree(stage)

    # 直接复制 gateway/ 目录
    shutil.copytree(GATEWAY_SRC, stage)
    print("  ✓ gateway/ 内容已复制")

    # 打包
    zip_path = DIST_DIR / "creator-gateway.zip"
    zip_directory(stage, zip_path)
    print(f"  ✓ 打包完成: {zip_path.name}")

    # 清理暂存
    shutil.rmtree(stage)


# ── 主函数 ────────────────────────────────────────────────────────────


def main():
    version = read_version()
    print(f"creator.skill 发布构建 — 版本 {version}")
    print(f"仓库根目录: {REPO_ROOT}")
    print(f"输出目录: {DIST_DIR}\n")

    # 验证源文件
    if not SKILLS_SRC.exists():
        print(f"错误: 找不到 skills 目录 {SKILLS_SRC}")
        return 1
    if not GATEWAY_SRC.exists():
        print(f"错误: 找不到 gateway 目录 {GATEWAY_SRC}")
        return 1

    # 自动发现 skills
    skills = discover_skills()
    if not skills:
        print("错误: 没有发现任何 Skill")
        return 1
    print(f"发现 {len(skills)} 个 Skill: {', '.join(skills)}\n")

    # 检查命令名映射完整性
    unmapped = [s for s in skills if s not in COMMAND_NAMES]
    if unmapped:
        print(f"警告: 以下 Skill 未配置中文命令名，Claude commands 将跳过: {', '.join(unmapped)}")

    clean_dist()
    build_codex(skills, version)
    build_claude(skills, version)
    build_gateway()

    # 汇总
    print("\n=== 构建完成 ===")
    for f in sorted(DIST_DIR.glob("*.zip")):
        size_kb = f.stat().st_size / 1024
        print(f"  {f.name} ({size_kb:.1f} KB)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
