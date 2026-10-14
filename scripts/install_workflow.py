#!/usr/bin/env python3
"""Ownership-aware, offline creator.skill installer. Dry-run unless --apply is set.

Hashes establish an installation baseline, not publisher authenticity. Obtain ZIPs
from a trusted release or explicitly selected local build. No host is executed.
"""
import argparse
import base64
import hashlib
import json
import os
import re
import stat
import sys
import uuid
import zipfile
from contextlib import contextmanager
from pathlib import Path

MANIFEST = ".creator-manifest.json"
STATE = ".creator/install-state.json"
JOURNAL = ".creator/install-transaction.json"
LOCK = ".creator/install.lock"
CASES = ".creator/tests/prompt-cases/cases.json"
SIGNALS = {".creator/evolution/signals.md", ".codex/evolution/signals.md", ".claude/evolution/signals.md"}
MAX_FILE = 8 * 1024 * 1024
MAX_TOTAL = 64 * 1024 * 1024
MAX_ENTRIES = 4096
HEX = re.compile(r"[0-9a-f]{64}")
DEVICE = re.compile(r"(?i)(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?")


class InstallError(ValueError):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encode_json(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def decode_json(data, label):
    try:
        def unique_pairs(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError("duplicate object key")
                result[key] = value
            return result
        return json.loads(data.decode("utf-8-sig"), object_pairs_hook=unique_pairs)
    except (UnicodeError, ValueError) as exc:
        raise InstallError("Invalid JSON in " + label + ": " + str(exc)) from exc


def relative_name(name):
    if not isinstance(name, str) or not name or "\\" in name or ":" in name or name.startswith("/"):
        raise InstallError("Unsafe relative path: " + repr(name))
    parts = name.split("/")
    if any(not part or part in {".", ".."} or part.rstrip(" .") != part or DEVICE.fullmatch(part)
           or any(ord(char) < 32 for char in part) or any(char in '<>"|?*' for char in part) for part in parts):
        raise InstallError("Unsafe path component: " + repr(name))
    return name


def linked(info):
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & 0x400)


def check_absolute(path):
    """Check before resolve(), so a link cannot disappear into its resolved target."""
    path = Path(os.path.abspath(path))
    for item in reversed([path] + list(path.parents)):
        try:
            info = item.lstat()
        except FileNotFoundError:
            continue
        if linked(info):
            raise InstallError("Symlink/reparse point is not supported: " + str(item))
        if item != path and not stat.S_ISDIR(info.st_mode):
            raise InstallError("Parent is not a directory: " + str(item))
    return path


def project_root(value):
    root = check_absolute(value)
    if not root.is_dir() or root == Path(root.anchor):
        raise InstallError("--root must name an existing project directory, not a filesystem root")
    return root


def target_path(root, name):
    relative_name(name)
    path = check_absolute(root / name)
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise InstallError("Target leaves selected project") from exc
    return path


def read_current(root, name, limit=MAX_FILE):
    if name == STATE:
        limit = MAX_TOTAL
    path = target_path(root, name)
    try:
        info = path.lstat()
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(info.st_mode) or info.st_nlink > 1:
        raise InstallError("Expected an unlinked regular file: " + name)
    if info.st_size > limit:
        raise InstallError("File exceeds size limit: " + name)
    return path.read_bytes()


def owned_path(name, legacy=False):
    relative_name(name)
    if name in {"AGENTS.md", "EVOLUTION.md", ".version", MANIFEST}:
        return True
    if name in SIGNALS:
        return True
    if legacy and name == "CLAUDE.md":
        return True
    if name.startswith(".agents/skills/") and len(name.split("/")) >= 4:
        return True
    if name.startswith(".claude/skills/"):
        return legacy or (len(name.split("/")) == 4 and name.endswith("/SKILL.md"))
    if legacy and name.startswith(".claude/commands/") and name.endswith(".md"):
        return True
    return any(name.startswith(prefix) for prefix in (".creator/scripts/", ".creator/references/", ".creator/tests/"))


def read_archive(path):
    """Read bounded regular files without ever extracting an archive."""
    path = check_absolute(path)
    if not path.is_file() or path.stat().st_nlink > 1 or path.stat().st_size > MAX_TOTAL:
        raise InstallError("Package must be an unlinked regular ZIP under 64 MiB")
    raw = path.read_bytes()
    import io
    files, names, total = {}, {}, 0
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            entries = archive.infolist()
            if len(entries) > MAX_ENTRIES:
                raise InstallError("Too many ZIP entries")
            for info in entries:
                if info.orig_filename != info.filename:
                    raise InstallError("ZIP filename was truncated or normalized")
                name = info.filename.rstrip("/") if info.is_dir() else info.filename
                relative_name(name)
                key = name.casefold()
                if key in names:
                    raise InstallError("Duplicate/case-colliding ZIP entry: " + name)
                names[key] = (name, info.is_dir())
                mode = info.external_attr >> 16
                if stat.S_IFMT(mode) not in {0, stat.S_IFDIR if info.is_dir() else stat.S_IFREG} or (info.external_attr & 0x400):
                    raise InstallError("Non-regular ZIP entry: " + name)
                if info.flag_bits & 1:
                    raise InstallError("Encrypted ZIP entries are unsupported")
                total += info.file_size
                if info.file_size > MAX_FILE or total > MAX_TOTAL:
                    raise InstallError("ZIP exceeds expanded size limits")
                if not info.is_dir():
                    files[name] = archive.read(info)
            # Detect directory aliases and file-as-parent collisions on all hosts.
            aliases = {}
            for name, is_dir in names.values():
                parts = name.split("/")
                for index in range(1, len(parts) + 1):
                    prefix = "/".join(parts[:index])
                    key = prefix.casefold()
                    if key in aliases and aliases[key] != prefix:
                        raise InstallError("Case-colliding ZIP directories: " + name)
                    aliases[key] = prefix
                    existing = names.get(key)
                    if index < len(parts) and existing and not existing[1]:
                        raise InstallError("ZIP file used as parent: " + prefix)
    except (OSError, zipfile.BadZipFile, RuntimeError, NotImplementedError) as exc:
        raise InstallError("Invalid ZIP: " + str(exc)) from exc
    return files, digest(raw)


def load_package(path, baseline=False):
    files, package_hash = read_archive(path)
    if MANIFEST not in files:
        raise InstallError("Package has no workflow manifest")
    manifest = decode_json(files[MANIFEST], MANIFEST)
    if not isinstance(manifest, dict) or manifest.get("workflow") != "creator.skill":
        raise InstallError("Not a creator.skill package")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(manifest.get("version", ""))):
        raise InstallError("Invalid package version")
    if files.get(".version", b"").decode("utf-8-sig").strip() != manifest["version"]:
        raise InstallError("Package version does not match manifest")
    schema = manifest.get("schema_version")
    if schema == 1 and baseline:
        skills = manifest.get("skills")
        if not isinstance(skills, list) or not skills or any(not isinstance(name, str) for name in skills) or manifest.get("skill_count") != len(skills):
            raise InstallError("Invalid legacy Skill manifest")
        prefix = manifest.get("skill_root", "") + "/"
        if prefix not in {".agents/skills/", ".claude/skills/"}:
            raise InstallError("Invalid legacy Skill root")
        if any(prefix + str(name) + "/SKILL.md" not in files for name in skills):
            raise InstallError("Legacy package missing declared Skill")
        entries = {name: {"sha256": digest(data), "kind": "create-only" if name in SIGNALS else "merge-cases" if name == CASES else "managed"}
                   for name, data in files.items() if name != MANIFEST}
    elif schema == 2:
        entries = manifest.get("files")
        if not isinstance(entries, dict) or set(entries) != set(files) - {MANIFEST}:
            raise InstallError("Manifest must describe every package file exactly")
    else:
        raise InstallError("Only schema 2 installs are supported; schema 1 is baseline-only")
    for name, entry in entries.items():
        if not owned_path(name, legacy=baseline) or not isinstance(entry, dict):
            raise InstallError("Package contains non-workflow path: " + name)
        expected_kind = "create-only" if name in SIGNALS else "merge-cases" if name == CASES else "managed"
        if entry.get("kind") != expected_kind or entry.get("sha256") != digest(files[name]):
            raise InstallError("Invalid file hash or ownership kind: " + name)
    if not baseline:
        skills = manifest.get("skills")
        if not isinstance(skills, list) or not skills or any(not isinstance(name, str) for name in skills) or len(set(skills)) != len(skills) or manifest.get("skill_count") != len(skills):
            raise InstallError("Invalid Skill list")
        if manifest.get("platform") != "unified" or manifest.get("instruction_file") != "AGENTS.md" or manifest.get("skill_root") != ".agents/skills":
            raise InstallError("Package does not use canonical workflow layout")
        required = {"AGENTS.md", "EVOLUTION.md", CASES, ".creator/scripts/install_workflow.py"}
        required.update(".agents/skills/" + name + "/SKILL.md" for name in skills)
        required.update(".claude/skills/" + name + "/SKILL.md" for name in skills)
        if not required.issubset(files):
            raise InstallError("Missing canonical policy, Skill, adapter, or installer")
    return {"files": files, "manifest": manifest, "entries": entries, "sha256": package_hash}


