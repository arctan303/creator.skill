# 自进化信号记录

本文件记录真实使用中发现的问题。这里只记录信号，不在当前关键任务中直接修改 Skill。

新开话题时，如果本文件存在 `状态：待处理`，主 Agent 应按 `AGENTS.md` 静默派发 `self-evolver` 子代理处理。

## 记录格式

```markdown
## Signal YYYY-MM-DD-序号

- 来源 Skill：
- 触发场景：
- 用户反馈或观察到的问题：
- 影响：
- 可能涉及的现有规则：
- 初步处理建议：
- 状态：待处理 / 已转补丁 / 已忽略
- 处理说明：
```

## Signal 2026-06-22-01

- 来源 Skill：dev-builder / reviewer
- 触发场景：用户指出项目开发阶段应由写代码的 Agent 自行启动子代理代码审查。
- 用户反馈或观察到的问题：现有规则虽然写了 fresh 子代理审查，但没有足够明确说明“开发 Agent 自行启动审查，审查通过前不能表明任务结束”。
- 影响：可能导致开发完成后把审查责任留给用户，或者在没有独立审查通过时提前宣布任务完成。
- 可能涉及的现有规则：`AGENTS.md` 项目开发规则、`dev-builder` 核心原则和阶段契约、`reviewer` 核心原则。
- 初步处理建议：把自动启动审查和通过后才能结束写成强制交付门槛。
- 状态：已转补丁
- 处理说明：已同步补充 `AGENTS.md`、`dev-builder/SKILL.md`、`dev-builder/references/stage-contract.md` 和 `reviewer/SKILL.md`。

## Signal 2026-06-22-02

- 来源 Skill：design-maker / agents openai.yaml
- 触发场景：用户确认技能列表已经显示中文名称，并指出应按流程顺序展示，同时 `design-maker` 不是必跑实际技能。
- 用户反馈或观察到的问题：展示名没有序号，`设计制图 -> $design-maker` 容易被误解为主流程必选技能；实际上它是可选流程阶段，并且需要外部工具时才启用。
- 影响：可能导致 Agent 或用户把设计制图当成固定必经环节，拖慢第一版文本链路落地。
- 可能涉及的现有规则：各 Skill 的 `agents/openai.yaml` 展示名、`AGENTS.md` 总任务和设计制图阶段规则、README 技能说明。
- 初步处理建议：给展示名加流程序号，并把 `design-maker` 标成可选设计制图阶段。
- 状态：已转补丁
- 处理说明：已同步更新所有 Skill 展示名序号，并把 `design-maker` 的展示描述、`AGENTS.md` 和 `README.md` 改成可选阶段表述。

## Signal 2026-06-23-01

- 来源 Skill：dev-builder / dev-planner / release-builder
- 触发场景：用户指出开发计划应在需求收集、设计规范、开发计划之后，由项目开发阶段按上一阶段产物完整执行，而不是只做一个 Phase 后就停；其余技能是可选技能。
- 用户反馈或观察到的问题：当前规则和执行把 `dev-builder` 理解成“每次完成当前 Phase”，导致 Phase 1 完成后就进入发布准备检查，偏离“按开发计划完成全部开发范围、派子代理验收、没问题才告知开发完毕”的主线。
- 影响：可能导致 Agent 过早停止开发，或把单个 Phase 通过误报为项目开发完成；也可能把可选技能当成主线必跑阶段。
- 可能涉及的现有规则：`AGENTS.md` 总任务与项目开发规则、`dev-builder/SKILL.md`、`dev-builder/references/stage-contract.md`、`DEV-PLAN.md` 的 Phase 执行解释。
- 初步处理建议：明确主线四步为需求收集、设计规范、开发计划、项目开发；`dev-builder` 应连续执行计划内未完成 Phase 或任务，每个切片验证和审查，全部完成或明确阻塞后才输出项目开发完成；其他 Skill 标为按需可选。
- 状态：已转补丁
- 处理说明：已更新 `AGENTS.md`、`dev-builder/SKILL.md` 和 `dev-builder/references/stage-contract.md`，把单 Phase 完成和项目开发完成明确区分。
