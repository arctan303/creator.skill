# Current repository state

Baseline: [1.6.0 is published](https://github.com/arctan303/creator.skill/releases/tag/v1.6.0), 2026-10-14, at release commit `55bb1fb`. GitHub Actions, the tag, downloaded assets and installation were verified. The project is now in sustained real-project use; subsequent main changes record the release receipt and feedback. [Public overview](../README.md) explains usage.

## Architecture and current work

- AGENTS.md is the canonical workflow policy; .agents/skills contains scoped capabilities and English discovery metadata.
- Project knowledge upkeep separates current facts, effective conventions, active tasks and historical evidence; 12 canonical skills share one policy.
- Unified package/ownership-aware upgrade, bilingual guides and isolated behavioral fixtures are implemented; see [completed 1.6 plan](DEV-PLAN.md#completed-160-delivery) and [effective decisions/evidence](workflow-1.6.md).
- Build/verification scripts live in scripts; shared runtime references and checkers in .creator; Python regression tests in tests.
- GitHub About uses an English-first bilingual description of the supported hosts, reusable skills, flexible delivery and project knowledge, with focused topics. Its homepage is the original blog entry at `https://blog.arctan.top/post/52/`; an unrequested replacement with the quickstart was reverted on 2026-10-14. Copy/topic optimization does not itself establish a decision to replace that destination.
- Current stage: sustained real-project use of 1.6.0. User-reported issues are collected in the [1.7 feedback and candidate record](workflow-1.7.md); no 1.7 feature scope or automatic sibling-project rollout is implied.
- Field investigation on 2026-11-06 compared four registered 1.6.0 business workspaces with older and experimental samples. Current design-rule inheritance, asset reuse and visual evidence inform FB17-003; an entry/reference contradiction in design interviews is confirmed as FB17-004. Findings are recorded for the next scoped design-workflow update; runtime rules and installed projects were not changed.
- Local source update on 2026-11-11 requires task-relevant project-design reading and reconciles design interview/sizing rules. The [first baseline patch evidence](validation/1.7-ui-baseline.md) is historical: its direct shared fallback is superseded by the user-authorized adaptation model in FB17-006.
- Completed local scope: [scenario library and project design adaptation](tasks/design-library-20261111.md). Nine [authoring modules](../design-library/README.md) belong to the gateway; shared procedures govern selective adoption and existing-rule reconciliation. Daily development and review read project-adopted rules and relevant nested references. See [usage](design-adaptation.md). No publication, installed gateway replacement or sibling upgrade was performed.
- Pending user confirmation, 2026-11-12: [evaluation-first skill improvement plan](tasks/workflow-eval-loop-20261112.md). It fixes the current uncommitted workflow as W0, records pinned research and proposes repeated control/workflow trials with hidden checks and host traces. Methods and chapter removal depend on the same evaluation; no new skill edits or evaluation executions have begun.

## Active limitations

- Current unreleased source: 71 script tests, 58 structural cases, package/install isolation checks and three executed synthetic design-document tasks passed their respective checks. [Detailed evidence](tasks/design-library-20261111.md#verification-evidence--2026-11-11) distinguishes scope, semantic review and reported read selection. Real rendered UI quality and long-term model adherence remain untested.
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

Current decisions: [1.6 contract](workflow-1.6.md). Active work: [plan](DEV-PLAN.md). Historical rules explain previous behavior and do not reopen retired work.
