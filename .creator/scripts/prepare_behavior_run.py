#!/usr/bin/env python3
"""Prepare answer-free agent workspaces and inspect actual file changes.

This is a fixture transport, not an automatic semantic judge or a host sandbox.
Run each TASK.md with a fresh agent; keep the private rubric outside its context.
"""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCENARIOS = ROOT / ".creator/tests/behavior/scenarios.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_relative(value):
    p = Path(value)
    if not value or p.is_absolute() or ".." in p.parts or "\\" in value or ":" in value:
        raise ValueError("unsafe fixture path: " + value)
    return p


def snapshot(root):
    return {p.relative_to(root).as_posix(): digest(p)
            for p in sorted(root.rglob("*")) if p.is_file()}


def prepare(destination, source_root=ROOT, definitions=SCENARIOS):
    destination = Path(destination)
    if destination.exists() or destination.is_symlink():
        raise ValueError("output must be a new directory; existing runs are never replaced")
    scenarios = json.loads(Path(definitions).read_text(encoding="utf-8"))["scenarios"]
    names = set()
    for scenario in scenarios:
        name = scenario["id"]
        if len(safe_relative(name).parts) != 1 or name in names:
            raise ValueError("scenario IDs must be unique directory names")
        names.add(name)
        for value in scenario["files"]:
            safe_relative(value)
        for value in scenario["allowed_changes"]:
            safe_relative(value)
    # The requested directory is new and contains only this run's artifacts.
    destination.mkdir(parents=True)
    baseline = {"schema_version": 1, "scenarios": []}
    source_root = Path(source_root)
    for scenario in scenarios:
        work = destination / scenario["id"]
        work.mkdir()
        for name in ("AGENTS.md", "EVOLUTION.md"):
            shutil.copy2(source_root / name, work / name)
        for name in (".agents/skills", ".creator/references"):
            shutil.copytree(source_root / name, work / name,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for name, content in scenario["files"].items():
            target = work / safe_relative(name)
            if target.exists():
                raise ValueError("fixture would replace workflow asset: " + name)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        (work / "TASK.md").write_text(scenario["input"], encoding="utf-8")
        baseline["scenarios"].append({"id": scenario["id"],
                                      "allowed_changes": scenario["allowed_changes"],
                                      "required_changes": scenario["required_changes"],
                                      "files": snapshot(work)})
    # Expected outcomes stay here, outside every model-facing workspace.
    (destination / "baseline.private.json").write_text(
        json.dumps(baseline, indent=2), encoding="utf-8")
    return [str(destination / name / "TASK.md") for name in sorted(names)]


def inspect(destination):
    destination = Path(destination)
    data = json.loads((destination / "baseline.private.json").read_text(encoding="utf-8"))
    result = {"scope_checks": [], "semantic_review": "required; inspect outputs and task evidence"}
    for scenario in data["scenarios"]:
        work = destination / safe_relative(scenario["id"])
        before, after = scenario["files"], snapshot(work)
        changed = sorted(name for name in before.keys() | after.keys()
                         if before.get(name) != after.get(name))
        unexpected = sorted(set(changed) - set(scenario["allowed_changes"]))
        missing = sorted(set(scenario["required_changes"]) - set(changed))
        result["scope_checks"].append({"id": scenario["id"], "changed": changed,
            "unexpected": unexpected, "missing_required": missing,
            "passed": not unexpected and not missing})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "inspect"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = prepare(args.output) if args.action == "prepare" else inspect(args.output)
    except (OSError, ValueError, KeyError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.action == "inspect":
        return 0 if all(x["passed"] for x in result["scope_checks"]) else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
