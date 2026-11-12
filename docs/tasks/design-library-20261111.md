# Project design adaptation and scenario library

Applicability: effective, task completed locally. User authorization: 2026-11-11, implement the direction in FB17-006. Route: product change, bounded task, R1. This follows the local UI-baseline draft, not a new release authorization.

## Goal and scope

Provide a rich scenario reference library for authoring project-specific design rules. The gateway can establish rules for a new project or reconcile existing ones while preserving effective choices, local exceptions and document ownership. Daily development and review use only adopted project design rules, not the authoring library as an implicit fallback.

Implement nine scenario modules, one selection index, a shared adaptation procedure, gateway routing and discovery metadata, runtime reading boundaries, separate distribution, bilingual usage notes and regressions. No business UI edits, sibling upgrade, external skill installation, global gateway replacement, release, version bump or new search service.

## Expected behavior

- Adapt by page/task, not repository category alone. Source material is advisory until concretely adopted for a project; preserve provenance without copying the entire library.
- New projects get a small useful local design entry and only applicable detail. Existing projects retain paths, language, decisions and exceptions; unchanged adequate rules need no rewrite.
- A library revision does not change project rules or expand feature, save, privacy or publishing contracts. Ask only for a consequential unresolved choice; preserve independent progress.
- Gateway install and design adaptation are separately scoped routes. The ownership-aware installer does not merge project prose.
- The authoring library ships with the gateway only. The workflow package retains small reading/adaptation procedures and does not install the library into projects.
- UI work reads the actual project entry and its relevant nested references. Missing local guidance is resolved as a bounded design decision and captured locally, never by silently declaring the library effective.

## Dependencies and verification

Library and procedure drafts precede integrated gateway trials. Packaging must be checked after all source references stabilize. Reuse the existing skills, link checker, fixture transport and installer; preserve prior working-tree changes.

Verify structure/local links; run Python script regressions and real package/install/idempotence checks; execute answer-free synthetic gateway tasks for new-project authoring and existing-project reconciliation, plus a daily-work counterexample where unadopted library guidance must not override local rules. Inspect actual changed files and evidence limits. Do not count static cases as agent trials or document edits as rendered UI validation.

## Status

Implementation: complete in local source. Verification: the bounded checks below passed. Review: main-agent integration/diff review and two bounded cross-checks of the nine modules completed. Release: not performed or authorized; VERSION remains 1.6.0, so rebuilt archives are local candidates and not the published 1.6.0 assets. No real project or installed personal gateway was upgraded.

## Delivered behavior

- [Nine scenario modules and selection index](../../design-library/README.md), revision `2026-11-11.1`, with boundaries, decisions, states, examples, exceptions, acceptance and primary sources. No third-party skill installation or wholesale policy import.
- [Gateway routing](../../gateway/SKILL.md), [shared adaptation](../../.creator/references/design-adaptation.md) and [daily reading](../../.creator/references/project-design.md), integrated with the existing design/development/review/knowledge skills. The earlier large shared baseline was retired from runtime and its original draft retained under ignored local historical evidence.
- Separate gateway-only library packaging and verification; project prose remains outside installer ownership. Paired [English](../design-adaptation.md) and [Chinese](../design-adaptation.zh-CN.md) public usage guides explain unreleased status and independent design adaptation.
- Source-only trial preparation reuses the existing isolated-workspace transport, builds the real gateway into each workspace, and keeps private rubrics/baselines outside it. No new model service or automatic deployment was added.

The bounded module review found one disclosure-policy ambiguity: reading guidance could discourage generic not-found responses even when a project intentionally hides restricted resources. The clause now explicitly preserves that policy, consistent with the access module. The other four-module cross-check found no actionable issue. These are text reviews, not UI certification.

## Verification evidence — 2026-11-11

Commands ran with Python 3.12 on Windows. Temporary filesystem tests used tool-approved access to isolated temporary directories.

| Check | Observed result | Evidence limit |
| --- | --- | --- |
| `py -3.12 -B -m unittest discover -s tests -v` | 71 tests passed, including 4 distribution and 4 trial-transport regressions | Filesystem/script behavior, not model or visual success |
| `.creator/scripts/evaluate_prompt_cases.py` | 58 cases passed structure, metadata and local-link validation | No model responses supplied; not 58 executed agent tasks |
| `scripts/build_release.py` then `scripts/verify_build.py` | Passed real ZIP content/link closure, gateway library equality, workflow exclusion, temporary install and idempotence | No published asset or installed real workspace changed |
| `.creator/scripts/check_docs.py --root . --require-complete` | 19 registered docs, zero errors; four density warnings remain advisory (historical record, this task's evidence, prior baseline evidence and 1.7 feedback) | Local registration/links; not external HTTP or semantic completeness |
| `git -c core.safecrlf=false diff --check` | Passed | Whitespace only; semantic review performed separately |

Prepared `.creator/evaluations/design-adaptation-20261111/run-1` with `scripts/prepare_design_trials.py prepare --output ...`. Three fresh `gpt-6.1-sol` agents with high reasoning each received only one workspace and its TASK. These are synthetic projects, not Tune/Mail upgrades. The isolated-workspace rule is an instruction boundary, not an OS sandbox. All three ran once; no failing model trial was discarded or hidden.

| Model task | Scope inspector | Main-agent inspection of actual output |
| --- | --- | --- |
| New project | Exactly DESIGN, README and RESULT changed | English local owner contains token mappings, task-specific list/edit/save/state/accessibility rules and adoption provenance; README registers it. Product/data unknowns remain explicit, and no installed components or application verification are invented |
| Existing project | Exactly the design entry, forms, lists and RESULT changed | Preserves square corners, English owners, conditional links, whole-form Save/Cancel and FORM-EX-2; replaces both missing-rule clauses with observable failure recovery and secondary metadata hierarchy |
| Ordinary local update | Exactly forms and RESULT changed | Preserves Save/Cancel and the dialog exception; adds retained input, failed-item retry and keyboard location. No design regeneration, library copy, token or other-document change |

`inspect` reports all three scope checks passed and correctly leaves semantic review to the reader; the main agent read every changed design document and RESULT against the private rubric. Adopted rules are self-contained and sources are provenance. Agents reported selective reference reads; the parent has file/hash evidence and their reports, not a separately exported instrumented trace proving every read or non-read. The ordinary task's reported exclusion of the library is therefore bounded evidence, not a universal enforcement guarantee.

Two trial agents initially used an unavailable pathlib API in the host's legacy default Python during their own checks, then completed compatible read-only checks successfully. No environment installation was performed; these interruptions do not establish document failure or business-runtime validation.

## Remaining observation

Real generated interfaces, rendered alignment/type/density, keyboard/screen-reader behavior, long-term adherence, and a model old/new comparison were not tested here. Future project trials should inspect actual UI states against that project's adopted rules. Local docs and packaging are complete for this scope; real-project adoption and any publication require their own authorized task, not automatic continuation of this one.
