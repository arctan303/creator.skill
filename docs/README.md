# Current repository state

Current source: **1.7.0 local candidate, unpublished**, prepared on 2026-11-12 on `codex/1.7-local-candidate`. Only basic script, structure, build/package/install and documentation checks were run in this iteration. The user will install and trial it in real projects; [task and evidence](tasks/1.7-local-candidate-20261112.md) record scope and gaps. No push, tag, publication, sibling installation or personal gateway replacement was performed.

Published baseline: [1.6.0](https://github.com/arctan303/creator.skill/releases/tag/v1.6.0), 2026-10-14, at release commit `55bb1fb`. GitHub Actions, the tag, downloaded assets and installation were verified. [Public overview](../README.md) and quickstarts continue to target this published version until release authorization.

## Architecture and current work

- AGENTS.md is the canonical workflow policy; .agents/skills contains scoped capabilities and English discovery metadata.
- Project knowledge upkeep separates current facts, effective conventions, active tasks and historical evidence; 12 canonical skills share one policy.
- Unified package/ownership-aware upgrade, bilingual guides and isolated behavioral fixtures are implemented; see [completed 1.6 plan](DEV-PLAN.md#completed-160-delivery) and [effective decisions/evidence](workflow-1.6.md).
- Build/verification scripts live in scripts; shared runtime references and checkers in .creator; Python regression tests in tests.
- GitHub About uses an English-first bilingual description of the supported hosts, reusable skills, flexible delivery and project knowledge, with focused topics. Its homepage is the original blog entry at `https://blog.arctan.top/post/52/`; an unrequested replacement with the quickstart was reverted on 2026-10-14. Copy/topic optimization does not itself establish a decision to replace that destination.
- Current stage: local 1.7.0 candidate prepared under the user's 2026-11-12 bounded execution instruction; user trial and review-side diff inspection are next. [Feedback and trial focus](workflow-1.7.md) keep stable report IDs. No automatic sibling-project rollout is authorized.
- Field investigation on 2026-11-06 compared four registered 1.6.0 business workspaces with older and experimental samples. Current design-rule inheritance, asset reuse and visual evidence inform FB17-003; an entry/reference contradiction in design interviews is confirmed as FB17-004. Findings are recorded for the next scoped design-workflow update; runtime rules and installed projects were not changed.
- Local source update on 2026-11-11 requires task-relevant project-design reading and reconciles design interview/sizing rules. The [first baseline patch evidence](validation/1.7-ui-baseline.md) is historical: its direct shared fallback is superseded by the user-authorized adaptation model in FB17-006.
- Completed local scope: [scenario library and project design adaptation](tasks/design-library-20261111.md). Nine [authoring modules](../design-library/README.md) belong to the gateway; shared procedures govern selective adoption and existing-rule reconciliation. Daily development and review read project-adopted rules and relevant nested references. See [usage](design-adaptation.md). No publication, installed gateway replacement or sibling upgrade was performed.
- Completed local scope on 2026-11-12: S1–S5 align stale clauses and structural-check wording; M1–M5 add conditional verification, diagnosis, UI evidence, outcome slices and recovery methods. Related duplication is consolidated; AGENTS.md stays unchanged from the saved worktree baseline.
- The [formal evaluation plan](tasks/workflow-eval-loop-20261112.md) is **deferred and retained for future use**. Its source appendix and baseline manifest remain historical records; they do not gate this basic-test iteration. No formal model A/B, hidden-test environment or independent scoring was run.

## Active limitations

- Current 1.7 candidate: 71 script tests, 63 structural cases, package/temporary-install and documentation checks passed. No new model tasks or actual UI rendering were tested. The three synthetic design-document tasks in the [2026-11-11 evidence](tasks/design-library-20261111.md#verification-evidence--2026-11-11) apply to that earlier source baseline; they do not prove the final candidate's behavior.
- Published 1.6 verification: 63 script regressions, 46 structural policy cases, 3 executed synthetic tasks, package installation/link checks and independent upgrade/distribution review passed. These are distinct evidence categories, not a combined count of model trials; the current task records new-source checks separately.
- The real local FlareMail upgrade and scoped reconciliation are complete. The application-link follow-up adds five explicit mappings: all 136 registered Markdown documents pass with zero errors and 22 audited resolutions; registration is now complete. The 20 existing density warnings remain advisory. See [acceptance scope and results](validation/1.6-mail-upgrade.md).
- Exact application/resource mapping support, its regressions and rebuilt-package Mail verification are complete; see the [closed short task](DEV-PLAN.md). Source files and declaration scopes must exist, and unrelated missing or conflicting links still fail.
- [Release CI](https://github.com/arctan303/creator.skill/actions/runs/38576027027) passed on Ubuntu: 63 tests, 46 structural cases, build and package verification. Both published ZIPs passed digest/content checks and the downloaded gateway's Windows installation/repeat smoke test. See [release evidence](workflow-1.6.md).
- Live Claude discovery, interactive Linux-host loading and actual power-loss recovery remain untested; filesystem and interruption fixtures do not prove those behaviors. Long-term knowledge retention remains an observation gap. This 1.6.0 publication does not grant standing permission for later releases or imply measured adoption gains.

## Retired assumptions

- 1.5 dual instruction/package generation and blanket R0/R1 delegation prohibition are superseded by D16-01/04. Their historical release evidence is retained in [1.5 record](workflow-optimization.md), not a current task list.
- A removed capability's historical untested item is not automatically an active obligation. Applicability needs the effective decision; historical outcomes are never rewritten as passed.

## Validation entry points

Use Python 3.10+; some Windows PATHs point to an unrelated legacy Python. Confirm python --version or choose a suitable installed interpreter.

```text
python .creator/scripts/evaluate_prompt_cases.py
python -B -m unittest discover -s tests -v
python scripts/build_release.py
python scripts/verify_build.py
python .creator/scripts/check_docs.py --root . --require-complete
```

Current decisions: [1.6 contract](workflow-1.6.md) with the bounded [1.7 candidate update](tasks/1.7-local-candidate-20261112.md). Active work: [plan](DEV-PLAN.md). Historical rules explain previous behavior and do not reopen retired work. Pushing VERSION changes to main triggers automatic release; that action remains unauthorized.