def case_map(data, label):
    value = decode_json(data, label) if isinstance(data, bytes) else data
    if not isinstance(value, dict) or value.get("schema_version") != 1 or not isinstance(value.get("cases"), list):
        raise InstallError("Invalid case collection: " + label)
    result = {}
    for case in value["cases"]:
        if not isinstance(case, dict) or not isinstance(case.get("id"), str) or not case["id"] or case["id"] in result:
            raise InstallError("Missing/duplicate case ID: " + label)
        result[case["id"]] = case
    return value, result


def merge_cases(current, incoming, baselines):
    new_doc, new = case_map(incoming, "incoming cases")
    if current is None:
        return incoming, []
    local_doc, local = case_map(current, "project cases")
    old_maps = [case_map(old, "baseline cases")[1] for old in baselines]
    conflicts, merged = [], []
    for case_id, proposed in new.items():
        present = local.get(case_id)
        if present is None or present == proposed or any(old.get(case_id) == present for old in old_maps):
            merged.append(proposed)
        else:
            conflicts.append(CASES + "#" + case_id)
            merged.append(present)
    for case_id, present in local.items():
        if case_id not in new and not any(old.get(case_id) == present for old in old_maps):
            merged.append(present)
    # Preserve project metadata; advance metadata only when it matches a baseline.
    result = dict(local_doc)
    for key, value in new_doc.items():
        if key != "cases" and (key not in result or any(old.get(key) == result[key] for old in baselines)):
            result[key] = value
    result["cases"] = merged
    if result == local_doc:
        return current, conflicts
    return encode_json(result), conflicts


