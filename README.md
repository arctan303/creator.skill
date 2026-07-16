# creator.skill

面向 Codex 与 Claude Code 的产品交付工作流。它不把用户的一句话直接当成完整需求，而是先判断任务性质，再选择与风险相称的流程、文档和验证强度。

主 Agent 名为**创造者（Creovator）**，由 Creator 与 Innovator 组合而来。它的职责不是替用户堆砌流程，而是把表面诉求拆成目的、使用者、场景、成功证据、约束与非目标；只追问真正会改变方向、范围或验收方式的问题。

## 为什么需要它

许多 Agent 工作流只有一条重型流水线：新产品、改按钮文案、修 CI 都被要求先写完整需求和开发计划。另一类工作流则完全相反，收到一句话便直接改代码，直到交付时才发现目标、边界或验证方式从未明确。

creator.skill 将任务分成三条路线：

| 路线 | 适用场景 | 主要契约 | 典型流程 |
| --- | --- | --- | --- |
| 0→1 产品 | 新产品、核心用户或价值主张未确定 | Product Spec，可选 Design Brief，完整 DEV-PLAN | 需求 → 设计 → 计划 → 实施 → 审查 → 发布 |
| 产品变更 | 新增能力、改变用户可见行为、公开契约或权限边界 | 增量 Product Spec、影响分析、增量 DEV-PLAN | 变更定义 → 必要设计 → 增量计划 → 实施 → 审查 → 发布 |
| 维护执行 | 修复既定行为、测试/CI、内部重构、文档、依赖维护 | 维护任务契约 | 契约 → 诊断或实施 → 验证 → 按风险审查 |

维护任务不强制生成 `Product-Spec.md` 或 `DEV-PLAN.md`。但如果正确行为不清，或修改会改变公开 API、持久化格式、公开数据模型、权限或用户流程，任务必须升级到“产品变更”路线。

## 维护任务契约

维护路线开始前至少明确以下内容：

```markdown
- 目标 / 预期行为：
- 现象与证据：
- 修改范围：
- 非目标：
- 完成证据 / 验证命令：
- 风险级别：R0 / R1 / R2
```

R0、R1 的短任务可以只在当前会话中记录；R2、跨会话、多阶段或多人协作任务写入 `docs/maintenance/<task-id>.md`。

## 风险与验证

| 级别 | 典型范围 | 最低门禁 |
| --- | --- | --- |
| R0 | 文案、注释、无行为变化的局部文档 | 结构、链接、格式或静态检查 |
| R1 | 局部逻辑、低影响修复、有限配置变更 | 针对性测试、diff 自查、回归证据 |
| R2 | 数据迁移、权限、安全、发布、跨模块或不确定风险 | 完整验证与 fresh reviewer 独立审查 |

风险不清时向上取级。任何路线都不能跳过目标、权限边界和可复现的验证证据。

## 内置技能

发布包中的实际技能清单和数量以 `.creator-manifest.json` 为准。当前源码包含：

| Skill | 职责 |
| --- | --- |
| `product-spec-builder` | 收敛 0→1 产品或产品变更，维护 Product Spec |
| `design-brief-builder` | 将产品目标转成可验证的视觉与交互约束 |
| `design-maker` | 根据需求与设计规范产出设计稿、原型或线框 |
| `dev-planner` | 生成完整或增量开发计划 |
| `dev-builder` | 按产品契约或维护任务契约实施并验证 |
| `bug-fixer` | 证据驱动地复现、定位和修复既定行为缺陷 |
| `reviewer` | 独立核验契约符合性、回归、安全和风险分级 |
| `release-builder` | 识别技术栈，完成构建、隐私检查和发布准备 |
| `goal-writer` | 将长线目标转换为可持续执行的 Goal |
| `self-evolver` | 从真实失败和纠正中积累信号并生成可验证补丁 |
| `skill-builder` | 创建或维护符合本工作流约束的 Skill |

## 自进化如何触发

安装包会预建 `.codex/evolution/signals.md` 或 `.claude/evolution/signals.md`。以下事件会在安全检查点记录或合并信号：用户明确纠正、规则遗漏导致重复要求、测试或审查发现规则本应阻止的问题、规则冲突、同类人工绕行再次出现，以及用户明确要求吸取教训。

- 普通信号首次进入“观察中”，同类累计 3 次后转为“待处理”。
- 安全、隐私、数据损坏、错误发布或越权等严重事件单次直达“待处理”。
- 同类能力盲区出现 5 次以上时，才评估是否创建新 Skill。
- 改变主流程、审查标准或安全边界的补丁必须先由用户确认。

个人偏好、无证据猜测和一次性外部故障不会被包装成“系统进化”。

## 安装与初始化

### 1. 安装 gateway Skill

从 [最新 Release](https://github.com/arctan303/creator.skill/releases/latest) 下载 `creator-gateway.zip`，解压到对应目录：

- Codex：`~/.codex/skills/creator/`
- Claude Code：`~/.claude/skills/creator/`

也可以直接让 Agent 执行：

> 从 https://github.com/arctan303/creator.skill 安装 creator skill。

安装后重启 CLI 会话，使 Skill 被重新发现。

### 2. 初始化项目工作流

在目标项目目录中对 Agent 说：

> 初始化 creator 工作流。

gateway 会检测当前 CLI，下载 `creator.codex.zip` 或 `creator.claude.zip`，检查现有文件冲突，释放到项目根目录，并校验 `.version`、`.creator-manifest.json`、技能目录与自进化台账。更新已有工作流时，现有信号台账不会被空模板覆盖。

### 3. 直接描述任务

初始化完成后无需先选择 Skill。直接描述目标即可，例如：

> 做一个供仓库管理员使用的依赖升级看板。

> 给现有导出功能增加 CSV 格式和权限限制。

> 修复 Windows 下构建产物路径错误，外部行为保持不变。

创造者会先输出当前路线；只有缺失信息确实会改变交付结果时才继续追问。

## 双平台发布结构

| 内容 | Codex | Claude Code |
| --- | --- | --- |
| 系统指令 | `AGENTS.md` | `CLAUDE.md` |
| 技能目录 | `.agents/skills/` | `.claude/skills/` |
| 技能入口 | `agents/openai.yaml` | `.claude/commands/*.md` |
| 自进化台账 | `.codex/evolution/signals.md` | `.claude/evolution/signals.md` |

修改 `VERSION` 并推送到 `main` 后，GitHub Actions 会构建并验证：

- `creator.codex.zip`
- `creator.claude.zip`
- `creator-gateway.zip`

发布 manifest 由源码目录动态生成，包含平台、语义版本、技能根目录与完整技能清单；gateway 不会用安装日期覆盖版本。

## 本地开发

```powershell
python scripts/build_release.py
python scripts/verify_build.py
```

构建器会阻止以下问题进入 Release：缺失或重复的命令映射、缺少 `openai.yaml` 必填字段、manifest 与压缩包内容不一致、Claude Code 包残留 Codex 路径或 `$skill` 语法、版本不一致以及 gateway 结构缺失。

源码结构：

```text
creator.skill/
├─ AGENTS.md                 # 全局路由、风险和交付协议
├─ EVOLUTION.md              # 自进化信号与补丁协议
├─ .agents/skills/           # Skill 单一源码
├─ gateway/                  # 初始化与升级 Skill
├─ scripts/                  # 构建和发布包验证
├─ docs/                     # 决策与工作流记录
└─ VERSION                   # 语义版本
```

## License

[MIT License](LICENSE)
