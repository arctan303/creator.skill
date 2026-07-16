#!/usr/bin/env python3
"""验证 creator.skill 三套发布包的结构、版本与平台转换质量。"""

import json
import re
import zipfile
from pathlib import Path
from typing import List, Set


REPO_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = REPO_ROOT / "dist"
SOURCE_VERSION = (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()


def fail(message: str):
    raise SystemExit(f"验证失败: {message}")


def read_text(archive: zipfile.ZipFile, name: str) -> str:
    return archive.read(name).decode("utf-8")


def verify_release_structure(
    zip_path: Path,
    instruction_file: str,
    skill_prefix: str,
    signal_file: str,
    expected_platform: str,
):
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        required = {
            instruction_file,
            "EVOLUTION.md",
            signal_file,
            ".creator-manifest.json",
            ".version",
        }
        missing = sorted(required - names)
        if missing:
            fail(f"{zip_path.name} 缺少关键文件: {', '.join(missing)}")

        manifest = json.loads(read_text(archive, ".creator-manifest.json"))
        if manifest.get("schema_version") != 1:
            fail(f"{zip_path.name} manifest schema_version 不支持")
        if manifest.get("workflow") != "creator.skill":
            fail(f"{zip_path.name} manifest workflow 不正确")

        expected_skills = sorted(manifest.get("skills", []))
        actual_skills = sorted(
            name[len(skill_prefix) :].split("/", 1)[0]
            for name in names
            if name.startswith(skill_prefix) and name.endswith("/SKILL.md")
        )
        if not expected_skills:
            fail(f"{zip_path.name} manifest 没有声明任何 Skill")
        if len(expected_skills) != len(set(expected_skills)):
            fail(f"{zip_path.name} manifest 包含重复 Skill")
        if actual_skills != expected_skills:
            fail(
                f"{zip_path.name} Skill 清单不一致: "
                f"manifest={expected_skills}, package={actual_skills}"
            )
        if manifest.get("skill_count") != len(expected_skills):
            fail(f"{zip_path.name} manifest skill_count 与 skills 列表不一致")

        version = read_text(archive, ".version").strip()
        if manifest.get("version") != version:
            fail(f"{zip_path.name} manifest version 与 .version 不一致")
        if version != SOURCE_VERSION:
            fail(f"{zip_path.name} 版本 {version} 与源码 VERSION {SOURCE_VERSION} 不一致")
        if manifest.get("platform") != expected_platform:
            fail(f"{zip_path.name} manifest platform 不正确")
        if manifest.get("skill_root") != skill_prefix.rstrip("/"):
            fail(f"{zip_path.name} manifest skill_root 不正确")

        signals = read_text(archive, signal_file)
        for field in ("关联规则", "问题类别", "次数", "严重度", "状态"):
            if field not in signals:
                fail(f"{zip_path.name} 信号模板缺少字段: {field}")

        print(
            f"  OK: {zip_path.name} 包含 {len(expected_skills)} 个 Skill，"
            f"平台={expected_platform}，版本={version}"
        )
        return manifest, names


def assert_no_residue(label: str, text: str, patterns: List[str]):
    for pattern in patterns:
        lines = [
            index + 1
            for index, line in enumerate(text.splitlines())
            if pattern in line
        ]
        if lines:
            fail(f"{label} 残留 {pattern!r}，行号: {lines}")
        print(f"  OK: {label} 无 {pattern!r} 残留")


def verify_claude_conversion(manifest: dict, names: Set[str]):
    zip_path = DIST_DIR / "creator.claude.zip"
    with zipfile.ZipFile(zip_path) as archive:
        claude_md = read_text(archive, "CLAUDE.md")
        evolution_md = read_text(archive, "EVOLUTION.md")

        print("=== Claude Code 平台转换检查 ===")
        assert_no_residue(
            "CLAUDE.md", claude_md, [".codex/", ".agents/skills/", "AGENTS.md"]
        )
        assert_no_residue("EVOLUTION.md", evolution_md, [".codex/", "AGENTS.md"])
        for expected in ("CLAUDE.md", ".claude/", ".claude/skills/"):
            if expected not in claude_md:
                fail(f"CLAUDE.md 缺少预期平台引用: {expected}")
            print(f"  OK: CLAUDE.md 包含 {expected!r}")

        command_files = sorted(
            name
            for name in names
            if name.startswith(".claude/commands/") and name.endswith(".md")
        )
        if len(command_files) != manifest["skill_count"]:
            fail(
                "Claude command 数量与 Skill 数量不一致: "
                f"commands={len(command_files)}, skills={manifest['skill_count']}"
            )

        print("=== Claude commands 检查 ===")
        for command_file in command_files:
            content = read_text(archive, command_file)
            prompt_body = content.split("---")[-1].split("$ARGUMENTS")[0]
            if re.search(r"\$[a-zA-Z][\w-]*", prompt_body):
                fail(f"{command_file} 残留 Codex $skill 语法")
            if "$ARGUMENTS" not in content:
                fail(f"{command_file} 缺少 $ARGUMENTS")
            print(f"  OK: {Path(command_file).name}")


def verify_gateway():
    zip_path = DIST_DIR / "creator-gateway.zip"
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
        required = {"SKILL.md", "references/cli-adapters.md", "agents/openai.yaml"}
        missing = sorted(required - names)
        if missing:
            fail(f"{zip_path.name} 缺少关键文件: {', '.join(missing)}")
    print(f"  OK: {zip_path.name} 网关结构完整")


def main():
    print("=== 发布包结构检查 ===")
    verify_release_structure(
        DIST_DIR / "creator.codex.zip",
        "AGENTS.md",
        ".agents/skills/",
        ".codex/evolution/signals.md",
        "codex",
    )
    claude_manifest, claude_names = verify_release_structure(
        DIST_DIR / "creator.claude.zip",
        "CLAUDE.md",
        ".claude/skills/",
        ".claude/evolution/signals.md",
        "claude-code",
    )
    verify_claude_conversion(claude_manifest, claude_names)
    verify_gateway()
    print("\n全部发布包验证通过。")


if __name__ == "__main__":
    main()
