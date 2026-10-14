"""Structural checker tests only; not model-task or semantic migration tests."""
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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
        result = module.inspect(self.root)
        self.assertEqual(result["status"], "unregistered")
        self.assertEqual(result["registration_status"], "unregistered")
        self.assertEqual(result["inventory_status"], "passed")
        self.assertTrue(module.inspect(self.root, True)["errors"])

    def test_complete_and_read_only_repeat(self):
        self.state()
        before = {str(p): (p.read_bytes(), p.stat().st_mtime_ns) for p in self.root.rglob("*") if p.is_file()}
        first = module.inspect(self.root, True)
        self.assertEqual(first["errors"], [])
        self.assertEqual(first["registration_status"], "complete")
        self.assertEqual(first["inventory_status"], "passed")
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

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_directory_mapping_inventories_documents_and_finds_broken_links(self):
        self.write("public/guide/one.md", "[two](two.md)\n")
        second = self.write("public/guide/two.md", "# Two\n")
        self.state(mappings=[dict(source="old/guide", action="merge", targets=["public/guide"], reason="source docs")])
        result = module.inspect(self.root, True)
        self.assertEqual(result["errors"], [])
        self.assertEqual({item["path"] for item in result["documents"]},
                         {"docs/README.md", "public/guide/one.md", "public/guide/two.md"})
        second.unlink()
        result = module.inspect(self.root, True)
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("public/guide/one.md -> two.md", result["errors"][0])

    def test_source_citations_validate_file_without_reading_source(self):
        source = self.write("src/app.py", "private source content\n")
        self.write("docs/README.md", "[source](../src/app.py:1)\n[range](../src/app.py:1-2)\n")
        original = Path.read_bytes
        def guarded_read(path):
            self.assertNotEqual(path.resolve(), source.resolve(), "checker must not read linked source contents")
            return original(path)
        with mock.patch.object(Path, "read_bytes", guarded_read):
            self.assertEqual(module.inspect(self.root)["errors"], [])
        source.unlink()
        result = module.inspect(self.root)
        self.assertEqual(len(result["errors"]), 2)

    def test_source_citation_invalid_lines_directory_and_traversal_are_rejected(self):
        self.write("src/app.py", "pass\n")
        for target in ("../src/app.py:0", "../src/app.py:5-2", "../src:1", "../../outside.py:1",
                       "../src/app.py:bad", "../src/app.py:1:2", "../src/app.py:stream"):
            with self.subTest(target=target):
                self.write("docs/README.md", "[source]({})\n".format(target))
                self.assertEqual(len(module.inspect(self.root)["errors"]), 1)

    def test_bare_source_filename_is_not_misclassified_as_remote_scheme(self):
        self.write("docs/sample.py", "pass\n")
        self.write("docs/README.md", "[bare](sample.py:1)\n")
        self.assertEqual(module.inspect(self.root)["errors"], [])
        for target in ("missing.py:1", "sample.py:0", "sample.py:stream"):
            self.write("docs/README.md", "[bare]({})\n".format(target))
            self.assertEqual(len(module.inspect(self.root)["errors"]), 1)

    def route_fixture(self):
        self.write("web/docs/en/start.md", "[costs](/docs/en/costs)\n[relative](costs?from=start#pricing)\n[index](/docs/en)\n")
        self.write("web/docs/en/costs.md", "# Costs\n")
        self.write("web/docs/en/index.md", "# Index\n")
        self.state(site_routes=[dict(source="web/docs", url_prefix="/docs")])

    def test_declared_absolute_relative_and_index_routes_use_real_sources(self):
        self.route_fixture()
        result = module.inspect(self.root, True)
        self.assertEqual(result["errors"], [])
        self.assertEqual(len(result["documents"]), 4)
        (self.root / "web/docs/en/costs.md").unlink()
        result = module.inspect(self.root, True)
        self.assertEqual(len(result["errors"]), 2)
        self.assertTrue(all("missing declared site route" in error for error in result["errors"]))

    def test_route_declaration_does_not_mask_missing_files_or_other_routes(self):
        self.route_fixture()
        self.write("web/docs/en/start.md", "[missing](missing.md)\n[other](/other/costs)\n[prefix](/docsets/en/costs)\n")
        result = module.inspect(self.root)
        self.assertEqual(len(result["errors"]), 3)
        self.assertEqual(result["inventory_status"], "failed")

    def test_undeclared_routes_are_not_silently_accepted(self):
        self.write("docs/README.md", "[route](/docs/en/costs)\n")
        self.write("web/docs/en/costs.md", "# Costs\n")
        self.assertEqual(len(module.inspect(self.root)["errors"]), 1)

    def test_route_scope_does_not_accept_unrelated_files_or_escape_source(self):
        self.route_fixture()
        self.write("web/outside.md", "# Not a site page\n")
        self.write("docs/en/costs", "An unrelated local file\n")
        (self.root / "web/docs/en/costs.md").unlink()
        self.write("web/docs/en/start.md", "[escape](/docs/../outside)\n[relative](../../outside)\n[absent](/docs/en/costs)\n")
        result = module.inspect(self.root)
        self.assertEqual(len(result["errors"]), 3)
        self.assertEqual(sum("leaves its source" in error for error in result["errors"]), 2)
        self.assertTrue(any("missing declared site route" in error for error in result["errors"]))

    def test_route_prefix_uses_path_boundary_and_most_specific_mapping(self):
        self.route_fixture()
        self.write("special/index.md", "# Special\n")
        self.write("docs/README.md", "[specific](/docs/special)\n")
        self.state(site_routes=[dict(source="web/docs", url_prefix="/docs"),
                                dict(source="special", url_prefix="/docs/special")])
        self.assertEqual(module.inspect(self.root)["errors"], [])

    def test_invalid_route_declarations_are_errors_not_ignored(self):
        self.write("web/docs/index.md", "# Index\n")
        invalid = ["bad", [None], [dict(source="../outside", url_prefix="/docs")],
                   [dict(source="web/missing", url_prefix="/docs")],
                   [dict(source="web/docs/index.md", url_prefix="/docs")]]
        for prefix in ("docs", "https://example.com/docs", "//host/docs", "/docs/../x", "/docs//x",
                       "/docs?x", "/docs#x", "/docs?", "/docs#", "/docs\x00", "/%2e%2e", "/docs\\x", "/docs:1"):
            invalid.append([dict(source="web/docs", url_prefix=prefix)])
        invalid.append([dict(source="web/docs", url_prefix="/docs")] * 2)
        for value in invalid:
            with self.subTest(routes=value):
                self.state(site_routes=value)
                result = module.inspect(self.root)
                self.assertTrue(result["errors"])
                self.assertEqual(result["registration_status"], "invalid")

    def test_encoded_traversal_and_absolute_filesystem_links_are_rejected(self):
        for target in ("%2e%2e/%2e%2e/outside.md", "..%5coutside.md", "C:/outside.md:1",
                       "file:///outside.md", "../%00name", "/C%3a/outside.md"):
            with self.subTest(target=target):
                self.write("docs/README.md", "[unsafe]({})\n".format(target))
                self.assertTrue(module.inspect(self.root)["errors"])

    def test_symlinked_mapping_and_link_must_not_read_outside_root(self):
        with tempfile.TemporaryDirectory() as outside_name:
            outside = Path(outside_name)
            (outside / "outside.md").write_text("[bad](missing.md)\n", encoding="utf-8")
            try:
                (self.root / "linked").symlink_to(outside, target_is_directory=True)
            except (OSError, NotImplementedError):
                if os.name != "nt":
                    self.skipTest("host does not permit creating directory symlinks")
                # Windows junctions need no symlink privilege. Both endpoints are
                # owned temporary fixtures, and tempfile cleanup does not traverse it.
                result = subprocess.run(["cmd", "/c", "mklink", "/J", str(self.root / "linked"), str(outside)],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                if result.returncode:
                    self.skipTest("host does not permit symlinks or directory junctions")
            self.state(mappings=[dict(source="old", action="keep", targets=["linked"], reason="unsafe")])
            self.write("docs/README.md", "[outside](../linked/outside.md)\n")
            result = module.inspect(self.root)
            self.assertEqual(len(result["errors"]), 2)
            self.assertEqual([item["path"] for item in result["documents"]], ["docs/README.md"])

    def test_partial_registration_is_not_complete_when_inventory_passes(self):
        self.state(status="partial", pending=["semantic review remains"])
        result = module.inspect(self.root)
        self.assertEqual(result["inventory_status"], "passed")
        self.assertEqual(result["registration_status"], "partial")
        self.assertTrue(module.inspect(self.root, True)["errors"])

    def exact_fixture(self, **overrides):
        self.write("web/docs/start.md", "[inbox](/inbox)\n[license](LICENSE)\n")
        self.write("src/router.js", "private route definition\n")
        self.write("src/Inbox.vue", "private component\n")
        self.write("LICENSE", "license text\n")
        route = dict(source="web/docs", href="/inbox", kind="app_route", target="src/Inbox.vue",
                     evidence="src/router.js", reason="Router mounts inbox component")
        resource = dict(source="web/docs", href="LICENSE", kind="resource", target="LICENSE",
                        evidence="src/router.js", reason="Renderer and build expose this resource")
        route.update(overrides)
        self.state(exact_links=[route, resource])
        return route, resource

    def test_exact_application_and_resource_links_are_audited_and_read_only(self):
        self.exact_fixture()
        before = {str(p): (p.read_bytes(), p.stat().st_mtime_ns) for p in self.root.rglob("*") if p.is_file()}
        original = Path.read_bytes
        def guarded_read(path):
            self.assertNotIn(path.suffix, (".js", ".vue"), "must not read mapping targets or evidence")
            self.assertNotEqual(path.name, "LICENSE", "must not read mapped resource contents")
            return original(path)
        with mock.patch.object(Path, "read_bytes", guarded_read):
            result = module.inspect(self.root, True)
            self.assertEqual(result, module.inspect(self.root, True))
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["registration_status"], "complete")
        self.assertEqual([(x["href"], x["kind"], x["declaration"]) for x in result["exact_link_resolutions"]],
                         [("/inbox", "app_route", 0), ("LICENSE", "resource", 1)])
        self.assertEqual(before, {str(p): (p.read_bytes(), p.stat().st_mtime_ns) for p in self.root.rglob("*") if p.is_file()})

    def test_exact_link_scope_and_near_matches_do_not_suppress_missing_links(self):
        self.exact_fixture()
        self.write("docs/README.md", "[outside](/inbox)\n[license](LICENSE)\n")
        self.write("web/docs/start.md", "[slash](/inbox/)\n[similar](/inboxes)\n[missing](missing.md)\n")
        result = module.inspect(self.root)
        self.assertEqual(len(result["errors"]), 5)
        self.assertEqual(result["exact_link_resolutions"], [])

    def test_exact_single_document_scope_and_disjoint_same_href_are_allowed(self):
        route, _ = self.exact_fixture(source="web/docs/start.md")
        other = dict(route, source="web/docs/other.md")
        self.write("web/docs/other.md", "[inbox](/inbox)\n")
        self.write("web/docs/unmapped.md", "[inbox](/inbox)\n")
        self.state(exact_links=[route, other, dict(route, href="LICENSE", kind="resource", target="LICENSE")],
                   site_routes=[dict(source="web/docs", url_prefix="/docs")])
        result = module.inspect(self.root)
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("unmapped.md", result["errors"][0])
        self.assertEqual(len(result["exact_link_resolutions"]), 3)

    def test_exact_query_and_fragment_must_match_the_whole_declared_href(self):
        route, _ = self.exact_fixture(href="/inbox?mode=full#messages")
        self.state(exact_links=[route])
        self.write("web/docs/start.md", "[exact](/inbox?mode=full#messages)\n[query](/inbox?mode=other#messages)\n"
                   "[fragment](/inbox?mode=full#other)\n[bare](/inbox)\n")
        result = module.inspect(self.root)
        self.assertEqual(len(result["errors"]), 3)
        self.assertEqual(len(result["exact_link_resolutions"]), 1)

    def test_exact_target_evidence_and_scope_must_still_exist(self):
        for missing in ("src/Inbox.vue", "src/router.js", "web/docs/start.md"):
            with self.subTest(missing=missing):
                self.exact_fixture(source="web/docs/start.md")
                (self.root / missing).unlink()
                result = module.inspect(self.root)
                self.assertEqual(result["registration_status"], "invalid")
                self.assertTrue(any("exact link" in error for error in result["errors"]))

    def test_malformed_exact_declarations_fail_registration(self):
        route, _ = self.exact_fixture()
        invalid = ["bad", [None], [dict(route, source="src/router.js")], [dict(route, target="src")],
                   [dict(route, evidence="src")], [dict(route, kind="ignore")], [dict(route, reason=" ")],
                   [dict(route, unknown="typo")], [dict(route, href=7)]]
        for value in invalid:
            with self.subTest(value=value):
                self.state(exact_links=value)
                self.assertEqual(module.inspect(self.root)["registration_status"], "invalid")

    def test_exact_declaration_paths_and_hrefs_reject_unsafe_syntax(self):
        route, _ = self.exact_fixture()
        for field in ("source", "target", "evidence"):
            for value in ("../outside", "/src/router.js", "C:/x", "https://example.com/x", "src\\router.js",
                          "src/router.js:stream", "src/%2e%2e/router.js", "src/../src/router.js", "src//router.js",
                          "src/router.js?x", "src/router.js#x", "src/\x00x"):
                with self.subTest(field=field, value=value):
                    self.state(exact_links=[dict(route, **{field: value})])
                    self.assertEqual(module.inspect(self.root)["registration_status"], "invalid")
        for href in ("https://example.com/inbox", "//host/inbox", "///inbox", " /inbox", "C:/inbox", "file:///inbox", "../inbox",
                     "/inbox/../other", "/inbox//other", "/inbox//", "/./", "/../", "/%2e%2e/inbox", "/inbox%2fother",
                     "inbox\\other", "/inbox:1", "/inbox:stream", "#only"):
            with self.subTest(href=href):
                self.state(exact_links=[dict(route, href=href)])
                self.assertEqual(module.inspect(self.root)["registration_status"], "invalid")

    def test_duplicate_and_overlapping_exact_scopes_are_not_prioritized(self):
        route, _ = self.exact_fixture()
        for other in (dict(route), dict(route, source="web/docs/start.md"), dict(route, source="web"),
                      dict(route, target="LICENSE", kind="resource")):
            with self.subTest(other=other):
                self.state(exact_links=[route, other])
                result = module.inspect(self.root)
                self.assertEqual(result["registration_status"], "invalid")
                self.assertTrue(any("overlapping" in error for error in result["errors"]))
                self.assertEqual(result["exact_link_resolutions"], [])

    def test_exact_links_cannot_silently_override_real_files_or_site_articles(self):
        route, _ = self.exact_fixture()
        self.write("inbox", "ordinary root file\n")
        self.state(exact_links=[route])
        self.write("web/docs/start.md", "[inbox](/inbox)\n")
        result = module.inspect(self.root)
        self.assertTrue(any("conflicts with ordinary" in error for error in result["errors"]))
        self.state(exact_links=[dict(route, target="inbox")])
        self.assertEqual(module.inspect(self.root)["errors"], [])
        (self.root / "inbox").unlink()
        self.write("web/docs/inbox.md", "# Article\n")
        self.state(exact_links=[route], site_routes=[dict(source="web/docs", url_prefix="/")])
        self.assertTrue(any("conflicts with ordinary" in error for error in module.inspect(self.root)["errors"]))
        self.state(exact_links=[dict(route, target="web/docs/inbox.md")],
                   site_routes=[dict(source="web/docs", url_prefix="/")])
        self.assertEqual(module.inspect(self.root)["errors"], [])

    def test_exact_declaration_symlinks_cannot_escape_repository(self):
        route, _ = self.exact_fixture()
        with tempfile.TemporaryDirectory() as outside_name:
            outside = Path(outside_name)
            (outside / "router.js").write_text("private\n", encoding="utf-8")
            (outside / "page.md").write_text("private\n", encoding="utf-8")
            try:
                (self.root / "linked").symlink_to(outside, target_is_directory=True)
            except (OSError, NotImplementedError):
                if os.name != "nt":
                    self.skipTest("host does not permit directory symlinks")
                result = subprocess.run(["cmd", "/c", "mklink", "/J", str(self.root / "linked"), str(outside)],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                if result.returncode:
                    self.skipTest("host does not permit symlinks or directory junctions")
            for field, value in (("source", "linked"), ("target", "linked/router.js"), ("evidence", "linked/router.js")):
                with self.subTest(field=field):
                    self.state(exact_links=[dict(route, **{field: value})])
                    result = module.inspect(self.root)
                    self.assertEqual(result["registration_status"], "invalid")
                    self.assertTrue(any("leaves repository" in error for error in result["errors"]))
                    self.assertNotIn("linked/page.md", [doc["path"] for doc in result["documents"]])

    def test_explicit_root_trailing_slash_and_dotted_application_routes(self):
        route, _ = self.exact_fixture()
        routes = [dict(route, href=href) for href in ("/", "/inbox/", "/callback.json")]
        (self.root / "inbox").mkdir()
        self.state(exact_links=routes)
        self.write("web/docs/start.md", "[home](/)\n[slash](/inbox/)\n[callback](/callback.json)\n"
                   "[bare](/inbox)\n[similar](/callback.json/other)\n[missing](missing.md)\n")
        result = module.inspect(self.root)
        # The undeclared /inbox is an ordinary existing directory link. The
        # other undeclared near match and explicit missing.md remain errors.
        self.assertEqual(len(result["errors"]), 2)
        self.assertEqual({item["href"] for item in result["exact_link_resolutions"]},
                         {"/", "/inbox/", "/callback.json"})
        self.write("web/docs/start.md", "[home](/)\n[slash](/inbox/)\n[callback](/callback.json)\n")
        self.assertEqual(module.inspect(self.root)["errors"], [])
        self.write("web/docs/index.md", "# Home article\n")
        self.state(exact_links=routes, site_routes=[dict(source="web/docs", url_prefix="/")])
        result = module.inspect(self.root)
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("start.md -> /:", result["errors"][0])
        self.assertIn("conflicts with ordinary", result["errors"][0])
        (self.root / "web/docs/index.md").unlink()
        self.write("callback.json", "{}\n")
        self.state(exact_links=routes)
        result = module.inspect(self.root)
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("/callback.json:", result["errors"][0])
        self.state(exact_links=[dict(route, href="/", kind="resource", target="LICENSE")])
        self.write("web/docs/start.md", "[resource](/)\n")
        self.assertTrue(any("conflicts with ordinary" in error for error in module.inspect(self.root)["errors"]))


if __name__ == "__main__":
    unittest.main()