def baseline_state(root, baseline_packages):
    known, old_cases = {}, []
    receipt = read_current(root, STATE)
    if receipt is not None:
        state = decode_json(receipt, STATE)
        if not isinstance(state, dict) or state.get("schema_version") != 1 or state.get("workflow") != "creator.skill" or not isinstance(state.get("files"), dict):
            raise InstallError("Invalid installation state; preserve and inspect it")
        for name, entry in state["files"].items():
            if not owned_path(name, legacy=True) or not isinstance(entry, dict) or not HEX.fullmatch(str(entry.get("sha256", ""))):
                raise InstallError("Unsafe installation baseline")
            if name not in SIGNALS:
                known.setdefault(name, set()).add(entry["sha256"])
        if state.get("official_cases") is not None:
            case_map(state["official_cases"], "installed official cases")
            old_cases.append(state["official_cases"])
    for package in baseline_packages:
        for name, data in package["files"].items():
            if name not in SIGNALS and owned_path(name, legacy=True):
                known.setdefault(name, set()).add(digest(data))
        if CASES in package["files"]:
            old_cases.append(case_map(package["files"][CASES], "old official cases")[0])
    return known, old_cases, receipt


def claude_diagnostics(root, version=None):
    findings = []
    if version:
        match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version)
        if not match:
            raise InstallError("--claude-version must be a semantic version")
        if tuple(map(int, match.groups())) < (2, 1, 277):
            findings.append("Claude Code <2.1.277 requires an explicit CLAUDE.md @AGENTS.md import to load this policy.")
        elif tuple(map(int, match.groups())) < (2, 1, 281):
            findings.append("Claude Code <2.1.281 has AGENTS.md limitations in some sessions; upgrade or use an explicit import.")
    else:
        findings.append("Claude Code version is unverified. Native AGENTS.md requires >=2.1.277; >=2.1.281 fixes some host-specific cases.")
    for directory in [root] + list(root.parents):
        for relative in ("CLAUDE.md", ".claude/CLAUDE.md", "CLAUDE.local.md"):
            path = directory / relative
            # User ~/.claude/CLAUDE.md loads alongside AGENTS; it does not shadow it.
            if path == Path.home() / ".claude/CLAUDE.md":
                continue
            if os.path.lexists(path):
                findings.append("Possible AGENTS.md shadowing file (not read or modified): " + str(path))
    findings.append("Check Claude /context after installation. User/managed settings, disabled AGENTS support and session state may change discovery; these are not modified. Use an explicit @AGENTS.md fallback only after confirming the need.")
    return findings


