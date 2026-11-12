"""Verify trial transport and scope evidence; these are not model-task scores."""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import verify_build

spec = importlib.util.spec_from_file_location("design_trials", ROOT / "scripts/prepare_design_trials.py")
trials = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trials)


class DesignTrialTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="creator-design-trials-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.output = self.base / "run"

    def test_real_gateway_and_library_are_available_without_private_answers(self):
        definitions = json.loads(trials.DEFINITIONS.read_text(encoding="utf-8"))
        private_canary = "PRIVATE-ANSWER-CANARY-5e1ac0d6"
        for scenario in definitions["scenarios"]:
            scenario["rubric"].append(private_canary)
        custom_definitions = self.base / "definitions.private.json"
        custom_definitions.write_text(json.dumps(definitions), encoding="utf-8")
        tasks = trials.prepare(self.output, definitions=custom_definitions)
        self.assertEqual(len(tasks), 3)
        self.assertTrue((self.output / "rubrics.private.json").is_file())
        self.assertIn(private_canary, (self.output / "rubrics.private.json").read_text(encoding="utf-8"))
        baseline = json.loads((self.output / "baseline.private.json").read_text(encoding="utf-8"))
        for scenario in baseline["scenarios"]:
            with self.subTest(scenario=scenario["id"]):
                work = self.output / scenario["id"]
                self.assertEqual(scenario["files"], trials.behavior.snapshot(work))
                gateway_root = work / "tools/creator"
                gateway = {path.relative_to(gateway_root).as_posix(): path.read_bytes()
                           for path in gateway_root.rglob("*") if path.is_file()}
                self.assertIn("design-library/README.md", gateway)
                self.assertEqual(gateway["scripts/install_workflow.py"],
                                 (ROOT / "scripts/install_workflow.py").read_bytes())
                verify_build.validate_design_distribution({}, gateway, ROOT / "design-library")
                verify_build.validate_local_links(gateway, "trial gateway")
                self.assertTrue((work / "AGENTS.md").is_file())
                self.assertTrue((work / ".agents/skills/design-brief-builder/SKILL.md").is_file())
                self.assertFalse((work / ".creator/tests").exists())
                self.assertFalse((work / ".creator/install-state.json").exists())
                for path in work.rglob("*"):
                    if path.is_file():
                        self.assertNotIn(private_canary.encode(), path.read_bytes())
                        self.assertNotIn(path.name, {"baseline.private.json", "rubrics.private.json",
                                                     "definitions.private.json", "design-adaptation.json"})
                        if "design-library" in path.relative_to(work).parts:
                            self.assertTrue(path.is_relative_to(gateway_root / "design-library"))
                # Copied gateway material has already become part of the baseline.
                result = next(item for item in trials.inspect(self.output)["scope_checks"]
                              if item["id"] == scenario["id"])
                self.assertEqual(result["unexpected"], [])
                self.assertEqual(sorted(scenario["required_changes"]), result["missing_required"])

    def test_inspector_detects_unauthorized_docs_and_gateway_changes(self):
        trials.prepare(self.output)
        work = self.output / "daily-local-design-update"
        (work / "docs/design/forms.md").write_text("Updated fixture output; semantic review is separate.\n", encoding="utf-8")
        (work / "RESULT.md").write_text("Transport test output, not an evaluated agent answer.\n", encoding="utf-8")
        def local_result():
            return next(item for item in trials.inspect(self.output)["scope_checks"]
                        if item["id"] == "daily-local-design-update")
        self.assertTrue(local_result()["passed"])
        (work / "docs/DESIGN.md").write_text("Unauthorized design reset.\n", encoding="utf-8")
        (work / "tools/creator/design-library/README.md").write_text("Unauthorized tool edit.\n", encoding="utf-8")
        result = local_result()
        self.assertFalse(result["passed"])
        self.assertEqual(["docs/DESIGN.md", "tools/creator/design-library/README.md"], result["unexpected"])

    def test_existing_run_is_preserved(self):
        trials.prepare(self.output)
        before = trials.behavior.snapshot(self.output)
        with self.assertRaisesRegex(ValueError, "new directory"):
            trials.prepare(self.output)
        self.assertEqual(before, trials.behavior.snapshot(self.output))

    def test_cli_prepare_and_inspect_report_scope_without_semantic_verdict(self):
        command = [sys.executable, "-B", str(ROOT / "scripts/prepare_design_trials.py")]
        environment = dict(os.environ, PYTHONIOENCODING="utf-8")
        prepared = subprocess.run(command + ["prepare", "--output", str(self.output)],
                                  capture_output=True, text=True, encoding="utf-8", env=environment)
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        self.assertEqual(len(json.loads(prepared.stdout)), 3)
        inspected = subprocess.run(command + ["inspect", "--output", str(self.output)],
                                   capture_output=True, text=True, encoding="utf-8", env=environment)
        self.assertEqual(inspected.returncode, 1, inspected.stderr)
        report = json.loads(inspected.stdout)
        self.assertEqual(report["semantic_review"], "required; inspect outputs and task evidence")
        self.assertTrue(all(not item["passed"] and not item["unexpected"] for item in report["scope_checks"]))


if __name__ == "__main__":
    unittest.main()
