# creator.skill 1.6.0 delivery plan

Status: all three phases, the Mail upgrade, application-link checker follow-up and 1.6.0 publication are complete. The user's 2026-10-14 release authorization superseded the earlier local-only restriction for this release. The current stage is sustained use and evidence collection for 1.7.

Authorization: 2026-10-13 conversation — implement the discussed 1.6 improvements, including bilingual support. On 2026-10-14 the user authorized a real FlareMail upgrade/cleanup and then support for its application routes/resource mappings with another Mail verification. These explicit scopes supersede the earlier read-only sample restriction for FlareMail only. Technical decisions remain delegated; ask only about unresolved experience boundaries or missing authorization.

## Scope and acceptance

- One AGENTS.md policy and one workflow package; host discovery adapters may differ. Remove only proven workflow-owned obsolete files on upgrade, preserve local customization, project knowledge, signals and custom cases.
- Professional implementation choices proceed within established requirements. Ask about unresolved changes to user experience, capabilities, meaningful cost, privacy/scope or external authorization; do not repeat settled questions.
- Task structure determines delegation; concrete impact determines review. No fixed full pipeline for small changes.
- Project knowledge maintenance captures explicit project decisions naturally, separates inferred candidates, maintains one current-state entry, retires obsolete tasks, and preserves history without reviving it. Project scope first; cross-project application requires authorization.
- English and Chinese public entry, installation, usage and examples; agent conversation follows the user and existing document language. A single canonical instruction source, not duplicated translated policy trees.
- Meaningful upgrade/checker regression tests and isolated behavioral scenarios, including the removed AIWorker case. Distinguish static, scripted, model-behavior, host compatibility and release evidence.

Non-goals: change projects other than the specifically authorized FlareMail scope, rename the GitHub repository, publish promotional posts, deploy business systems, or claim measured adoption/production gains. No autonomous telemetry, cloud memory, or unlimited agent loops.

## Completed release and current use

1.6.0 was published through the existing main/VERSION GitHub Actions workflow at `55bb1fb`, preserving the validated runtime code and prior review. Remote commit/tag, successful Ubuntu checks, release asset digests/content and downloaded-package installation were verified; see [the 1.6 release record](workflow-1.6.md).

Collect the user's reports during sustained real-project use as [1.7 evidence and candidates](workflow-1.7.md). This authorizes recording feedback, not inventing 1.7 features, scheduling background monitoring or upgrading other repositories without their own scope.

## Completed short task: exact application links

Goal: resolve Mail's 22 application-route/resource false positives through explicit, scoped declarations backed by real repository files. Keep the read-only checker generic and preserve failures for missing, out-of-scope, ambiguous or unsafe links. Schema-1 projects without declarations remain compatible.

Implementation and Mail verification use `gpt-6.1-sol` with `high` reasoning. Scope is the checker, its regression tests/reference, local packages and Mail's installed workflow/knowledge registration. No business or public-document changes are needed. R1: incorrect declarations could hide broken navigation; exact matching, validated scope/targets, adversarial checks and a focused independent review address that consequence.

Dependencies: verify Mail's router/renderer/build mappings, then implement and test, rebuild the package, install it through the ownership-aware installer, and rerun Mail's complete inventory. Required evidence includes unchanged business/runtime files, repeated-check/install stability, and negative cases proving undeclared or missing targets still fail. Results and recovery evidence extend the [Mail acceptance record](validation/1.6-mail-upgrade.md).

Result: 63 regressions and 46 structural cases passed; the rebuilt package was installed in Mail through ownership-aware replacement. Five mappings resolved the original 22 reports, with zero errors across 136 registered Markdown documents and complete registration.

Only six expected files changed; 767 baseline files remained byte-identical. Repeated installation preserved all 773 hashes. Fresh review passed the implementation and actual Mail evidence; the main session verified its sole record-tense correction in the final receipt.

## Phases

| ID | Required outcome | Dependencies | State |
| --- | --- | --- | --- |
| [16-01](dev-plan/phase-16-01.md) | Effective workflow and project knowledge contract | Existing 1.5 rules and user decisions | Implemented; scoped verification complete |
| [16-02](dev-plan/phase-16-02.md) | Unified distribution, safe upgrade and useful checks | 16-01 contract and skill boundaries | Implemented; regressions and independent review passed |
| [16-03](dev-plan/phase-16-03.md) | Bilingual first-use docs, behavior evidence and integrated verification | 16-01 and 16-02 final behavior | Implemented; scoped behavior and package checks passed |

Starting baseline: clean main at VERSION 1.5.0. Current local version: 1.6.0. Prior release evidence remains in [1.5 development record](workflow-optimization.md). [Current state](README.md) and [1.6 evidence](workflow-1.6.md) record outcomes and actual host limitations; old plan entries are not new implementation obligations.
