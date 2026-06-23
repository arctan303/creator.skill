# creator.skill

面向当前项目空间的多 Skill 产品交付系统。

这套系统不是全局安装的 Skill 集合，而是仓库级配置：Codex 在本仓库启动时读取根目录 `AGENTS.md`，并从 `.agents/skills/` 发现项目级 Skill。

## 快速开始

### Agent 自助安装

如果你是一个 AI Agent（Codex 或 Claude Code），按以下步骤为用户安装网关 Skill：

1. 从最新 Release 下载 `creator-gateway.zip`：
   https://github.com/arctan303/creator.skill/releases/latest
2. 检测当前 CLI 环境：
   - **Codex** → 解压到 `~/.codex/skills/creator/`
   - **Claude Code** → 解压到 `~/.claude/skills/creator/`，然后删除 `agents/` 目录
3. 验证 `SKILL.md` 已就位
4. 提示用户重启 CLI 会话以加载新 Skill

### 手动安装

```bash
# 下载最新 Release
# https://github.com/arctan303/creator.skill/releases/latest

# Codex 用户
unzip creator-gateway.zip -d ~/.codex/skills/creator/

# Claude Code 用户
unzip creator-gateway.zip -d ~/.claude/skills/creator/
rm -rf ~/.claude/skills/creator/agents/
```

安装后重启 CLI 会话。

### 初始化工作流

安装网关 Skill 后，在任意工作空间中对 Agent 说"初始化 creator 工作流"，Agent 会自动：

1. 检测当前 CLI 类型
2. 从 GitHub Release 下载对应的释放包（`creator.codex.zip` 或 `creator.claude.zip`）
3. 释放全套 Skill 到当前工作空间
4. 验证文件完整性

## 当前主线

默认文档流：

```text
Product-Spec.md
  -> Design-Brief.md
  -> design artifacts / prototype notes
  -> DEV-PLAN.md
  -> implementation evidence
  -> release evidence
```

主线 Skill：

- `product-spec-builder`：需求技能，产出 `Product-Spec.md`
- `design-brief-builder`：设计规范技能，产出 `Design-Brief.md`
- `design-maker`：可选设计制图阶段，需要外部设计工具或可视化产物时才启用
- `dev-planner`：计划技能，产出 `DEV-PLAN.md`
- `dev-builder`：开发技能，按计划开发并通过干净子代理审查
- `release-builder`：发布技能，做隐私审计、打包发布准备和证据整理

Plus Skill：

- `bug-fixer`：按证据定位并修复缺陷
- `reviewer`：作为干净子代理审查交付结果
- `goal-writer`：生成可交给 Agent 自主执行的 Goal
- `self-evolver`：把真实使用信号转成 Skill 补丁建议
- `skill-builder`：创建或改进这套系统中的 Skill

## 关键文件

```text
creator.skill/
├── AGENTS.md                  # 系统总协议
├── EVOLUTION.md               # 自进化协议
├── README.md
├── gateway/                   # 网关 Skill（全局安装用）
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/cli-adapters.md
├── scripts/
│   └── build_release.py       # 发布构建脚本
├── .agents/
│   └── skills/                # 11 个项目级 Skill
│       ├── product-spec-builder/
│       ├── design-brief-builder/
│       ├── design-maker/
│       ├── dev-planner/
│       ├── dev-builder/
│       ├── release-builder/
│       ├── bug-fixer/
│       ├── reviewer/
│       ├── goal-writer/
│       ├── self-evolver/
│       └── skill-builder/
```

## Release 说明

每个 Release 包含三个文件：

| 文件 | 用途 |
|------|------|
| `creator-gateway.zip` | 网关 Skill，安装到全局 skill 目录 |
| `creator.codex.zip` | Codex 工作空间初始化包 |
| `creator.claude.zip` | Claude Code 工作空间初始化包 |

构建方式：

```bash
python scripts/build_release.py
# 产物输出到 dist/
```

## 使用方式

在本仓库或其子目录中新开 Codex 话题即可。

Codex 应读取：

- `AGENTS.md`：系统总协议
- `.agents/skills/*/SKILL.md`：当前项目级 Skill

这些 Skill 不需要复制到 `~/.codex/skills`。
