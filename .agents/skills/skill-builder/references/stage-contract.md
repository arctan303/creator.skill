# 技能构建阶段契约

## Skill 必须包含

- `SKILL.md`
- `agents/openai.yaml`
- 必要时的 `references/`

## SKILL.md 必须说明

- `## Purpose`
- `## Trigger`
- `## Required context`
- `## Workflow`
- `## Output`
- `## Stop or escalate`
- `## References`

## 新增 Skill 合格标准

新增 Skill 必须：

- 有明确触发场景。
- 不与现有 Skill 职责重复。
- 有清楚输入、输出、合格标准和红线。
- 有 `agents/openai.yaml` 展示名、描述和默认提示。
- 必要时有 `references/stage-contract.md`。
- 有至少一个正例、一个边界反例，以及相应 Prompt 行为用例。

## 修改 Skill 合格标准

修改现有 Skill 必须：

- 不破坏 `AGENTS.md` 的三路由、风险分级和权限边界。
- 不把主体写成冗长手册。
- 不降低验收、审查、隐私或发布标准。
- 同步更新相关 `stage-contract.md` 或 `agents/openai.yaml`。
- 同步更新行为用例并运行 Prompt 契约评测。

## 命名和展示规则

- `name` 使用稳定英文 kebab-case。
- 主体规则默认中文。
- 主线技能展示名只使用 `01-04`。
- 可选技能展示名使用 `可选｜...`。

## 必须打回的情况

- 新 Skill 没有明确触发场景。
- 职责可由现有 Skill 承担。
- 规则只是复制通用 Codex 行为。
- 修改会降低交付标准。
- 修改造成路线冲突、触发重叠或无法验证的交接。
