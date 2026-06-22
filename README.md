# creator.skill

> 通过讨论、项目调查和持续文档维护，把软件创意发展为可实施、可交接、可验收的设计。

`creator` 是一个面向软件项目规划的 Agent Skill。它不会在用户刚提出想法时立即开始编码，而是帮助用户理解目标、检查现有项目、评审关键取舍，并在用户明确要求后建立设计与实施文档。

设计完成后，Skill 默认停止在交付状态。实施开始后，进度文档为不同工作者提供连续上下文；项目完成后，再依据已确认的设计和真实产物进行验收。

## 核心能力

- 通过渐进式提问帮助用户收敛软件创意
- 调查现有仓库中的少量高价值材料
- 评审可行性、安全性、复杂度、维护成本和部署方式
- 区分项目事实、用户约束、临时假设和待确认问题
- 生成并维护项目背景、设计和实施进度文档
- 使用 `REQ`、`TASK`、`AC` 编号追踪需求、任务和验收标准
- 管理已确认设计的版本与后续变更
- 检查配置管理、工程完整性和可重复部署能力
- 按设计基线和实际证据验收实施成果

## 工作流

```text
探索想法
   ↓
调查现有项目
   ↓
建设性评审与共同决策
   ↓
确认首版范围和完成标准
   ↓
用户明确要求成文
   ↓
建立并确认设计基线
   ↓
实施者更新进度与交接记录
   ↓
依据设计和真实产物验收
```

Skill 不会机械执行完整流程。简单项目保持轻量，复杂项目才展开完整设计。

## 项目文档

进入正式设计阶段后，可在项目仓库的现有文档目录中维护以下文件：

| 文档 | 作用 | 创建时机 |
| --- | --- | --- |
| `project-context.md` | 保存项目背景、事实、约束和高密度项目地图 | 背景稳定且准备正式成文时 |
| `design.md` | 保存范围、需求、方案、任务、验收标准和设计版本 | 用户明确要求设计文档时 |
| `implementation-progress.md` | 保存实施进度、验证结果、设计偏离和交接信息 | 实施真正开始时 |

小型项目可以将背景合并进 `design.md`。Skill 不会在讨论初期创建空文档，也不允许实施进度记录静默改写已确认设计。

## 工程完整性

设计与验收会关注项目能否从仓库和受控秘密中可靠重建：

- 区分稳定常量、环境配置和秘密
- 集中管理接口地址、域名、资源标识和环境差异
- 不以普通开发环境判断绕过鉴权、人机验证或限流
- 使用目标平台支持的标准配置文件与部署流程
- 将安全的声明式配置保存在仓库中
- 通过 Secret Store 或 CI 注入密钥
- 减少后台手工录入和无法追踪的部署状态
- 避免没有真实场景的判断、兼容分支和长期临时代码

## 适用范围

适用于：

- 网站和 Web 应用
- API 与后端服务
- CLI、脚本和开发工具
- Docker 与 Compose 项目
- 编译型项目
- 现有代码仓库的重要功能或架构改造

不适用于：

- 普通技术问答
- 已经明确的小型修复
- 用户只要求立即实现且不需要设计讨论的任务
- Office 文件或其他非软件创作

## 安装

### 克隆仓库

```bash
git clone https://github.com/arctan303/creator.skill.git
```

将 [`skills/creator`](skills/creator) 复制或链接到 Agent 平台的 skills 目录。

常见安装位置：

```text
~/.codex/skills/creator/
```

安装后的目录中应直接包含 `SKILL.md`、`agents/` 和 `references/`。

## 使用示例

显式调用：

```text
使用 $creator 和我讨论一个部署在 Cloudflare Workers 上的工具网站。
先了解现有仓库和我的目标，不要立即写代码，也不要在我确认前生成设计文档。
```

继续进入设计：

```text
核心方向已经确定，请把讨论结果整理成正式设计文档。
```

实施后验收：

```text
项目已经实现完成。请读取已确认设计和实施进度，检查实际代码并进行验收。
```

## 仓库结构

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
└── skills/
    ├── product-spec-builder/
    ├── design-brief-builder/
    ├── design-maker/
    ├── dev-planner/
    ├── dev-builder/
    ├── release-builder/
    ├── bug-fixer/
    ├── reviewer/
    ├── goal-writer/
    ├── self-evolver/
    ├── skill-builder/
    └── creator/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        └── references/
            ├── acceptance.md
            ├── design-document.md
            ├── engineering-integrity.md
            ├── project-discovery.md
            └── project-documents.md
```

## 设计原则

- 讨论先于文档，文档先于实施
- 问题服务于决策，不制造新的困惑
- 只读取与当前设计相关的项目材料
- 解释取舍，让用户参与关键决定
- 文档保持精炼，但必须足以交接和验收
- 用户确认的设计才是验收基线
- 实际证据优先于“已经完成”的声明

## 状态

当前为首个公开版本。工作流和文档结构会根据真实项目使用情况继续调整。

## 5.0 多 Skill 架构草案

本仓库正在从单一 `creator` skill 演进为文档驱动的多 Skill 系统。项目背景和设计依据记录在 [`docs/project-context.md`](docs/project-context.md)，系统运行协议记录在 [`docs/system-operation.md`](docs/system-operation.md)。

第一层已搭建 6 个主线 Skill 骨架：

- `product-spec-builder`：把模糊想法整理为可开发的 `Product-Spec.md`
- `design-brief-builder`：把主观设计感觉转成具体 `Design-Brief.md`
- `design-maker`：可选地生成设计方案和原型图
- `dev-planner`：把需求拆成可运行、可验收的 `DEV-PLAN.md`
- `dev-builder`：按计划开发，并通过独立审查闭环
- `release-builder`：执行隐私审计和打包发布准备

同时已搭建 5 个 Plus Skill 骨架：

- `bug-fixer`：按证据定位并修复缺陷
- `reviewer`：作为干净子代理审查交付结果
- `goal-writer`：生成可交给 Agent 自主执行的 Goal
- `self-evolver`：把真实使用信号转成 Skill 补丁建议
- `skill-builder`：创建或改进这套系统中的 Skill

现有 `creator` skill 是旧版单 Skill 流程，暂时保留作为历史参考；新系统不围绕它继续扩展。
