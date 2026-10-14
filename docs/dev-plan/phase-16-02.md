# Phase 16-02: Distribution, upgrades and checks

Goal: ship one policy/package and perform ownership-aware upgrades without leaving obsolete official instructions active or destroying project data.
Depends on: 16-01 canonical AGENTS and project-knowledge boundaries; implementation can proceed against agreed paths.
Scope: builder/verifier, gateway and adapters, deterministic install/upgrade helper, manifests, checker and tests, CI artifact names.
Non-goals: automatically upgrading sibling projects or user-level installations during this development task.
Expected behavior: one creator-workflow.zip plus gateway; no generated duplicate CLAUDE.md; modern Claude host discovery adapters; local customization preserved; obsolete owned files removed only with reliable baseline; unknown conflicts remain visible and recoverable; retries are idempotent. Docs checks distinguish file links, directories, routes and source-line citations.
Risk: R2 — file cleanup could erase customization or install conflicting instructions; require adversarial filesystem/archive fixtures and fresh independent review. Refuse paths escaping the selected root and unsafe links.
Validation: real temporary-directory installs, same-version repeat, previous-version upgrade, modified/unowned files, signals/docs/custom case preservation, archive/path failures, package verification and relevant checker regressions.
Implementation: complete. Validation: installer 23, checker initially 22 (33 after the application-link follow-up) and package-link 3 regression tests passed; actual previous 1.5 upgrade fixtures and unified package checks passed. Independent review: passed after a gateway-reference fix and for the later Mail follow-up. Release: 1.6.0 published on 2026-10-14; CI results and host limits are in the [evidence record](../workflow-1.6.md).
