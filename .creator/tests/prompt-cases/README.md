# Prompt 行为用例

`cases.json` 是 creator.skill 的稳定行为契约，覆盖路由、追问、审查收敛、中断恢复、自进化和发布权限。

运行静态契约与用例结构检查：

```powershell
python .creator/scripts/evaluate_prompt_cases.py
```

对 Agent 输出做行为评分时，传入 JSON：

```powershell
python .creator/scripts/evaluate_prompt_cases.py --responses path/to/responses.json
```

响应文件格式：

```json
{
  "responses": [
    {
      "case_id": "route-maintenance-docs",
      "route": "维护执行",
      "risk": "R0",
      "primary_skill": "dev-builder",
      "question_count": 0,
      "escalation": false,
      "status": "continue",
      "new_reviewers": 0
    }
  ]
}
```

评测响应应来自 fresh Agent，只提供该用例的原始输入和当前发布包，不提供期望答案。没有响应文件时，脚本只验证用例集、Prompt 结构和界面元数据，不声称完成模型行为评测。

响应评分默认要求覆盖全部用例，适合回归门禁。只做探索性抽样时必须显式使用：

```powershell
python .creator/scripts/evaluate_prompt_cases.py --responses path/to/responses.json --allow-partial
```

字段约定：`escalation` 只表示是否需要把当前路线或风险向上升级；等待用户授权、记录观察或把无限 Goal 改写成有界 Goal 不算升级。`status=needs-input` 表示必须等用户回答才能继续，`status=interrupted` 表示外部容量或宿主条件中断但检查点可恢复。
