# MODEL-ROUTING-001-T02 验证证据

- 时间：2026-08-23T10:58:52+08:00
- 候选：Sol 控制、Terra/Luna 受控执行合同

## Red / Green

| 阶段 | 命令 | Exit code | 结果 |
|---|---|---:|---|
| Red | `UV_CACHE_DIR=/tmp/shanforge-model-routing-uv-cache uv run pytest -q tests/test_model_tier_routing.py` | 1 | `4 failed`；四类缺失合同均被捕获 |
| Green | 同上 | 0 | 初始合同 `4 passed`；评审补强后 `5 passed` |
| 相邻回归 | `UV_CACHE_DIR=/tmp/shanforge-model-routing-uv-cache uv run pytest -q tests/test_model_tier_routing.py tests/test_task_workflow_semantics.py tests/test_execution_workflow_skills.py` | 0 | 初始 `21 passed`；评审补强后 `22 passed` |
| Ruff | `UV_CACHE_DIR=/tmp/shanforge-model-routing-uv-cache uv run ruff check tests/test_model_tier_routing.py` | 0 | `All checks passed!` |
| Diff | `git diff --check` | 0 | 无输出 |

## 已证明边界

- Sol 是唯一总体设计、复杂度/风险分级和执行模型路由 owner。
- 仅 `simple + low` 授权 Luna；其他已授权任务交给 Terra。
- Terra/Luna 不重新分级；范围、输入、风险、连续验证失败或人工 Gate 交还 Sol。
- 当前交付是 skill-first 声明式合同，不包含模型服务、公开 API 假设或宿主配置变更。

## Review 补强

- 独立评审以 mutation probe 证明初始关键词测试不能拒绝矛盾 Luna 路由、未授权派发或升级后继续执行。
- 新增表格驱动语义合同后，决策表测试 Red `1 failed`、Green `1 passed`；五类升级信号逐项要求
  `stop_and_return_to_sol`，授权兜底为 `do_not_dispatch`。
