# creator.skill

面向当前项目空间的多 Skill 产品交付系统。

这套系统不是全局安装的 Skill 集合，而是仓库级配置：Codex 在本仓库启动时读取根目录 `AGENTS.md`，并从 `.agents/skills/` 发现项目级 Skill。

## 当前主线

默认文档流：

```text
Product-Spec.md
  -> Design-Brief.md
  -> design artifacts / prototype notes
  -> DEV-PLAN.md
  -> implementation evidence
  -> release evidence
```

主线 Skill：

- `product-spec-builder`：需求技能，产出 `Product-Spec.md`
- `design-brief-builder`：设计规范技能，产出 `Design-Brief.md`
- `design-maker`：设计图技能，可选
- `dev-planner`：计划技能，产出 `DEV-PLAN.md`
- `dev-builder`：开发技能，按计划开发并通过干净子代理审查
- `release-builder`：发布技能，做隐私审计、打包发布准备和证据整理

Plus Skill：

- `bug-fixer`：按证据定位并修复缺陷
- `reviewer`：作为干净子代理审查交付结果
- `goal-writer`：生成可交给 Agent 自主执行的 Goal
- `self-evolver`：把真实使用信号转成 Skill 补丁建议
- `skill-builder`：创建或改进这套系统中的 Skill

## 关键文件

```text
creator.skill/
├── AGENTS.md
├── EVOLUTION.md
├── README.md
├── docs/
│   ├── project-context.md
│   └── system-operation.md
├── .codex/
│   └── evolution/
│       └── signals.md
├── .agents/
│   └── skills/
│       ├── product-spec-builder/
│       ├── design-brief-builder/
│       ├── design-maker/
│       ├── dev-planner/
│       ├── dev-builder/
│       ├── release-builder/
│       ├── bug-fixer/
│       ├── reviewer/
│       ├── goal-writer/
│       ├── self-evolver/
│       └── skill-builder/
└── archive/
    ├── legacy-skills/
    │   └── creator/
    └── video-reference/
```

## 使用方式

在本仓库或其子目录中新开 Codex 话题即可。

Codex 应读取：

- `AGENTS.md`：系统总协议
- `.agents/skills/*/SKILL.md`：当前项目级 Skill

这些 Skill 不需要复制到 `~/.codex/skills`。

## 归档内容

`archive/` 存放不属于当前主线的材料：

- `archive/legacy-skills/creator/`：旧版单 Skill 流程，仅作历史参考
- `archive/video-reference/`：视频截图、转写、音频和本地转写模型

其中 `.wav` 和 `.bin` 文件为本地生成或下载的大文件，已通过 `.gitignore` 排除。

