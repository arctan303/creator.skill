# Workflow evolution

Evolution repairs demonstrated workflow defects. Project design principles, release conventions and collaboration preferences belong to `project-knowledge`, even when the user never says “remember this”.

## Signal location and lifecycle

New installations use `.creator/evolution/signals.md`. Existing `.codex/evolution/signals.md` and `.claude/evolution/signals.md` remain valid evidence: discover and reconcile existing entries by stable ID/source before choosing one active ledger. Never overwrite, silently concatenate duplicates, or discard a legacy ledger during upgrade. Runtime ledgers are separate from versioned workflow rules.

Each signal records ID, affected rule, issue category, concise evidence/source, first/latest occurrence, count, severity and status:
- `观察中 / observed`: first ordinary demonstrated defect.
- `待处理 / pending`: three matching ordinary signals, one serious incident, or an explicit authorized optimization request.
- `待确认 / needs-input`: a necessary decision or authorization is genuinely missing.
- `已转补丁 / patched`: rule changed; distinguish structural, scripted and real agent evidence.
- `已忽略 / dismissed`: evidence shows it is not a workflow defect; retain the reason.

Merge by affected rule + issue category. A repeated event adds evidence rather than another competing entry. One-off infrastructure failures, unsupported speculation and personal preferences are not workflow defects. Explicit corrections showing a rule failure are valid evidence; a user's silence is not satisfaction.

## Patch discipline

1. Modify an ineffective rule; merge conflicting rules; remove obsolete rules. Add a rule only when those cannot solve the problem.
2. Bind each patch to a concrete regression scenario covering the failure and a relevant counterexample. Record observed baseline evidence honestly; do not invent a failing baseline run.
3. Validate relevant behavior and changed scripts. Static contracts or self-reported response fields are not proof of actual actions. Keep expected results out of model-facing fixtures.
4. Record files, replaced rule, new rule, scope, scenario IDs, evidence and remaining gaps.

Explicit user authorization persists across rule files and skills. Do not repeatedly ask to implement the already authorized optimization. Ask only for unresolved experience-boundary choices or missing authorization. Do not relax privacy, review or release boundaries by inference. If meaningful regression evidence cannot be formed, keep the signal without applying a speculative patch.

## Upgrade ownership

Record local workflow customizations with their rationale and regression cases so upgrades can reconcile them. An unregistered customization is still user data: lack of a ledger entry does not authorize overwriting it.

Use the gateway installer and file hashes / supplied previous package to distinguish unchanged owned files, modified owned files and unrelated files. Normal authorized upgrades may replace unchanged owned rules and remove obsolete unchanged owned paths. Preserve and report customized or unknown files; migrate their effective content before explicitly resolving a conflict. Keep project docs, docs-state, all signal ledgers and custom cases. Do not silently replay old policy patches over newer conflicting rules.

## Execution and recovery

Process signals at a safe checkpoint, never in the middle of a deployment, migration or critical write. Delegate bounded independent work when useful; risk determines fresh review. Respect user/host constraints. Stop repeated attempts without new evidence, record the checkpoint and resume only from verified state.

Source-repository development may use CHANGELOG and the development record instead of a second signal ledger. Record actual scripted/agent tests and separately disclose unavailable cross-host validation or user-reserved project testing.
