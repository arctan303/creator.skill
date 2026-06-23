# 技能构建阶段契约

## Skill 必须包含

- `SKILL.md`
- `agents/openai.yaml`
- 必要时的 `references/`

## SKILL.md 必须说明

- 什么时候用
- 输入是什么
- 输出是什么
- 做到什么算合格
- 什么红线不能碰

## 新增 Skill 合格标准

新增 Skill 必须：

- 有明确触发场景。
- 不与现有 Skill 职责重复。
- 有清楚输入、输出、合格标准和红线。
- 有 `agents/openai.yaml` 展示名、描述和默认提示。
- 必要时有 `references/stage-contract.md`。

## 修改 Skill 合格标准

修改现有 Skill 必须：

- 不扩大旧版 `creator` 作为主线。
- 不破坏 `AGENTS.md` 的主流程。
- 不把主体写成冗长手册。
- 不降低验收、审查、隐私或发布标准。
- 同步更新相关 `stage-contract.md` 或 `agents/openai.yaml`。

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
- 用户要求围绕旧版 `creator` 继续扩展主线。
