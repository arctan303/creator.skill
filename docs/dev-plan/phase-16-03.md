# Phase 16-03: First-use experience and evidence

Goal: let Chinese and English readers understand, install and try the workflow, with evidence proportionate to actual validation.
Depends on: 16-01 behavior and 16-02 package/CLI interface.
Scope: English README with Chinese counterpart, bilingual quickstarts and walkthrough, current project entry, changelog, prompt cases, behavioral runner/evidence, integrated checks.
Non-goals: repository rename, external promotion, fake user testimonials or claims of live Claude compatibility without a host run.
Expected behavior: first screen explains outcomes; instructions are executable; retired AIWorker scenario never revives obsolete tests; English interaction stays English; evidence explicitly distinguishes illustrative demo from observed execution. No evaluator expected answers in model-facing fixtures.
Risk: R1; R2 integration review covers installation contract and claims.
Validation: both language paths and links, all regression tests, source/package structural checks, bounded isolated model scenarios with observed outputs; record any unavailable host validation.
Implementation: complete. Validation: bilingual links and command parity, 46 structural cases, 4 fixture-runner regressions, 3 actual synthetic model tasks and unified package verification passed. Initial full script suite: 52 tests, expanded to 63 after the application-link follow-up. See [behavior evidence](../validation/1.6-behavior.md) for scope/limits. Release: 1.6.0 published on 2026-10-14; see the [release record](../workflow-1.6.md).
