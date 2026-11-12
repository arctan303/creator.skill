# Current repository state

Current stage: **1.7.0 published; sustained use and 1.8 feedback collection**. The [release](https://github.com/arctan303/creator.skill/releases/tag/v1.7.0) was published on 2026-11-12 at `edb39b531264b116d02ac2be7e6edf987bfdbe10` through the existing Release workflow. See [publication and asset evidence](validation/1.7-release.md) for completed checks and their limits. Record new observations in [1.8 field feedback](workflow-1.8.md); [1.7](workflow-1.7.md) is a closed historical record.

Previous published baseline: [1.6.0](https://github.com/arctan303/creator.skill/releases/tag/v1.6.0), 2026-10-14, at release commit `55bb1fb`. GitHub Actions, the tag, downloaded assets and installation were verified. The [public overview](../README.md) and quickstarts now target published 1.7.0.

## Architecture and current work

- AGENTS.md is the canonical workflow policy; .agents/skills contains scoped capabilities and English discovery metadata.
- Project knowledge upkeep separates current facts, effective conventions, active tasks and historical evidence; 12 canonical skills share one policy.
- Unified package/ownership-aware upgrade, bilingual guides and isolated behavioral fixtures are implemented; see [completed 1.6 plan](DEV-PLAN.md#completed-160-delivery) and [effective decisions/evidence](workflow-1.6.md).
- Build/verification scripts live in scripts; shared runtime references and checkers in .creator; Python regression tests in tests.
- GitHub About uses an English-first bilingual description of the supported hosts, reusable skills, flexible delivery and project knowledge, with focused topics. The historical homepage `https://blog.arctan.top/post/52/` was restored after an unrequested quickstart replacement on 2026-10-14. Read-only metadata verification during the 1.7 release found the current homepage `https://blog.arcinks.com/post/52`; no About, homepage or topics write was made in this release. Copy/topic optimization does not itself establish a decision to replace that destination.
- Current work: observe 1.7.0 in real projects and capture [1.8 feedback](workflow-1.8.md), including the installed package hash prefix. [Candidate evidence](tasks/1.7-local-candidate-20261112.md) and [release evidence](validation/1.7-release.md) remain separate. This release does not authorize sibling installation, personal gateway updates, GitHub About/homepage/topics changes or later publication.
- Field investigation on 2026-11-06 compared four registered 1.6.0 business workspaces with older and experimental samples. Current design-rule inheritance, asset reuse and visual evidence inform FB17-003; an entry/reference contradiction in design interviews is confirmed as FB17-004. Findings are recorded for the next scoped design-workflow update; runtime rules and installed projects were not changed.
- Local source update on 2026-11-11 requires task-relevant project-design reading and reconciles design interview/sizing rules. The [first baseline patch evidence](validation/1.7-ui-baseline.md) is historical: its direct shared fallback is superseded by the user-authorized adaptation model in FB17-006.
- Completed local scope: [scenario library and project design adaptation](tasks/design-library-20261111.md). Nine [authoring modules](../design-library/README.md) belong to the gateway; shared procedures govern selective adoption and existing-rule reconciliation. Daily development and review read project-adopted rules and relevant nested references. See [usage](design-adaptation.md). No publication, installed gateway replacement or sibling upgrade was performed.
- Completed local scope on 2026-11-12: S1–S5 align stale clauses and structural-check wording; M1–M5 add conditional verification, diagnosis, UI evidence, outcome slices and recovery methods. Related duplication is consolidated; AGENTS.md stays unchanged from the saved worktree baseline.
- The [formal evaluation plan](tasks/workflow-eval-loop-20261112.md) is **deferred and retained for future use**. Its source appendix and baseline manifest remain historical records; they remain available for 1.8 and do not gate this completed basic-test iteration. No formal model A/B, hidden-test environment or independent scoring was run.

## Active limitations

- 1.7.0 asset digests and fresh/repeat/real-CRLF upgrade checks passed. Strict Windows LF rebuilding differs only in manifest key order (67/68 workflow members match; gateway 20/20); all manifest values and declared hashes agree. See [release evidence](validation/1.7-release.md) and [FB18-001](workflow-1.8.md#fb18-001-cross-platform-manifest-order-affects-byte-reproduction). No independent Linux rebuild was available.

- Current 1.7 installer fix: 77 script tests, 63 structural cases, package/install/docs checks and scoped R2 review passed; see [current evidence](tasks/1.7-local-candidate-20261112.md). No model or rendered-UI trial ran. The [2026-11-11 synthetic document tasks](tasks/design-library-20261111.md#verification-evidence--2026-11-11) belong to their earlier baseline and do not establish this candidate's behavior.
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

Current decisions: [1.6 contract](workflow-1.6.md) with the bounded [1.7 implementation](tasks/1.7-local-candidate-20261112.md) and [one-time release authorization](validation/1.7-release.md). Active work: [plan](DEV-PLAN.md). Historical rules explain previous behavior and do not reopen retired work. Pushing VERSION changes to main triggers automatic release; this one 1.7.0 release and its documentation receipt do not grant permission for future releases.
