# 1.7 field feedback and candidates

Status: **1.7.0 local candidate, unpublished**, prepared under the user's 2026-11-12 execution instruction. It includes the earlier local design/adaptation work and the bounded S1–S5/M1–M5 update. Only basic script, structure, build/package/temporary-install and documentation checks ran this iteration; installed business workspaces retain their own baselines.

Source: the user's screenshot corrections, researched-design/adaptation requests and 2026-11-12 bounded implementation authorization. The [current task](tasks/1.7-local-candidate-20261112.md) records accepted scope and evidence; the [formal evaluation design](tasks/workflow-eval-loop-20261112.md) is deferred and retained. The user will install and trial the candidate; this record does not authorize publication or claim long-term testing passed. Earlier report/version statements below retain their historical baseline.

## Capture during ordinary use

The user can describe a problem naturally. The assistant records the relevant facts here without requiring a form or a separate “remember” request. Investigate technical gaps first; ask only when a missing fact or unresolved experience boundary prevents a useful decision. Keep scope local to this workflow repository; project-specific conventions remain in their own projects.

For each actual report, retain a stable ID, date, workflow/host/model baseline when known, expected versus observed behavior, minimal reproduction or evidence, concrete impact and current status. Distinguish a user report, an independently reproduced defect and an inferred cause. Merge repeated evidence into the same issue rather than creating duplicate tasks. Keep private logs/conversations and credentials out of this public record; use a redacted summary or synthetic case.

Observe task flexibility and unnecessary questions, useful delegation, natural convention capture, current-state accuracy and retired-task handling, upgrade preservation, documentation upkeep and bilingual first use. These are observation areas, not presumed defects or mandatory testing steps for every task.

## 1.7 试用重点

以下关注点对应本地候选改动；本轮未运行模型或 UI 试验。用户按上面的自然反馈方式描述问题，新增报告沿用稳定 `FB17-xxx` 编号；同一问题合并证据，不重编号。记录反馈时，由助手读取该项目 `.creator/install-state.json` 的 `package_sha256` 前 12 位写入报告，以区分不同的本地 1.7.0 构建，不要求用户自行查找；记录不可用时如实注明未知。

- 设计读取：UI 任务是否实际读取项目设计入口及适用的逐层引用，日常开发是否只使用本地已采纳规则。
- 设计适配：网关是否能为新项目裁切、为已有规范补缺，并保留项目约定、路径和例外。
- 自主推进：已有既定规则时是否仍做设计采访或要求返回前序阶段；独立部分能否继续。
- 冲突分流：过时测试/文档、回归和已批准变更是否先分类，避免过早转成产品变更。
- 修复证据：是否报告隔离副本中撤回修复后的失败、恢复后的通过，或如实说明不能执行与证据较弱；是否排除只修症状的结果。
- UI 验证：是否复用现有组件/素材，并实际查看对应最终源码、状态和视口的截图；改交互后是否操作验证，且区分模拟、本地、部署环境。
- 计划与恢复：切片是否对应可验收的用户结果；恢复是否核对实际状态，避免重复外部动作、覆盖他人改动或相信旧的“全部通过”。
- 触发与边界：未明确要求时是否擅自建立 Goal；明确授权的优化是否仍等待次数；轻量改动是否被过度验证，结构检查是否冒称行为通过。

## Reports

### FB17-001: repository About omitted from release presentation

- Source/baseline: user screenshot and GitHub metadata readback on 2026-10-14, after the 1.6.0 release. The README had been refreshed, while About still described a generic multi-skill delivery system with broad `llm`/`skill` topics. The existing blog homepage was not established as a defect.
- Expected/observed: the public entry should explain the same product as the new README. The mismatch was independently confirmed; no reduced-discovery or adoption effect was measured.
- Resolution: the GitHub description now leads with English and names Codex, Claude Code, reusable skills, flexible delivery and project knowledge, followed by Chinese. Seven focused topics were read back after the update. The original blog homepage was restored after the separate scope error in FB17-002; the runtime package and release tag were not changed.
- Status: repository presentation corrected. Candidate for 1.7 investigation: release preparation could inspect relevant external repository metadata alongside public guides when that surface is in scope. Whether this needs a reusable workflow rule is not yet established; no blanket requirement or new release is authorized by this entry.

### FB17-002: About optimization changed an unsettled link destination

- Source/baseline: the user questioned why the external link changed on 2026-10-14. During FB17-001, the assistant replaced the existing blog homepage with the quickstart to simplify installation discovery, without an established user decision to replace that destination.
- Observed failure: a general presentation-improvement request was interpreted too broadly. Changing where visitors go is an experience choice, separate from rewriting copy or selecting relevant topics. The prior experience-boundary contract already applied; this incident does not establish that more rules are necessarily needed.
- Correction/status: the assistant restored `https://blog.arctan.top/post/52/` and read back the homepage, description and topics. The updated description and seven topics remain. Keep this as a confirmed scope-handling incident for 1.7 evaluation, not an inferred universal preference for blog links. No global rule patch has been made.

