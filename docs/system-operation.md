# Skill System Operation Guide

Status: operating draft
Last updated: 2026-06-22

## 1. Purpose

This document defines how the multi-skill product-building system should run before individual skills are deeply expanded.

It is the coordination layer for:

- stage order
- document handoff
- user decision points
- goal execution
- independent review
- release evidence
- self-evolution signals

Individual `SKILL.md` files should stay concise. If a skill-specific rule conflicts with this document, fix the conflict before refining that skill.

## 2. System Shape

The system has 6 mainline stages and 5 plus skills.

Mainline:

1. `product-spec-builder`
2. `design-brief-builder`
3. `design-maker` optional
4. `dev-planner`
5. `dev-builder`
6. `release-builder`

Plus:

- `bug-fixer`
- `skill-builder`
- `goal-writer`
- `self-evolver`
- `reviewer`

The mainline builds the product. Plus skills support repair, expansion, goal creation, improvement, and independent review.

## 3. Operating Philosophy

Write less process and more standards.

Each skill should define:

- when it is used
- what input it needs
- what output it must produce
- what counts as acceptable
- what is forbidden

Each skill should avoid:

- long step-by-step micromanagement
- repeating general Codex behavior
- hiding acceptance criteria in prose
- mixing design, implementation, and review authority

The agent should have room to plan and execute, but no room to lower the acceptance bar.

## 4. Document Handoff Model

Documents are the durable context between stages.

Default document names:

| Stage | Skill | Default output |
| --- | --- | --- |
| 01 | `product-spec-builder` | `Product-Spec.md` |
| 02 | `design-brief-builder` | `Design-Brief.md` |
| 03 | `design-maker` | design artifacts or prototype notes |
| 04 | `dev-planner` | `DEV-PLAN.md` |
| 05 | `dev-builder` | implementation evidence / progress notes |
| 06 | `release-builder` | release evidence |

Default location:

- use the target repo's existing docs convention when one exists
- otherwise use `docs/`
- for this repository's own system design, use `C:\git\creator.skill\docs`

Required rule:

- a later stage must not silently rewrite the authority of an earlier stage
- if a later stage discovers a conflict, it records a change request or open question
- confirmed documents become the baseline for later acceptance

## 5. Stage Transitions

### 5.1 Idea To Spec

Start with `product-spec-builder` when the user has an idea that is not yet buildable.

Exit condition:

- `Product-Spec.md` can answer what to build, who it is for, first-version scope, non-goals, and how success is verified.

Do not move forward when:

- the main user workflow is unclear
- the first version is not bounded
- acceptance cannot be tested

### 5.2 Spec To Brief

Use `design-brief-builder` when the product has UI, brand, interaction, or experience concerns.

Exit condition:

- `Design-Brief.md` converts subjective style into concrete design decisions.

Skip when:

- the product has no meaningful visual/interface design surface
- the user explicitly wants a purely technical or backend deliverable

### 5.3 Brief To Design Artifacts

Use `design-maker` only when visual decisions need inspection before planning or building.

Exit condition:

- screens, flows, states, and visual priorities are inspectable.

Skip when:

- the UI is obvious enough to plan directly
- the extra design artifact would add ceremony without reducing risk

### 5.4 Spec/Design To Plan

Use `dev-planner` after enough requirements and optional design context exist.

Exit condition:

- every phase is runnable, inspectable, or otherwise verifiable
- each phase has tasks, acceptance criteria, and evidence requirements

Do not accept a plan when:

- phases only describe code layers
- a phase can finish without visible or testable evidence
- review expectations are missing

### 5.5 Plan To Build

Use `dev-builder` for one planned phase at a time unless the plan explicitly allows parallel phases.

Exit condition:

- scoped implementation is complete
- verification evidence is attached
- independent review passes or a blocker is recorded

Do not mark complete when:

- checks were skipped without reason
- review was performed by the same agent that implemented the work
- scope changed without updating the plan or requesting approval

### 5.6 Build To Release

Use `release-builder` when implementation evidence indicates the product is ready for packaging, deployment, or final delivery.

Exit condition:

- privacy and sensitive-data exposure have been checked
- package/build/deploy path is documented and verified where possible
- unresolved release blockers are explicit

Do not release when:

- secrets or private data are exposed
- deploy configuration is undocumented
- required build or review gates are missing

## 6. Human Decision Points

The human should decide:

- product direction when tradeoffs matter
- first-version scope
- design direction among meaningful options
- whether optional design artifacts are worth creating
- whether a plan is acceptable
- whether a design change is approved
- whether release should actually be published
- whether self-evolution proposals should be applied

