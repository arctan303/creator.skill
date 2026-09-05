# CLI 适配差异

## 环境检测

判断当前 CLI 类型的方式（按优先级）：

1. **技能自身安装位置**：gateway `SKILL.md` 位于 `~/.codex/skills/creator/` → Codex；位于 `~/.claude/skills/creator/` → Claude Code。
2. **目录存在性回退**：存在 `~/.codex/` 目录 → Codex；存在 `~/.claude/` 目录 → Claude Code。
3. **仍无法判断时**才询问用户。

## 目录映射

| 内容 | Codex | Claude Code |
|------|-------|-------------|
| 系统指令文件 | AGENTS.md | CLAUDE.md |
| 项目 Skill 目录 | .agents/skills/ | .claude/skills/ |
| 配置目录 | .codex/ | .claude/ |
| 信号文件 | .codex/evolution/signals.md | .claude/evolution/signals.md |
| 界面配置 | agents/openai.yaml | 不适用 |
| 快捷命令 | openai.yaml default_prompt | .claude/commands/*.md |
| Prompt 回归资产 | `.creator/tests/`、`.creator/scripts/` | `.creator/tests/`、`.creator/scripts/` |

## 释放包映射

| CLI | 下载文件 |
|-----|---------|
| Codex | creator.codex.zip |
| Claude Code | creator.claude.zip |

## 冲突检测清单

### 两个平台共同检查

- `.creator/` 目录
- `.creator/tests/prompt-cases/cases.json`（按 case `id` 合并；已证实未定制的官方条目正常升级，无法判定的本地冲突才询问）
- `.creator/scripts/evaluate_prompt_cases.py`（版本化文件，已有升级授权时正常替换，保护未解决的本地定制）
- `.creator/docs-state.json`（运行时迁移状态，保留，不从包覆盖）
- `.creator/references/` 与 `.creator/scripts/check_docs.py`（版本化指南和只读检查器）

### Codex

- AGENTS.md
- EVOLUTION.md
- .version
- .creator-manifest.json
- .agents/skills/ 目录
- .codex/evolution/signals.md（已有台账只保留，不覆盖）

### Claude Code

- CLAUDE.md
- EVOLUTION.md
- .version
- .creator-manifest.json
- .claude/skills/ 目录
- .claude/commands/ 目录
- .claude/evolution/signals.md（已有台账只保留，不覆盖）

## 安装后验证

- `.creator/tests/prompt-cases/cases.json` 存在且 JSON 可解析。
- `.creator/scripts/evaluate_prompt_cases.py` 存在。
- 从工作空间根目录执行 `python .creator/scripts/evaluate_prompt_cases.py` 成功。
- 更新后确认项目自进化新增的 case `id` 仍存在。
- manifest 的 docs_schema_version 只声明包支持的协议，不能代替项目迁移状态。
- 已授权 docs 迁移时按手册完成后运行 `python .creator/scripts/check_docs.py --root . --require-complete`，另外核对语义、旧条款失效及历史完整性。只安装工作流则可只读盘点，不写 complete。

## AGENTS.md 到 CLAUDE.md 转换规则

仅做以下文本替换，不改动业务逻辑：

| 查找 | 替换为 |
|------|--------|
| `AGENTS.md` | `CLAUDE.md` |
| `Codex` | `Claude Code`（仅 CLI 名称引用处） |
| `.codex/` | `.claude/` |
| `.agents/skills/` | `.claude/skills/` |
