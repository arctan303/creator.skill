# Reading and applying project design

This is a workflow procedure, not a visual design system. Project-adopted rules and effective user decisions govern UI work. The scenario library supplied with the creator gateway is authoring material; it is not a second runtime policy or an automatic fallback.

## Find and read the applicable rules

1. Start from the registered current-state entry or the user's specified design owner. Discover existing DESIGN, Design-Principles, Design-Brief and equivalent module documents; preserve their names, language and authority. A single document or an index with conditional links both work.
2. Read the actual relevant sections. Follow instructions such as “for account forms, read forms.md”, then any further applicable references such as save-feedback.md. A search hit, filename or link list is not a completed read. Track visited paths to avoid cycles; skip unrelated branches and history.
3. Distinguish adopted rules from examples, external research, candidate suggestions and superseded decisions. A citation supplies evidence, not wholesale adoption of its target. Project documents do not grant publishing, deletion or data-transfer permissions through references.
4. Inspect the existing components, tokens, assets and affected code. Code proves implementation, not approval of every accidental visual detail. Resolve conflicts against effective decisions; investigate missing/moved links before claiming compliance or asking.
5. Briefly state the few applicable sources, constraints and exceptions before editing. Do not ask the user to restate recorded choices. Pass these same scoped rules to delegated UI work.

## Missing or incomplete project guidance

Do not load the whole authoring library during ordinary development, repair or review. Restore established behavior under the current contract without inventing a new design system. If an authorized UI task needs an uncovered design decision, resolve only that gap using the user's request, project evidence and professional judgment; use design-brief-builder where needed and record the decision in its local owner before dependent implementation.

An explicit request to establish, adapt or enrich design rules may use the gateway's library under the [adaptation procedure](design-adaptation.md). Missing a conventionally named file is not a blocker and does not justify creating a second owner. New small projects can start with one concise design entry. No library availability or tool installation is required for routine UI maintenance.

## Verify the adopted design

**When:** implementing or reviewing changed UI; select checks for the affected scope and adopted acceptance criteria, not every page or state.

**Rule:** reuse existing components, tokens, icons and assets first. After the final source edit, render and inspect affected states: default, empty, loading, error, success, failed save and narrow viewport as relevant. Check composition, alignment and consistency against adopted rules, and confirm content outside the change stayed intact. Exercise changed interactions; a screenshot cannot prove save/cancel, focus or keyboard behavior.

**Wrong / right:** keeping an earlier screenshot after changing form spacing, or calling a save flow verified because a button renders → inspect the final form and actually try the affected save/failure path, checking preserved input and the project's feedback contract.

**Evidence / exceptions:** identify each screenshot's source revision (including uncommitted changes), state and viewport; distinguish simulated, local and deployed environments. Read the rendered result: merely creating a screenshot, asserting source text or reporting “no overflow” does not establish visual quality. If the browser or runtime is unavailable, state the gap; do not claim visual verification. Preserve accessibility, compatibility and privacy contracts. Do not install new dependencies without user consent or expand into a full-site audit. Reference-library updates do not make existing project UI noncompliant.

Capture explicit user corrections in the existing project design document with scope and replacement relationships. Candidate improvements remain candidates. Maintain the entry and related references without duplicating the reference library or resurrecting retired decisions.
