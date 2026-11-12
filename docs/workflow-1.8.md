# 1.8 field feedback and candidates

Status: **open for ordinary-use feedback**, following the 1.7.0 publication on 2026-11-12. The [release evidence](validation/1.7-release.md) records publication and downloaded-asset verification separately; this feedback entry does not certify the downloaded assets. It does not claim model, real-UI, live Claude Code or long-term validation, and it does not establish a 1.8 implementation or release.

The [1.7 feedback record](workflow-1.7.md) is closed and retained as history. New reports use stable `FB18-xxx` IDs, including observations made while using 1.7.0. The first entry is an observed release-reproduction issue, separate from user/model behavior feedback.

## Capture during ordinary use

Describe a problem naturally; no form or separate “remember” request is needed. The assistant investigates technical gaps and records relevant facts here. Ask only when a missing fact or unresolved experience boundary prevents a useful decision. Keep scope local to this workflow repository; project-specific conventions remain in their own projects.

For each actual report, retain a stable ID, date, workflow/host/model baseline when known, expected versus observed behavior, minimal reproduction or evidence, concrete impact and current status. The assistant reads the affected project's `.creator/install-state.json` and records the first 12 characters of `package_sha256`; do not ask the user to look it up. If the receipt cannot be read or the value is unavailable, record it as unknown without guessing. This distinguishes package builds without treating a reported version as proof of identical content.

Distinguish a user report, an independently reproduced defect and an inferred cause. Merge repeated evidence into the same issue rather than renumbering or creating duplicate tasks. Keep private logs/conversations and credentials out of this public record; use a redacted summary or synthetic case.

## 1.7.0 使用观察重点

以下八项沿用 1.7 的试用关注点，供日常使用时自然反馈；它们不是已发现的问题，也不是每项任务必须执行的测试清单。新增报告使用 `FB18-xxx`，由助手记录可读取的包摘要，不要求用户查找。

- 设计读取：UI 任务是否实际读取项目设计入口及适用的逐层引用，日常开发是否只使用本地已采纳规则。
- 设计适配：网关是否能为新项目裁切、为已有规范补缺，并保留项目约定、路径和例外。
- 自主推进：已有既定规则时是否仍做设计采访或要求返回前序阶段；独立部分能否继续。
- 冲突分流：过时测试/文档、回归和已批准变更是否先分类，避免过早转成产品变更。
- 修复证据：是否报告隔离副本中撤回修复后的失败、恢复后的通过，或如实说明不能执行与证据较弱；是否排除只修症状的结果。
- UI 验证：是否复用现有组件/素材，并实际查看对应最终源码、状态和视口的截图；改交互后是否操作验证，且区分模拟、本地、部署环境。
- 计划与恢复：切片是否对应可验收的用户结果；恢复是否核对实际状态，避免重复外部动作、覆盖他人改动或相信旧的“全部通过”。
- 触发与边界：未明确要求时是否擅自建立 Goal；明确授权的优化是否仍等待次数；轻量改动是否被过度验证，结构检查是否冒称行为通过。

## Reports

### FB18-001: cross-platform manifest order affects byte reproduction

- Source/date: post-publication verification on 2026-11-12; [release evidence](validation/1.7-release.md). Release commit `edb39b531264b116d02ac2be7e6edf987bfdbe10`, workflow 1.7.0; installed package prefix `bbae2033a78b` was verified from the synthetic installation receipt. This is a build-tool observation, not a reported agent-behavior failure.
- Expected/observed: rebuilding identical LF Git blobs should reproduce package member bytes. Existing Windows Python 3.12 and the unmodified build script match all 20 gateway members and 67 of 68 workflow members; only manifest key order differs from the published Ubuntu artifact. Manifest values and every declared file digest are identical. Main-session independent checking attributes the order exactly to Windows versus POSIX Path sorting.
- Reproduction: build the release commit from LF-only blobs on Windows and compare ZIP-member hashes with the official assets. Do not use a CRLF worktree, semantic JSON normalization or a reordered diagnostic as proof that the original byte comparison passed.
- Impact: strict cross-platform reproduction reports a difference; package identity still uses the official asset digest. Fresh/repeated installation and real Git CRLF upgrade passed. No runtime-rule or content defect was observed from this ordering difference.
- Status: recorded for 1.8 consideration; no build-script change or asset replacement authorized by this entry. A future bounded fix could use platform-independent path ordering, with a regression check before deciding implementation. Linux independent rebuilding remains unavailable locally; no new environment was installed.

## From evidence to 1.8

Use [EVOLUTION.md](../EVOLUTION.md) to distinguish demonstrated workflow failures from project preferences and transient host/tool failures. Prioritize by concrete impact and recurrence; an explicit optimization request does not need an occurrence threshold. Candidate fixes need a relevant failure scenario, a counterexample and evidence appropriate to the change.

Reports do not themselves authorize implementation, publication, automatic global rule propagation, background telemetry or upgrades to other repositories. Preserve each report's actual source baseline and separate proposed changes from verified results.