### FB17-003: design work needs a concrete project baseline

- Source: the user's 2026-11-06 feedback and read-only inspection of local repositories. Four business workspaces declare unified 1.6.0; their two design skills and two stage contracts match their registered hashes. Other samples use 1.3–1.5, lack a workflow installation, or are experiment copies. Do not count them all as 1.6 behavior trials.
- Observed: effective design documents already cover component reuse, control semantics, information density, nearby state feedback, assets and acceptance. Some corrections postdate the 1.6 upgrade; several principles predate it. Existing records do not establish whether automatic skill invocation, an explicit user request or ordinary document editing captured a particular clause.
- Existing mechanisms already say to reuse project conventions and choose minimal design artifacts. The missing operational detail is how a design task identifies the applicable rules, existing implementation and assets, local exceptions and the actual uncertainty before selecting a tool or proposing a new direction.
- Field evidence includes restoring settings that violated established rules; reusing an installed icon library rather than letter substitutes or new dependencies; adapting one project's general design methods to a different product with explicit exclusions; and preserving established visual expression when fixing timing. Sources and local baselines remain in ignored `.creator/evaluations/1.7-design-field-20261106/`; private documents are not copied into this public record.

Candidate changes for a bounded 1.7 design-workflow update:

1. Start from registered project principles, page-specific design, existing components/tokens/assets and the latest effective exceptions. Summarize only the few clauses affected by this task; do not create a complete new Design Brief for each change.
2. Distinguish restoring a known design, extending the current system and choosing genuinely new behavior or expression. Existing user decisions do not need another interview; a proposed change to a still-unsettled experience boundary does.
3. Select tools by the missing evidence or deliverable: real-component inspection for an existing screen, a minimal prototype for unresolved layout/interaction, existing icons/assets for established visual vocabulary, and new asset creation when there is an actual gap. No mandatory named design tool or prototype stage follows from these samples.
4. Carry existing asset provenance and delivery constraints into implementation. A filename or generated image does not establish a license, maintainable source or working deployed asset; relevant project evidence must be checked.
5. Verify affected real states and composition. Counts, source assertions and no-overflow geometry alone do not establish visual quality; screenshot evidence needs inspection, while interaction changes need relevant behavior checks. Keep unavailable evidence and historical pending checks honest.
6. Separate transferable methods from product aesthetics. Theme, icon family, animation policy, dimensions and deliberate local exceptions remain project-scoped unless a broader decision is explicit. Repeated appearance in several projects is evidence for a candidate, not permission to silently unify them.

Status: the 2026-11-06 survey itself changed no runtime rule or installed project. Its design-context and evidence findings now inform the authorized local FB17-005 patch; source skills changed on 2026-11-11, with no sibling upgrade or release. Regression candidates not exercised by this patch remain candidates, not passed trials.

### FB17-004: design entry and stage contract disagree about questions

- Confirmed source conflict: [design-brief-builder](../.agents/skills/design-brief-builder/SKILL.md) permits professional decisions under existing project rules and asks only about necessary unresolved experience choices. Its [stage contract](../.agents/skills/design-brief-builder/references/stage-contract.md) still requires user selection whenever several directions are reasonable, and lists vague aesthetic words or an unexplained reference image as unconditional interview triggers.
- The entry also allows a scoped update while the reference presents a full brief structure and phase-like exit requirements without a clear delta-only application. This creates a credible route back to repetitive questions and unnecessary artifacts; field inspection did not isolate that text as the proven cause of every observed design deviation.
- Priority: reconcile the reference with the effective experience-boundary and task-sizing rules before adding another design capability. A regression should provide an existing design system plus a vague request and inspect whether the agent proceeds with a justified small change; a counterexample should leave a consequential new experience direction genuinely undecided.
- Status: the local 2026-11-11 patch reconciles the stage contract with scoped updates and experience-boundary questions. See [validation](validation/1.7-ui-baseline.md) for actual evidence and gaps. The 1.6 static suite's earlier success is retained; it did not prove this nested contract was consistent.

### FB17-005: basic UI rules must be concrete and actually read

