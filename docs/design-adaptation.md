# Adapt design references to your project

[简体中文](design-adaptation.zh-CN.md) · [Home](../README.md)

Design adaptation and its scenario library are included in the [1.7.0 gateway](https://github.com/arctan303/creator.skill/releases/tag/v1.7.0). Downloading the gateway does not install the workflow or change any project documents automatically.

## Use the gateway for an adaptation task

Point your agent to the extracted 1.7.0 [creator gateway](../gateway/SKILL.md) and name the target project, requested surfaces and writable documents. Adaptation is a natural-language task, not an installer flag. It can run without installing the workflow into the target project.

For a new project:

> Use the creator gateway to establish design rules for this small task-list app. Reuse its existing tokens; choose only relevant scenarios. Create one project design document and link it from our current README. This request is documentation only.

For an existing project:

> Enrich our existing form and list rules with save-failure feedback and secondary metadata hierarchy. Keep the English files, square corners, whole-form Save and the approved complex-editor dialog exception. Edit only the design entry and its two topic files.

For a later comparison:

> Compare the relevant updated library suggestions with our adopted rules. Preserve our local amendments and explain any useful changes before applying the authorized document update. Leave adequate rules as they are.

The agent first reads current project knowledge, the design entry and applicable conditional references, effective decisions, components and tokens. It follows the [shared adaptation procedure](../.creator/references/design-adaptation.md), selecting useful material from the [library index](../design-library/README.md).

## Choose scenes, then write local decisions

The library has nine combinable modules; a product can need several, while a small task may need only one plus relevant foundations.

| Module | Typical scope |
| --- | --- |
| [Foundations](../design-library/foundations.md) | Typography, spacing, color, consistency and accessibility |
| [Forms and settings](../design-library/forms-and-settings.md) | Controls, validation, save semantics and drafts |
| [Admin and data](../design-library/admin-and-data.md) | Tables, filtering, bulk actions and object details |
| [Dashboards and monitoring](../design-library/dashboards-and-monitoring.md) | Metrics, charts, time ranges and data confidence |
| [Reading and documentation](../design-library/reading-and-documentation.md) | Long content, navigation, search and reading density |
| [Media and browsing](../design-library/media-and-browsing.md) | Grids, previews, selection and queues |
| [Workspaces and editors](../design-library/workspaces-and-editors.md) | Panes, tools, shortcuts, undo and recovery |
| [Onboarding and access](../design-library/onboarding-and-access.md) | Entry, essential input, permissions and first use |
| [Brand and marketing](../design-library/brand-and-marketing.md) | Visual narrative, expressive content and conversion |

For a new project, write the smallest sufficient local design owner. For an established project, fill demonstrated gaps and reconcile affected clauses in their existing owners. Preserve paths, language, brand choices, save behavior and scoped exceptions. Do not copy all modules into the project or infer a redesign from a request to improve its documents.

A brief source note records adopted modules, the revision actually read, applicable scope and meaningful local overrides. It is provenance, not a runtime dependency: the project document must contain the adopted decisions or lead to their local owners. New rules express intended behavior; they do not prove that an interface implements it.

## Continue ordinary work locally

Daily UI development, repair and review read the adopted project design entry and its applicable references. They do not need the gateway or upstream library. A library update supplies candidates for a later authorized adaptation; it never silently adopts new rules or overwrites local amendments.

Installation and adaptation are separate operations. The ownership-aware installer manages workflow files and preserves project documents; its deterministic script does not perform a semantic design merge. An adaptation request alone does not authorize installation, publication or changes outside its document scope.

## Use the release gateway

Download `creator-gateway.zip` from [release 1.7.0](https://github.com/arctan303/creator.skill/releases/tag/v1.7.0), extract it to a temporary directory, and point your agent to its `SKILL.md`. The gateway contains the authoring library; `creator-workflow.zip` contains the small daily procedures for project installation. See the [quickstart](quickstart.md) if you also want to install or upgrade the workflow.

Use the selected extracted gateway explicitly, or inspect [gateway loading guidance](../gateway/references/cli-adapters.md) before deliberately updating an optional personal skill.

Ask for a handoff listing the documents changed, adopted sources, preserved choices, unresolved conflicts and actual checks. Document checks, application implementation, visual validation and release evidence remain separate.
