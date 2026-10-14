# 快速开始

[English](quickstart.md) · [首页](../README.zh-CN.md)

本页适用于 [1.6.0 Release](https://github.com/arctan303/creator.skill/releases/tag/v1.6.0)。旧版 [1.5](https://github.com/arctan303/creator.skill/releases/tag/v1.5.0) 使用不同包名与[安装说明](https://github.com/arctan303/creator.skill/blob/v1.5.0/README.md)。

## 安装发布版

下载两个发布 ZIP，保留 `creator-workflow.zip` 原文件，将 `creator-gateway.zip` 解压到名为 `creator-gateway` 的目录，目录内应直接包含 `SKILL.md` 和 `scripts/`。准备 Python 3.10+ 和已存在的目标项目，在下载目录运行：

```powershell
python creator-gateway/scripts/install_workflow.py --root "C:/path/to/your-project" --package "creator-workflow.zip"
python creator-gateway/scripts/install_workflow.py --root "C:/path/to/your-project" --package "creator-workflow.zip" --apply
```

第一条命令预览变更，核对后再运行第二条。这不会安装个人技能。升级时请加入下文的基线参数，并沿用此处 gateway 安装器与下载包路径。

## 本地构建与安装

也可以使用标签 `v1.6.0` 的源码检出、Python 3.10+ 和已存在的目标项目自行构建。以下命令在 creator.skill 源码目录执行。请替换示例项目路径；Linux 或 macOS 可使用 `/home/you/projects/example` 等绝对路径。

```powershell
python scripts/build_release.py
python scripts/verify_build.py
python scripts/install_workflow.py --root "C:/path/to/your-project" --package "dist/creator-workflow.zip"
```

最后一条命令只输出 JSON 预览，不修改项目。查看待写入、待清理、保留文件及冲突后，再执行：

```powershell
python scripts/install_workflow.py --root "C:/path/to/your-project" --package "dist/creator-workflow.zip" --apply
```

存在未解决冲突时，apply 会在写入前停止。核对并合并相关定制后重新预览；没有强制覆盖开关。对需要独立保留的项目改动，请使用版本控制或备份。

安装后在**目标项目中新开会话**。工作流版本与项目文档状态分开管理：安装不会自动迁移旧 docs。需要适配时明确提出，具体方式见[迁移手册](../.creator/references/docs-migration-1.5.md)。

## 升级已有安装

使用同一安装器和目标目录。升级 1.5 时，提供原宿主对应的官方 ZIP 作为基线：

```powershell
python scripts/install_workflow.py --root "C:/path/to/your-project" --package "dist/creator-workflow.zip" --baseline-package "C:/downloads/creator.codex-1.5.0.zip"
```

请填写实际本地文件名；1.5 Release 资产名为 `creator.codex.zip` 或 `creator.claude.zip`。项目同时存在两个旧布局时，可以重复 `--baseline-package` 提供对应官方包。查看预览后再加 `--apply`。

旧版工作流拥有的 `CLAUDE.md`、commands 等废弃文件，只有内容能够与可靠基线匹配时才会清理。本地修改或无法识别的文件作为冲突保留。其他技能、项目文档、signals 和自定义用例必须保留。不要通过删除整个 `.claude/`、`.agents/` 或 `.creator/` 目录完成升级。

安装中断后，先查看恢复信息，再继续安装：

```powershell
python scripts/install_workflow.py --root "C:/path/to/your-project" --recover
```

加入 `--apply` 执行已报告的恢复。并行修改会保留并列为冲突，应按现有证据处理，不能直接丢弃。

## Codex 与 Claude Code

两个宿主使用同一个工作流包和 `AGENTS.md`。规范技能文件位于 `.agents/skills/`；包内同时提供 `.claude/skills/` 下的 Claude 发现入口，指向同一套指令。

直接读取 AGENTS 时，请使用较新的 Claude Code。官方要求 **v2.1.277+**，部分会话类型的修复在 **v2.1.281**。默认情况下，工作目录及其上级存在 `CLAUDE.md`、`.claude/CLAUDE.md` 或 `CLAUDE.local.md` 时，会优先读取这些文件。无关的个人或项目定制应核对合并，不能静默删除。见 [Claude AGENTS 加载条件](https://code.claude.com/docs/en/memory#agentsmd)。

支持 AGENTS 不代表 Claude 会自动发现 `.agents/skills/`。官方项目技能路径仍为 `.claude/skills/`；旧 `.claude/commands/` 虽兼容，但使用新入口后无需再保留同一套命令副本。见[技能发现说明](https://code.claude.com/docs/en/skills#choose-where-skills-load)。

已知 Claude 版本时，可在安装命令加入 `--claude-version 2.1.281`（或实际版本）获取兼容诊断。该参数不会启动 Claude，也不能证明它已加载文件。请在新宿主会话中核对已加载指令和技能。实际宿主验证范围见[项目现状](README.md)。

## 安装或更新个人 gateway

可选的 `creator` gateway 是个人技能，用于在你选定的项目中安装或升级工作流。个人入口与项目内工作流是两项独立安装。

1. 下载 1.6.0 Release 的 `creator-gateway.zip`，或从同一标签源码构建；先解压到临时目录并核对内容。ZIP 根目录直接包含 `SKILL.md`、`agents/`、`references/` 和 `scripts/`。
2. 将这些内容放入 Codex 的 `~/.codex/skills/creator/` 或 Claude Code 的 `~/.claude/skills/creator/`。最终应存在 `creator/SKILL.md` 和 `creator/scripts/install_workflow.py`，不要再嵌套一层 `creator/`。
3. 更新已有个人入口时，保留并核对本地定制。只替换 gateway 自身文件，不触碰相邻技能。项目安装器不会更新个人技能目录。
4. 重启宿主会话，打开目标项目，然后提出：

> 使用 creator gateway，从我提供的本地 `creator-workflow.zip` 安装当前项目的工作流。预览变更，执行没有歧义的安装，并分别报告工作流版本与文档状态。

升级时同时提供旧官方基线包。也可以让 gateway 从 GitHub 获取 `v1.6.0`，明确版本可避免选错发布资产。

也可直接执行 gateway 随包的安装器：`python <gateway目录>/scripts/install_workflow.py`，参数与前文相同。

## 把第一项任务说具体

| 场景 | 可以这样开始 |
| --- | --- |
| 新产品 | “帮我确定共享阅读清单的第一个可用版本。问清用户和用途，常规技术选择由你决定。” |
| 修改已有项目 | “在这个结果页增加 CSV 导出，沿用已有权限和界面约定，并验证结果。” |
| 继续工作 | “读取当前项目入口与活跃任务，核对之前哪些证据仍有效，然后继续未完成的工作。” |
| 纠正项目知识 | “AIWorker 已退役。更新当前需求和任务，保留历史证据，不恢复旧功能。” |

明确的项目约定会写入相关文档，不必额外说“记住这个”。未经确认的推断仍作为候选；规定发版检查清单，不等于授权执行发布。查看[连续性示例](examples/project-continuity.zh-CN.md)。

直接使用中文或英文即可。回复跟随你的语言；已有文档保持原有语言，除非你要求改变。公开示例有对等翻译，规范工作流规则只维护一份。
