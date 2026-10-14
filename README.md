# Creovator · creator.skill

[简体中文](README.zh-CN.md)

**Help your coding agent understand the project, finish the task, and carry the right knowledge into the next session.**

Creovator is a project workflow for Codex and Claude Code. Describe the result you want; the agent uses your existing requirements, design conventions, and release practices to choose the work and verification that fit.

- **Less re-explaining.** Explicit project decisions become part of the relevant project documents, with their scope and source.
- **Work that fits the task.** A small fix stays small. Independent work can be delegated; consequential changes receive independent review.
- **Continuity you can inspect.** Current work, retired requirements, and verification evidence stay distinguishable when a new session takes over.

For example:

> AIWorker was removed from this product. Retire its unfinished verification tasks and update the current project notes. Keep the historical evidence. Also keep our design rule: settings changes use an inline save action.

The expected outcome is an updated current plan and design guidance. The removed feature's historical tests do not become today's work again. See the [illustrative walkthrough](docs/examples/project-continuity.md).

## Install 1.6.0

Download `creator-workflow.zip` and `creator-gateway.zip` from [release 1.6.0](https://github.com/arctan303/creator.skill/releases/tag/v1.6.0). Extract the gateway ZIP into a `creator-gateway` directory next to the workflow ZIP. The gateway directory should directly contain `SKILL.md` and `scripts/`.

From that download directory, with Python 3.10+ available:

```powershell
python creator-gateway/scripts/install_workflow.py --root "C:/path/to/your-project" --package "creator-workflow.zip"
```

Read the proposed changes, then apply the same operation:

```powershell
python creator-gateway/scripts/install_workflow.py --root "C:/path/to/your-project" --package "creator-workflow.zip" --apply
```

The project directory must already exist. The installer previews by default and stops on unresolved customization conflicts. For a 1.5 upgrade, supply the old official package as a baseline so obsolete files can be identified safely. See the [quickstart](docs/quickstart.md) for upgrades, Claude compatibility, and the personal gateway skill.

Start a new agent session in the project and try:

> Read this project's current context and conventions. Add a CSV export to the existing results page using its current permissions. Make the normal implementation choices, ask me only about unresolved user experience or authorization boundaries, and show how you verified the result.

For an existing project, you can also request documentation alignment:

> Align the existing project documents with this workflow. Reuse the current entry document, preserve history, and distinguish current requirements from retired work.

## What is included

The release includes one `creator-workflow.zip` for project installation and one `creator-gateway.zip` containing the installer and optional personal skill. Both hosts share `AGENTS.md` and the canonical skills under `.agents/skills/`. Claude uses thin discovery adapters under `.claude/skills/`; there is no second translated policy tree or generated `CLAUDE.md`.

Public setup and examples are available in English and Chinese. The agent follows your conversation language and the language of existing project documents. The rules have one canonical source; bilingual documentation does not create two competing sets of instructions.

| You want to… | Start here |
| --- | --- |
| Install, upgrade, or update the gateway | [Quickstart](docs/quickstart.md) |
| See how project decisions survive a handoff | [Project continuity walkthrough](docs/examples/project-continuity.md) |
| Understand task sizing, risk, and evidence | [Shared workflow contract](.creator/references/workflow-contract.md) |
| Adapt an existing document structure | [Documentation migration guide](.creator/references/docs-migration-1.5.md) |
| Check actual implementation and validation status | [Project status](docs/README.md) |
| Contribute or inspect the current work | [Development plan](docs/DEV-PLAN.md) · [1.6 evidence](docs/workflow-1.6.md) |

## Scope and evidence

Creovator supplies instructions, project knowledge practices, and local checking/install tools. It depends on the host agent's available tools and permissions. Installing files does not prove that a host has loaded them or that a real task will succeed.

The walkthrough is illustrative. Current validation and remaining host or behavior gaps are reported in [project status](docs/README.md); no adoption figures or productivity gains are claimed. Publishing, deploying, or changing another project requires the corresponding user authorization.

[MIT License](LICENSE)
