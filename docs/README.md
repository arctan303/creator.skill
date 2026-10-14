# Current repository state

Baseline: [1.6.0 is published](https://github.com/arctan303/creator.skill/releases/tag/v1.6.0), 2026-10-14, at release commit `55bb1fb`. GitHub Actions, the tag, downloaded assets and installation were verified. The project is now in sustained real-project use; subsequent main changes record the release receipt and feedback. [Public overview](../README.md) explains usage.

## Architecture and current work

- AGENTS.md is the canonical workflow policy; .agents/skills contains scoped capabilities and English discovery metadata.
- Project knowledge upkeep separates current facts, effective conventions, active tasks and historical evidence; 12 canonical skills share one policy.
- Unified package/ownership-aware upgrade, bilingual guides and isolated behavioral fixtures are implemented; see [closed local plan](DEV-PLAN.md) and [effective decisions/evidence](workflow-1.6.md).
- Build/verification scripts live in scripts; shared runtime references and checkers in .creator; Python regression tests in tests.
- Current stage: sustained real-project use of 1.6.0. User-reported issues are collected in the [1.7 feedback and candidate record](workflow-1.7.md); no 1.7 feature scope or automatic sibling-project rollout is implied.

## Active limitations

- Local verification: 63 script regressions, 46 structural policy cases, 3 executed synthetic tasks, package installation/link checks and independent upgrade/distribution review passed. These are distinct evidence categories, not a combined count of model trials.
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
