---
name: dev-planner
description: 将已确认的 Product Spec 和设计约束拆成可运行、可验证的开发计划。用于 0→1 产品生成完整 DEV-PLAN，或产品变更维护增量 Phase；不用于普通 Bug、内部重构、文档和其他维护任务。
---

# 开发计划技能 (dev-planner)

## Purpose

把已确认的产品契约拆成另一个开发者可直接执行、验证和审查的 Phase 计划。

## Trigger

- 0→1 产品已有可验收 Product Spec，需要完整开发计划。
- 产品变更已有变更记录，需要增量 Phase。
- 当前工作不是普通 Bug、内部重构、文档或其他维护任务。

## Required context

- 可验收的 `Product-Spec.md` 和相关变更 ID。
- `Design-Brief.md` 或设计产物（如果相关）。
- 现有仓库、脚本、测试、CI、技术栈和平台事实。
- 依赖、非目标、迁移与发布约束。

## Workflow

1. 扫描仓库事实，拒绝凭空假设技术栈或文件结构。
2. 按可运行、可演示、可审查的能力切分 Phase。
3. 每个 Phase 映射 `REQ-*`、`AC-*` 或产品变更 ID。
4. 为任务写明预期文件/产物、依赖、验证命令和交付证据。
5. 标记 R2 审查要求；产品变更只更新受影响范围，不改写仍有效的已完成工作。

## Output

- `docs/DEV-PLAN.md` 或项目约定的等价文件。
- 0→1 的完整 Phase，或产品变更的增量 Phase。
- 需求映射、验证证据、依赖、非目标和审查门禁。

## Stop or escalate

- 当前任务实际属于维护路线：转交维护执行，不生成产品 Phase。
- Product Spec 或变更记录不可验收：返回 `product-spec-builder`。
- 依赖、影响范围或用户决策不清：停止并指出最小阻塞。
- Phase 无法独立运行、验证或审查：重新切分后再输出。

## References

执行前读取 [stage-contract.md](references/stage-contract.md)。
