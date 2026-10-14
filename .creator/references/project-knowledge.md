# Project knowledge and documentation checks

The `project-knowledge` skill owns scoped capture and reconciliation of project conventions, current documentation and task retirement. It preserves existing file responsibilities rather than creating a universal memory ledger. Product/design skills make or clarify new choices; `self-evolver` handles reproducible defects in the workflow itself.

## Lightweight navigation

Reuse a verified README, MANUAL, PROJECT-CONTEXT or equivalent current-state entry. Register existing authoritative files in `.creator/docs-state.json` when useful:

```json
{
  "entrypoints": {
    "context": "docs/README.md",
    "spec": "docs/Product-Spec.md",
    "plan": "docs/DEV-PLAN.md",
    "design_principles": "docs/Design-Principles.md",
    "release": "docs/Development-Release.md"
  }
}
```

This is an entrypoint fragment, not a complete migration record. Only register real files with those responsibilities; names are not mandatory. Entrypoint keys other than `context` are descriptive, so existing `product` or `overview` keys remain valid. Keep the registry limited to navigation, migration mappings, pending work and concise evidence references. Do not copy ongoing execution logs or every project's rules into it.

`verified_at` records when the declared migration/registration scope was checked. It is not the verification date of every capability, deployment or task. Those retain their own code/environment baselines in the appropriate records. Installation version, docs schema, migration scope and deployment state remain separate.

## Safe link declarations

`python .creator/scripts/check_docs.py --root .` is read-only. It inventories Markdown under `docs/`, registered Markdown files, mapped directories and explicitly declared link-source scopes. It reads those Markdown documents and registration data; ordinary linked source-file contents and exact-link target/evidence contents are not read. Do not register private material that should not be inspected.

- Entrypoints must be existing repository-local files.
- Migration mapping `targets` may be existing repository-local files **or directories**. Directories contribute their Markdown inventory; nonexistent targets are still errors. A moved source need not still exist.
- File and directory links are resolved relative to the document; `/path` means repository-root-relative unless an explicitly declared site route applies. Missing targets and paths escaping the repository are errors, including encoded traversal and external symlink targets.
- A source citation such as `../src/app.py:12` or `../src/app.py:12-16` checks the actual file and positive, ordered line syntax. It does not read source contents or prove those lines exist or support a claim. Windows absolute paths and `file:` URLs are not portable repository links.
- Remote links are not fetched. Fragment/anchor correctness and product semantics need their appropriate verification.

Some public Markdown uses application routes rather than filesystem links. Declare a route source explicitly instead of suppressing missing links:

```json
{
  "site_routes": [
    {"source": "apps/web/docs", "url_prefix": "/docs"}
  ]
}
```

This optional field is compatible with schema 1. With the declaration above, `/docs/en/costs` resolves to `apps/web/docs/en/costs.md` or `apps/web/docs/en/costs/index.md`; relative `costs` from another article in that source works the same way. `/docs/en` can resolve to `apps/web/docs/en.md` or `apps/web/docs/en/index.md`. The source must exist inside the repository, and route targets must remain inside it. Queries and fragments do not change the source path.

Only extensionless links within an explicit route scope use this resolution. An explicit `missing.md`, an unrelated `/other/page`, or a missing declared article remains an error unless that exact href has its own valid declaration below. Route prefixes use path-segment boundaries; the most specific declared prefix wins. Existing unrelated local directories do not satisfy a declared site route.

Application routes and renderer/build resource rewrites can instead use optional `exact_links`, also compatible with schema 1:

```json
{
  "exact_links": [
    {
      "source": "apps/web/docs",
      "href": "/inbox",
      "kind": "app_route",
      "target": "apps/web/src/Inbox.vue",
      "evidence": "apps/web/src/router.js",
      "reason": "The router mounts this component at /inbox."
    },
    {
      "source": "apps/web/docs/licenses.md",
      "href": "LICENSE",
      "kind": "resource",
      "target": "LICENSE",
      "evidence": "apps/web/vite.config.js",
      "reason": "The renderer/build exposes the repository license as a downloadable resource."
    }
  ]
}
```

Each object requires exactly these six fields. `source` is an existing repository directory or a single Markdown file and adds its Markdown documents to the inventory. Matching is restricted to that scope. `target` and `evidence` must be existing repository files; evidence identifies the source/configuration for human review, while `reason` explains the mapping. `kind` is `app_route` for an application path (including `/`, a single trailing slash or a dotted path such as `/callback.json`) or `resource` for a resource rewrite. There is no wildcard or automatic inference from failed links.

The complete `href` matches literally, including query and fragment. A declaration for `/inbox` does not accept `/inbox/`, `/inboxes`, `/inbox?mode=full` or `/inbox#messages`; declare each supported variant separately when needed. These declarations cannot map remote URLs, fragment-only links or source-line citations. Filesystem declaration paths must be literal repository-relative POSIX paths without URLs, absolute paths, drive/ADS syntax, backslashes, percent encoding, empty/traversal segments or wildcard/query/fragment syntax. Href paths follow the same literal-path restrictions except that `/`, a single leading/trailing `/` and exact queries/fragments are supported; middle `//` and traversal segments remain invalid. Symlink targets must remain inside the repository.

Two declarations with the same href and overlapping source scopes are errors, even if their targets agree. Disjoint scopes may map the same href independently. An exact mapping also fails if ordinary file or declared site-route resolution succeeds with a different file/article target; reconcile the declarations rather than silently override a real file/article. For `app_route`, an existing repository directory alone is not a competing application target (for example, the repository root for `/`); `resource` retains directory conflicts. Source citations retain their ordinary validation. Unmatched links continue through ordinary file/site-route checks, so declarations cannot suppress unrelated `missing.md` failures.

The report's `exact_link_resolutions` lists every accepted use with document, href, declaration index (zero-based), source, kind, target and evidence for auditing. The checker verifies only that declarations are well formed and their files exist within the repository. It does not read or execute the router, renderer or build configuration, prove the reason, verify fragments, fetch resources, or prove live application/HTTP behavior. Use the project's native checks and review for those claims.

## Reading the report

- `status` retains the declared migration status for compatibility.
- `registration_status` distinguishes `unregistered`, `pending`, `partial`, `complete` and structurally `invalid` registration. It does not certify the semantics of migration.
- `inventory_status` is `passed` or `failed` for the checks actually run; `errors` and `warnings` explain the result.
- An unregistered empty project can have a successful inventory. That is not a complete migration. Use `--require-complete` to require a structurally complete registration in the checked scope.
- Density warnings invite a review of responsibilities and duplication, not automatic splitting or deletion. A large archive is not inherently a defect.

The checker cannot decide that an old Phase is obsolete, a user approved a change, or a test passed. Perform targeted semantic reconciliation using the current decision, its source and dependent obligations. Keep historical results intact while retiring only the no-longer-applicable work; see the [workflow contract](workflow-contract.md) and [migration guide](docs-migration-1.5.md).