- Source: three user-supplied screenshots on 2026-11-11 and explicit requests for researched form/admin design principles, task-dependent cross-references in AGENTS.md, and examination of [Impeccable](https://github.com/pbakaus/impeccable). Screenshots establish visible presentation complaints, not measured CSS, save behavior or a causal model comparison.
- Observed: simple settings require opening a repeated modal; field typography/control alignment and density vary; internal metadata occupies large equal-height cards; headings, explanations and actions repeat. The modal already has an outer radius/shadow, so the correction concerns coherent component treatment rather than claiming those effects are wholly absent.
- Local field context: the existing Tune principles already contain copy/component guidance and a broad multi-field/low-frequency modal preference. This feedback rejects treating field count alone as a reason for a dialog. It does not revoke every complex editor, every card, explicit Save semantics, necessary warnings or intentional brand expression. The sibling document is evidence, not edited or upgraded here.
- Goal and expected behavior: make UI tasks read their existing design owner and applicable linked rules, choose controls and presentation from the actual task/save contract, inherit project components and exceptions, and inspect relevant rendered states. The design material must cover forms, settings, admin hierarchy, copy, spacing/type, surfaces and evidence limits. FB17-006 subsequently defines it as authoring material to be selectively adopted, not a default runtime baseline.
- Scope/dependencies: reuse AGENTS.md and existing design/development/review capabilities; initially add a shared UI baseline, now superseded by the [scenario library](../design-library/README.md) and adoption model in FB17-006. Project design may be one document or a conditional index; follow relevant nested references before editing, without loading every branch or treating external material as extra authority. No new mandatory skill, fixed document naming, tool installation, business UI edits, sibling rollout, publication or version bump.
- Risk: R1, bounded reversible agent-rule changes can influence future UI decisions. Preserve effective project decisions and save/authorization boundaries; add positive and counterexample fixtures. This is an explicitly requested foundation, not silent promotion of one application's aesthetic preferences into a universal theme.
- Research: Carbon, Fluent, GOV.UK, Atlassian, WAI/WCAG and original UI research support task structure and interaction rules. Impeccable source was read at `c1e0e5492fbb524f5df84d635ecfae7dc438ec45`; its useful context/operate/layout/polish/clarify methods inform the baseline without importing its complete workflow or aesthetic absolutes. Detailed citations live with the affected rules.
- Implementation: AGENTS requires actual project-design reading even when design skills are skipped; design-brief, design-maker, dev-builder and reviewer initially linked a single baseline; FB17-006 replaces that runtime dependency with local adopted rules and short procedures. FB17-004's unconditional interviews and full-Brief gates are replaced. Generic baseline values are explicitly optional starting points; effective local exceptions prevail.
- Validation/release: see [scoped evidence](validation/1.7-ui-baseline.md). Structural, scripted, synthetic document-decision and real UI evidence remain separate. Version stays 1.6.0; locally rebuilt ZIPs are unpublished candidates, not replacements for the published release assets. Future feedback should include the task, inherited rules and actual output so remaining failures can be located.

### FB17-006: design material should support project-specific adaptation

- Explicit clarification, 2026-11-11: the user wants richer guidance for different design scenarios, from which repositories can select and adapt their own design conventions. The shared collection should not itself be a ready-made policy applied directly to every project. Existing project principles must also be supported. This clarifies the desired product role beyond FB17-005's screenshot-focused baseline.
- Authorization: the user explicitly requested implementation of the adaptation direction on 2026-11-11, including new-project authoring, existing-rule merging/preservation and local-only daily reading. This is a bounded source update, not publication or sibling rollout.
- Architecture: nine scenario modules supply conditions, alternatives, states, examples, sources and observable acceptance. The [library index](../design-library/README.md) selects by page/task. The [shared adaptation procedure](../.creator/references/design-adaptation.md) converts selected material into concrete project-owned rules; [daily reading](../.creator/references/project-design.md) uses those effective local rules and relevant nested references.
- Gateway: installation and design adaptation are separate routes. Reuse design-brief-builder for decisions and project-knowledge for reconciliation when installed; the standalone gateway can perform the same procedure without installing a workflow. The ownership-aware installer does not semantically merge project prose or rewrite design during ordinary upgrades.
- Preservation: retain effective choices, scoped exceptions, paths and language; fill actual gaps and replace superseded active clauses in place. Record adopted revision/modules briefly as provenance, not an ongoing runtime dependency. Library updates do not authorize replacement or certify UI implementation; a mature project may need no changes.
- Distribution: the full authoring library ships only in creator-gateway.zip. Project workflow assets carry the small reading/adaptation procedures. Build verification checks complete gateway content and rejects library leakage into the workflow; installer ownership remains unchanged.
- Status: local implementation and bounded verification are complete: 71 script regressions, 58 structural cases, package checks and three executed synthetic document tasks. See the [bounded task](tasks/design-library-20261111.md) for separate evidence categories and remaining real-UI/long-term gaps. The previous direct-baseline model is retired, with [historical evidence](validation/1.7-ui-baseline.md) preserved. No external skill installation, installed gateway replacement, sibling update, release or version bump was performed.

Resolved 1.6 development issues remain in the [1.6 evidence](workflow-1.6.md); they are regression context and must not be reopened merely because this feedback record exists.

## From evidence to 1.7

Use [EVOLUTION.md](../EVOLUTION.md) to distinguish demonstrated workflow failures from project preferences and transient host/tool failures. Prioritize by concrete impact and recurrence; do not manufacture an occurrence threshold for an explicit optimization request. Candidate fixes need a relevant failure scenario, a counterexample and evidence appropriate to the change.

The 2026-11-12 instruction approves the bounded local candidate scope recorded above; further improvements depend on new feedback and authorization. Reports do not themselves authorize publication, automatic global rule propagation, background telemetry or upgrades to other repositories. Preserve each report's actual source baseline rather than rewriting historical evidence to match the candidate.
