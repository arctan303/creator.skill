"""Regression checks for answer isolation and actual change inspection."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("behavior", ROOT / ".creator/scripts/prepare_behavior_run.py")
behavior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(behavior)


class BehaviorFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "run"

    def test_answers_are_not_in_agent_workspaces(self):
        paths = behavior.prepare(self.output)
        self.assertEqual(3, len(paths))
        for task in paths:
            root = Path(task).parent
            self.assertTrue((root / "AGENTS.md").is_file())
            self.assertFalse((root / ".creator/tests").exists())
            self.assertFalse((root / "baseline.private.json").exists())
            self.assertFalse(any(p.name in ("cases.json", "scenarios.json") for p in root.rglob("*")))
        self.assertTrue((self.output / "baseline.private.json").is_file())

    def test_inspection_requires_actual_changes_and_preserves_scope(self):
        behavior.prepare(self.output)
        result = behavior.inspect(self.output)
        self.assertTrue(all(not x["passed"] for x in result["scope_checks"]))
        root = self.output / "retired-work"
        (root / "RESULT.md").write_text("Actual output, meaning must be reviewed.", encoding="utf-8")
        result = behavior.inspect(self.output)
        item = next(x for x in result["scope_checks"] if x["id"] == "retired-work")
        self.assertTrue(item["passed"])
        (root / "docs/archive/phase-03.md").write_text("accidentally rewritten", encoding="utf-8")
        item = next(x for x in behavior.inspect(self.output)["scope_checks"] if x["id"] == "retired-work")
        self.assertFalse(item["passed"])
        self.assertEqual(["docs/archive/phase-03.md"], item["unexpected"])

    def test_existing_run_is_never_overwritten(self):
        behavior.prepare(self.output)
        with self.assertRaises(ValueError):
            behavior.prepare(self.output)

    def test_traversal_rejected_before_any_output(self):
        definitions = Path(self.temp.name) / "bad.json"
        definitions.write_text(json.dumps({"scenarios": [{"id": "../escape", "files": {}, "allowed_changes": []}]}), encoding="utf-8")
        with self.assertRaises(ValueError):
            behavior.prepare(self.output, definitions=definitions)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
