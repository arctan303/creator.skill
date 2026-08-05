---
name: creator
description: 在当前工作空间初始化或升级 creator.skill 产品交付工作流。当用户想要在一个新项目或已有项目中启用、初始化或升级 creator.skill 的需求收集、设计规范、开发计划、项目开发等全套技能时触发。支持从 GitHub Release 下载或从用户指定的本地压缩包释放。
---

# 工作流初始化技能

在当前工作空间部署 creator.skill 全套产品交付工作流。

## 核心原则

初始化是释放，不是创造。源文件来自预构建的释放包，不要在初始化过程中生成或修改 Skill 内容。

## 工作方式

1. 确认用户意图：初始化工作流到当前工作空间。
2. 检测当前宿主：优先按 gateway 技能**自身安装位置**判断——`SKILL.md` 位于 `~/.codex/skills/creator/` → Codex；位于 `~/.claude/skills/creator/` → Claude Code。无法定位自身时回退到 `~/.codex/`、`~/.claude/` 目录存在性；仍歧义时才询问用户。
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
   - 检测到目标平台但工作空间已有另一平台产物（如目标为 Codex 却存在 `.claude/`）时，提示共存/覆盖，不静默双部署。
   - 存在冲突时，询问用户处理方式。
5. 解压释放包到当前工作空间根目录。
6. 从释放包原样复制 `.version` 与 `.creator-manifest.json` 到工作空间根目录；`.version` 内容必须等于 manifest 的 `version` 字段。**禁止写入安装日期或当前时间**，版本一律以释放包内容为准。
7. 验证关键文件已就位：
   - 系统指令文件存在
   - `.creator-manifest.json` 中列出的每个 Skill 目录均包含 SKILL.md，实际数量与 `skill_count` 一致
   - 对应 CLI 的 evolution/signals.md 已生成
   - `.creator/tests/prompt-cases/cases.json` 与 `.creator/scripts/evaluate_prompt_cases.py` 已就位，并能完成静态 Prompt 契约评测
   - `.version` 与 manifest 中的版本一致
8. 报告初始化结果：工作流版本、目标平台、技能数量、`.version` 与 `.creator-manifest.json` 位置、安装后验证结论、可用更新（如有）。

## 更新已有工作流

如果工作空间已有 `.version` 文件，展示当前版本并与释放包 manifest 比较，提示可用更新，由用户决定是否继续。

更新 = **整体替换工作流文件 + 保留运行时状态 + 冲突询问用户**：

- 工作流文件（系统指令、EVOLUTION.md、技能目录、评测脚本、用例 README、`.version`、`.creator-manifest.json`）直接用释放包整体替换；不自动回放或合并旧版本的自进化补丁——自进化历史保留在 signals.md 中，不随替换丢失。
- `evolution/signals.md` 是运行时台账，保留不清空；其中“已转补丁”条目若与新版本规则冲突，列出并询问用户，不静默应用或丢弃。
- `.creator/tests/prompt-cases/cases.json` 按 `id` 合并；仅存在于任一侧的条目保留，同 ID 内容不同时列出冲突并让用户选择，禁止静默覆盖。
- 其余任何冲突（文件内容不同、跨平台残留、补丁与新版规则冲突等）一律列出并询问用户，不自动选择。
- 替换后验证关键文件与版本一致，报告旧 → 新版本、保留 / 合并 / 询问项与验证结论。

## 红线

- 不在初始化过程中修改 Skill 内容。
- 不在用户未确认的情况下覆盖已有文件。
- 不在更新工作流时清空或覆盖已有的 evolution/signals.md。
- 不静默覆盖 `.creator/tests/prompt-cases/cases.json` 中的项目自进化用例。
- 能判断当前宿主时直接按宿主初始化，不询问；只有无法判断时才询问。
- 不把 `.version` 写成安装日期或当前时间；版本以释放包内容为准。
- 不跳过验证步骤。

## 参考

初始化时参考 [cli-adapters.md](references/cli-adapters.md) 了解两套 CLI 的目录差异。
