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
2. **范围对账**（切分 Phase 前必做）：扫描 Product Spec 与既有计划中与本次范围相关的非目标、延期或“先不管”声明，逐条三分——
   - 仍成立 → 保持；
   - 被本次承接 → 修订并标记“由 Phase N 承接，本声明作废”，把“更新 Spec 受影响章节”排进该 Phase 任务；
   - 承接但无变更记录 → 暂停，返回 `product-spec-builder` 记录变更，不直接追加。
3. 按可运行、可演示、可审查的能力切分 Phase；**索引与明细分离**。
4. 每个 Phase 映射 `REQ-*`、`AC-*` 或产品变更 ID。
5. 索引 `docs/DEV-PLAN.md` 维护状态总览与 Phase 清单；明细写入 `docs/dev-plan/phase-NN.md`，写明预期文件/产物、依赖、验证命令和交付证据。
6. 标记 R2 审查要求；产品变更只更新受影响范围，不改写已完成 Phase 的实现细节。

## Output

- `docs/DEV-PLAN.md` 索引：状态总览、规则边界、当前 Phase、每行 = `能力 + 状态 + REQ-AC 映射 + 验证命令 + 明细链接 + 完成证据摘要`。
- `docs/dev-plan/phase-NN.md` 明细：目标 / 范围与非范围 / 依赖 / 任务与预期文件 / REQ-AC 映射 / 验证命令与证据 / 审查要求 + 完成证据追加区。
- 范围对账结果：被承接 / 作废 / 保留的声明清单及对应 Phase。
- 0→1 的完整 Phase，或产品变更的增量 Phase；依赖、非目标和审查门禁。

## Stop or escalate

- 当前任务实际属于维护路线：转交维护执行，不生成产品 Phase。
- Product Spec 或变更记录不可验收：返回 `product-spec-builder`。
- 承接既有非目标/延期声明但无变更记录：返回 `product-spec-builder`，不直接追加 Phase。
- 依赖、影响范围或用户决策不清：停止并指出最小阻塞。
- Phase 无法独立运行、验证或审查：重新切分后再输出。

## References

执行前读取 [stage-contract.md](references/stage-contract.md)。
