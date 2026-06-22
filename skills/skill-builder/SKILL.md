---
name: skill-builder
description: 为这套产品交付系统创建或改进 Skill。适用于需要新增技能、拆分职责、更新中文 SKILL.md、维护 agents/openai.yaml、增加 references，或让 Skill 更符合 AGENTS.md 和 EVOLUTION.md 规则的场景。
---

# 技能构建技能

为这套系统创建和改进 Skill。

## 核心原则

Skill 应该短、准、可触发。不要写成百科或操作手册。

## 工作方式

1. 先读取 `AGENTS.md`，确认系统定位。
2. 判断要创建新 Skill，还是编辑现有 Skill。
3. 定义触发场景、输入、输出、合格标准和红线。
4. 主体规则写在 `SKILL.md`，细节放入 `references/`。
5. 同步 `agents/openai.yaml`。
6. 检查命名、frontmatter 和占位文本残留。

## 红线

- 不扩展旧版 `creator` 作为新系统主线。
- 不写英文主体规则，除非用户明确要求。
- 不复制大量通用 Codex 行为。
- 不创建没有明确触发场景的 Skill。
