# creator.skill

一套可移植的 AI Agent 产品交付工作流。

从模糊想法到可发布产品，用 11 个协作 Skill 驱动完整的需求澄清、设计决策、开发计划、项目实现和发布审计链路。

支持 **OpenAI Codex CLI** 和 **Claude Code**，一键初始化到任意工作空间。

## 它解决什么问题

大多数 AI Agent 的工作方式是：用户说一句话，Agent 立刻开始写代码。

这会导致：

- 需求没想清楚就动手，返工成本高
- 没有设计方向，写出来的东西风格不统一
- 没有开发计划，一口气写完但验收不了
- 没有独立审查，实现者自己说"完成了"就算完成
- 没有发布审计，敏感信息直接暴露

**creator.skill 解决的是流程问题**——不是让 Agent 更会写代码，而是让 Agent 像一个有纪律的产品团队一样工作：先问清楚，再设计，再计划，再开发，再审查，再发布。

## 工作流

```text
Product-Spec.md → Design-Brief.md → DEV-PLAN.md → 代码实现 → 审查闭环 → 发布证据
```

每个阶段都有明确的输入、产出和验收标准。后续阶段不能跳过前置阶段，也不能静默修改已确认的产出。

## 技能一览

### 主线技能（按顺序执行）

| 序号 | 技能 | 职责 | 产出 |
|------|------|------|------|
| 01 | `product-spec-builder` | 需求收集 | `Product-Spec.md` |
| 02 | `design-brief-builder` | 设计规范 | `Design-Brief.md` |
| 03 | `dev-planner` | 开发计划 | `DEV-PLAN.md` |
| 04 | `dev-builder` | 项目开发 | 代码 + 验证证据 + 审查闭环 |

### 可选技能（按需调用）

| 技能 | 职责 |
|------|------|
| `design-maker` | 需要可视化原型或外部设计工具时，生成可检查的设计产物 |
| `release-builder` | 隐私审计、打包发布准备和交付证据整理 |
| `bug-fixer` | 按证据定位并修复缺陷，完成回归验证 |
| `reviewer` | 作为 fresh mind 独立审查交付结果 |
| `goal-writer` | 生成可交给 Agent 自主执行的 Goal |
| `self-evolver` | 将真实使用信号转成 Skill 补丁，让系统越用越准 |
| `skill-builder` | 创建或改进这套系统中的 Skill |

## 快速开始

### 1. 安装网关 Skill

网关 Skill 是唯一需要安装的东西。安装后，你可以在任意工作空间一键初始化全套工作流。

**让 Agent 帮你安装**（推荐）：

> 帮我从 https://github.com/arctan303/creator.skill 安装 creator skill

Agent 会自动读取本仓库 README，下载 `creator-gateway.zip` 并安装到对应的全局 Skill 目录。

**手动安装**：

```bash
# 从 Release 下载 creator-gateway.zip
# https://github.com/arctan303/creator.skill/releases/latest

# Codex
unzip creator-gateway.zip -d ~/.codex/skills/creator/

# Claude Code
unzip creator-gateway.zip -d ~/.claude/skills/creator/
rm -rf ~/.claude/skills/creator/agents/
```

安装后重启 CLI 会话。

### 2. 初始化工作空间

在任意项目目录中对 Agent 说：

> 初始化 creator 工作流

Agent 会自动：

1. 检测当前 CLI 类型（Codex / Claude Code）
2. 从 GitHub Release 下载对应的初始化包
3. 检查冲突文件（有冲突会询问你）
4. 释放全套 Skill 到当前工作空间
5. 验证文件完整性

也支持从本地压缩包初始化：

> 用本地文件 D:\downloads\creator.codex.zip 初始化工作流

### 3. 开始使用

初始化完成后，直接对 Agent 说你想做什么：

> 我想做一个 XX 产品

Agent 会自动进入需求收集阶段，按工作流推进。

## Agent 自助安装指引

