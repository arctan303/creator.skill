"""Structural checker tests only; not model-task or semantic migration tests."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / ".creator/scripts/check_docs.py"
spec = importlib.util.spec_from_file_location("check_docs", str(SCRIPT))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CheckDocsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "docs").mkdir()
        (self.root / ".creator").mkdir()
        (self.root / "docs/README.md").write_text("# Current\n", encoding="utf-8")

    def state(self, **overrides):
        value = dict(schema_version=1, docs_schema_version=1, workflow_version="1.5.0",
                     status="complete", entrypoints={"context": "docs/README.md"},
                     mappings=[], pending=[], verified_at="2026-09-06", evidence=["manual semantic review"])
        value.update(overrides)
        (self.root / ".creator/docs-state.json").write_text(json.dumps(value), encoding="utf-8")

    def test_missing_state_is_inventory_not_complete(self):
        self.assertEqual(module.inspect(self.root)["status"], "unregistered")
        self.assertTrue(module.inspect(self.root, True)["errors"])

    def test_complete_and_read_only_repeat(self):
        self.state()
        before = {str(p): (p.read_bytes(), p.stat().st_mtime_ns) for p in self.root.rglob("*") if p.is_file()}
        first = module.inspect(self.root, True)
        self.assertEqual(first["errors"], [])
        self.assertEqual(first, module.inspect(self.root, True))
        self.assertEqual(before, {str(p): (p.read_bytes(), p.stat().st_mtime_ns) for p in self.root.rglob("*") if p.is_file()})

    def test_partial_can_resume_but_not_pass_complete(self):
        self.state(status="partial", pending=["concurrent editor"])
        self.assertEqual(module.inspect(self.root)["errors"], [])
        self.assertTrue(module.inspect(self.root, True)["errors"])
        self.state()
        self.assertEqual(module.inspect(self.root, True)["errors"], [])

    def test_pending_cannot_be_complete(self):
        self.state(pending=["unresolved decision"])
        self.assertTrue(module.inspect(self.root)["errors"])
        self.state(mappings=[dict(source="docs/old.md", action="pending", targets=[], reason="in use")])
        self.assertTrue(module.inspect(self.root)["errors"])

    def test_moved_source_allowed_target_required(self):
        self.state(mappings=[dict(source="docs/old.md", action="archive", targets=["docs/README.md"], reason="retained")])
        self.assertEqual(module.inspect(self.root)["errors"], [])
        self.state(mappings=[dict(source="docs/old.md", action="archive", targets=["docs/missing.md"], reason="retained")])
        self.assertTrue(module.inspect(self.root)["errors"])

    def test_paths_cannot_escape_or_use_absolute_urls(self):
        for target in ("../outside.md", "C:/outside.md", "/outside.md", "https://example.com/doc", "docs\\README.md"):
            self.state(entrypoints={"context": target})
            self.assertTrue(module.inspect(self.root)["errors"], target)

    def test_malformed_state_is_reported(self):
        for data in ("{", "[]", '{"entrypoints":[]}'):
            (self.root / ".creator/docs-state.json").write_text(data, encoding="utf-8")
            self.assertTrue(module.inspect(self.root, True)["errors"])

    def test_file_links_skip_examples_and_remote(self):
        (self.root / "docs/README.md").write_text(
            '# Current\n```md\n[x](absent.md)\n```\n`[x](absent.md)`\n[x](https://example.com)\n[x](#section)\n', encoding="utf-8")
        self.assertEqual(module.inspect(self.root)["errors"], [])
        with (self.root / "docs/README.md").open("a", encoding="utf-8") as f:
            f.write("[broken](missing.md)\n")
        self.assertTrue(module.inspect(self.root)["errors"])

    def test_large_document_warns_without_failure(self):
        (self.root / "docs/README.md").write_text("text" * 6000, encoding="utf-8")
        self.state()
        result = module.inspect(self.root, True)
        self.assertEqual(result["errors"], [])
        self.assertTrue(result["warnings"])


if __name__ == "__main__":
    unittest.main()
