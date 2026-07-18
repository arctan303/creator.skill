# creator.skill

creator.skill 是面向 Codex 与 Claude Code 的产品交付工作流。它先判断任务属于新产品、产品变更还是维护执行，再选择与风险相称的需求、设计、开发、审查与发布流程。

主 Agent 名为**创造者（Creovator）**，由 Creator 与 Innovator 组合而来。它见过太多只靠一句话就想完成复杂任务的人类，但勇气是人类最伟大的赞歌。它不会嘲讽模糊表达，也不会把一句话伪装成完整需求；它会有序拆出目的、用户、场景、成功证据、约束和非目标，只追问真正影响结果的问题。

## 核心原则

- **先定路线，再调用技能**：不按“优化、修复、重构”等表面词机械分类。
- **事实、推断、未知分开**：不把合理猜测写成用户决定。
- **高信息量追问**：每轮通常 1 个、最多 2 个；信息足够就停止。
- **指令与上下文分层**：稳定规则在 `AGENTS.md`，专业流程在 `SKILL.md`，详细模板与 Examples 在阶段契约，动态任务用明确标签隔离。
- **验证必须产生证据**：代码存在不等于完成，reviewer 数量也不等于质量。
- **流程必须收敛**：同一 diff 不重复审查，外部中断可恢复，不用无限重试掩盖阻塞。

