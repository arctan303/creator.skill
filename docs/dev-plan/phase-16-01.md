# Phase 16-01: Workflow and project knowledge

Goal: make authorized delivery adaptive and preserve current project knowledge across sessions.
Scope: AGENTS, shared contract, existing skill boundaries, project-knowledge skill, evolution distinction, language policy.
Non-goals: changing business repositories or creating a cross-project memory service.
Depends on: existing 1.5 rules and 2026-10-13 user decisions.
Supersedes: 1.5 blanket R0/R1 subagent restriction, broad technical-question gates, and incomplete task-retirement handling. Preserve risk-based independent review and external authorization.
Expected behavior: read current state first; distinguish applicability from execution; capture explicit local conventions without a remember command; candidate inferences do not become user decisions; delegate bounded independent work when beneficial; user language controls replies.
Validation: structural checks plus isolated scenarios for experience questions, delegation, knowledge capture, removed tasks and bilingual behavior; diff review for contradictory rules.
Risk: R1 for scoped agent behavior; upgrade deletion is separately R2 in 16-02.
Implementation: complete. Validation: 46 policy cases structurally valid; three bounded model scenarios inspected against actual file diffs (see [evidence](../validation/1.6-behavior.md)). General cross-model adherence remains unmeasured. Release: 1.6.0 published on 2026-10-14; see the [release record](../workflow-1.6.md).