def make_plan(root, package, baseline_packages=(), claude_version=None):
    if read_current(root, JOURNAL, MAX_TOTAL * 3) is not None:
        raise InstallError("An unfinished installation journal exists; use --recover before installing")
    known, old_cases, receipt = baseline_state(root, baseline_packages)
    actions, changes, conflicts = [], [], []
    new_files, entries = package["files"], package["entries"]

    def record(name, before, after, action):
        actions.append({"path": name, "action": action})
        if before != after:
            changes.append({"path": name, "before": before, "after": after})

    for name, incoming in sorted(new_files.items()):
        current = read_current(root, name)
        kind = entries[name]["kind"] if name in entries else "managed"
        if kind == "create-only" and current is not None:
            record(name, current, current, "preserve-runtime")
        elif kind == "merge-cases":
            try:
                merged, case_conflicts = merge_cases(current, incoming, old_cases)
                conflicts.extend(case_conflicts)
                record(name, current, merged, "merge-cases" if current != merged else "unchanged")
            except InstallError as exc:
                conflicts.append(str(exc))
                record(name, current, current, "conflict")
        elif current == incoming:
            record(name, current, current, "unchanged")
        elif current is None:
            record(name, None, incoming, "add")
        elif digest(current) in known.get(name, set()):
            record(name, current, incoming, "replace-owned")
        else:
            conflicts.append(name)
            record(name, current, current, "conflict")
    for name in sorted(set(known) - set(new_files)):
        if name in SIGNALS or name == CASES:
            continue
        current = read_current(root, name)
        if current is None:
            continue
        if digest(current) in known[name]:
            record(name, current, None, "remove-obsolete-owned")
        else:
            conflicts.append(name)
            record(name, current, current, "preserve-modified-obsolete")
    state_files = dict(entries)
    state_files[MANIFEST] = {"kind": "managed", "sha256": digest(new_files[MANIFEST])}
    state = {"schema_version": 1, "workflow": "creator.skill", "version": package["manifest"]["version"],
             "package_sha256": package["sha256"], "files": state_files,
             "official_cases": case_map(new_files[CASES], "incoming cases")[0]}
    desired_receipt = encode_json(state)
    record(STATE, receipt, desired_receipt, "record-baseline" if receipt != desired_receipt else "unchanged")
    return {"root": str(root), "version": state["version"], "package_sha256": package["sha256"],
            "actions": actions, "conflicts": sorted(set(conflicts)), "changes": changes,
            "diagnostics": claude_diagnostics(root, claude_version)}


def atomic_write(root, name, data):
    path = target_path(root, name)
    path.parent.mkdir(parents=True, exist_ok=True)
    target_path(root, name)  # Recheck created parents.
    temp = path.parent / (".creator-tmp-" + uuid.uuid4().hex)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(str(temp), flags, 0o600)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        target_path(root, name)
        os.replace(str(temp), str(path))
    finally:
        if temp.exists():
            temp.unlink()


def replace_current(root, change, forward):
    expected = change["before"] if forward else change["after"]
    desired = change["after"] if forward else change["before"]
    current = read_current(root, change["path"])
    if not forward and current == desired:
        return
    if current != expected:
        raise InstallError("Concurrent modification preserved: " + change["path"])
    if desired is None:
        if current is not None:
            target_path(root, change["path"]).unlink()
    else:
        atomic_write(root, change["path"], desired)


def journal_bytes(root, changes):
    entries = [{"path": change["path"], **{key: None if change[key] is None else base64.b64encode(change[key]).decode("ascii")
                                            for key in ("before", "after")}} for change in changes]
    return encode_json({"schema_version": 1, "workflow": "creator.skill", "root": str(root), "changes": entries})


