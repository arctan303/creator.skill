# creator.skill

面向 Codex 与 Claude Code 的产品交付工作流。主 Agent 名为创造者（Creovator）；先判断用户要改变什么，再选择需求、设计、规划、开发、审查与发布步骤。

当前版本 **1.5.0**，安装包见 [v1.5.0 Release](https://github.com/arctan303/creator.skill/releases/tag/v1.5.0)。本轮调整规则并验证结构、脚本与发布包；真实项目任务及跨模型效果由用户后续运行反馈。当前范围、依据与验证见[开发记录](docs/workflow-optimization.md)。

## 如何工作

路线、计划规模、风险分别判断：

| 判断 | 规则 |
| --- | --- |
| 0→1 产品 | 用户、目标、首版范围尚未明确，先收敛需求 |
| 产品变更 | 新增或改变预期行为；已有明确决定就补记录并执行，不重复访谈 |
| 维护执行 | 恢复既定行为或维护内部实现；根因不明先诊断 |
| 短任务 | 单一可独立完成并验收的工作，产品小改也适用 |
| Phase | 用户明确要求，或多个分别验收、存在先后依赖的交付阶段；实施前建计划 |
| R0 | 纯说明/格式/文案，不改变运行或代理行为；相关静态检查 |
| R1 | 影响可界定、可回滚、针对性验证可覆盖；行为验证和 diff 自查 |
| R2 | 鉴权隔离、敏感数据、不可逆操作、不兼容契约、关键业务或广泛故障等具体重大影响；相关验证和独立审查 |

多文件、依赖、Phase 身份不自动判 R2，一行租户过滤条件也不能因改动小降为 R1。尚在需求访谈可暂不评级；实施前说明“改什么、可能造成什么后果、需要什么证据”。提示词虽是 Markdown，修改代理行为不按纯文档 R0。

R0/R1 默认当前会话完成，不自动派遣子代理。已验证的小型维护进入简短的持久待复查队列，小型产品变更更新需求/短任务。batch.md 只保存当前待复查项；每次复查收尾移出已关闭项，全部关闭后重置为空队列，仅保留最近回执链接。未决或复查后新增的项保留，历史证据按需查回执。R2 使用 fresh reviewer，受用户与宿主限制时披露独立证据缺口。

同一契约、diff 和证据只运行一个 reviewer。有实质修复可以继续聚焦复核；连续两轮无进展或达到已声明预算时暂停并写恢复条件。模型容量和宿主故障记为中断。实施、验证、审查、发布分别记录，例外不写成审查通过。

## 项目知识与文档

新会话从现状入口和相关活跃任务开始，历史按需读取。优先复用已有 README、MANUAL、PROJECT-CONTEXT，不按文件名重复建手册。

| 职责 | 内容与维护时机 |
| --- | --- |
| 当前入口 | 实际能力、架构概览、运行/验证命令、当前进度和限制；受影响时更新 |
| 当前需求/设计 | 有效预期、验收与约束；新决定确认后原位修订旧条款 |
| 活跃计划 | 任务、稳定 Phase ID、前置成果、范围和证据；状态变化时同步 |
| 专题与历史 | 详细模块知识、完整旧任务与证据；按职责拆分，保留导航和替代来源 |

代码证明实际状态，用户有效决定定义预期；不能把代码回归改写成新规范。旧决定保留替代关系，退出当前约束。入口建议约 150 行或 8 KiB，详细主题约 300 行或 20 KiB 时检查是否拆分；这是整理提示，不能删证据或压长行凑数。

完整规则见[共同契约](.creator/references/workflow-contract.md)。

## 安装与旧项目升级

从[公开 Release](https://github.com/arctan303/creator.skill/releases/latest)取得 gateway，安装到 Codex 的 `~/.codex/skills/creator/` 或 Claude Code 的 `~/.claude/skills/creator/`，重启会话后在目标项目请求初始化。已安装旧 gateway 的用户需用新版 `creator-gateway.zip` 更新入口；项目工作流和旧 docs 再按已授权范围升级。

升级旧项目时可明确说：

> 使用本地 creator.codex.zip 升级当前工作流，并按 1.5 手册适配当前仓库的旧 docs。保留本地定制与历史证据。

[**1.5 旧 docs 迁移手册**](.creator/references/docs-migration-1.5.md)包含盘点、职责映射、决策对账、拆分承接、状态登记、验证和重复执行规则。自定义文件名、日期形式旧版本及并行编辑都有处理方式。

只要求安装时只读盘点文档。工作流 `.version` 与 `.creator/docs-state.json` 的迁移状态分开报告；升级不能自动把旧 docs 标为完成。保留项目 signals、迁移状态与自进化用例，普通官方版本更新无需重复确认，无法区分的本地冲突单独处理。禁止顺手迁移兄弟仓库。

## 源码架构

| 位置 | 职责 |
| --- | --- |
| [AGENTS.md](AGENTS.md) | 精简全局路由、风险、授权和上下文规则 |
| [.agents/skills](.agents/skills) | 11 个 Skill 的单一源码，按任务加载阶段细则 |
| [.creator/references](.creator/references) | 共同契约与可随安装包分发的迁移手册 |
| [.creator/scripts](.creator/scripts) | 静态/响应字段评测、只读 docs 检查器 |
| [.creator/tests/prompt-cases](.creator/tests/prompt-cases) | 路由与行为策略用例基线 |
| [EVOLUTION.md](EVOLUTION.md) | 失败信号合并、授权与规则补丁记录 |
| [gateway](gateway) | 安装/升级入口；安装和 docs 适配分开处理 |
| [scripts](scripts) | Codex、Claude Code、gateway 三包构建与验证 |
| [tests](tests) | docs 检查器的边界与只读性单元测试 |

技能包括 product-spec-builder、design-brief-builder、design-maker、dev-planner、dev-builder、bug-fixer、reviewer、release-builder、goal-writer、self-evolver、skill-builder；实际包清单以 manifest 为准。普通自进化信号累计处理，用户明确要求规则优化时不等待次数阈值；已有授权不反复确认。

## 本地验证与构建

```powershell
python .creator/scripts/evaluate_prompt_cases.py
python -B -m unittest discover -s tests -v
python scripts/build_release.py
python scripts/verify_build.py
```

只读文档盘点：`python .creator/scripts/check_docs.py --root .`。旧 docs 实际迁移并完成语义核对后，可用 `--require-complete` 检查登记、路径与文件链接；工具不证明旧原文完整、锚点正确或产品决策正确。

响应字段评分格式见[用例说明](.creator/tests/prompt-cases/README.md)。没有真实响应时只验证静态结构，字段通过也不等于实际文件行为通过。本轮没有真实任务响应评测。

构建生成 `dist/creator.codex.zip`、`dist/creator.claude.zip`、`dist/creator-gateway.zip`。Claude 包转换为 CLAUDE.md、.claude/skills 与 commands；共享迁移资料均随包分发，项目迁移完成状态不入包。现有 CI 在 VERSION 推送到 main 时运行检查并发布。发布回读结果记录于开发记录；真实任务效果由用户后续反馈。

## 参考与许可

本版采用 OpenAI 官方的结果导向、减少冲突指令、渐进加载和按风险验证原则，来源与本仓库自主设计的边界见[开发记录](docs/workflow-optimization.md)。

[MIT License](LICENSE)
