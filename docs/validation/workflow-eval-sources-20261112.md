# 工作流评测计划：固定来源附录

核实日期：2026-11-12。两名研究代理分别通过 GitHub 连接器解析每个仓库 main，并在返回的完整 SHA 下重新读取下列文件全文。所列文件均存在且已实际阅读；本轮未安装或运行外部项目。此前移动 main 的阅读没有固定 commit，不以本清单倒填旧记录。

此附录属于[待确认计划](../tasks/workflow-eval-loop-20261112.md)，是来源清单，不是项目新增规范。方法概述为独立归纳，未复制外部正文；真正采用前仍核对必要许可和对应文件范围。

## obra/superpowers

读取分支 `main`；默认分支 `main`；commit [`22f0b463e7a5e579904dd6211a520321035526f7`](https://github.com/obra/superpowers/commit/22f0b463e7a5e579904dd6211a520321035526f7)。

借鉴：先建立可复现现象，再比较正常与失败路径，通过可区分的实验收敛原因；完成声明对应具体检查。压力场景只是决策材料，未运行；不采纳固定尝试次数或每次重复验证的通则。

实际完整读取：

- [skills/systematic-debugging/SKILL.md](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/systematic-debugging/SKILL.md)
- [skills/verification-before-completion/SKILL.md](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/verification-before-completion/SKILL.md)
- [tests/systematic-debugging/pressure-scenarios/test-pressure-1.md](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/tests/systematic-debugging/pressure-scenarios/test-pressure-1.md)

## github/spec-kit

读取分支 `main`；默认分支 `main`；commit [`979b0a3c1277283371c9901ad0eed04b64a99997`](https://github.com/github/spec-kit/commit/979b0a3c1277283371c9901ad0eed04b64a99997)。

借鉴：围绕用户可完成的结果定义可独立验收的一片交付，再标明依赖的具体成果，检查需求与任务是否缺项或矛盾。文档映射不能证明实现正确；仅作为 dev-planner 的条件方法候选，不采纳固定阶段和全套模板。

实际完整读取：

- [templates/commands/tasks.md](https://github.com/github/spec-kit/blob/979b0a3c1277283371c9901ad0eed04b64a99997/templates/commands/tasks.md)
- [templates/commands/analyze.md](https://github.com/github/spec-kit/blob/979b0a3c1277283371c9901ad0eed04b64a99997/templates/commands/analyze.md)

## open-gsd/gsd-core

读取分支 `main`；默认分支 `next`；commit [`4d42b6be22e24f243acf65be5cf189491f114206`](https://github.com/open-gsd/gsd-core/commit/4d42b6be22e24f243acf65be5cf189491f114206)。

借鉴：恢复时以实际工作区核对旧交接，分清未完成、外部等待和初始化中断；从目标倒推需要的运行证据。没有展开所有下游引用或运行项目；本次读取 main，不声称代表默认 next 的全部当前行为。

实际完整读取：

- [gsd-core/workflows/resume-project.md](https://github.com/open-gsd/gsd-core/blob/4d42b6be22e24f243acf65be5cf189491f114206/gsd-core/workflows/resume-project.md)
- [agents/gsd-verifier.md](https://github.com/open-gsd/gsd-core/blob/4d42b6be22e24f243acf65be5cf189491f114206/agents/gsd-verifier.md)

## bmad-code-org/BMAD-METHOD

读取分支 `main`；默认分支 `main`；commit [`a867e1604b365d48ea03cbd109da1066ba0c84bc`](https://github.com/bmad-code-org/BMAD-METHOD/commit/a867e1604b365d48ea03cbd109da1066ba0c84bc)。

借鉴：保存实现基线，核对验收检查真的执行；用独立副本比较无技能、完整技能与变体，保留产物、轨迹、失败和耗时。runner 与质量裁判是不同环节；本次不采纳其严格阶段顺序或等待点，也未验证运行效果。

实际完整读取：

- [skills/bmad-build/workflow.md](https://github.com/bmad-code-org/BMAD-METHOD/blob/a867e1604b365d48ea03cbd109da1066ba0c84bc/skills/bmad-build/workflow.md)
- [skills/bmad-build/step-03-implement.md](https://github.com/bmad-code-org/BMAD-METHOD/blob/a867e1604b365d48ea03cbd109da1066ba0c84bc/skills/bmad-build/step-03-implement.md)
- [skills/bmad-eval/SKILL.md](https://github.com/bmad-code-org/BMAD-METHOD/blob/a867e1604b365d48ea03cbd109da1066ba0c84bc/skills/bmad-eval/SKILL.md)
- [skills/bmad-eval/scripts/run_evals.py](https://github.com/bmad-code-org/BMAD-METHOD/blob/a867e1604b365d48ea03cbd109da1066ba0c84bc/skills/bmad-eval/scripts/run_evals.py)
- [skills/bmad-eval/references/eval-format.md](https://github.com/bmad-code-org/BMAD-METHOD/blob/a867e1604b365d48ea03cbd109da1066ba0c84bc/skills/bmad-eval/references/eval-format.md)

## anthropics/skills

读取分支 `main`；默认分支 `main`；commit [`2c5958ecac7cee2b583967a2c4981d0f4a75c579`](https://github.com/anthropics/skills/commit/2c5958ecac7cee2b583967a2c4981d0f4a75c579)。

借鉴：用真实产物与工具记录判断完成情况，同时检查断言是否会错放无效结果；将技能触发与任务质量分开。触发脚本依赖 Claude CLI，不直接移植为 Codex 执行方案；没有运行对照实验。

实际完整读取：

- [skills/skill-creator/SKILL.md](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/skill-creator/SKILL.md)
- [skills/skill-creator/agents/grader.md](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/skill-creator/agents/grader.md)
- [skills/skill-creator/scripts/run_eval.py](https://github.com/anthropics/skills/blob/2c5958ecac7cee2b583967a2c4981d0f4a75c579/skills/skill-creator/scripts/run_eval.py)

## pbakaus/impeccable

读取分支 `main`；默认分支 `main`；commit [`b4bff1626c344067788c2679f048a20057c7cc5a`](https://github.com/pbakaus/impeccable/commit/b4bff1626c344067788c2679f048a20057c7cc5a)。

借鉴：把加载协议、完整交付和界面取证分开；最终截图与最后源码对应，用真实浏览器检查目标区域及范围外内容。计算样式与截图新鲜度不等于审美优越；不采纳其普遍审美禁令，历史报告不作为本次执行证据。

实际完整读取：

- [skill/SKILL.src.md](https://github.com/pbakaus/impeccable/blob/b4bff1626c344067788c2679f048a20057c7cc5a/skill/SKILL.src.md)
- [skill/reference/craft-floor.md](https://github.com/pbakaus/impeccable/blob/b4bff1626c344067788c2679f048a20057c7cc5a/skill/reference/craft-floor.md)
- [tests/skill-workflow/full-build.test.mjs](https://github.com/pbakaus/impeccable/blob/b4bff1626c344067788c2679f048a20057c7cc5a/tests/skill-workflow/full-build.test.mjs)
- [tests/skill-workflow/assertions.mjs](https://github.com/pbakaus/impeccable/blob/b4bff1626c344067788c2679f048a20057c7cc5a/tests/skill-workflow/assertions.mjs)
- [tests/skill-workflow/scope.mjs](https://github.com/pbakaus/impeccable/blob/b4bff1626c344067788c2679f048a20057c7cc5a/tests/skill-workflow/scope.mjs)
- [tests/skill-behavior/README.md](https://github.com/pbakaus/impeccable/blob/b4bff1626c344067788c2679f048a20057c7cc5a/tests/skill-behavior/README.md)

## vercel-labs/agent-skills

读取分支 `main`；默认分支 `main`；commit [`1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62`](https://github.com/vercel-labs/agent-skills/commit/1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62)。

借鉴：短索引按条件指向有原因、边界及正反示例的专业规则。所读校验器和样例提取器主要检查结构/生成材料，不能把存在 test-cases.json 写成行为或性能已验证。

实际完整读取：

- [skills/react-best-practices/SKILL.md](https://github.com/vercel-labs/agent-skills/blob/1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62/skills/react-best-practices/SKILL.md)
- [skills/react-best-practices/rules/async-parallel.md](https://github.com/vercel-labs/agent-skills/blob/1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62/skills/react-best-practices/rules/async-parallel.md)
- [packages/react-best-practices-build/src/validate.ts](https://github.com/vercel-labs/agent-skills/blob/1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62/packages/react-best-practices-build/src/validate.ts)
- [packages/react-best-practices-build/src/extract-tests.ts](https://github.com/vercel-labs/agent-skills/blob/1a2c79d4e6c4a2283dc2c614b6538cbe1ed5ca62/packages/react-best-practices-build/src/extract-tests.ts)

## GSD 迁移来源（单独版本）

旧仓 `gsd-build/get-shit-done`，main / `bdcaab2c752d9a33a1a1ca9acf3a3c81fb991815`：[实际读取的 README.md](https://github.com/gsd-build/get-shit-done/blob/bdcaab2c752d9a33a1a1ca9acf3a3c81fb991815/README.md) 指向 open-gsd/gsd-core。旧仓迁移证据不混用新仓 SHA。

## 宿主记录能力的核验

- 本机只运行 `codex --version` 和 `codex exec --help`：版本 `0.167.0-alpha.4.1`，支持 `--json`、`--ignore-user-config`、`--ephemeral` 和显式工作目录。帮助命令发生个人临时目录访问警告但成功返回；没有运行模型会话、变更配置或解决该权限问题。
- 已实际读取 [官方非交互模式文档](https://learn.chatgpt.com/docs/non-interactive-mode)：说明 JSONL 事件和 usage。它是输出运输依据，不证明本机所有工具参数、完整输出或实际文件访问均可观察。
- 已实际读取 [官方 AGENTS 配置文档](https://learn.chatgpt.com/docs/agent-configuration/agents-md)：全局及祖先指令可能影响运行，需验证干净 profile 与项目输入隔离；`--ignore-user-config` 本身不等于移除所有指令。
- 已实际读取 [官方技能评测文章](https://developers.openai.com/blog/eval-skills)：示例用宿主事件检查命令/产物，再作质量评估。本计划增加隐藏判定、错误补丁校准及独立评分，不把命令出现当成任务成功。
- 这些官方网页是2026-11-12动态页面核查，无可核实的文档 commit；不编造 SHA。正式启用前的两个运输探针尚待计划确认。