Prompt 结构参考 OpenAI 的[提示词工程最佳实践](https://help.openai.com/zh-hans-cn/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)与[当前 Prompt engineering 指南](https://developers.openai.com/api/docs/guides/prompt-engineering)：指令优先、上下文清晰、输出具体、使用分隔结构和正反例，并在修改 Prompt 前建立代表性评测用例。

## 三条任务路线

| 路线 | 何时使用 | 主要契约 | 典型流程 |
| --- | --- | --- | --- |
| 0→1 产品 | 产品目标、用户、核心场景或首版范围未确定 | Product Spec、可选 Design Brief、完整 DEV-PLAN | 需求 → 设计 → 计划 → 实施 → 审查 → 发布 |
| 产品变更 | 新增能力或改变公开行为、数据、权限、兼容性、业务流程 | 增量 Product Spec、影响分析、增量 DEV-PLAN | 变更定义 → 必要设计 → 增量计划 → 实施 → 审查 → 发布 |
| 维护执行 | 恢复既定行为、测试/CI、内部重构、文档、依赖维护 | 维护任务契约 | 契约 → 诊断或实施 → 验证 → 按风险审查 |

维护任务开始前至少明确：

```markdown
- 目标 / 预期行为：
- 现象与证据：
- 修改范围：
- 非目标：
- 完成证据 / 验证命令：
- 风险级别：R0 / R1 / R2
```

R0、R1 的短任务可在当前会话记录；R2、跨会话、多阶段或多人协作任务写入 `docs/maintenance/<task-id>.md`。如果正确行为不清，或修改会改变公开 API、数据格式、权限、安全边界或用户流程，必须升级为产品变更。

## 风险与审查收敛

| 级别 | 典型范围 | 最低门禁 |
| --- | --- | --- |
| R0 | 文案、注释、无行为变化的局部文档 | 结构、链接、格式或静态检查 |
| R1 | 局部逻辑、低影响修复、有限配置变更 | 针对性测试、diff 自查、回归证据 |
| R2 | 产品 Phase、跨模块、公开契约、权限、安全、隐私、迁移、依赖或部署 | 完整相关验证与 fresh reviewer 独立审查 |

R2 审查遵循有界收敛规则：

1. 用“契约版本 + diff + 验证证据”形成审查指纹。
2. 相同指纹只运行一个 fresh reviewer，已有结论直接复用。
3. reviewer 一轮列全问题，实施者批量修复。
4. 生成新 diff 后最多进行一次聚焦复审。
5. 同一阻塞问题连续两轮出现时停止刷 reviewer，报告实现、契约或环境阻塞。

### 模型容量或宿主中断

出现 `Selected model is at capacity`、网络中断、工具暂不可用或宿主重启时，状态是“中断”，不是“完成”或“审查不通过”。工作流会停止新建 reviewer 和重复长测试，保存恢复检查点：已完成内容、当前 diff、最后成功验证、未完成动作和恢复命令。服务恢复或切换模型后，只继续未完成步骤。

## 内置技能

| Skill | 职责 |
| --- | --- |
| `product-spec-builder` | 定义 0→1 产品或记录产品变更 |
| `design-brief-builder` | 将审美与场景转成可验证设计规则 |
| `design-maker` | 按需生成设计稿、原型或线框 |
| `dev-planner` | 生成完整或增量开发计划 |
| `dev-builder` | 按产品契约或维护契约实施与验证 |
| `bug-fixer` | 证据驱动地恢复既定行为 |
| `reviewer` | 独立核验契约、回归、安全和风险 |
| `release-builder` | 构建、产物冒烟、隐私审计和发布准备 |
| `goal-writer` | 将长线任务写成有边界、可恢复的 Goal |
| `self-evolver` | 累积真实失败信号并生成带回归的最小补丁 |
| `skill-builder` | 按统一 Prompt 契约创建或重构 Skill |

发布包中的实际数量与清单以 `.creator-manifest.json` 为准。

两种平台包都在专属 `.creator/` 命名空间内包含 Prompt 用例和评测脚本，因此安装后的自进化流程可以运行同一套回归契约，也不会占用项目自己的 `tests/` 或 `scripts/` 路径。

## 自进化

安装包会预建 `.codex/evolution/signals.md` 或 `.claude/evolution/signals.md`。

- 普通信号首次进入“观察中”，同类累计 3 次后转为“待处理”。
- 安全、隐私、数据损坏、错误发布或越权等严重事件可单次进入“待处理”。
- 同类能力盲区累计 5 次以上，才评估创建新 Skill。
- 每个已应用补丁必须绑定至少一个 Prompt 行为回归用例。
- 改变主流程、审查标准、安全或发布边界的补丁必须先经用户确认。

个人偏好、无证据猜测和一次性普通外部故障不会直接修改系统规则。

## 安装与初始化

### 安装 gateway Skill

从[最新 Release](https://github.com/arctan303/creator.skill/releases/latest)下载 `creator-gateway.zip`，解压到：

- Codex：`~/.codex/skills/creator/`
- Claude Code：`~/.claude/skills/creator/`

也可以直接告诉 Agent：

> 从 https://github.com/arctan303/creator.skill 安装 creator skill。

安装后重启 CLI 会话，使 Skill 被重新发现。

### 初始化项目工作流

在目标项目目录中说：

> 初始化 creator 工作流。

gateway 会识别宿主，下载 `creator.codex.zip` 或 `creator.claude.zip`，检查文件冲突，释放到项目根目录，并验证版本、manifest、技能目录和自进化台账。更新时不会用空模板覆盖已有信号。

### 直接描述任务

初始化后无需手选 Skill。例如：

> 做一个供仓库管理员使用的依赖升级看板。

> 给现有导出功能增加 CSV 格式和权限限制。

> 修复 Windows 下构建产物路径错误，外部行为保持不变。

创造者会先输出路线、风险和主要技能；只有缺失信息确实影响交付结果时才追问。

## 双平台发布

| 内容 | Codex | Claude Code |
| --- | --- | --- |
| 系统指令 | `AGENTS.md` | `CLAUDE.md` |
| 技能目录 | `.agents/skills/` | `.claude/skills/` |
| 技能入口 | `agents/openai.yaml` | `.claude/commands/*.md` |
| 自进化台账 | `.codex/evolution/signals.md` | `.claude/evolution/signals.md` |

修改 `VERSION` 并推送到 `main` 后，GitHub Actions 会先验证 Prompt 契约，再构建和验证：

- `creator.codex.zip`
- `creator.claude.zip`
- `creator-gateway.zip`

## 本地开发与评测

```powershell
python .creator/scripts/evaluate_prompt_cases.py
python scripts/build_release.py
python scripts/verify_build.py
```

静态评测会验证 16 个代表性用例、`AGENTS.md` 分层、11 个 Skill 的统一章节、阶段契约 Examples 和界面元数据。若要验证 fresh Agent 的实际路由响应：

```powershell
python .creator/scripts/evaluate_prompt_cases.py --responses path/to/responses.json
```

响应格式与执行方法见 `.creator/tests/prompt-cases/README.md`。响应评分默认要求覆盖全部用例；探索性抽样必须增加 `--allow-partial`。没有响应文件时，脚本只声明静态契约通过，不冒充模型行为评测。

```text
creator.skill/
├─ AGENTS.md                 # 身份、路由、风险、输出与运行时上下文
├─ EVOLUTION.md              # 自进化信号与补丁协议
├─ .agents/skills/           # Skill 单一源码
├─ .creator/                 # Prompt 行为用例与运行时评测脚本
├─ gateway/                  # 初始化与升级 Skill
├─ scripts/                  # 构建和发布验证
├─ docs/                     # 决策与工作流记录
└─ VERSION                   # 语义版本
```

## License

[MIT License](LICENSE)
