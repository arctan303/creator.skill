# 1.6 development contract and evidence

Status: implemented and locally verified; 1.6.0 release preparation is in progress, 2026-10-14. User authorization: implementation/bilingual support on 2026-10-13, followed by explicit 1.6.0 publication and sustained-use feedback for 1.7 on 2026-10-14. Follow [current state](README.md) and [delivery plan](DEV-PLAN.md). Previous [1.5 evidence](workflow-optimization.md) remains historical.

## Effective decisions and acceptance

| ID | Authorized requirement | Acceptance and replacement |
| --- | --- | --- |
| D16-01 | One AGENTS policy and unified workflow package | No generated second CLAUDE policy or old slash commands; host skill discovery adapters use canonical source. Replaces dual distribution/transformation. |
| D16-02 | Upgrade clears obsolete owned files while preserving project data | Hash/baseline proof, conflict report, idempotence and recovery fixtures; missing registration never authorizes losing customization. Replaces EVOLUTION blanket overwrite wording. |
| D16-03 | Ask at unresolved experience boundaries | Ordinary engineering choices proceed; already authorized visible changes are not asked again. Privacy/scope, consequential compatibility/cost and external authorization remain boundaries. |
| D16-04 | Task-dependent collaboration | Bounded parallel work allowed where beneficial; risk independently determines review. Replaces blanket R0/R1 no-subagent rule. |
| D16-05 | Project-first knowledge maintenance | Explicit conventions captured naturally in existing topic documents; inferred candidates and temporary exceptions distinguished; no automatic global propagation. Gateway routes; internal project-knowledge owns upkeep. |
| D16-06 | Current state and task applicability | One current entry; retire approved removed capabilities and their obsolete tests, preserve historical outcomes and still-active portions. AIWorker scenario must not revive old tasks. |
| D16-07 | Bilingual first-use experience | English and Chinese README/quickstart/walkthrough have equivalent claims; conversation follows user language; no duplicated translated policy trees. Repository identity stays unchanged. |
| D16-08 | Evidence-driven validation and concise documentation | Separate static checks, real filesystem tests, bounded model scenarios and actual host tests. Expected answers stay out of model-facing fixtures. No claim that a script certifies document semantics. |
| D16-09 | Explicit application-route and resource link support | User-authorized Mail follow-up: scoped exact href declarations identify real in-repository targets and evidence. Missing, ambiguous, unsafe and undeclared links still fail. This extends the earlier Markdown article route support; it does not execute application code or certify live HTTP behavior. |

User preferences are scoped to this project first. The release workflow remains explicitly authorized per release; knowing a procedure does not authorize publication. Cross-project commonalities can be proposed later, without silently changing sibling repositories.

## Motivation and observations

- User reports repeated technical questions, rigid sequencing and repeated manual documentation cleanup.
- User reports removed AIWorker work repeatedly resurfacing from old unchecked tests. A read-only sample confirmed archived unfinished evidence alongside explicit retirement; this is not an independent reproduction of every reported agent failure.
- Tune and Mail use existing design/release topic documents with different release conventions; do not copy either convention into global workflow defaults.
- 1.5 checker treated some directory, source-line and declared website-route links as missing files. Fix targeted link semantics, without suppressing true missing files.
- GitHub presentation led with workflow internals and offered Chinese-only onboarding. Improve first-use clarity without inventing adoption statistics or promising growth.

## Compatibility and ownership

Modern Claude Code supports AGENTS.md conditionally; configuration and ancestor instructions affect loading. Native skill discovery still uses .claude/skills. Adapters and diagnostics must preserve that distinction; do not equate a built archive with an observed host load.

