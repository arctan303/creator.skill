"""Check archive link closure; a valid top-level guide can still omit a dependency."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import verify_build


class PackageLinkTests(unittest.TestCase):
    def test_missing_transitive_reference_fails(self):
        files = {"SKILL.md": b"[guide](references/guide.md)",
                 "references/guide.md": b"[knowledge](knowledge.md)"}
        with self.assertRaisesRegex(RuntimeError, "missing local link"):
            verify_build.validate_local_links(files, "gateway")
        files["references/knowledge.md"] = b"[guide](guide.md)"
        verify_build.validate_local_links(files, "gateway")

    def test_relative_directory_and_encoded_file(self):
        files = {"SKILL.md": b"[directory](references) [file](references/a%20b.md#part)",
                 "references/a b.md": b"[root](../SKILL.md)"}
        verify_build.validate_local_links(files, "gateway")

    def test_escape_fails_and_examples_are_not_links(self):
        with self.assertRaisesRegex(RuntimeError, "escapes archive"):
            verify_build.validate_local_links({"SKILL.md": b"[bad](../outside.md)"}, "gateway")
        verify_build.validate_local_links({"SKILL.md": b"`[example](missing.md)` [web](https://example.com)"}, "gateway")


if __name__ == "__main__":
    unittest.main()
