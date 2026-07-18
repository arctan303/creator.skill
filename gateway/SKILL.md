---
name: creator
description: 在当前工作空间初始化 creator.skill 产品交付工作流。当用户想要在一个新项目或已有项目中启用 creator.skill 的需求收集、设计规范、开发计划、项目开发等全套技能时触发。支持从 GitHub Release 下载或从用户指定的本地压缩包释放。
---

# 工作流初始化技能

在当前工作空间部署 creator.skill 全套产品交付工作流。

## 核心原则

初始化是释放，不是创造。源文件来自预构建的释放包，不要在初始化过程中生成或修改 Skill 内容。

## 工作方式

1. 确认用户意图：初始化工作流到当前工作空间。
2. 检测当前运行的 CLI 环境（Codex 或 Claude Code）。
3. 确定源文件获取方式：
   - 默认：从 GitHub Release 下载对应的释放包
     - Codex → creator.codex.zip
     - Claude Code → creator.claude.zip
     - Release 地址：https://github.com/arctan303/creator.skill/releases/latest
   - 备选：用户指定本地压缩包路径
4. 检查目标工作空间是否已有冲突文件。
   - 两个平台共同检查：`.creator/` Prompt 回归资产目录。
   - Codex 检查：AGENTS.md、EVOLUTION.md、.version、.creator-manifest.json、.agents/skills/、.codex/evolution/signals.md
   - Claude Code 检查：CLAUDE.md、EVOLUTION.md、.version、.creator-manifest.json、.claude/skills/、.claude/commands/、.claude/evolution/signals.md
   - 存在冲突时，询问用户处理方式。
5. 解压释放包到当前工作空间根目录。
6. 读取释放包自带的 `.version` 和 `.creator-manifest.json`，确认工作流版本、目标平台和技能清单；不得把版本改写成安装日期。
7. 验证关键文件已就位：
   - 系统指令文件存在
   - `.creator-manifest.json` 中列出的每个 Skill 目录均包含 SKILL.md，实际数量与 `skill_count` 一致
   - 对应 CLI 的 evolution/signals.md 已生成
   - `.creator/tests/prompt-cases/cases.json` 与 `.creator/scripts/evaluate_prompt_cases.py` 已就位，并能完成静态 Prompt 契约评测
   - `.version` 与 manifest 中的版本一致
8. 报告初始化结果。

## 更新已有工作流

如果工作空间已有 `.version` 文件，展示当前版本并与释放包 manifest 比较，提示可用更新，由用户决定是否继续。

更新时：

- evolution/signals.md 是运行时台账，已有文件必须保留，不得用空模板覆盖。
- `.creator/tests/prompt-cases/cases.json` 可能包含自进化新增用例，必须按 `id` 合并现有与新包用例；仅存在于任一侧的条目保留，同 ID 内容不同时列出冲突并让用户选择，禁止静默覆盖。
- `.creator/scripts/evaluate_prompt_cases.py` 和用例 README 属于版本化运行时文件，只能在用户确认更新冲突文件后替换。
- 其余冲突文件按用户选择更新或合并。

## 红线

- 不在初始化过程中修改 Skill 内容。
- 不在用户未确认的情况下覆盖已有文件。
- 不在更新工作流时清空或覆盖已有的 evolution/signals.md。
- 不静默覆盖 `.creator/tests/prompt-cases/cases.json` 中的项目自进化用例。
- 不替用户选择 CLI 类型，必须自动检测或询问确认。
- 不跳过验证步骤。

## 参考

初始化时参考 [cli-adapters.md](references/cli-adapters.md) 了解两套 CLI 的目录差异。