Sources checked 2026-10-13: [Claude memory/AGENTS](https://code.claude.com/docs/en/memory#agentsmd), [Claude skills](https://code.claude.com/docs/en/skills), [OpenAI skill evaluations](https://developers.openai.com/blog/eval-skills). These support compatibility and evaluation mechanics; project policy remains this user's chosen contract.

Migration does not automatically migrate docs or overwrite local instructions. Retain old signal ledgers and custom cases. Conflict resolution must preserve local content and must not treat an unregistered edit as disposable.

The original implementation scope covered source and temporary fixtures. On 2026-10-14 the user additionally authorized a real local FlareMail upgrade and document cleanup using `gpt-6.1-sol` delegates; see the [scoped acceptance record](validation/1.6-mail-upgrade.md). Other business repositories and personal installations remain outside scope.

## Validation record

Local observations through 2026-10-14:

- `evaluate_prompt_cases.py`: 46 cases pass structural/interface/link checks; these are not 46 executed agent tasks.
- `python -B -m unittest discover -s tests`: current suite 63/63 passed (23 installer, 33 checker, 4 fixture-runner, 3 package-link tests). The application-link follow-up added 11 checker tests to the initial 52-test baseline, covering exact scope/query/fragment matching, root/trailing/dotted routes, missing files, overlap, conflicting resolutions and unsafe paths/symlinks.
  Temporary-directory sandbox setup previously failed; the authorized fixture-only suite ran through tool automatic approval. Actual Mail evidence is separate below.
- Three synthetic agent tasks completed with actual output files; scope hashes and semantic inspection passed. See [method and outcomes](validation/1.6-behavior.md). This used one fresh Codex subagent session and no parent history, not an OS sandbox or a multi-model comparison.
- Source document inventory has no link errors; density warnings concern retained history/evidence and do not automatically justify deletion or splitting.
- `build_release.py` and `verify_build.py`: two 1.6.0 packages, 12 canonical skills, hashes, adapters, all Markdown local links, temporary real installation, same-package idempotence and packaged scripts passed.
- Fresh independent upgrade/distribution review passed after one focused fix: the gateway initially omitted project-knowledge.md referenced by its guides; the builder now includes the shared-reference closure and the verifier checks transitive links. The reviewer independently removed that member in memory and observed rejection.
- The reviewer tested actual locally retained 1.5 release archives for Codex, Claude and both layouts together: all three upgraded, preserved custom skills/signals, removed obsolete owned Claude files and repeated without changes. Installer SHA256: CF5581B98DC8E01BFAD90CE155F78BBC214401783319E091330FD3F202C0C540; final builder/verifier review hash prefixes: 999A8EA2933B / CCC803177CD6.
- The initial authorized FlareMail upgrade passed official ownership, package content, 475 preserved-file hashes, old cases and repeat-install checks. The active plan was separated from historical evidence without cancelling remaining obligations. Its original inventory remained partial with 22 unsupported application-link reports; that historical result is retained.
- The authorized exact-link follow-up used `gpt-6.1-sol` with `high` reasoning for implementation, Mail installation and fresh review. Five declarations now yield 22 audited resolutions and zero errors across 136 Markdown documents; registration is complete, with 20 original density warnings retained. Only six expected files changed, 767 remained byte-identical, and repeat installation preserved all 773 hashes.
  Independent review also disabled declarations in memory and recovered exactly the original 22 failures. See [real workspace acceptance and limitations](validation/1.6-mail-upgrade.md); this is not a long-term memory, live HTTP or Claude evaluation.
- `git diff --check` passed. The later user instruction authorizes this 1.6.0 publication. Live Claude discovery, Linux execution and real power-loss recovery remain unverified at the local preparation stage; compatibility conditions are documented, recovery evidence uses fixtures/simulated interruption. Actual CI and release results belong below.

Current local artifact SHA256: creator-workflow.zip F77DEC79A24222A8F60BB5D577D54CFD1E7BC14F99D053FFA803BCCD5D7EC4F3; creator-gateway.zip A421F39B671B537287C709B0D8904FD907BB1FFEE2037B5D5A53DA35F8C8F327. These identify the rebuilt local 1.6.0 package with exact-link support, not publisher authenticity. The initial Mail upgrade's earlier package hash is retained in its acceptance record.

## Release 1.6.0

Authorization: the user's 2026-10-14 instruction to publish 1.6.0 and enter sustained use. Release preparation reuses the validated runtime baseline; only publication documentation and the 1.7 feedback entry are updated. The existing workflow triggers on a VERSION change pushed to main, runs checks/build/verification on Ubuntu and creates `v1.6.0` with the workflow and gateway ZIPs. No separate business deployment or global/project rollout is included.

Pre-publication scope/privacy review passed: the candidate source set contains only workflow source, tests and documentation; no actual secrets, private evaluation runs, business copies, logs, uploads or binary data were found. The two packages contain 64 and 7 entries respectively, with complete local references and no project knowledge/runtime state; the signal ledger is a blank installation template. GitHub Actions uses its scoped `GITHUB_TOKEN`; no credential values are copied into records.

The local checkout uses Git newline conversion. Ubuntu-generated package byte hashes may differ from the Windows preparation build; retain both baselines, verify published asset digests and contents against the release commit, and smoke-test the downloaded files. Do not silently replace an already published asset with a differently built archive.

Publication result: pending actual CI, tag/commit readback, asset download and installation verification. If CI fails, keep the failure evidence and fix only the demonstrated cause before resuming. If release recovery is needed, retain `v1.5.0` and use a separately authorized corrective release; an installer rollback must first reconcile post-upgrade edits with the retained local snapshot. Do not forcibly rewrite tags or erase project knowledge.
