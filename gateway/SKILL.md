---
name: creator
description: 在当前工作空间初始化 creator.skill 产品交付工作流。当用户想要在一个新项目或已有项目中启用 creator.skill 的需求收集、设计规范、开发计划、项目开发等全套技能时触发。支持从 GitHub Release 下载或从用户指定的本地压缩包释放。
---

# 工作流初始化技能

在当前工作空间部署 creator.skill 全套产品交付工作流。

## 核心原则

初始化是释放，不是创造。源文件来自预构建的释放包，不要在初始化过程中生成或修改 Skill 内容。

## 工作方式

1. 确认用户意图：初始化工作流到当前工作空间。
2. 检测当前运行的 CLI 环境（Codex 或 Claude Code）。
3. 确定源文件获取方式：
   - 默认：从 GitHub Release 下载对应的释放包
     - Codex → creator.codex.zip
     - Claude Code → creator.claude.zip
     - Release 地址：https://github.com/arctan303/creator.skill/releases/latest
   - 备选：用户指定本地压缩包路径
4. 检查目标工作空间是否已有冲突文件。
   - Codex 检查：AGENTS.md、EVOLUTION.md、.agents/skills/
   - Claude Code 检查：CLAUDE.md、EVOLUTION.md、.claude/skills/、.claude/commands/
   - 存在冲突时，询问用户处理方式。
5. 解压释放包到当前工作空间根目录。
6. 在工作空间根目录写入 .version 文件，记录当前日期。
7. 验证关键文件已就位：
   - 系统指令文件存在
   - 11 个 Skill 目录各含 SKILL.md
   - .version 文件存在
8. 报告初始化结果。

## 更新已有工作流

如果工作空间已有 .version 文件，展示当前版本日期，提示可用更新，由用户决定是否继续。

## 红线

- 不在初始化过程中修改 Skill 内容。
- 不在用户未确认的情况下覆盖已有文件。
- 不替用户选择 CLI 类型，必须自动检测或询问确认。
- 不跳过验证步骤。

## 参考

初始化时参考 [cli-adapters.md](references/cli-adapters.md) 了解两套 CLI 的目录差异。
