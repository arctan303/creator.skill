# Checking whether evidence distinguishes failure

## When to use

Use for a repair or behavior change when passing checks may miss the original defect or accept an incorrect result. R0 copy edits and obvious mechanical fixes need proportionate checks, not this full procedure.

## Short rule

- Derive expected results from the effective contract, independently of the implementation. Inspect the actual output, relevant state or generated artifact; a test name, exit code or completion claim is insufficient.
- For a repair, use a disposable isolated copy of the task baseline. Revert only the repair there, retain new tests, and confirm they fail because of the original defect. Restore the repair and confirm they pass. Never revert user or others' edits in their working trees; preserve pre-existing edits in the copied baseline.
- Try a relevant plausible wrong result in that copy: hardcoded examples, swallowed exceptions, deleted tests or a symptom-only patch. If it still passes, strengthen the check before relying on it. Choose examples by concrete risk, not an exhaustive mutation quota.
- Inspect the final artifact and connect each check to the behavior it establishes. Explain what it does not establish; source assertions do not prove runtime or visual behavior.

## Wrong / right example

Wrong: a CSV export check sees a file and reports success even when an embedded quote is lost.

Right: inspect parsed fields against independent expected values, including quotes and ordinary rows. Keeping the new check while removing the repair reproduces the original corruption; restoring it passes. A hardcoded sample-only export must fail another relevant input.

## Evidence and exceptions

Record baseline, commands, observed failures/passes, inspected outputs and remaining gaps. Distinguish original-defect failures from setup failures. If repair removal is unsafe or inseparable, do not force it: state that regression evidence is weaker and use the best available independent check. Unavailable runtime checks remain unverified; structural checks establish structure only. Do not invent a failing run or claim broader coverage than the artifacts support.
