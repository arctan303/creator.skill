#!/usr/bin/env python3
"""Read-only Markdown/route inventory and registration checks; no semantic migration."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

DOCS_SCHEMA = 1
ACTIONS = {"keep", "update", "split", "merge", "archive", "pending"}


def contained(root, path):
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except (ValueError, OSError, RuntimeError):
        return False


def local_file(root, value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("expected a non-empty repository-relative POSIX path")
    if value.startswith("/") or urlsplit(value).scheme:
        raise ValueError("absolute paths and URLs are not allowed")
    path = root / value
    if not contained(root, path):
        raise ValueError("path leaves repository")
    return path


def markdown_links(text):
    # Exclude examples in fenced/inline code; fragments are not validated.
    text = re.sub(r"(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$", "", text)
    text = re.sub(r"`+[^`\n]*`+", "", text)
    for match in re.finditer(r"\[[^\]\n]*\]\((?:<([^>\n]+)>|([^\s)]+)(?:\s+\"[^\"]*\")?)\)", text):
        yield match.group(1) or match.group(2)
    for match in re.finditer(r"(?m)^\s*\[[^\]]+\]:\s*(?:<([^>]+)>|(\S+))", text):
        yield match.group(1) or match.group(2)


def site_routes(root, state, errors):
    """Load explicit source-directory routes; never infer routes from broken links."""
    values = state.get("site_routes", []) if state else []
    if not isinstance(values, list):
        errors.append("site_routes must be a list")
        return []
    routes = []
    for index, item in enumerate(values):
        try:
            if not isinstance(item, dict):
                raise ValueError("route must be an object")
            source = local_file(root, item.get("source"))
            if not source.is_dir():
                raise ValueError("source must be an existing directory")
            prefix = item.get("url_prefix")
            if not isinstance(prefix, str) or not prefix.startswith("/") or prefix.startswith("//"):
                raise ValueError("url_prefix must be a site-root path")
            url = urlsplit(prefix)
            if url.query or url.fragment or any(char in prefix for char in "%\\:?#") or any(ord(char) < 32 for char in prefix):
                raise ValueError("url_prefix must be a literal path without query or fragment")
            prefix = prefix.rstrip("/") or "/"
            if any(part in (".", "..", "") for part in prefix[1:].split("/")) and prefix != "/":
                raise ValueError("url_prefix contains an empty or traversal segment")
            if any(known[0] == prefix for known in routes):
                raise ValueError("duplicate url_prefix")
            routes.append((prefix, source))
        except (ValueError, OSError, TypeError) as exc:
            errors.append("site route {}: {}".format(index, exc))
    return routes


def exact_link_path(root, value):
    """Literal declarations are portable paths, never encoded filesystem syntax."""
    path = local_file(root, value)
    if any(char in value for char in "%:?#*") or any(ord(char) < 32 for char in value):
        raise ValueError("expected a literal repository-relative path")
    if any(part in ("", ".", "..") for part in value.split("/")):
        raise ValueError("path contains an empty or traversal segment")
    return path


def exact_link_declarations(root, state, errors):
    """Validate explicit mappings without reading or executing their evidence files."""
    values = state.get("exact_links", []) if state else []
    if not isinstance(values, list):
        errors.append("exact_links must be a list")
        return []
    declarations = []
    required = {"source", "href", "kind", "target", "evidence", "reason"}
    for index, item in enumerate(values):
        try:
            if not isinstance(item, dict) or set(item) != required:
                raise ValueError("mapping must contain source, href, kind, target, evidence and reason only")
            source = exact_link_path(root, item["source"])
            if not source.is_dir() and not (source.is_file() and source.suffix.lower() == ".md"):
                raise ValueError("source must be an existing directory or Markdown file")
            target = exact_link_path(root, item["target"])
            evidence = exact_link_path(root, item["evidence"])
            if not target.is_file() or not evidence.is_file():
                raise ValueError("target and evidence must be existing files")
            href = item["href"]
            if not isinstance(href, str) or not href or any(char.isspace() or ord(char) < 32 for char in href):
                raise ValueError("href must be a non-empty literal local link")
            url = urlsplit(href)
            if href.startswith("//") or url.scheme or url.netloc or not url.path or any(char in url.path for char in "%\\:*"):
                raise ValueError("href must be a literal local path, not a URL or source citation")
            segments = url.path.removeprefix("/").removesuffix("/")
            if url.path != "/" and (not segments or any(part in ("", ".", "..") for part in segments.split("/"))):
                raise ValueError("href contains an empty or traversal segment")
            if item["kind"] not in ("app_route", "resource"):
                raise ValueError("kind must be app_route or resource")
            if not isinstance(item["reason"], str) or not item["reason"].strip():
                raise ValueError("reason is required")
            declarations.append(dict(item, index=index, source_path=source, target_path=target))
        except (ValueError, OSError, TypeError) as exc:
            errors.append("exact link {}: {}".format(index, exc))
    conflicting = set()
    for offset, item in enumerate(declarations):
        for other in declarations[:offset]:
            if item["href"] == other["href"] and (
                    contained(item["source_path"], other["source_path"]) or
                    contained(other["source_path"], item["source_path"])):
                errors.append("exact links {} and {}: overlapping sources for the same href".format(other["index"], item["index"]))
                conflicting.update((other["index"], item["index"]))
    return [item for item in declarations if item["index"] not in conflicting]


def link_destination(root, document, target, routes, exact_links=(), resolutions=None):
    """Resolve an exact declaration only when ordinary resolution is unambiguous."""
    matches = [item for item in exact_links if item["href"] == target and
               (document.resolve() == item["source_path"].resolve() if item["source_path"].is_file()
                else contained(item["source_path"], document))]
    if not matches:
        return ordinary_link_destination(root, document, target, routes)
    if len(matches) != 1:
        raise ValueError("ambiguous exact link declarations")
    item = matches[0]
    try:
        ordinary = ordinary_link_destination(root, document, target, routes)
    except ValueError as exc:
        if not str(exc).startswith("missing "):
            raise
    else:
        directory_route = ordinary is not None and ordinary.is_dir() and item["kind"] == "app_route"
        if not directory_route and (ordinary is None or ordinary.resolve() != item["target_path"].resolve()):
            raise ValueError("exact link conflicts with ordinary file or site-route resolution")
    if resolutions is not None:
        resolutions.append({"document": document.relative_to(root).as_posix(), "href": target,
                            "declaration": item["index"], "source": item["source"],
                            "kind": item["kind"], "target": item["target"], "evidence": item["evidence"]})
    return item["target_path"]


def ordinary_link_destination(root, document, target, routes):
    """Resolve files, directories, source-line citations and declared Markdown routes.

    Returns None for external/fragment-only links. No target content is read.
    """
    url = urlsplit(target)
    if re.match(r"^[A-Za-z]:", target) or url.scheme.lower() == "file":
        raise ValueError("absolute filesystem links are not repository-relative")
    # urlsplit mistakes a bare citation like app.py:12 for a URI scheme.
    if url.scheme and "." in url.scheme and not url.netloc:
        url = urlsplit("./" + target)
    if url.scheme or url.netloc or not url.path:
        return None
    name = unquote(url.path)
    if "\\" in name or "\x00" in name or re.match(r"^/?[A-Za-z]:", name):
        raise ValueError("unsafe filesystem link")
    citation = re.fullmatch(r"(.+):(\d+)(?:-(\d+))?", name)
    if citation:
        name, start, end = citation.groups()
        if int(start) < 1 or (end is not None and int(end) < int(start)):
            raise ValueError("source line numbers must be positive and ordered")
    # Reject alternate data streams and unsupported line suffixes on every host.
    if ":" in name:
        raise ValueError("unsupported colon in filesystem link")
    dest = root / name.lstrip("/") if name.startswith("/") else document.parent / name
    if not contained(root, dest):
        raise ValueError("link leaves repository")
    # Explicit route scopes take priority over coincidentally existing local directories.
    candidates = []
    if not citation and not Path(name).suffix:
        for prefix, source in routes:
            if name.startswith("/"):
                base = "" if prefix == "/" else prefix
                if name != prefix and not name.startswith(base + "/"):
                    continue
                relative = name[len(base):].lstrip("/")
                candidates.append((len(prefix), source, source / relative))
            elif contained(source, document):
                candidates.append((len(source.parts), source, document.parent / name))
    if not candidates:
        if dest.exists():
            if citation and not dest.is_file():
                raise ValueError("source-line target must be a file")
            return dest
        raise ValueError("missing file link (site routes require an explicit declaration)")
    _, source, route = max(candidates, key=lambda item: item[0])
    if not contained(source, route) or not contained(root, route):
        raise ValueError("site route leaves its source directory")
    targets = [] if route.resolve() == source.resolve() else [Path(str(route) + ".md")]
    targets.append(route / "index.md")
    for path in targets:
        if not contained(source, path) or not contained(root, path):
            raise ValueError("site route leaves its source directory")
        if path.is_file():
            return path
    raise ValueError("missing declared site route")


def inspect(root, require_complete=False):
    root = Path(root).resolve()
    report = {"root": str(root), "status": "unregistered", "registration_status": "unregistered",
              "inventory_status": "failed", "documents": [], "exact_link_resolutions": [],
              "warnings": [], "errors": [], "limitations": [
                  "structural registration and inventory only; migration semantics and historical completeness require review",
                  "declared site routes resolve Markdown sources, not live router or HTTP behavior",
                  "exact links check declared target/evidence files exist, not application logic or HTTP behavior",
                  "fragments and source-line contents/ranges are not verified; linked source files are not read"]}
    errors = report["errors"]
    if not root.is_dir():
        errors.append("repository root does not exist")
        return report
    state_path = root / ".creator" / "docs-state.json"
    state = None
    if not contained(root, state_path):
        errors.append("docs-state path leaves repository")
    elif state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8-sig"))
            if not isinstance(state, dict):
                raise ValueError("state must be an object")
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append("invalid docs-state: " + str(exc))
            state = None
    elif require_complete:
        errors.append("docs-state is missing; installation does not prove migration")

    extra_files = []
    if state is not None:
        report["status"] = state.get("status")
        for key in ("schema_version", "docs_schema_version"):
            if type(state.get(key)) is not int or state[key] != DOCS_SCHEMA:
                errors.append("unsupported " + key)
        if state.get("status") not in ("pending", "partial", "complete"):
            errors.append("invalid migration status")
        if not isinstance(state.get("workflow_version"), str) or not re.fullmatch(r"\d+\.\d+\.\d+", state["workflow_version"]):
            errors.append("workflow_version must be semantic version, not installation date")
        entries = state.get("entrypoints")
        if not isinstance(entries, dict):
            errors.append("entrypoints must be an object")
            entries = {}
        for key, value in entries.items():
            try:
                path = local_file(root, value)
                if not path.is_file():
                    raise ValueError("file is missing")
                extra_files.append(path)
            except (ValueError, OSError) as exc:
                errors.append("entrypoint {}: {}".format(key, exc))
        mappings = state.get("mappings")
        if not isinstance(mappings, list):
            errors.append("mappings must be a list")
            mappings = []
        for index, item in enumerate(mappings):
            try:
                if not isinstance(item, dict):
                    raise ValueError("mapping must be an object")
                local_file(root, item.get("source"))  # source may have been moved
                action = item.get("action")
                if action not in ACTIONS:
                    raise ValueError("invalid action")
                targets = item.get("targets")
                if not isinstance(targets, list) or (not targets and action != "pending"):
                    raise ValueError("targets must be a list, non-empty except for pending")
                if not isinstance(item.get("reason"), str) or not item["reason"].strip():
                    raise ValueError("reason is required")
                if state.get("status") == "complete" and action == "pending":
                    raise ValueError("complete state contains pending mapping")
                for value in targets:
                    path = local_file(root, value)
                    if not path.exists():
                        raise ValueError("missing target: " + value)
                    if path.is_dir():
                        extra_files.extend(path.rglob("*.md"))
                    elif path.is_file():
                        extra_files.append(path)
                    else:
                        raise ValueError("target must be a file or directory: " + value)
            except (ValueError, OSError, TypeError) as exc:
                errors.append("mapping {}: {}".format(index, exc))
        pending = state.get("pending")
        if not isinstance(pending, list) or any(not isinstance(x, str) for x in pending):
            errors.append("pending must be a list of strings")
        if state.get("status") == "complete":
            if pending != []:
                errors.append("complete state must have no pending items")
            if not entries.get("context"):
                errors.append("complete state requires context entrypoint")
            if not isinstance(state.get("verified_at"), str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", state["verified_at"]):
                errors.append("complete state requires verified_at date")
            evidence = state.get("evidence")
            if not isinstance(evidence, list) or not evidence or any(not isinstance(x, str) or not x.strip() for x in evidence):
                errors.append("complete state requires evidence descriptions")
    routes = site_routes(root, state, errors)
    for _, source in routes:
        extra_files.extend(source.rglob("*.md"))
    exact_links = exact_link_declarations(root, state, errors)
    for item in exact_links:
        source = item["source_path"]
        extra_files.extend(source.rglob("*.md") if source.is_dir() else [source])
    if state is not None:
        report["registration_status"] = "invalid" if errors else state.get("status")
    elif state_path.exists():
        report["registration_status"] = "invalid"
    if require_complete and state is not None and state.get("status") != "complete":
        errors.append("docs migration is not complete")

    docs = root / "docs"
    paths = set(extra_files)
    if not contained(root, docs):
        errors.append("docs directory leaves repository")
    elif docs.exists():
        paths.update(docs.rglob("*.md"))
    for path in sorted(paths):
        if not contained(root, path):
            errors.append("document leaves repository: " + str(path))
            continue
        if path.suffix.lower() != ".md":
            continue
        rel = path.relative_to(root).as_posix()
        try:
            raw = path.read_bytes()
            text = raw.decode("utf-8-sig")
        except (OSError, UnicodeError) as exc:
            errors.append("cannot read {}: {}".format(rel, exc))
            continue
        lines = text.splitlines()
        size = {"path": rel, "bytes": len(raw), "lines": len(lines),
                "longest_line": max((len(line) for line in lines), default=0)}
        report["documents"].append(size)
        context = (state or {}).get("entrypoints", {})
        is_context = isinstance(context, dict) and context.get("context") == rel
        if len(raw) > (8192 if is_context else 20480) or len(lines) > (150 if is_context else 300) or size["longest_line"] > 500:
            report["warnings"].append("consider splitting or reducing density: " + rel)
        for target in markdown_links(text):
            try:
                link_destination(root, path, target, routes, exact_links, report["exact_link_resolutions"])
            except (ValueError, OSError) as exc:
                errors.append("{} -> {}: {}".format(rel, target, exc))
    report["inventory_status"] = "failed" if errors else "passed"
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    result = inspect(args.root, args.require_complete)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
