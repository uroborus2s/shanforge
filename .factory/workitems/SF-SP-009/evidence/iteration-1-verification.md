# SF-SP-009 Iteration 1 Verification

## 基本信息

- Work item：`SF-SP-009`
- Actor：`codex`
- 时间：`2026-07-05T17:39:02+08:00`
- 验证声明：黑盒流程 eval 契约、`using-shanforge` 入口和结构测试已完成，可进入独立 review。
- 结论：`passed`

## Red-Green 证据

### Red

```bash
.venv/bin/pytest tests/test_black_box_workflow_eval.py
```

- exit code：`1`
- 失败数量：`4`
- 错误数量：`0`
- 跳过数量：`0`
- 未运行项：无

真实输出摘要：

```text
tests/test_black_box_workflow_eval.py FFFF
FAILED ... FileNotFoundError: ... skills/using-shanforge/references/black-box-flow-eval.md
FAILED ... assert '`SF-SP-009`：当前已进入黑盒流程 eval 开发' in plan
4 failed in 0.06s
```

### Green

```bash
.venv/bin/pytest tests/test_black_box_workflow_eval.py
```

- exit code：`0`
- 失败数量：`0`
- 错误数量：`0`
- 跳过数量：`0`
- 未运行项：无

真实输出摘要：

```text
tests/test_black_box_workflow_eval.py .... [100%]
4 passed in 0.01s
```

## 追加验证命令

```bash
.venv/bin/ruff check tests/test_black_box_workflow_eval.py
```

- exit code：`0`
- 输出摘要：`All checks passed!`

```bash
python3 skills/skill-creator/scripts/quick_validate.py skills/using-shanforge
```

- exit code：`0`
- 输出摘要：`Skill is valid!`

```bash
.venv/bin/pytest tests/test_execution_workflow_skills.py tests/test_review_workflow_skills.py tests/test_verification_debugging_workflow_skills.py tests/test_pr_commit_workflow_rules.py tests/test_black_box_workflow_eval.py
```

- exit code：`0`
- 失败数量：`0`
- 错误数量：`0`
- 跳过数量：`0`
- 输出摘要：`26 passed in 0.03s`

```bash
git diff --check
```

- exit code：`0`
- 输出摘要：无输出。

## 需求核对

- 一句话需求场景：`SF-SP-009-S1` 已在 `black-box-flow-eval.md` 定义。
- Bug 修复场景：`SF-SP-009-S2` 已定义复现、根因和回归验证断言。
- Review 反馈场景：`SF-SP-009-S3` 已定义逐条核实和 unclear 先问。
- 压缩恢复场景：`SF-SP-009-S4` 已定义 ledger 恢复和 idempotency 跳过。
- 完成声明场景：`SF-SP-009-S5` 已定义新鲜验证、review、PR / commit 和 memory sync 证据门。
- 自评隔离场景：`SF-SP-009-S6` 已定义实现者自检不得写成 `approved`。
- 评分断言：已定义 `2 分 / 1 分 / 0 分`、`总分必须 >= 90`、critical assertion 失败门。
- 脚本回退：reference 明确不新增中心脚本 gate，结构测试禁止重引入已废弃 gate 名称。

## 偏离

- 未运行项：真实 LLM 对话评分器、外部模型 eval、仓库全量 pytest。
- 原因：本 work item 交付的是本地黑盒 eval 契约与结构测试；仓库存在大量无关脏改动，全量测试不适合作为当前任务完成门。
- 替代验证：定向测试、邻近 workflow 回归、ruff、skill validator、`git diff --check`。
- 残余风险：需要独立 reviewer 检查场景断言是否足够代表真实黑盒行为。

## 结论

`passed`