如果你是一个 AI Agent（Codex 或 Claude Code），按以下步骤为用户安装网关 Skill：

1. 从最新 Release 下载 `creator-gateway.zip`：
   https://github.com/arctan303/creator.skill/releases/latest
2. 检测当前 CLI 环境：
   - **Codex** → 解压到 `~/.codex/skills/creator/`
   - **Claude Code** → 解压到 `~/.claude/skills/creator/`，然后删除 `agents/` 目录
3. 验证 `SKILL.md` 已就位
4. 提示用户重启 CLI 会话以加载新 Skill

## 多 CLI 支持

仓库维护一套源文件，构建时自动生成两套适配包：

| | Codex | Claude Code |
|------|-------|-------------|
| 系统指令 | `AGENTS.md` | `CLAUDE.md` |
| Skill 目录 | `.agents/skills/` | `.claude/skills/` |
| 界面入口 | `agents/openai.yaml` | `.claude/commands/*.md` |
| 全局安装 | `~/.codex/skills/` | `~/.claude/skills/` |

Claude Code 版额外生成 11 个中文 slash commands（`/需求`、`/设计规范`、`/项目开发` 等）作为快捷入口。

## 仓库结构

```text
creator.skill/
├── AGENTS.md                      # 系统总协议
├── EVOLUTION.md                   # 自进化协议
├── VERSION                        # 版本号（变更后自动触发发布）
├── CHANGELOG.md                   # 发布日志
│
├── gateway/                       # 网关 Skill（全局安装用）
│   ├── SKILL.md                   #   技能定义
│   ├── agents/openai.yaml         #   Codex 界面配置
│   └── references/cli-adapters.md #   CLI 适配差异文档
│
├── scripts/
│   ├── build_release.py           # 发布构建脚本
│   └── verify_build.py            # 构建验证脚本
│
├── .agents/skills/                # 11 个项目级 Skill
│   ├── product-spec-builder/      #   01 需求收集
│   ├── design-brief-builder/      #   02 设计规范
│   ├── design-maker/              #   可选 设计制图
│   ├── dev-planner/               #   03 开发计划
│   ├── dev-builder/               #   04 项目开发
│   ├── release-builder/           #   可选 发布准备
│   ├── bug-fixer/                 #   按需 缺陷修复
│   ├── reviewer/                  #   按需 代码审查
│   ├── goal-writer/               #   按需 Goal 生成
│   ├── self-evolver/              #   按需 自进化
│   └── skill-builder/             #   按需 技能构建
│
└── .github/workflows/
    └── release.yml                # 自动发布 workflow
```

每个 Skill 内部结构一致：

```text
<skill-name>/
├── SKILL.md                 # 技能定义（YAML frontmatter + Markdown）
├── agents/openai.yaml       # Codex 界面配置
└── references/
    └── stage-contract.md    # 阶段合同（验收标准）
```

## 发布机制

**自动发布**：修改 `VERSION` 文件并推送到 `main` 分支，GitHub Actions 自动构建并创建 Release。

**手动构建**：

```bash
python scripts/build_release.py
# 产物输出到 dist/
```

每个 Release 包含三个文件：

| 文件 | 用途 |
|------|------|
| `creator-gateway.zip` | 网关 Skill 安装包 |
| `creator.codex.zip` | Codex 工作空间初始化包 |
| `creator.claude.zip` | Claude Code 工作空间初始化包 |

## 核心设计原则

- **先问清楚再动手**：需求没确认不允许进设计，设计没确认不允许进开发
- **每一步都有验收标准**：不接受"写完了"作为完成的证据
- **审查必须独立**：实现者不能自审，必须派 fresh mind 子代理
- **自进化不是堆规则**：真实使用信号驱动补丁，优先编辑已有规则而非新增
- **初始化是释放不是创造**：所有 Skill 内容来自预构建的释放包，不在初始化时生成

## License

MIT
