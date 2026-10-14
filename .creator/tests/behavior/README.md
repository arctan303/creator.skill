# Agent behavior fixtures

Use `python .creator/scripts/prepare_behavior_run.py prepare --output <new-directory>`.
Give a fresh agent only one generated workspace and its TASK.md. The workspace
contains current instructions, project files and the task, but no cases.json,
expected fields, rubric or previous model output. Do not expose the parent run's
private baseline or this source directory to the agent. Hosts supporting a
restricted working root should enforce it. An instruction-only boundary is not
an OS sandbox and must be reported as such.

Run `inspect --output <directory>` after execution. This checks real changed files,
required edits and untouched evidence. It does **not** grade meaning or prove a
host integration. Review RESULT.md, the diff and tool trace against the private
rubric in scenarios.json; save actual outcomes and limitations in the development
record. A field-only response or copying the rubric is not a behavioral test.

These synthetic fixtures are not migrations of the user's real projects. Do not
claim a failing old baseline or cross-model improvement without actually running
that comparison. Retain failed/interrupted results; do not rerun unchanged input
until success. Prepare a new directory for any justified new baseline.
