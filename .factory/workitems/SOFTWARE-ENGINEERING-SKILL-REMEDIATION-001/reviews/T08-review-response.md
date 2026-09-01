# T08 评审反馈处理

## 核实结果

| Finding | 决策 | 核实证据 | 修复动作 |
|---|---|---|---|
| I-01 TaskCard 跳过语义仍使用 approved/done | 接受 | `subagent-driven-development/SKILL.md` 默认流程确有旧条款，与 T02 生命周期冲突 | 改为只跳过 completed/closed，按项目语义保留 superseded；review_status approved 不跳过；补测试 |
| I-02 Stratix CLI 引用绕过版本矩阵 | 接受 | 主 Skill 路由到该引用；引用仍含 latest dist-tags 与未固定创建命令 | 删除 latest 选择路径；创建前验证显式/已安装版本，不匹配 blocked；补测试 |
| I-03 T08 行为证据不可充分复核 | 接受 | 当前证据只有摘要，未保存 v6 原始输入/输出和 validator 完整命令 | 新增黑盒 evidence；补 validator 精确命令、回执与逐项断言 |

三项均在原整改目标和授权范围内，不需要新的用户决策或权限。

## I-03 整改结果

- 新增 `evidence/T08-black-box-v6.md`：完整输入、实际输出、代理回执和 9 项断言。
- `evidence/T08-verification.md` 已补 Skill validator 的绝对脚本路径、精确命令、38 个通过项和 exit code。
- 状态：`closed`；原独立 reviewer 复审通过。

## I-01 整改结果

- 修改 `skills/subagent-driven-development/SKILL.md` 的“默认流程”：只在 TaskCard 生命周期为 `completed/closed` 时跳过；`review_status=approved` 不代表实现完成。
- 修改 `tests/test_execution_workflow_skills.py`：增加 approved 评审不能跳过 active/ready_for_review TaskCard 的回归合同。
- 状态：`closed`；原独立 reviewer 复审通过。

## I-02 整改结果

- 修改 `skills/stratix-service/references/cli-workflow.md` 的版本预检与创建步骤：删除 `npm view`、`dist-tags` 和 latest 选择；未知或不兼容的本地版本直接 blocked。
- 修改 `tests/test_stratix_service_skill.py`、`tests/test_stratix_service_framework_guide.py`：锁定本地版本矩阵门和失败关闭行为。
- 状态：`closed`；原独立 reviewer 复审通过。

## 整改定向验证

- `uv run pytest -q tests/test_execution_workflow_skills.py tests/test_review_workflow_skills.py tests/test_stratix_service_skill.py tests/test_stratix_service_framework_guide.py`：41 passed，exit 0。
- 对上述测试执行 Ruff：passed，exit 0。
- 对两处 Skill 及对应测试执行 `git diff --check`：passed，exit 0。
- 两名 source/test worker 均回报 `code_shape_check: passed`。

## 整改后集中验证

- `uv run pytest -q`：322 passed、4 subtests passed，exit 0。
- `uv run ruff check skills tests`：passed，exit 0。
- 38 个 Skill validator：38/38 passed，exit 0。
- `git diff --check`：passed，exit 0。
- 三项 Finding 状态：均为 `closed`；复审 `approved / C0-I0-M0`。
