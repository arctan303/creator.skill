"""Build real archives and install them without relying on the authored library."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_release
import install_workflow as installer
import verify_build


class DesignDistributionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="creator-design-distribution-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.source = self.base / "source"
        fixtures = {
            "AGENTS.md": b"[project rules](.creator/references/project-design.md)\n",
            "EVOLUTION.md": b"# Evolution\n",
            ".creator/references/project-design.md": b"[adaptation](design-adaptation.md)\n",
            ".creator/references/design-adaptation.md": b"Read the project's own design rules.\n",
            ".creator/scripts/fixture.py": b"# Packaged script fixture\n",
            ".creator/tests/prompt-cases/cases.json": b'{"schema_version": 1, "cases": []}\n',
            ".agents/skills/demo/SKILL.md": b"---\nname: demo\ndescription: Demo fixture\n---\n\nDemo.\n",
            ".agents/skills/demo/agents/openai.yaml": b"interface:\n  display_name: Demo\n",
            "gateway/SKILL.md": b"[adapt](../.creator/references/design-adaptation.md) "
                                b"[library](../design-library/README.md)\n",
            "gateway/agents/openai.yaml": b"interface:\n  display_name: Creator\n",
            "design-library/README.md": b"[layout](topics/layout.md)\n",
            "design-library/topics/layout.md": b"[entry](../README.md) [sample](../assets/sample.bin)\n",
            "design-library/assets/sample.bin": b"\x00\xffauthoring sample\r\n",
        }
        for name, data in fixtures.items():
            self.write(self.source / name, data)
        self.write(self.source / "scripts/install_workflow.py", (ROOT / "scripts/install_workflow.py").read_bytes())
        for name, value in {
            "REPO_ROOT": self.source,
            "SKILLS_SRC": self.source / ".agents/skills",
            "GATEWAY_SRC": self.source / "gateway",
            "DESIGN_LIBRARY_SRC": self.source / "design-library",
        }.items():
            patch = mock.patch.object(build_release, name, value)
            patch.start()
            self.addCleanup(patch.stop)

    def write(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def build_archives(self):
        workflow = self.base / "workflow"
        gateway = self.base / "gateway"
        build_release.build_workflow(workflow, ["demo"], "1.6.0")
        build_release.build_gateway(gateway)
        workflow_zip, gateway_zip = self.base / "workflow.zip", self.base / "gateway.zip"
        build_release.zip_directory(workflow, workflow_zip)
        build_release.zip_directory(gateway, gateway_zip)
        return installer.load_package(workflow_zip), installer.read_archive(gateway_zip)[0]

    def test_gateway_contains_complete_library_and_rewritten_links(self):
        package, gateway = self.build_archives()
        workflow = package["files"]
        verify_build.validate_design_distribution(workflow, gateway, self.source / "design-library")
        verify_build.validate_local_links(workflow, "workflow")
        verify_build.validate_local_links(gateway, "gateway")
        self.assertEqual(gateway["SKILL.md"], b"[adapt](references/design-adaptation.md) "
                         b"[library](design-library/README.md)\n")
        self.assertFalse(any("design-library" in name.split("/") for name in package["entries"]))
        self.assertIn(".creator/references/project-design.md", workflow)
        self.assertIn(".creator/references/design-adaptation.md", workflow)

    def test_gateway_build_refuses_missing_library_entry(self):
        (self.source / "design-library/README.md").unlink()
        with self.assertRaisesRegex(ValueError, "missing its README.md"):
            build_release.build_gateway(self.base / "gateway")
        self.assertFalse((self.base / "gateway").exists())

    def test_verifier_rejects_library_omissions_changes_and_workflow_leaks(self):
        package, gateway = self.build_archives()
        source = self.source / "design-library"
        for member in ("design-library/topics/layout.md", "design-library/assets/sample.bin"):
            with self.subTest(member=member):
                incomplete = dict(gateway)
                del incomplete[member]
                with self.assertRaisesRegex(RuntimeError, "incomplete or differs"):
                    verify_build.validate_design_distribution(package["files"], incomplete, source)
        changed = dict(gateway, **{"design-library/README.md": b"changed"})
        with self.assertRaisesRegex(RuntimeError, "incomplete or differs"):
            verify_build.validate_design_distribution(package["files"], changed, source)
        leaked = dict(package["files"], **{".creator/references/design-library/README.md": b"copied"})
        with self.assertRaisesRegex(RuntimeError, "Workflow must not contain"):
            verify_build.validate_design_distribution(leaked, gateway, source)

    def test_install_and_repeat_preserve_project_design_and_custom_rules(self):
        package, _ = self.build_archives()
        project = self.base / "project"
        project.mkdir()
        preserved = {
            "docs/DESIGN.md": b"# Project design\r\nKeep existing choices.\r\n",
            "docs/design/component-rules.md": b"Custom project component rules.\r\n",
            ".creator/references/project-local-design.md": b"Custom local rules.\x00\r\n",
        }
        for name, data in preserved.items():
            self.write(project / name, data)
        for repeat in (False, True):
            plan = installer.make_plan(project, package)
            self.assertFalse(plan["conflicts"])
            if repeat:
                self.assertFalse(plan["changes"])
            installer.apply_plan(project, plan)
            for name, data in preserved.items():
                self.assertEqual((project / name).read_bytes(), data)
            self.assertFalse((project / "design-library").exists())
            self.assertFalse(any("design-library" in path.parts for path in project.rglob("*")))
        state = installer.decode_json((project / installer.STATE).read_bytes(), "state")
        self.assertTrue(set(preserved).isdisjoint(state["files"]))

        # A customized official rule remains a conflict, never a semantic merge.
        custom = b"My project-specific version of the official short rule.\r\n"
        target = project / ".creator/references/project-design.md"
        target.write_bytes(custom)
        plan = installer.make_plan(project, package)
        self.assertIn(".creator/references/project-design.md", plan["conflicts"])
        with self.assertRaises(installer.InstallError):
            installer.apply_plan(project, plan)
        self.assertEqual(target.read_bytes(), custom)
        for name, data in preserved.items():
            self.assertEqual((project / name).read_bytes(), data)


if __name__ == "__main__":
    unittest.main()
