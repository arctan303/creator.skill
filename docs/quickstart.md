# Quickstart

[简体中文](quickstart.zh-CN.md) · [Home](../README.md)

This guide covers [release 1.6.0](https://github.com/arctan303/creator.skill/releases/tag/v1.6.0). The older [1.5 release](https://github.com/arctan303/creator.skill/releases/tag/v1.5.0) uses different package names and [installation instructions](https://github.com/arctan303/creator.skill/blob/v1.5.0/README.md).

## Install the release

Download both release ZIPs. Keep `creator-workflow.zip` intact and extract `creator-gateway.zip` into a directory named `creator-gateway`, directly containing `SKILL.md` and `scripts/`. With Python 3.10+ and an existing target project, run from the download directory:

```powershell
python creator-gateway/scripts/install_workflow.py --root "C:/path/to/your-project" --package "creator-workflow.zip"
python creator-gateway/scripts/install_workflow.py --root "C:/path/to/your-project" --package "creator-workflow.zip" --apply
```

The first command previews changes; run the second after reviewing them. This does not install a personal skill. For upgrades, add the baseline arguments below using the same gateway installer and downloaded package paths.

## Build and install locally

Alternatively, use a source checkout at tag `v1.6.0`, Python 3.10+, and an existing target project. These commands run from the creator.skill source directory. Replace the example project path with your own; on Linux or macOS use an absolute path such as `/home/you/projects/example`.

```powershell
python scripts/build_release.py
python scripts/verify_build.py
python scripts/install_workflow.py --root "C:/path/to/your-project" --package "dist/creator-workflow.zip"
```

The last command prints a JSON preview and makes no project changes. Review proposed writes, removals, preserved files, and conflicts. To apply:

```powershell
python scripts/install_workflow.py --root "C:/path/to/your-project" --package "dist/creator-workflow.zip" --apply
```

An unresolved conflict stops an apply before it writes. Inspect and reconcile the relevant customization, then preview again; there is no force-overwrite switch. Use version control or a backup for project changes you want to preserve independently of the installer.

Start a **new session in the target project** after installation. The workflow version and the state of your project documentation are separate: installing the workflow does not migrate existing docs. Request documentation alignment when you want it, using the [migration guide](../.creator/references/docs-migration-1.5.md).

## Upgrade an existing installation

Use the same installer and target root. For a 1.5 installation, supply the official ZIP used by that host as a baseline:

```powershell
python scripts/install_workflow.py --root "C:/path/to/your-project" --package "dist/creator-workflow.zip" --baseline-package "C:/downloads/creator.codex-1.5.0.zip"
```

Use the actual local filename; the 1.5 release asset is named `creator.codex.zip` or `creator.claude.zip`. If the project contains both old layouts, repeat `--baseline-package` for each relevant official package. Add `--apply` only after reviewing the preview.

Old workflow-owned `CLAUDE.md`, commands, and other obsolete files are removable only when their content can be matched to a reliable baseline. Modified or unrecognized files remain conflicts to resolve. Other skills, project documents, signals, and custom cases must remain intact. Do not delete the whole `.claude/`, `.agents/`, or `.creator/` directory as an upgrade shortcut.

If an installation was interrupted, inspect recovery before attempting another install:

```powershell
python scripts/install_workflow.py --root "C:/path/to/your-project" --recover
```

Add `--apply` to perform the reported recovery. Concurrent edits are preserved and reported as conflicts; resolve them from the available evidence rather than discarding them.

## Codex and Claude Code

Both hosts use the same workflow package and `AGENTS.md`. The canonical skill files live in `.agents/skills/`; the package also provides Claude discovery adapters under `.claude/skills/` that point to those instructions.

For direct AGENTS loading, use a current Claude Code release. Official documentation requires **v2.1.277+**, with fixes for some session types in **v2.1.281**. By default, a `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` in the working directory or its ancestors takes precedence over AGENTS. An unrelated personal or project customization should be reconciled, not silently deleted. See [Claude's AGENTS loading conditions](https://code.claude.com/docs/en/memory#agentsmd).

AGENTS support does not make `.agents/skills/` a documented Claude discovery directory. Claude still documents `.claude/skills/` for project skills; legacy `.claude/commands/` works, but is unnecessary alongside the new adapters. See [skill discovery](https://code.claude.com/docs/en/skills#choose-where-skills-load).

If you know the installed Claude version, include `--claude-version 2.1.281` (or your actual version) in the installer command for its compatibility diagnostic. This does not run Claude or prove that it loaded the files. Verify the loaded instructions and available skills in a fresh host session. Current host validation limits are listed in [project status](README.md).

## Install or update the personal gateway

The optional `creator` gateway is a personal skill that installs or upgrades the workflow in the project you select. It is separate from a project's installed workflow.

1. Download `creator-gateway.zip` from release 1.6.0, or build it from the same tagged source. Extract it to a temporary directory and inspect the contents. The ZIP root contains `SKILL.md`, `agents/`, `references/`, and `scripts/`.
2. Copy those contents into `~/.codex/skills/creator/` for Codex or `~/.claude/skills/creator/` for Claude Code. The resulting directory must contain `creator/SKILL.md` and `creator/scripts/install_workflow.py`; do not add another nested `creator/` directory.
3. If replacing a personal gateway, preserve and reconcile any local customization. Replace only the gateway's own files, not neighboring skills. The project installer does not update personal skill directories.
4. Start a new host session, open the intended project, and ask:

> Use the creator gateway to install the workflow from my local `creator-workflow.zip` in this project. Preview the changes, apply the unambiguous installation, and report the installed version and document status separately.

For upgrades, provide the old official baseline ZIP as well. You can also ask the gateway to fetch release `v1.6.0` from GitHub; naming the version keeps the selected release explicit.

The bundled installer can also be run directly as `python <gateway-directory>/scripts/install_workflow.py` with the same arguments shown above.

## Make the first task concrete

| Situation | A useful first request |
| --- | --- |
| Starting a product | “Help me define the first usable version of a shared reading list. Ask about who uses it and what they need; make routine technical choices yourself.” |
| Changing an existing project | “Add CSV export to this results page using its existing permissions. Follow the current UI conventions and verify the result.” |
| Continuing work | “Read the current project entry and active task. Check which previous evidence is still applicable, then continue the unfinished work.” |
| Correcting project knowledge | “AIWorker is retired. Update current requirements and tasks while preserving historical evidence. Do not restore the old feature.” |

You do not need to say “remember this” for an explicit project convention to be kept in the relevant document. Unconfirmed inferences remain candidates. A release convention such as a required checklist does not itself authorize a release. See the [illustrative continuity example](examples/project-continuity.md).

Use English or Chinese naturally. Replies follow your language; existing documents keep their established language unless you request a change. Public examples have paired translations; canonical workflow rules are maintained once.
