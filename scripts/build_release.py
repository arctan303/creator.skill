#!/usr/bin/env python3
"""Build one canonical workflow package and the standalone installation gateway."""
import hashlib
import json
import re
import shutil
import stat
import tempfile
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = REPO_ROOT / "dist"
SKILLS_SRC = REPO_ROOT / ".agents/skills"
GATEWAY_SRC = REPO_ROOT / "gateway"
RELEASE_MANIFEST = ".creator-manifest.json"
CASES_PATH = ".creator/tests/prompt-cases/cases.json"
SIGNALS_PATH = ".creator/evolution/signals.md"
SIGNALS_TEMPLATE = """# Workflow evolution signals / 工作流改进信号

No recorded signals / 暂无记录。

Record real events and patch evidence using EVOLUTION.md. Preserve existing host-specific ledgers; do not import their content automatically.
按 EVOLUTION.md 记录真实事件与补丁证据。保留已有宿主台账，不自动搬迁其内容。
"""


def write_text(path, text):
    path.write_bytes(text.encode("utf-8"))


def read_version():
    version = (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("VERSION must be a semantic version")
    return version


def is_link(path):
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & 0x400)


def source_files(directory):
    for path in sorted(directory.rglob("*")):
        if any(part in {"__pycache__", "results", "runs"} for part in path.relative_to(directory).parts):
            continue
        if is_link(path):
            raise ValueError("Refusing linked package source: " + str(path))
        if path.is_file() and path.suffix not in {".pyc", ".pyo"}:
            yield path


def copy_tree(source, target):
    for path in source_files(source):
        dest = target / path.relative_to(source)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest)


def discover_skills():
    return sorted(path.name for path in SKILLS_SRC.iterdir() if (path / "SKILL.md").is_file())


def metadata(text, key):
    """Repository interfaces use single-line YAML scalars; fail on other forms."""
    frontmatter = text.split("---", 2)
    if len(frontmatter) != 3 or frontmatter[0].strip():
        raise ValueError("Missing Skill frontmatter")
    match = re.search(r"(?m)^" + re.escape(key) + r":\s*(.+)$", frontmatter[1])
    if not match or match.group(1).strip() in {"|", ">", "|-", ">-"}:
        raise ValueError("Missing single-line Skill " + key)
    value = match.group(1).strip()
    return json.loads(value) if value.startswith('"') else value.strip("'")


def claude_adapter(skill_name, canonical):
    return (
        "---\nname: " + skill_name + "\ndescription: " + json.dumps(metadata(canonical, "description"), ensure_ascii=False) + "\n---\n\n"
        + "Read and follow the [canonical skill](../../../.agents/skills/" + skill_name + "/SKILL.md) before acting. "
        + "Resolve its relative references from that canonical file's directory.\n"
    )


def zip_directory(source, destination):
    """Fixed ZIP metadata makes identical source builds byte-reproducible."""
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in source_files(source):
            entry = zipfile.ZipInfo(path.relative_to(source).as_posix(), (2020, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.create_system = 3
            entry.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(entry, path.read_bytes())


def write_release_manifest(stage, skills, version):
    files = {}
    for path in source_files(stage):
        name = path.relative_to(stage).as_posix()
        kind = "merge-cases" if name == CASES_PATH else "create-only" if name == SIGNALS_PATH else "managed"
        files[name] = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "kind": kind}
    manifest = {
        "schema_version": 2, "workflow": "creator.skill", "version": version,
        "platform": "unified", "instruction_file": "AGENTS.md", "skill_root": ".agents/skills",
        "skill_count": len(skills), "skills": skills, "adapters": {"claude-code": ".claude/skills"},
        "docs_schema_version": 1, "docs_guide": ".creator/references/docs-migration-1.5.md",
        "preserve": [SIGNALS_PATH, ".codex/evolution/signals.md", ".claude/evolution/signals.md", ".creator/docs-state.json", ".creator/project-knowledge/"],
        "files": files,
    }
    write_text(stage / RELEASE_MANIFEST, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")


def build_workflow(stage, skills, version):
    stage.mkdir()
    policy = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    write_text(stage / "AGENTS.md", "> Workflow version / 工作流版本: " + version + "\n\n" + policy)
    shutil.copyfile(REPO_ROOT / "EVOLUTION.md", stage / "EVOLUTION.md")
    for name in ("references", "scripts", "tests"):
        copy_tree(REPO_ROOT / ".creator" / name, stage / ".creator" / name)
    shutil.copyfile(REPO_ROOT / "scripts/install_workflow.py", stage / ".creator/scripts/install_workflow.py")
    for skill_name in skills:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_name):
            raise ValueError("Unsafe Skill name: " + skill_name)
        source = SKILLS_SRC / skill_name
        canonical = (source / "SKILL.md").read_text(encoding="utf-8")
        if metadata(canonical, "name") != skill_name:
            raise ValueError("Skill name does not match directory: " + skill_name)
        if not (source / "agents/openai.yaml").is_file():
            raise ValueError("Missing Codex discovery metadata: " + skill_name)
        copy_tree(source, stage / ".agents/skills" / skill_name)
        adapter = stage / ".claude/skills" / skill_name / "SKILL.md"
        adapter.parent.mkdir(parents=True)
        write_text(adapter, claude_adapter(skill_name, canonical))
    signal = stage / SIGNALS_PATH
    signal.parent.mkdir(parents=True)
    write_text(signal, SIGNALS_TEMPLATE)
    write_text(stage / ".version", version + "\n")
    write_release_manifest(stage, skills, version)


def build_gateway(stage):
    copy_tree(GATEWAY_SRC, stage)
    # Shared references link to one another; include their complete small closure.
    copy_tree(REPO_ROOT / ".creator/references", stage / "references")
    script = stage / "scripts/install_workflow.py"
    script.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(REPO_ROOT / "scripts/install_workflow.py", script)
    skill = stage / "SKILL.md"
    write_text(skill, skill.read_text(encoding="utf-8").replace("../.creator/references/", "references/"))


def main():
    version = read_version()
    skills = discover_skills()
    if not skills:
        raise ValueError("No skills found")
    if DIST_DIR.exists() and is_link(DIST_DIR):
        raise ValueError("Refusing linked dist directory")
    DIST_DIR.mkdir(exist_ok=True)
    # Do not erase unrelated outputs. Replace only these two generated archives.
    for name in ("creator-workflow.zip", "creator-gateway.zip"):
        output = DIST_DIR / name
        if output.exists() and is_link(output):
            raise ValueError("Refusing linked output: " + name)
    with tempfile.TemporaryDirectory(prefix="creator-build-") as temp:
        workflow = Path(temp) / "workflow"
        gateway = Path(temp) / "gateway"
        build_workflow(workflow, skills, version)
        build_gateway(gateway)
        zip_directory(workflow, DIST_DIR / "creator-workflow.zip")
        zip_directory(gateway, DIST_DIR / "creator-gateway.zip")
    print("Built creator-workflow.zip and creator-gateway.zip: version {}, {} canonical skills".format(version, len(skills)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
