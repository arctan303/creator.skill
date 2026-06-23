# CLI 适配差异

## 环境检测

判断当前 CLI 类型的方式：

- 存在 ~/.codex/ 目录 → Codex
- 存在 ~/.claude/ 目录 → Claude Code
- 都存在时询问用户

## 目录映射

| 内容 | Codex | Claude Code |
|------|-------|-------------|
| 系统指令文件 | AGENTS.md | CLAUDE.md |
| 项目 Skill 目录 | .agents/skills/ | .claude/skills/ |
| 配置目录 | .codex/ | .claude/ |
| 信号文件 | .codex/evolution/signals.md | .claude/evolution/signals.md |
| 界面配置 | agents/openai.yaml | 不适用 |
| 快捷命令 | openai.yaml default_prompt | .claude/commands/*.md |

## 释放包映射

| CLI | 下载文件 |
|-----|---------|
| Codex | creator.codex.zip |
| Claude Code | creator.claude.zip |

## 冲突检测清单

### Codex

- AGENTS.md
- EVOLUTION.md
- .agents/skills/ 目录

### Claude Code

- CLAUDE.md
- EVOLUTION.md
- .claude/skills/ 目录
- .claude/commands/ 目录

## AGENTS.md 到 CLAUDE.md 转换规则

仅做以下文本替换，不改动业务逻辑：

| 查找 | 替换为 |
|------|--------|
| `AGENTS.md` | `CLAUDE.md` |
| `Codex` | `Claude Code`（仅 CLI 名称引用处） |
| `.codex/` | `.claude/` |
| `.agents/skills/` | `.claude/skills/` |
