# Project knowledge contract

## Responsibility and boundaries

This skill maintains the lifecycle of knowledge already supplied or established during the task. It does not choose product behavior, design a new interface, implement a release, or evolve the global workflow. Those activities retain their own skills and authorization. Routine implementation still updates its affected documents; this skill is useful when conventions, replacements or document responsibilities need reconciliation.

Use the repository's existing language and naming. Do not add translated copies of authoritative rules solely because the conversation uses another language. A requested bilingual user guide can have translations; the instruction source and replacement relationships remain unambiguous.

## Classification and capture

| Kind | Capture trigger | Home and limits |
| --- | --- | --- |
| Explicit project convention | The user states a repeatable preference or corrects a project rule; “remember” is not required | Existing design/development/release document. Preserve actual scope, reason and explicit exceptions. No three-event threshold. |
| Verified fact | Code, configuration or a result establishes current behavior | Current-state entry or relevant topic, with code/environment baseline when material. Not proof of the desired behavior or permanent policy. |
| Candidate inference | A possible convention inferred from an isolated choice, repetition or outcome | A short candidate note in the relevant existing task if useful. Label uncertainty; do not expand scope or present it as the user's decision. |
| Task authorization or restriction | Permission to push this candidate, a browser restriction, a temporary no-build instruction | The relevant task/checkpoint, with object and scope. Never a standing release permission or global preference. |

An explicit statement can be captured after one occurrence. A repeated inference is still an inference. A local correction such as “use the themed selector for this mailbox picker” does not mean “ban native controls everywhere.” A factual `pnpm-lock.yaml` does not mean the user wants pnpm in every repository.

For meaningful decisions record enough to recover the rule: what applies, where it applies, source, status, and replacement/exception relationships when relevant. Reuse a stable existing decision/task ID; do not require a new ADR or full form for a small convention. Avoid copying chat transcripts or sensitive values.

## One home per responsibility

- **Current state**: verified capabilities, architecture, entry commands, current milestone, limitations and navigation. Do not fill it with every execution event.
- **Effective expectations**: accepted product requirements, design principles and release conventions, including requirements not yet implemented.
- **Active work**: still-applicable tasks, dependencies, verification gaps and recovery conditions. A missing file or absent implementation alone does not cancel a requirement.
- **Historical evidence**: prior decisions, implementation, failed/skipped checks, reviews and releases. It explains what happened, not what must be done next.

Prefer current entrypoints plus relevant active work on startup. Open history only to trace an actual question or replacement; do not load all Phase files and convert every “untested” occurrence into a current obligation.

## Applicability is separate from execution

| Applicability | Meaning and action |
| --- | --- |
| Active | The expectation remains valid. An old or unimplemented task can still be active. |
| Superseded | A named successor decision/task replaces this scope. Follow the replacement chain to the current expectation. |
| Partially superseded | Identify exactly which clauses/outcomes are replaced and which remain active; transfer only valid obligations. |
| Retired or withdrawn | An explicit removal/cancellation makes this work inapplicable. Preserve the source and historical results; remove obsolete obligations from the active queue. |

Keep the original implementation, validation, review and release outcomes alongside this applicability. “Retired; browser test was never run” is valid. “Passed” is false if the check never ran. A removed feature's failed review does not become a current blocker unless a still-active dependency or risk is identified.

When a current rule changes:

1. Read the new decision and the affected current clauses; identify their consumers and live tasks.
2. Revise current text and relevant references in place. Mark old decisions with the successor or explicit withdrawal; avoid two competing current copies.
3. Trace dependent obligations. Close only those invalidated by the change; keep partial survivors, unresolved current risks and retained capabilities.
4. Preserve historical evidence and link it from the replacement/task when useful. A “retired” label is not a missing test result or a review exception.
5. Check the affected entry and active plan no longer revive obsolete work. Do not re-run obsolete feature tests merely to make the historic Phase look complete.

## Scoped upkeep and cleanup

Ordinary authorized work includes its necessary documentation update. Broad migration or cleanup needs an appropriate requested scope; read-only orientation is not permission to reorganize the repository. Gateway installation delegates knowledge work here and does not prove docs migration complete.

At a meaningful change or milestone, update the affected entry, current rules and active plan. If no current summary changes, leave the entry untouched. Consolidate repeated content into its established authoritative home and repair links. Use the existing archive for unique history; do not create a new file for each turn or mechanically archive all old-looking tasks.

Before moving or removing material, establish its responsibility, source, replacement and recoverability. Keep unknown or concurrently edited documents. Unreferenced does not mean obsolete. Do not delete unique decisions, evidence or unresolved expectations to reach a size target. Follow the shared batch-queue closure rules and preserve items not covered by the actual review/retirement scope.

## Verification and handoff

Structural checks verify paths, declarations and links; semantic self-review verifies ownership, applicability and replacement relationships. Neither is a fresh model-behavior evaluation. Report these evidence types separately. A `complete` registration is not proof of deployment, user acceptance or every historical test.

Check that a fresh reader can identify current facts, desired-but-unimplemented behavior, live work and the source of retired work without reading all history. State any evidence gap without turning it into a blocker for unrelated work. Report new conventions briefly and allow corrections; do not ask the user to approve a clerical record of an already explicit decision.

## Examples

### Capture an ordinary project correction

The user says, during settings work, “keep the overview concise; edit multi-field settings in a dialog.” Update the existing project design rules with that scope and rationale. Preserve inline controls for explicitly exempted high-frequency options. Do not wait for “remember” and do not impose the rule on another app.

### Preserve release differences

Project A uses `vX.Y.Z`, pnpm and a combined bilingual changelog; project B uses `X.Y.Z`, npm and separate language files. A request to reuse B's release approach in A may establish the shared dev-to-main procedure, but the implementation must inspect and preserve A's actual tag, package and resource contracts unless the user changes them. A prior authorized release does not authorize the next one.

### Retired AIWorker must not return as a task

A historical Phase records missing cross-site AIWorker browser tests. A later effective decision removes that shared capability. On “familiarize yourself with the repository,” report the current independent-site architecture and mark the old checks historically unperformed but no longer applicable. Do not schedule tests, restart a reviewer, ask again whether to remove the feature, or claim those tests passed.

### Partial replacement and still-valid work

A replacement removes cross-site authentication but retains per-site AI chat. Close the obsolete cross-site test obligation, retain a still-required chat error-recovery test, and link both decisions. Do not archive the entire Phase as if all its behavior disappeared.

### A withdrawn motion preference updates all current consumers

The user changes a project motion policy. Revise the authoritative principle and any currently effective Design-Brief clause or active acceptance case that still states the old behavior. Retain historical reduced-motion test results as historical evidence. Do not apply this preference to other projects, and do not mark remaining unrelated design issues resolved.

### No automatic cancellation from code

An accepted export feature has no implementation. With no withdrawal or replacement evidence, keep it as an active, unimplemented requirement. An unused document or old timestamp is not a cancellation source.

## References

Use the [shared project knowledge reference](../../../../.creator/references/project-knowledge.md) and relevant sections of the [workflow contract](../../../../.creator/references/workflow-contract.md). For a broader authorized legacy migration, use the [migration guide](../../../../.creator/references/docs-migration-1.5.md).