@contextmanager
def installation_lock(root):
    """Serialize mutation and recovery; keep a harmless empty lock file on disk.

    OS locks release on process exit, so a crashed install remains recoverable.
    Do not remove the lock inode: another process may already have opened it.
    """
    path = target_path(root, LOCK)
    if path.exists():
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) or info.st_nlink > 1 or info.st_size:
            raise InstallError("Installation lock path contains unexpected data")
    path.parent.mkdir(parents=True, exist_ok=True)
    target_path(root, LOCK)
    fd = os.open(str(path), os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
    acquired = False
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink > 1 or info.st_size:
            raise InstallError("Unsafe installation lock")
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            acquired = True
        except OSError as exc:
            raise InstallError("Another installer or recovery is running for this project") from exc
        yield
    finally:
        if acquired:
            if os.name == "nt":
                msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def apply_plan(root, plan):
    if plan["conflicts"]:
        raise InstallError("Resolve the reported conflicts before applying; no files changed")
    if not plan["changes"]:
        return
    with installation_lock(root):
        _apply_plan_locked(root, plan)


def _apply_plan_locked(root, plan):
    changes = plan["changes"]
    # Recheck the entire snapshot before writing the journal or any target file.
    for change in changes:
        if read_current(root, change["path"]) != change["before"]:
            raise InstallError("Plan is stale: " + change["path"])
    if read_current(root, JOURNAL, MAX_TOTAL * 3) is not None:
        raise InstallError("An unfinished installation journal exists")
    atomic_write(root, JOURNAL, journal_bytes(root, changes))
    try:
        for change in changes:
            replace_current(root, change, True)
    except Exception as exc:
        # Revert only installer-owned changes; a concurrent edit is never overwritten.
        try:
            recovery = recover(root, apply=True, _locked=True)
            if recovery["conflicts"]:
                raise InstallError("Concurrent edits prevent automatic rollback")
        except (OSError, InstallError):
            raise InstallError("Installation interrupted; journal retained. Inspect and run --recover. Cause: " + str(exc)) from exc
        raise InstallError("Installation failed and file contents were rolled back: " + str(exc)) from exc
    target_path(root, JOURNAL).unlink()


def recover(root, apply=False, _locked=False):
    raw = read_current(root, JOURNAL, MAX_TOTAL * 3)
    if raw is None:
        return {"root": str(root), "mode": "recover", "applied": False, "actions": [], "conflicts": [], "status": "no-journal"}
    data = decode_json(raw, JOURNAL)
    if not isinstance(data, dict) or data.get("schema_version") != 1 or data.get("workflow") != "creator.skill" or data.get("root") != str(root) or not isinstance(data.get("changes"), list):
        raise InstallError("Invalid installation journal; manual inspection required")
    changes, conflicts, seen = [], [], set()
    for entry in data["changes"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise InstallError("Invalid journal entry")
        name = entry["path"]
        if name.casefold() in seen or not (owned_path(name, legacy=True) or name == STATE) or name in SIGNALS:
            # A fresh signal creation is legitimate; a signal overwrite is never legitimate.
            if name not in SIGNALS or entry.get("before") is not None or name.casefold() in seen:
                raise InstallError("Unsafe journal target: " + name)
        seen.add(name.casefold())
        change = {"path": name}
        try:
            for key in ("before", "after"):
                encoded = entry[key]
                change[key] = None if encoded is None else base64.b64decode(encoded, validate=True)
                if change[key] is not None and len(change[key]) > (MAX_TOTAL if name == STATE else MAX_FILE):
                    raise ValueError("journal file too large")
        except (KeyError, TypeError, ValueError) as exc:
            raise InstallError("Invalid journal content: " + name) from exc
        if read_current(root, name) not in (change["before"], change["after"]):
            conflicts.append(name)
        changes.append(change)
    result = {"root": str(root), "mode": "recover", "applied": False,
              "actions": [{"path": x["path"], "action": "restore-pre-install"} for x in reversed(changes)], "conflicts": conflicts}
    if apply and not conflicts:
        if not _locked:
            with installation_lock(root):
                return recover(root, apply=True, _locked=True)
        for change in reversed(changes):
            replace_current(root, change, False)
        if read_current(root, JOURNAL, MAX_TOTAL * 3) != raw:
            raise InstallError("Journal changed concurrently; retained for inspection")
        target_path(root, JOURNAL).unlink()
        result["applied"] = True
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path, help="Explicit existing project directory")
    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument("--package", type=Path, help="Trusted creator-workflow.zip")
    operation.add_argument("--recover", action="store_true", help="Inspect or roll back an unfinished transaction")
    parser.add_argument("--baseline-package", type=Path, action="append", default=[], help="Trusted old official ZIP; repeat for old host packages")
    parser.add_argument("--claude-version", help="Known Claude Code version for diagnostics; no host command is run")
    parser.add_argument("--apply", action="store_true", help="Apply a conflict-free plan; otherwise no writes")
    args = parser.parse_args(argv)
    try:
        root = project_root(args.root)
        if args.recover:
            if args.baseline_package or args.claude_version:
                raise InstallError("--recover cannot be combined with installation options")
            report = recover(root, args.apply)
        else:
            package = load_package(args.package)
            baselines = [load_package(path, baseline=True) for path in args.baseline_package]
            report = make_plan(root, package, baselines, args.claude_version)
            report["mode"] = "apply" if args.apply else "dry-run"
            report["applied"] = False
            if args.apply and not report["conflicts"]:
                apply_plan(root, report)
                report["applied"] = True
            report.pop("changes")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2 if report["conflicts"] else 0
    except (InstallError, OSError, UnicodeError, zipfile.BadZipFile) as exc:
        print(json.dumps({"error": str(exc), "applied": False}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
