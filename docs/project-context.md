# Skill System Project Context

Status: background draft
Last updated: 2026-06-22

## 1. Project Goal

Build a new Codex skill system for turning a product idea into a usable software product through a lightweight, document-driven workflow.

The system should not be a dense step-by-step operating manual. Its rules should define:

- when a skill should be used
- what output counts as acceptable
- which red lines must not be crossed

Implementation details should be left to the model where possible, because the system assumes modern models can plan, execute, correct mistakes, and run long development loops when the goal and acceptance criteria are clear.

## 2. Source Material

Current source material:

- Video excerpt audio, first 6m41s:
  - `C:\git\creator.skill\archive\video-reference\video_codex_top_0_2_first_6m41s.wav`
- Transcript files with recognition errors:
  - `C:\git\creator.skill\archive\video-reference\video codex top 0 2 first 6m41s.txt`
  - `C:\git\creator.skill\archive\video-reference\video_codex_top_0_2_first_6m41s.wav.txt`
- Key screenshots:
  - `C:\git\creator.skill\archive\video-reference\images`
- Existing baseline skill:
  - `C:\git\creator.skill\archive\legacy-skills\creator`
- Repo-local skill system:
  - `C:\git\creator.skill\.agents\skills`
- Operating guide:
  - `C:\git\creator.skill\docs\system-operation.md`

The transcripts contain encoding and speech-recognition errors. Screenshot text is treated as higher-confidence for names, labels, and system structure. Transcript content is used mainly to recover the speaker's reasoning and workflow intent.

## 3. Core Method

The system is a shift from a heavy process to a light process:

- Earlier style: write each workflow step in detail, like an operations manual.
- New style: write goals, requirements, acceptance standards, and red lines; let the model organize the specific execution.

The system relies on documents as durable context between skills. Each stage produces a document or artifact that the next stage can consume, so the agent does not lose context across stages.

Human responsibility is intentionally narrow:

- make decisions
- approve or reject outputs
- verify acceptance evidence

AI responsibility expands to:

- planning
- execution
- correction
- review preparation
- goal drafting
- proposing skill improvements

## 4. Mainline Skill Map

The main workflow has 6 stages. Each stage should become a dedicated skill.

| Stage | Chinese label | Working skill name | Purpose | Primary output |
| --- | --- | --- | --- | --- |
| 01 | 需求 | product-spec-builder | Turn a vague idea into a directly buildable product spec | `Product-Spec.md` |
| 02 | 设计规范 | design-brief-builder | Convert subjective design intent into concrete design decisions | `Design-Brief.md` |
| 03 | 设计图 | design-maker | Produce visual design方案 and high-fidelity prototype from spec and brief | design artifacts / prototype |
| 04 | 开发计划 | dev-planner | Split the work into independently verifiable, runnable phases | plan document |
| 05 | 开发 | dev-builder | Build according to the plan and close the loop with independent review | working implementation + review evidence |
| 06 | 发布 | release-builder | Perform privacy audit and package/release preparation | release package / release evidence |

Stage 03 is optional. The screenshots label it as `OPTIONAL 可选`.

## 5. Plus Skills

The screenshots show 11 total skills: 6 mainline skills plus 5 extra skills.

The 5 plus skills are:

- bug-fixer: fix bugs inside the same evidence-driven system
- skill-builder: create new skills
- goal-writer: write high-quality actionable goals
- self-evolver: collect correction signals and propose skill/rule changes
- reviewer: independently review work produced by another agent

The existing repository currently contains a single `creator` skill. It already covers part of the idea-discovery and project-design space, but it is not yet split into the 11-skill system.

## 6. Stage Details From Source

### 01 Product Spec Builder

Working role: "毒舌产品经理" / strict product manager.

Purpose:

- take a vague product idea
- ask hard clarifying questions
- turn it into a product requirements document that can be developed directly

Key reason:

- AI naturally tends to agree with the user
- users may be praised while the requirement remains vague
- the skill must explicitly forbid empty agreement and flattery

Hard rule:

- do not accept vague requirements as buildable
- do not flatter or blindly comply
- push back until the idea is clear enough to implement

Expected output:

- `Product-Spec.md`

### 02 Design Brief Builder

Working role: designer interviewing the client.

Purpose:

- translate subjective feelings into concrete design decisions

Example:

- User says: "要高级感"
- Skill offers directions A/B/C and asks the user to choose
- Skill converts the decision into concrete variables:
  - dark or light
  - density
  - typography style
  - background style

Expected output:

