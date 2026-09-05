---
name: creator
description: 在当前工作空间初始化或升级 creator.skill 产品交付工作流。当用户想要在一个新项目或已有项目中启用、初始化或升级 creator.skill 的需求收集、设计规范、开发计划、项目开发等全套技能时触发。支持从 GitHub Release 下载或从用户指定的本地压缩包释放。
---

# 工作流初始化技能

在当前工作空间部署 creator.skill 全套产品交付工作流。

## 核心原则

初始化是释放，不是创造。源文件来自预构建的释放包，不要在初始化过程中生成或修改 Skill 内容。

## 工作方式

1. 判断用户已授权范围：仅安装/升级工作流，还是同时适配旧 docs。明确指令不重复确认；只安装时只读盘点 docs，不擅自迁移。
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
   - 普通版本化文件在已授权升级范围内替换；真实本地定制、未提交的他人工作及无法判定的冲突先列明，只询问影响结果的最小选择。
5. 先解包到临时暂存目录，检查 manifest 与包内相对路径不得越出暂存目录；按下方更新规则将工作流拥有的文件应用到项目。已有 signals、docs-state、本地定制和 cases 的合并必须在写入前处理，不先覆盖再尝试恢复。
6. 从释放包原样复制 `.version` 与 `.creator-manifest.json` 到工作空间根目录；`.version` 内容必须等于 manifest 的 `version` 字段。**禁止写入安装日期或当前时间**，版本一律以释放包内容为准。
7. 验证关键文件已就位：
   - 系统指令文件存在
   - `.creator-manifest.json` 中列出的每个 Skill 目录均包含 SKILL.md，实际数量与 `skill_count` 一致
   - 对应 CLI 的 evolution/signals.md 已生成
   - `.creator/tests/prompt-cases/cases.json` 与 `.creator/scripts/evaluate_prompt_cases.py` 已就位，并能完成静态 Prompt 契约评测
   - `.version` 与 manifest 中的版本一致
   - manifest 声明的 docs 迁移手册、共同契约及 `check_docs.py` 存在
8. 文档适配：按[旧 docs 迁移手册](../.creator/references/docs-migration-1.5.md)检测已有入口和 `.creator/docs-state.json`。旧 `.version` 是日期时记未知旧版，以实际结构盘点，不猜布局。已授权 docs 适配则执行对账/迁移并验证；否则仅报告待迁移或已登记状态。
9. 分别报告工作流安装版本和 docs 状态（未登记/待迁移/部分迁移/已迁移），以及保留/合并/未决项。静态检查不冒充真实模型任务测试；`.version` 更新不等于 docs 适配完成。

## 更新已有工作流

已有 `.version` 时比较释放包 manifest；用户已要求升级则直接完成已授权范围，不重复询问是否继续。版本无法识别时说明旧值，不假装已知。

更新 = **整体替换工作流文件 + 保留运行时状态 + 冲突询问用户**：

- 已识别且未定制的工作流文件（系统指令、EVOLUTION.md、manifest 声明的 Skill、评测脚本、用例 README、`.version`、`.creator-manifest.json`）在授权升级范围内整体替换。不得整目录删除其他 Skill、命令或项目 `.creator/` 资产；新旧 manifest 无法确定归属时保留并列明，不猜测删除。不自动回放旧版本自进化补丁，历史保留在 signals.md。
- `evolution/signals.md` 是运行时台账，保留不清空；其中“已转补丁”条目若与新版本规则冲突，列出并询问用户，不静默应用或丢弃。
- `.creator/tests/prompt-cases/cases.json` 按 `id` 合并；仅存在于任一侧的条目保留；同 ID 按下面的官方基线/本地定制规则处理，禁止静默覆盖项目定制。
- `.creator/docs-state.json` 是项目运行时状态，保留且不被释放包覆盖；迁移成功后由本次迁移更新，不复制别的项目的 complete 状态。
- 同 ID 的官方用例在有证据确认未被本地修改时随官方版本更新；无法区分本地变更时保留原值并列冲突，不通过覆盖“修好”回归。用户明确授权某冲突处理后不重复询问。
- 其他冲突区分正常官方升级与项目定制，不能把所有字节差异都变成批准请求。保护他人未提交修改；跨平台产物不顺手删除。
- 替换后验证关键文件与版本一致，报告旧 → 新版本、保留 / 合并 / 询问项与验证结论。

## 红线

- 不在初始化过程中修改 Skill 内容。
- 不覆盖未授权范围或未解决的本地定制；用户已授权的常规版本升级无需再次确认。
- 不在更新工作流时清空或覆盖已有的 evolution/signals.md。
- 不静默覆盖 `.creator/tests/prompt-cases/cases.json` 中的项目自进化用例。
- 能判断当前宿主时直接按宿主初始化，不询问；只有无法判断时才询问。
- 不把 `.version` 写成安装日期或当前时间；版本以释放包内容为准。
- 不跳过验证步骤。

## 参考

初始化时参考 [cli-adapters.md](references/cli-adapters.md) 了解两套 CLI 的目录差异。