The agent should decide:

- which questions are necessary
- how to structure the document
- how to split verifiable phases
- which checks are appropriate
- how to fix implementation failures
- how to summarize evidence

The agent must not decide:

- new product scope without user approval
- major design changes after confirmation
- release publication without explicit instruction
- permanent rule changes from self-evolution without approval

## 7. Goal Protocol

A `Goal` is the execution unit for handing work to an agent.

Each goal must include:

- objective
- completion criteria
- acceptance method

Recommended shape:

```markdown
## Goal
<single concrete objective>

## Completion Criteria
- <observable criterion>
- <observable criterion>
- <observable criterion>

## Acceptance Method
- <what evidence the agent must paste, attach, or update>
```

Good goal example:

```markdown
## Goal
Complete Phase 1 from DEV-PLAN.md.

## Completion Criteria
- Build passes with zero errors.
- Required tests for Phase 1 pass.
- Independent reviewer approves the changes.

## Acceptance Method
- Provide changed file summary.
- Paste build and test outputs.
- Include reviewer result and unresolved findings.
```

Bad goal patterns:

- "make it better"
- "finish the app"
- "implement everything"
- "optimize the code"
- "use your judgment" without acceptance criteria

## 8. Subagent And Review Rules

Default to one main agent.

Use subagents only when:

- independent review is required
- parallel tasks do not depend on each other
- a fresh perspective is necessary to avoid implementation bias

Reviewer must receive:

- the relevant spec, brief, plan, and phase scope
- changed files or artifact summary
- verification commands and outputs
- explicit acceptance criteria

Reviewer must return:

- pass, conditional pass, or fail
- blocking findings first
- file/line references when reviewing code
- missing verification or residual risk

The main agent remains responsible for:

- merging review feedback
- fixing issues
- deciding whether another review cycle is needed
- reporting final evidence to the user

## 9. Change Control

Confirmed documents are baselines.

Allowed without user approval:

- small implementation details that satisfy existing requirements
- clearer wording that does not alter scope
- progress notes and evidence updates

Requires user approval:

- changing first-version scope
- changing major design direction
- changing public behavior or API
- removing acceptance criteria
- skipping planned review or release gates
- adding new dependencies with meaningful cost, privacy, or deployment impact

When a change is needed, record:

- what changed
- why
- affected requirements/tasks/acceptance criteria
- whether user approval is pending or granted

## 10. Self-Evolution Signals

Self-evolution should use real usage signals, not theoretical preferences.

Signal examples:

- user correction
- repeated misunderstanding
- repeated missing evidence
- rule that caused unnecessary friction
- rule that was never useful
- review finding that should have been prevented by a skill

Suggested signal record:

```markdown
## Signal
Date:
Source skill:
Context:
Observed problem:
Proposed rule change:
Confidence:
Needs user approval: yes/no
```

Rules:

- collect signals during real work
- digest them later, not in the middle of a critical task
- propose changes one by one
- ask the user before changing a skill
- delete stale rules as actively as adding new ones

## 11. First Refinement Order

Refine in this order:

1. system operation guide
2. `product-spec-builder`
3. `design-brief-builder`
4. `dev-planner`
5. `reviewer`
6. `dev-builder`
7. `release-builder`
8. `goal-writer`
9. `self-evolver`
10. `bug-fixer`
11. `skill-builder`
12. `design-maker`

Reasoning:

- spec quality controls everything downstream
- design brief and planning define the handoff quality
- reviewer is needed before dev-builder can truly close the loop
- design-maker can stay optional until the text pipeline works

## 12. Current Decisions

- Keep the existing `creator` skill for now.
- Treat it as a legacy skill, not the new system entrance.
- Do not expand the new system around `creator`.
- Use `docs/` for this repository's own operating documents.
- Keep `Product-Spec.md`, `Design-Brief.md`, and `DEV-PLAN.md` as default handoff names.
- Build the 6 mainline skills first, then add plus skills.

## 13. Open Questions

- Should generated product documents always use `Product-Spec.md`, `Design-Brief.md`, and `DEV-PLAN.md` in target repos, or allow local conventions?
- Should self-evolution patch proposals be stored beside `.codex/evolution/signals.md`, or only emitted in conversation?
- Should `reviewer` be a full installable skill or only a reference contract used by `dev-builder`?
- Should `goal-writer` create formal goal files, or only produce message-ready goal blocks?
