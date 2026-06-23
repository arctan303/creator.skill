# Changelog

记录每次发布的变更内容。

## [1.0.1] - 2026-06-23

### 新增

- 网关 Skill（gateway/）：全局安装的工作流初始化器
- 发布构建脚本（scripts/build_release.py）：自动生成三套释放包
- GitHub Actions 自动发布：VERSION 变更时自动构建并创建 Release
- Claude Code 适配：CLAUDE.md 转换、中文 slash commands、.claude/ 目录结构
- Agent 自助安装指引

### 产物

- `creator.codex.zip` — Codex 工作空间初始化包
- `creator.claude.zip` — Claude Code 工作空间初始化包
- `creator-gateway.zip` — 网关 Skill 安装包
