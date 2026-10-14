#!/usr/bin/env python3
"""Validate the unified artifacts and perform isolated real installation checks."""
import os
import posixpath
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

import build_release
import install_workflow as installer

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
sys.path.insert(0, str(ROOT / ".creator/scripts"))
from check_docs import markdown_links


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run_script(root, name, *arguments):
    result = subprocess.run([sys.executable, "-B", name, *arguments], cwd=root, capture_output=True,
                            text=True, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    require(result.returncode == 0, name + " failed:\n" + result.stdout + result.stderr)


def validate_local_links(files, label):
    """Check every Markdown member, including transitive references in gateway ZIPs."""
    for name, data in files.items():
        if not name.endswith(".md"):
            continue
        for target in markdown_links(data.decode("utf-8-sig")):
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            path = unquote(url.path)
            resolved = posixpath.normpath(path.lstrip("/") if path.startswith("/")
                                         else posixpath.join(posixpath.dirname(name), path))
            require(resolved != ".." and not resolved.startswith("../") and "\\" not in resolved,
                    label + " link escapes archive: " + name + " -> " + target)
            exists = resolved in files or any(member.startswith(resolved.rstrip("/") + "/") for member in files)
            require(exists, label + " missing local link: " + name + " -> " + target)


def main():
    package = installer.load_package(DIST / "creator-workflow.zip")
    manifest, files = package["manifest"], package["files"]
    require(manifest["version"] == build_release.read_version(), "Package VERSION differs from source")
    require("CLAUDE.md" not in files and not any(name.startswith(".claude/commands/") for name in files),
            "Unified package must not contain duplicate policy or legacy commands")
    require(".creator/docs-state.json" not in files and not any(name.startswith("docs/") for name in files),
            "Package must not contain source-project state or project knowledge")
    expected_policy = ("> Workflow version / 工作流版本: " + manifest["version"] + "\n\n" +
                       (ROOT / "AGENTS.md").read_text(encoding="utf-8"))
    require(files["AGENTS.md"].decode("utf-8") == expected_policy, "Canonical policy differs from source")
    for skill in manifest["skills"]:
        canonical = files[".agents/skills/" + skill + "/SKILL.md"].decode("utf-8")
        adapter = files[".claude/skills/" + skill + "/SKILL.md"].decode("utf-8")
        require(adapter == build_release.claude_adapter(skill, canonical), "Adapter duplicated or changed policy: " + skill)
        names = [name for name in files if name.startswith(".claude/skills/" + skill + "/")]
        require(len(names) == 1, "Claude adapter contains copied policy assets: " + skill)
    gateway, _ = installer.read_archive(DIST / "creator-gateway.zip")
    require({"SKILL.md", "agents/openai.yaml", "references/cli-adapters.md", "scripts/install_workflow.py"}.issubset(gateway),
            "Gateway is incomplete")
    source_installer = (ROOT / "scripts/install_workflow.py").read_bytes()
    require(gateway["scripts/install_workflow.py"] == source_installer == files[".creator/scripts/install_workflow.py"],
            "Gateway and workflow installer must match source")
    for reference in build_release.source_files(ROOT / ".creator/references"):
        name = reference.relative_to(ROOT / ".creator/references").as_posix()
        require(gateway.get("references/" + name) == files[".creator/references/" + name], "Shared reference missing/differs: " + name)
    validate_local_links(files, "workflow")
    validate_local_links(gateway, "gateway")
    with tempfile.TemporaryDirectory(prefix="creator-package-verify-") as directory:
        root = Path(directory)
        plan = installer.make_plan(root, package)
        require(not plan["conflicts"] and not list(root.iterdir()), "Fresh dry-run changed files or conflicted")
        installer.apply_plan(root, plan)
        require(not installer.make_plan(root, package)["changes"], "Same-package install is not idempotent")
        run_script(root, ".creator/scripts/evaluate_prompt_cases.py")
        run_script(root, ".creator/scripts/check_docs.py", "--root", ".")
    print("Unified workflow and gateway verified: hashes, adapters, real temporary install, idempotence and packaged checks.")
    print("Claude/Codex live discovery and model-task behavior remain separate evidence; this check does not prove them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
