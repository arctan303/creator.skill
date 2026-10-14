"""Real temporary-directory installation, ownership and adversarial input regressions."""
import importlib.util
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/install_workflow.py"
spec = importlib.util.spec_from_file_location("install_workflow", SCRIPT)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


def cases(*items):
    return installer.encode_json({"schema_version": 1, "description": "official", "cases": list(items)})


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="creator-install-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "project"
        self.root.mkdir()
        self.counter = 0

    def package(self, version="1.6.0", overrides=None, legacy=False):
        self.counter += 1
        files = {
            "AGENTS.md": b"canonical policy " + version.encode(), "EVOLUTION.md": b"evolution " + version.encode(),
            ".version": (version + "\n").encode(), installer.CASES: cases({"id": "official-case", "value": version}),
            ".creator/scripts/install_workflow.py": b"# installer fixture\n",
            ".creator/evolution/signals.md": b"# New signals\n",
            ".agents/skills/demo/SKILL.md": b"canonical skill " + version.encode(),
            ".claude/skills/demo/SKILL.md": b"thin adapter " + version.encode(),
        }
        if legacy:
            files.pop("AGENTS.md")
            files.pop(".agents/skills/demo/SKILL.md")
            files.pop(".creator/evolution/signals.md")
            files["CLAUDE.md"] = b"old official policy"
            files[".claude/skills/demo/references/stage-contract.md"] = b"old copied policy"
            files[".claude/commands/develop.md"] = b"old command"
            files[".claude/evolution/signals.md"] = b"old signal template"
        for name, data in (overrides or {}).items():
            if data is None:
                files.pop(name, None)
            else:
                files[name] = data
        manifest = {"schema_version": 1 if legacy else 2, "workflow": "creator.skill", "version": version,
                    "skills": ["demo"], "skill_count": 1, "skill_root": ".claude/skills" if legacy else ".agents/skills",
                    "platform": "claude-code" if legacy else "unified", "instruction_file": "AGENTS.md"}
        if not legacy:
            manifest["files"] = {name: {"sha256": installer.digest(data), "kind": "create-only" if name in installer.SIGNALS else "merge-cases" if name == installer.CASES else "managed"}
                                 for name, data in files.items()}
        files[installer.MANIFEST] = installer.encode_json(manifest)
        path = self.base / ("package-" + str(self.counter) + ".zip")
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
            for name, data in files.items():
                archive.writestr(name, data)
        return path

    def write(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def snapshot(self, timestamps=False):
        return {path.relative_to(self.root).as_posix(): (path.read_bytes(), path.stat().st_mtime_ns) if timestamps else path.read_bytes()
                for path in self.root.rglob("*") if path.is_file()}

    def install(self, path, baselines=()):
        package = installer.load_package(path)
        plan = installer.make_plan(self.root, package, [installer.load_package(x, baseline=True) for x in baselines])
        installer.apply_plan(self.root, plan)
        return package

    def test_fresh_dry_run_apply_and_idempotence(self):
        package = installer.load_package(self.package())
        plan = installer.make_plan(self.root, package)
        self.assertEqual(list(self.root.iterdir()), [])
        self.assertFalse(plan["conflicts"])
        installer.apply_plan(self.root, plan)
        before = self.snapshot(timestamps=True)
        second = installer.make_plan(self.root, package)
        self.assertFalse(second["changes"])
        installer.apply_plan(self.root, second)
        self.assertEqual(before, self.snapshot(timestamps=True))
        self.assertFalse((self.root / installer.JOURNAL).exists())

    def test_upgrade_preserves_runtime_project_files_and_local_cases(self):
        self.install(self.package())
        for name in installer.SIGNALS | {".creator/docs-state.json", "docs/README.md", ".creator/project-knowledge/choices.json", ".claude/commands/mine.md"}:
            self.write(name, b"project content")
        local_cases = cases({"id": "official-case", "value": "1.6.0"}, {"id": "project:mine:extra", "value": "mine"})
        self.write(installer.CASES, local_cases)
        before = self.snapshot()
        package = self.install(self.package("1.7.0"))
        for name in installer.SIGNALS | {".creator/docs-state.json", "docs/README.md", ".creator/project-knowledge/choices.json", ".claude/commands/mine.md"}:
            self.assertEqual(before[name], (self.root / name).read_bytes())
        actual = installer.case_map((self.root / installer.CASES).read_bytes(), "actual")[1]
        self.assertEqual(actual["official-case"]["value"], "1.7.0")
        self.assertIn("project:mine:extra", actual)
        self.assertFalse(installer.make_plan(self.root, package)["changes"])

    def test_modified_managed_file_blocks_all_apply_writes(self):
        self.install(self.package())
        self.write("AGENTS.md", b"my policy customization")
        before = self.snapshot(timestamps=True)
        plan = installer.make_plan(self.root, installer.load_package(self.package("1.7.0")))
        self.assertIn("AGENTS.md", plan["conflicts"])
        with self.assertRaises(installer.InstallError):
            installer.apply_plan(self.root, plan)
        self.assertEqual(before, self.snapshot(timestamps=True))

    def test_unknown_existing_file_is_not_adopted_by_filename(self):
        self.write("AGENTS.md", b"pre-existing project instructions")
        plan = installer.make_plan(self.root, installer.load_package(self.package()))
        self.assertIn("AGENTS.md", plan["conflicts"])
        self.assertEqual((self.root / "AGENTS.md").read_bytes(), b"pre-existing project instructions")

    def test_legacy_baseline_removes_only_unchanged_owned_files(self):
        old = self.package("1.5.0", legacy=True)
        old_package = installer.load_package(old, baseline=True)
        for name, data in old_package["files"].items():
            self.write(name, data)
        self.write(".claude/evolution/signals.md", b"recorded historical signal")
        self.write(".claude/commands/custom.md", b"user command")
        new = self.package()
        without = installer.make_plan(self.root, installer.load_package(new))
        self.assertTrue(without["conflicts"])
        self.assertTrue((self.root / "CLAUDE.md").exists())
        self.install(new, [old])
        self.assertFalse((self.root / "CLAUDE.md").exists())
        self.assertFalse((self.root / ".claude/commands/develop.md").exists())
        self.assertFalse((self.root / ".claude/skills/demo/references/stage-contract.md").exists())
        self.assertEqual((self.root / ".claude/commands/custom.md").read_bytes(), b"user command")
        self.assertEqual((self.root / ".claude/evolution/signals.md").read_bytes(), b"recorded historical signal")

    def test_modified_obsolete_file_is_preserved_as_conflict(self):
        old = self.package("1.5.0", legacy=True)
        old_package = installer.load_package(old, baseline=True)
        for name, data in old_package["files"].items():
            self.write(name, data)
        self.write("CLAUDE.md", b"old policy plus project knowledge")
        plan = installer.make_plan(self.root, installer.load_package(self.package()), [old_package])
        self.assertIn("CLAUDE.md", plan["conflicts"])
        self.assertEqual((self.root / "CLAUDE.md").read_bytes(), b"old policy plus project knowledge")

    def test_same_id_custom_case_conflicts_without_losing_original(self):
        self.install(self.package())
        self.write(installer.CASES, cases({"id": "official-case", "value": "custom"}))
        before = self.snapshot()
        plan = installer.make_plan(self.root, installer.load_package(self.package("1.7.0")))
        self.assertIn(installer.CASES + "#official-case", plan["conflicts"])
        with self.assertRaises(installer.InstallError):
            installer.apply_plan(self.root, plan)
        self.assertEqual(before, self.snapshot())

    def test_removed_official_case_and_modified_local_case(self):
        self.install(self.package(overrides={installer.CASES: cases({"id": "removed", "value": 1}, {"id": "customized", "value": 1})}))
        self.write(installer.CASES, cases({"id": "removed", "value": 1}, {"id": "customized", "value": 2}))
        self.install(self.package("1.7.0"))
        actual = installer.case_map((self.root / installer.CASES).read_bytes(), "actual")[1]
        self.assertNotIn("removed", actual)
        self.assertEqual(actual["customized"]["value"], 2)

    def test_malformed_or_duplicate_local_cases_block_apply(self):
        self.install(self.package())
        for data in (b"{bad", cases({"id": "same"}, {"id": "same"})):
            self.write(installer.CASES, data)
            plan = installer.make_plan(self.root, installer.load_package(self.package("1.7.0")))
            self.assertTrue(plan["conflicts"])

    def bad_archive(self, names):
        path = self.base / "unsafe.zip"
        with zipfile.ZipFile(path, "w") as archive:
            for name in names:
                archive.writestr(name, b"bad")
        # Python's ZIP writer normalizes backslashes on Windows; retain hostile
        # on-disk names in this fixture instead of accidentally testing safe names.
        raw = path.read_bytes()
        for name in names:
            if "\\" in name:
                raw = raw.replace(name.replace("\\", "/").encode(), name.encode())
        path.write_bytes(raw)
        return path

    def test_archive_path_traversal_absolute_ads_devices_and_aliases(self):
        for name in ("../escape", "/absolute", "C:/absolute", "x\\y", "file:stream", "./file", "a/../file", "COM1", "CON.txt", "tail.", "space ", "a//b"):
            with self.subTest(name=name), self.assertRaises(installer.InstallError):
                installer.read_archive(self.bad_archive([name]))
        self.assertEqual(list(self.root.iterdir()), [])

    def test_archive_case_duplicate_and_file_parent_collisions(self):
        for names in (("file", "FILE"), ("dir/a", "DIR/b"), ("parent", "parent/file")):
            with self.subTest(names=names), self.assertRaises(installer.InstallError):
                installer.read_archive(self.bad_archive(names))

    def test_archive_symlink_reparse_and_resource_limits(self):
        for attrs in ((stat.S_IFLNK | 0o777) << 16, 0x400):
            path = self.base / "links.zip"
            with zipfile.ZipFile(path, "w") as archive:
                entry = zipfile.ZipInfo("link")
                entry.external_attr = attrs
                archive.writestr(entry, "outside")
            with self.assertRaises(installer.InstallError):
                installer.read_archive(path)
        path = self.bad_archive(["normal"])
        with mock.patch.object(installer, "MAX_FILE", 1), self.assertRaises(installer.InstallError):
            installer.read_archive(path)

    def test_hash_mismatch_and_non_workflow_content_rejected(self):
        package = self.package()
        files, _ = installer.read_archive(package)
        files["AGENTS.md"] = b"tampered"
        with zipfile.ZipFile(package, "w") as archive:
            for name, data in files.items():
                archive.writestr(name, data)
        with self.assertRaises(installer.InstallError):
            installer.load_package(package)
        for name in ("docs/README.md", ".git/config", ".creator/docs-state.json"):
            with self.subTest(name=name), self.assertRaises(installer.InstallError):
                installer.load_package(self.package(overrides={name: b"not workflow-owned"}))

    def test_symlink_or_windows_junction_parent_is_refused(self):
        outside = self.base / "outside"
        outside.mkdir()
        link = self.root / ".agents"
        try:
            os.symlink(outside, link, target_is_directory=True)
            self.addCleanup(lambda: link.unlink() if link.is_symlink() else None)
        except OSError:
            if os.name != "nt":
                self.skipTest("Symlink creation unavailable")
            result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(outside)], capture_output=True)
            if result.returncode:
                self.skipTest("Symlink and junction creation unavailable")
            self.addCleanup(lambda: os.rmdir(link) if os.path.lexists(link) else None)
        with self.assertRaises(installer.InstallError):
            installer.make_plan(self.root, installer.load_package(self.package()))
        self.assertFalse(list(outside.iterdir()))

    def test_linked_root_and_hardlinked_destination_are_refused(self):
        outside = self.base / "outside.txt"
        outside.write_bytes(b"outside")
        try:
            os.link(outside, self.root / "AGENTS.md")
        except OSError:
            self.skipTest("Hardlinks unavailable")
        with self.assertRaises(installer.InstallError):
            installer.make_plan(self.root, installer.load_package(self.package()))
        self.assertEqual(outside.read_bytes(), b"outside")

    def test_stale_plan_is_rejected_before_any_write(self):
        package = self.install(self.package())
        plan = installer.make_plan(self.root, installer.load_package(self.package("1.7.0")))
        self.write("AGENTS.md", b"concurrent edit")
        before = self.snapshot(timestamps=True)
        with self.assertRaises(installer.InstallError):
            installer.apply_plan(self.root, plan)
        self.assertEqual(before, self.snapshot(timestamps=True))

    def test_partial_failure_rolls_back_file_contents(self):
        self.install(self.package())
        before = self.snapshot()
        plan = installer.make_plan(self.root, installer.load_package(self.package("1.7.0")))
        original = installer.replace_current
        count = 0
        def fail_second(root, change, forward):
            nonlocal count
            if forward:
                count += 1
                if count == 2:
                    raise OSError("simulated write failure")
            return original(root, change, forward)
        with mock.patch.object(installer, "replace_current", side_effect=fail_second), self.assertRaises(installer.InstallError):
            installer.apply_plan(self.root, plan)
        self.assertEqual(before, self.snapshot())

    def test_concurrent_installer_is_rejected_by_process_lock(self):
        package = self.package()
        args = [sys.executable, "-B", str(SCRIPT), "--root", str(self.root), "--package", str(package), "--apply"]
        with installer.installation_lock(self.root):
            lock_mtime = (self.root / installer.LOCK).stat().st_mtime_ns
            result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
            self.assertEqual(result.returncode, 1)
            self.assertIn("Another installer", result.stderr)
            self.assertEqual(lock_mtime, (self.root / installer.LOCK).stat().st_mtime_ns)
            self.assertEqual([path.relative_to(self.root).as_posix() for path in self.root.rglob("*") if path.is_file()], [installer.LOCK])
        self.install(package)

    def test_crash_recovery_dry_run_apply_and_repeat(self):
        self.install(self.package())
        before = self.snapshot()
        plan = installer.make_plan(self.root, installer.load_package(self.package("1.7.0")))
        installer.atomic_write(self.root, installer.JOURNAL, installer.journal_bytes(self.root, plan["changes"]))
        installer.replace_current(self.root, plan["changes"][0], True)
        crashed = self.snapshot(timestamps=True)
        self.assertFalse(installer.recover(self.root)["conflicts"])
        self.assertEqual(crashed, self.snapshot(timestamps=True))
        self.assertTrue(installer.recover(self.root, apply=True)["applied"])
        self.assertEqual(before, self.snapshot())
        self.assertEqual(installer.recover(self.root, apply=True)["status"], "no-journal")

    def test_recovery_preserves_concurrent_edits_and_journal(self):
        self.install(self.package())
        plan = installer.make_plan(self.root, installer.load_package(self.package("1.7.0")))
        installer.atomic_write(self.root, installer.JOURNAL, installer.journal_bytes(self.root, plan["changes"]))
        changed = plan["changes"][0]["path"]
        self.write(changed, b"concurrent user content")
        before = self.snapshot(timestamps=True)
        self.assertIn(changed, installer.recover(self.root, apply=True)["conflicts"])
        self.assertEqual(before, self.snapshot(timestamps=True))
        with self.assertRaises(installer.InstallError):
            installer.make_plan(self.root, installer.load_package(self.package()))

    def test_recovery_rejects_non_workflow_targets(self):
        changes = [{"path": ".git/config", "before": b"before", "after": b"after"}]
        self.write(installer.JOURNAL, installer.journal_bytes(self.root, changes))
        with self.assertRaises(installer.InstallError):
            installer.recover(self.root, apply=True)

    def test_cli_defaults_to_dry_run_and_conflicts_return_two(self):
        package = self.package()
        args = [sys.executable, "-B", str(SCRIPT), "--root", str(self.root), "--package", str(package)]
        result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)["applied"])
        self.assertFalse(list(self.root.iterdir()))
        self.write("AGENTS.md", b"custom")
        result = subprocess.run(args + ["--apply"], capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertFalse(json.loads(result.stdout)["applied"])
        self.assertEqual(set(self.snapshot()), {"AGENTS.md"})

    def test_claude_compatibility_reports_shadowing_without_modifying(self):
        self.write("CLAUDE.local.md", b"personal project notes")
        before = self.snapshot(timestamps=True)
        findings = installer.claude_diagnostics(self.root, "2.1.276")
        self.assertTrue(any("explicit" in item for item in findings))
        self.assertTrue(any("CLAUDE.local.md" in item for item in findings))
        self.assertEqual(before, self.snapshot(timestamps=True))


if __name__ == "__main__":
    unittest.main()
