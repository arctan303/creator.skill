#!/usr/bin/env python3
"""Prepare source-only design-adaptation trials; inspect scope, not semantics.

Run TASK.md from one workspace with a fresh agent. Keep the run's private files
outside that agent's context. No workflow installation or model execution occurs.
"""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFINITIONS = ROOT / "tests/fixtures/design-adaptation.json"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


behavior = load_module("design_trial_transport", ROOT / ".creator/scripts/prepare_behavior_run.py")


def prepare(destination, source_root=ROOT, definitions=DEFINITIONS):
    destination, source_root = Path(destination), Path(source_root)
    builder = load_module("design_trial_builder", ROOT / "scripts/build_release.py")
    builder.REPO_ROOT = source_root
    builder.GATEWAY_SRC = source_root / "gateway"
    builder.DESIGN_LIBRARY_SRC = source_root / "design-library"
    # Fail before producing a partial run when its authoring material is absent.
    if not (builder.DESIGN_LIBRARY_SRC / "README.md").is_file():
        raise ValueError("source design library is missing its README.md entry")
    tasks = behavior.prepare(destination, source_root=source_root, definitions=definitions)
    baseline_path = destination / "baseline.private.json"
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    for scenario in baseline["scenarios"]:
        work = destination / scenario["id"]
        builder.build_gateway(work / "tools/creator")
        # Gateway/library files must participate in the same immutable scope check.
        scenario["files"] = behavior.snapshot(work)
    baseline_path.write_text(json.dumps(baseline, indent=2), encoding="utf-8")
    definitions_data = json.loads(Path(definitions).read_text(encoding="utf-8"))
    private = {"schema_version": 1, "scenarios": [
        {"id": scenario["id"], "rubric": scenario["rubric"]}
        for scenario in definitions_data["scenarios"]
    ]}
    (destination / "rubrics.private.json").write_text(
        json.dumps(private, ensure_ascii=False, indent=2), encoding="utf-8")
    return tasks


def inspect(destination):
    return behavior.inspect(destination)


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
        return 0 if all(item["passed"] for item in result["scope_checks"]) else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
