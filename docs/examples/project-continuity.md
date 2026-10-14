# A project decision that survives the next session

[简体中文](project-continuity.zh-CN.md) · [Quickstart](../quickstart.md)

**Illustrative walkthrough, not a report of a live project run.** This is a synthetic project with invented document names. It explains intended behavior; it does not claim that an agent completed these steps in a user's repository. Actual validation is recorded in [project status](../README.md).

## The situation

A small desktop app has an existing project guide, a design brief, and an active task list. An older plan still contains an unfinished check for AIWorker, a background automation feature. The user says:

> AIWorker has been removed from the product. Retire its unfinished verification tasks, keep the historical record, and continue with settings. For this project, save settings inline instead of opening a confirmation modal. Release notes should separate user-visible changes from internal maintenance.

Three different kinds of knowledge have arrived: a feature retirement, a design convention, and a release convention. None of them authorizes publishing a release.

## What should change now

The agent checks the current requirements and relevant code to distinguish a completed removal from a removal still needing implementation. It then updates the existing documents, using their established language and structure:

| Existing document | Update |
| --- | --- |
| Project guide | Record AIWorker's actual current state, the settings work that remains, and links to the current design/release guidance. |
| Requirements | Remove AIWorker from the current product scope and link the retirement decision to the old requirement. If implementation remains, state that gap. |
| Active task list | Mark AIWorker-only checks as retired because their requirement was withdrawn. Keep relevant settings work active. |
| Design brief | Record the inline-save convention with project scope and the user's decision as its source. |
| Release guide | Record the requested release-note categories. Keep publishing authorization separate. |
| Historical record | Preserve what was planned, changed, or verified at the time; add a link to the superseding decision where needed. |

Retired is different from passed. The agent must not claim that the removed feature's test passed, or recreate that feature just to complete an old checkbox. It also checks whether a shared requirement—such as migration of saved settings—still needs verification after the removal.

An illustrative current task entry could read:

```text
AIWorker background-processing check
State: retired; no longer applicable
Reason: the product owner removed AIWorker from current scope
Evidence: link to the recorded retirement decision
Historical verification: unchanged; not represented as a new pass
```

The agent does not need a separate “remember this” request to record the explicit conventions. A tentative statement such as “the interface probably should use compact spacing” is treated as a candidate, with its uncertainty intact.

## What the next session should do

The user starts a new session:

> Continue the settings work. Follow the project's current conventions.

The agent reads the current project entry and relevant active task, follows the inline-save rule, and checks the last evidence against the current files. The retired AIWorker check stays retired. Historical material is available when needed, without making every old requirement active again.

If the implementation calls for an unrelated engineering choice, the agent makes it within the established contract. If it would change a user-visible boundary—for example, saving settings automatically instead of using the agreed inline action—it asks about that choice before the dependent change. Independent work can continue.

When preparing release notes later, the agent uses the recorded categories. It reports build, test, review, and release state separately, and requests any missing authorization before publishing.

## What would demonstrate this behavior

A useful check starts with the stale AIWorker task, applies the retirement request, then opens a fresh session to continue settings work. Inspect the actual artifacts and execution for:

- The current requirement and active task agree about retirement, without fabricated passing evidence.
- Historical evidence and unrelated active tasks remain available.
- The next session uses the recorded design convention and does not restore AIWorker or run its obsolete-only checks.
- An inferred preference remains distinct from an explicit decision; a release convention does not trigger a release.
- The interaction follows the user's language and preserves the established language of project documents.

These observations test continuity. A correctly worded final reply alone does not demonstrate it.
