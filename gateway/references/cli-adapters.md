# Host adapters and installation / 宿主适配与安装

## One policy / 一份规则

| Content | Canonical location | Host discovery |
| --- | --- | --- |
| Project workflow | `AGENTS.md` | Codex; supported Claude sessions |
| Skill policy and resources | `.agents/skills/<name>/` | Codex directly |
| Claude Skill adapter | `.claude/skills/<name>/SKILL.md` | Metadata and a link to the canonical Skill; no second rule body |
| New evolution ledger | `.creator/evolution/signals.md` | Shared; preserve older host ledgers |
| Package baseline | `.creator-manifest.json`, `.creator/install-state.json` | Installer ownership and case baselines |
| Docs state | `.creator/docs-state.json` | Project runtime state, never distributed |

## Installer commands / 安装命令

Python 3.9+ is required. Run from any directory; select the project explicitly. The gateway ZIP has `SKILL.md` at its root, plus `scripts/install_workflow.py`.

```powershell
python <gateway-directory>/scripts/install_workflow.py --root C:/git/my-project --package C:/downloads/creator-workflow.zip
python <gateway-directory>/scripts/install_workflow.py --root C:/git/my-project --package C:/downloads/creator-workflow.zip --apply
```

For legacy ownership evidence, add the matching original official ZIP. Repeat the option when both old platform packages were installed:

```powershell
python <gateway-directory>/scripts/install_workflow.py --root C:/git/my-project --package C:/downloads/creator-workflow.zip --baseline-package C:/downloads/creator.claude-1.5.zip
```

The old filename is arbitrary; contents, manifest and hashes establish the baseline. Do not use a ZIP created from a modified project as an “official” baseline: doing so would incorrectly mark custom content as replaceable.

Defaults are read-only. `--apply` writes only a conflict-free plan. Exit codes: `0` successful plan/apply, `2` unresolved conflicts with no apply, `1` unsafe input or operation failure. All package paths are validated before mutation; archives are never extracted over the project. Installer state stores original official case definitions so later upgrades can preserve local cases.

An interrupted apply retains `.creator/install-transaction.json` with recovery snapshots. Keep it private: snapshots can contain local instruction content. Do not hand-edit or discard it to bypass recovery.

```powershell
python <gateway-directory>/scripts/install_workflow.py --root C:/git/my-project --recover
python <gateway-directory>/scripts/install_workflow.py --root C:/git/my-project --recover --apply
```

Recovery restores pre-install file contents only when current content still matches the recorded before/after state. Concurrent modifications stay intact and require reconciliation. Empty directories created before interruption may remain. For project conflicts, preserve/extract useful customization, deliberately reconcile the affected files, and rerun; there is no force option.

Apply/recovery operations use an OS lock on the empty runtime file `.creator/install.lock`. It stays on disk and contains no project content; the operating system releases the lock if a process exits. Do not delete the lock file to bypass another running installation.

## Claude discovery / Claude 发现机制

Official documentation checked 2026-10-13: [AGENTS.md discovery](https://code.claude.com/docs/en/memory#agentsmd), [Skills](https://code.claude.com/docs/en/skills).

Native AGENTS support requires Claude Code 2.1.277+. Version 2.1.281 fixes additional session/provider cases. A disabled built-in AGENTS plugin or user/managed configuration can still prevent loading. `--claude-version 2.1.281` only records a supplied version for installer diagnostics; it does not run or configure Claude.

By default, project/ancestor `CLAUDE.md`, `.claude/CLAUDE.md` and `CLAUDE.local.md` take precedence over AGENTS discovery. The user-level `~/.claude/CLAUDE.md` loads alongside AGENTS and is not itself a shadowing file. The installer lists existing candidate paths without reading or changing their content; a planned removal may still appear in the pre-install diagnosis.

After installation start a fresh session and inspect `/context`. Confirm the canonical `AGENTS.md` appears and invoke a relevant Skill to verify its adapter resolves to `.agents/skills/`. Document the actual version, settings and result. Structural tests do not establish this compatibility.

If support is unavailable, an explicitly chosen fallback is a real `@AGENTS.md` import in a root `CLAUDE.md`; when importing from `.claude/CLAUDE.md`, use `@../AGENTS.md`. Preserve other project instructions. This is a reference to the same policy, not a translated/copied second policy. Modern sessions that already load AGENTS need no generated CLAUDE file.

## Installed checks / 安装后检查

```powershell
python -B .creator/scripts/evaluate_prompt_cases.py
python -B .creator/scripts/check_docs.py --root .
```

Run these from the selected project. The first is structural without real response evidence. The second is read-only inventory; use `--require-complete` only after an authorized docs migration and semantic verification. Updating `.version` does not migrate docs. Do not install project source `docs/README.md` into a business project.
