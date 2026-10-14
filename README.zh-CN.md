# Creovator · creator.skill

[English](README.md)

**让编码 Agent 理解项目、完成任务，并把有效的项目知识带到下一次会话。**

Creovator 是面向 Codex 与 Claude Code 的项目工作流。你描述想要的结果，Agent 结合已有需求、设计约定和发版准则，选择合适的工作步骤与验证方式。

- **少重复解释。** 已明确的项目决定写回相关项目文档，并记录适用范围与来源。
- **任务有多大，流程就多大。** 小修保持简短；可独立的工作按需并行；有重大影响的变更接受独立审查。
- **交接有据可查。** 当前任务、已退役需求和验证证据保持清晰，新会话可以据此继续。

例如：

> AIWorker 已从产品中移除。请退役它尚未完成的验证任务，更新项目现状，保留历史证据。同时保留我们的设计约定：设置修改采用行内保存操作。

预期结果是更新当前计划和设计准则。旧功能的历史测试不会再次变成当前任务。查看[完整示例](docs/examples/project-continuity.zh-CN.md)。

## 安装 1.6.0

从 [1.6.0 Release](https://github.com/arctan303/creator.skill/releases/tag/v1.6.0) 下载 `creator-workflow.zip` 和 `creator-gateway.zip`。将 gateway ZIP 解压到工作流 ZIP 旁的 `creator-gateway` 目录，该目录应直接包含 `SKILL.md` 和 `scripts/`。

在该下载目录中，使用 Python 3.10+：

```powershell
python creator-gateway/scripts/install_workflow.py --root "C:/path/to/your-project" --package "creator-workflow.zip"
```

查看预览中的变更，再执行同一操作：

```powershell
python creator-gateway/scripts/install_workflow.py --root "C:/path/to/your-project" --package "creator-workflow.zip" --apply
```

目标项目目录须已存在。安装器默认只预览，遇到未解决的本地定制冲突会停止。升级 1.5 时需要提供旧官方包作为基线，以便安全识别应清理的旧文件。升级、Claude 兼容条件及个人 gateway 入口更新见[快速开始](docs/quickstart.zh-CN.md)。

在项目中新开 Agent 会话，然后试试：

> 先了解这个项目的现状和约定。在现有结果页增加 CSV 导出，沿用已有权限。常规实现选择由你决定，只在未确定的用户体验或授权边界上问我，并说明如何验证结果。

接入已有项目时，还可以要求适配文档：

> 请按这套工作流适配现有项目文档。复用当前入口、保留历史，并区分有效需求与已退役任务。

## 包含什么

发布资产包含项目安装包 `creator-workflow.zip`，以及内含安装器和可选个人技能的 `creator-gateway.zip`。两个宿主共用 `AGENTS.md` 和 `.agents/skills/` 下的规范技能；Claude 使用 `.claude/skills/` 下的薄入口发现技能，不生成第二套翻译规则或 `CLAUDE.md`。

公开安装说明和示例提供中英双语。Agent 跟随你的对话语言及项目现有文档语言工作。规则保持单一规范源，双语文档不会产生两套相互竞争的指令。

| 你想做什么 | 从这里开始 |
| --- | --- |
| 安装、升级或更新个人 gateway | [快速开始](docs/quickstart.zh-CN.md) |
| 了解项目决定如何跨会话承接 | [项目连续性示例](docs/examples/project-continuity.zh-CN.md) |
| 理解任务规模、风险与证据规则 | [共同工作契约](.creator/references/workflow-contract.md) |
| 适配已有文档结构 | [docs 迁移手册](.creator/references/docs-migration-1.5.md) |
| 查看实际实现与验证状态 | [项目现状](docs/README.md) |
| 参与开发或了解当前工作 | [开发计划](docs/DEV-PLAN.md) · [1.6 验证记录](docs/workflow-1.6.md) |

## 适用范围与证据

Creovator 提供指令、项目知识维护方式和本地检查/安装工具，执行能力取决于宿主 Agent 的工具与权限。文件安装成功不等于宿主已加载，也不等于真实任务一定成功。

示例是说明性演示。实际验证与宿主、行为验证缺口见[项目现状](docs/README.md)，不声称未经测量的采用规模或效率提升。发布、部署及修改其他项目仍需要对应的用户授权。

[MIT License](LICENSE)
