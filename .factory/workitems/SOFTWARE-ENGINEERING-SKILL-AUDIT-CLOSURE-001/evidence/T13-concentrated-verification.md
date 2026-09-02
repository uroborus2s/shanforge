# T13 集中质量门证据

时间：`2026-09-02T10:43:04+08:00`

## 回归修复

- 首次全量测试：`342 passed, 4 failed, 4 subtests passed`。
- 失败原因：3 个测试文件中的 4 条旧断言仍要求 `using-shanforge` 重复保存共享响应合同字段，或要求 receiving review 无条件写入 response；与 T12 已批准的单一 owner 和授权写入合同冲突。
- 精确修改：`tests/test_skill_flow_process_audit.py`、`tests/test_skill_progress_visibility_and_continuation.py`、`tests/test_work_skill_status_envelope_ownership.py`。
- 修复后定向验证：`29 passed, 0 failed`；Ruff、代码形状、`git diff --check` 通过。

## 完整质量门

| 检查 | 结果 |
|---|---|
| `uv run pytest -q` | `346 passed, 4 subtests passed, 0 failed` |
| `uv run ruff check skills tests` | passed |
| 38 个 Skill `quick_validate.py` | `38/38 passed` |
| 黑盒流程与人类可读响应合同 | `18 passed, 0 failed` |
| 45 项追踪 | `45/45` 唯一；`Important=27`、`Minor=18` |
| 当前闭环状态 | `verified_fixed=44`、`rejected_with_reason=1`、其他状态 `0` |
| ledger JSON 与唯一键 | JSONL 合法；event ID、idempotency key 唯一 |
| `git diff --check` | passed |

## 代码形状

- 对本轮所有新增或修改 Python 文件运行 `skills/tdd-workflow/scripts/check_code_shape.py`，退出码 `0`，没有命名局部函数，因此没有函数套函数。
- 检查器列出的 15 个单调用候选均已存在于整改前基线；`git diff -U0 -- '*.py'` 只新增 4 个测试方法，没有新增单调用公共 helper。
- 本轮新建的四个校验脚本只保留 `main()` 入口，没有拆出单调用公共函数。

## 实际派发回执

- T10、T11、T12 的 `source_or_test_write` 均由 Terra/medium worker 实际执行；派发身份、范围和回执记录在 ledger `E008`–`E025`。
- T13-R01 实际派发：`/root/t13_regression_assertion_fix`，`gpt-5.6-terra`、`medium`、`fork_turns=none`；父工具回执为 `accepted`，见 ledger `E029`，完成与父级独立验证见 `E030`。
- worker 的 `DONE` 只触发父级验证，没有直接关闭 T13。

结论：集中质量门通过，可以进入五位独立专家的 38/38 复评。`SD-M01` 的拒绝理由仍须由相关独立 reviewer 接受或重新打开。
