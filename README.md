# creator.skill

一套极度硬核、可移植的 AI Agent 产品交付工作流。

如果你受够了 AI Agent “上来就盲写代码”、“自嗨式开发”、“自己测自己”、“到处留 TODO 占位符”，那么本系统正是为你准备的。

`creator.skill` 不是为了让 Agent 变得更会写代码，而是通过 **11 个极其严酷的协作技能（Skill）和子代理机制**，强迫 Agent 像一支顶级、冷血且极其遵守纪律的产品研发团队一样工作。

它支持 **OpenAI Codex CLI** 和 **Claude Code**，一键初始化到任意工作空间。

---

## 🔥 系统核心理念 (The Hardcore Philosophy)

本系统由 `AGENTS.md` 协议驱动，所有的 Skill 都内置了不可妥协的底线：

1. **二选一引导，终结废话**：严禁问用户“你要什么风格”这种废话，强制提供具体选项（This-or-That）。
2. **拒绝占位符**：所有的开发计划必须精确到具体文件路径，严禁出现 `TBD` 或 `稍后补充`。
3. **验证即证据 (Verification is Evidence)**：代码写完必须当场运行终端命令（编译/跑通测试），没看到终端 `0 错误` 输出前，绝不允许宣称完成。
4. **绝对隔离的交叉审查**：开发者（`dev-builder`）完成开发后，**必须强制召唤独立的子代理（`reviewer`）** 进行干净视角的代码审查。自己测自己的代码等于没测。
5. **隐私防漏底线**：发布前强制执行命令行扫描。若发现本地文件路径、本地 DB 文件或硬编码 API Key 被打包，发布动作将被立即强行中止！

---

## ⚙️ 核心架构与技能一览

系统的核心工作流为：**需求 → 设计 → 计划 → 开发 → 审查 → 发布**。任何后续阶段不可跳过前置阶段的严格检验。

### 📌 四大核心主线 (Core Pipeline)

| 技能名称 | 角色定位 | 核心能力与门禁 | 产出物 |
|---------|----------|--------------|--------|
| `product-spec-builder` | 铁面产品经理 | 双模启动（0-1或迭代），不集齐 6 大核心维度（定位、流程、AI 赋能等）绝不输出文档。 | `Product-Spec.md` |
| `design-brief-builder` | 高级 UI 规范师 | 废除主观问卷，实行“真实产品锚定”和“感受翻译”，将玄学词汇翻译成具体的视觉参数。 | `Design-Brief.md` |
| `dev-planner` | 冷酷架构师 | 实行洋葱剥皮法拆解任务。无占位符原则，计划必须精确到文件级。技术栈必须经过联网验证兼容性。 | `DEV-PLAN.md` |
| `dev-builder` | 资深全栈开发 | **验证即证据**：强制要求代码本地编译成功；<br>**强制闭环**：代码写完强制派发独立的子代理审查。 | 代码、验证证据 |

### 🛠️ 四大硬核支撑技能 (Peripheral Support)

| 技能名称 | 触发场景 | 核心防御机制 |
|---------|----------|-------------|
| `bug-fixer` | 报错排查、修 Bug | 实行**“四阶段调试法”**（找证据 -> 分析 -> 假设 -> 修复）。内置防死循环机制：同一问题修 3 次失败，强行停机反思。 |
| `release-builder` | 打包、部署、上线 | 内置严苛的**终端隐私扫描流水线**。发布前强制执行真实平台的安装与在线冒烟测试。 |
| `design-maker` | 产出设计稿/线框图 | 强制要求先提取**“全局变量”**和**“可复用组件”**，内置状态完备校验（空状态/加载态必须有）。 |
| `skill-builder` | 扩展系统自身技能 | 强制三层模块化法则，自建技能必须带有强阻断防呆设计。 |

### 🧩 系统引擎与调度

- `gateway`：负责全套 Skill 的下发、安装与跨工作空间初始化。
- `reviewer`：干净视角的**独立审查子代理**，是把控代码质量的最后一道闸门。
- `self-evolver`：从真实的 `feedback` 中提取经验，自动修改技能或沉淀补丁，使系统越用越强。
- `goal-writer`：负责将长线任务翻译为极其明确且带检验指标的执行指令。

---

## 🚀 快速开始

### 1. 全局安装网关 Skill

网关 Skill 是你唯一需要手动获取的东西。安装后，你可以在任何工作空间一键初始化流水线。

**让 Agent 自动安装**（强烈推荐，直接对你的 CLI 说）：
> “帮我从 https://github.com/arctan303/creator.skill 安装 creator skill”

**手动解压安装**：
去 [Releases](https://github.com/arctan303/creator.skill/releases/latest) 下载 `creator-gateway.zip`，然后解压：
- **Codex**: 解压到 `~/.codex/skills/creator/`
- **Claude Code**: 解压到 `~/.claude/skills/creator/` 并删除里面的 `agents/` 文件夹。

安装后请重启你的 CLI 会话。

### 2. 初始化你的项目空间

在任意空项目或已有项目的目录下，对 Agent 说：
> “初始化 creator 工作流”

系统会自动从云端拉取最新的 `creator.claude.zip` 或 `creator.codex.zip`，并在当前目录释放 11 个原子技能和核心协议（`AGENTS.md`）。

### 3. 开始干活

初始化完成后，直接甩出你的需求：
> “我想做一个带 AI 翻译的浏览器插件”

`product-spec-builder` 会立刻接管对话，按极其严格的门禁对你进行灵魂拷问，随后整个研发流水线便会严丝合缝地运转起来。

---

## 📦 多平台适配与发布机制

仓库维护一套源文件，每次推送会自动触发 GitHub Actions 构建，生成两套适配包：

| 特性 | OpenAI Codex | Claude Code |
|------|-------|-------------|
| 系统指令 | `AGENTS.md` | `CLAUDE.md` |
| 技能目录 | `.agents/skills/` | `.claude/skills/` |
| 界面入口 | `agents/openai.yaml` 菜单配置 | `.claude/commands/*.md` 快捷指令 |

- 自动化部署：修改 `VERSION` 文件推送到 `main` 分支，CI 自动输出三大 Release 压缩包。
- 手动本地打包：运行 `python scripts/build_release.py`。

---

## 📄 License
MIT License