- `Design-Brief.md`

### 03 Design Maker

Optional skill.

Inputs:

- `Product-Spec.md`
- `Design-Brief.md`

Expected outputs:

- visual design方案
- high-fidelity prototype

This stage is useful when visual quality, interaction, or layout decisions need to be made before implementation.

### 04 Dev Planner

Purpose:

- split requirements into phases
- each phase must be independently acceptable and runnable

Hard rule:

- do not produce phases where "a lot of code was written but nothing visible or runnable can be verified"

Each phase must include:

- acceptance conditions
- how to run or inspect the result
- visible or otherwise verifiable output

### 05 Dev Builder

Purpose:

- implement according to the plan
- enforce a closed review loop

Loop:

1. complete a task
2. dispatch an independent reviewer subagent
3. if review passes, task can be considered done
4. if review fails, fix until it passes

Reviewer requirements:

- newly assigned
- did not write the code
- has no ownership bias
- reviews accurately

### 06 Release Builder

Purpose:

- privacy audit
- package and release

Expected outputs should include release evidence, not only a statement that release is ready.

## 7. Goal Mechanism

The source emphasizes `Goal` as the most practical action unit.

A good goal contains:

- objective
- completion criteria
- acceptance method

Example:

- Objective: complete development for one phase
- Completion criteria:
  - compile with zero errors
  - all tests pass
  - reviewer approves
- Acceptance method:
  - paste the outputs for the three criteria

The agent should keep working until the goal is completed. The user should be able to scan the goal and send it.

Reason for a dedicated goal-writer skill:

- many users write vague goals
- vague goals cause agents to drift or stop too early
- the agent at the current project context is often best positioned to draft the next goal because it knows the conversation state, project status, and next action

## 8. Subagent Policy

Default to one main agent from start to finish.

Dispatch subagents only when:

- the work needs an independent clean mind, especially review
- several workstreams are truly independent and can run in parallel

Subagent discipline:

- pass the full required context
- return results to the main agent for merge and judgment
- treat a subagent as another mind, not as another folder or dumping ground

## 9. Self-Evolution Mechanism

The system should improve through usage.

Loop:

1. use a skill
2. user corrects or criticizes the result
3. save the correction as a signal
4. in a later conversation, dispatch an agent to digest signals
5. abstract the signals into rule-change proposals
6. ask the user whether to apply each proposal

The mechanism is bidirectional:

- propose adding or changing rules based on repeated corrections
- propose deleting rules that are never used

Goal:

- skills become smarter through real usage
- rules do not grow without limit

## 10. Current Repository Baseline

Current repository:

- `README.md` describes a `creator` skill for software-project planning.
- `archive/legacy-skills/creator/SKILL.md` implements the old single-skill flow that helps discuss, investigate, design, document, and accept software projects.
- `archive/legacy-skills/creator/references/` contains supporting guidance:
  - `project-discovery.md`
  - `project-documents.md`
  - `design-document.md`
  - `engineering-integrity.md`
  - `acceptance.md`
- `archive/legacy-skills/creator/agents/openai.yaml` provides UI metadata.

The current `creator` skill is a legacy foundation. Keep it for reference, but do not use it as the new system entrance or expand the new system around it.

## 11. First Layer To Land

The first implementation layer should establish the mainline skill skeleton and shared doctrine before filling every skill deeply.

Recommended first layer:

- create or reorganize skill folders for the 6 mainline skills
- define concise trigger descriptions for each skill
- define required inputs and outputs for each stage
- define stage acceptance gates
- define hard red lines for each stage
- preserve document handoff names: `Product-Spec.md`, `Design-Brief.md`, `DEV-PLAN.md`, implementation evidence, release evidence
- keep detailed question banks and rubrics in references, not directly in every `SKILL.md`

The first skill to deepen should be `product-spec-builder`, because every later stage depends on a clear `Product-Spec.md`.

Before deepening individual skills, use `docs/system-operation.md` as the coordination baseline. It defines stage transitions, document handoff, human decision points, the goal protocol, review rules, change control, and self-evolution signals.

## 12. Open Questions

- Should target projects always use `Product-Spec.md`, `Design-Brief.md`, and `DEV-PLAN.md`, or allow local naming conventions?
- Should self-evolution patch proposals be stored as files, or only generated in conversation before applying?
- Which Plus Skill should be deepened first after the mainline is usable: `reviewer`, `goal-writer`, or `self-evolver`?
- What is the preferred install layout for this repository: one bundled skill system or separate installable skill folders?
