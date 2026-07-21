# TASK-SKILL-004-P001 验证证据

## 当前结论

- 本任务范围已独立复审批准并完成最终验证与 memory sync；实现者未自批 `approved`。
- 精确 32 个工作 Skill 的重复四字段和重复尾块已移除，完整专业正文 SHA-256 保持不变。
- black-box：`10/10`；33 个相关 Skill validator 全部 valid。
- 全仓 pytest：最终 `1143 passed / 3 failed`；失败是范围外 R002 候选冻结计数 `expected 299, got 323`。
- 全仓 Ruff/format 仍有既有债务，目标测试文件自身 Ruff/format 通过。

## TDD

RED：

```text
uv run pytest tests/test_remaining_skill_project_status_contract.py tests/test_work_skill_status_envelope_ownership.py -q
=> 5 failed, 3 passed
```

五个失败分别命中四字段残留、共享链接缺失、共享合同缺失和总控未分层。

GREEN：

```text
uv run pytest tests/test_remaining_skill_project_status_contract.py tests/test_work_skill_status_envelope_ownership.py -q
=> 8 passed
```

## 定向与相邻回归

```text
uv run pytest tests/test_*skill*.py tests/test_independent_review_gate.py tests/test_pr_commit_workflow_rules.py tests/test_bug_fix_root_cause_skill_rules.py tests/test_task_workflow_semantics.py tests/test_verification_debugging_workflow_skills.py -q
=> 首次 2 failed / 138 passed；恢复既有兼容锚点后 140 passed

uv run pytest tests/test_skill_progress_visibility_and_continuation.py tests/test_task_workflow_semantics.py tests/test_black_box_workflow_eval.py tests/test_independent_review_gate.py -q
=> 30 passed
```

首次相邻失败只指出 `using-shanforge` 的既有精确短语被改写；恢复“工作 skill 完成时只返回状态包，不写下一步 skill”后全部通过，未扩大行为。

## 黑盒与 Skill 校验

- fresh-context 黑盒：`10/10`，见 `TASK-SKILL-004-P001-black-box-transcript.md`。
- `using-shanforge` 加精确 32 个工作 Skill：33/33 `Skill is valid!`。

## 静态与全仓门禁

```text
uv run ruff check tests/test_remaining_skill_project_status_contract.py tests/test_work_skill_status_envelope_ownership.py
=> All checks passed!

uv run ruff format --check tests/test_remaining_skill_project_status_contract.py tests/test_work_skill_status_envelope_ownership.py
=> 2 files already formatted

uv run mypy src
=> Success: no issues found in 253 source files

git diff --check
=> exit 0
```

全仓 Ruff：exit 1，`552 errors`，集中在既有 `docx/xlsx/pdf` 脚本和并行草稿；本任务新增测试已从 553 降至范围外 552。全仓 format：exit 1，`56 files would be reformatted / 332 already formatted`，目标测试不在待格式化清单。

全仓 pytest：初次 exit 1，`1135 passed / 3 failed`；最终新鲜运行为 `1143 passed / 3 failed`。三项均来自 `tests/test_implementation_candidate_r002.py` 调用旧候选构建器，错误为 `product Python count drift: expected 299, got 323`；本任务未修改 `src/`、R002 builder、manifest 或候选资产。

## 未运行

- 产品 UI / 浏览器 E2E：无产品界面或运行时改动。
- remote / release / deployment：未授权。
- 本地 commit：在独立实现 review、最终验证和 memory sync 后按 `gitcommitzh` 尝试，仅提交可安全分离的当前任务范围。

## Review finding I-001 整改

- 技术核实：三个模板的固定 `needs` 与 `api-design`、`systematic-debugging`、`writing-plans` 等本地枚举冲突，finding 成立。
- finding RED：`1 failed / 4 deselected`。
- finding GREEN：`1 passed / 4 deselected`。
- 当前 owner 目标测试：`9 passed`。
- Skill 相邻：`141 passed`；流程/Gate 相邻：`30 passed`。
- 目标 Ruff/format、`using-shanforge` validator、`git diff --check`：通过。
- 详细记录：`TASK-SKILL-004-P001-review-fix-verification.md`。

同一独立 reviewer 复审：`approved / 100 / C0 I0 M0`；`I-001` closed，无新 finding；reviewer 新鲜 owner 测试 `5 passed`。

## 最终新鲜验证

- owner：`9 passed`。
- Skill 相邻：`141 passed`。
- 流程/Gate 相邻：`30 passed`。
- 目标 Ruff/format、JSONL、`git diff --check`：通过。
- mypy：`0 issues / 253 source files`。
- 全仓 pytest：`1143 passed / 3 failed`；三项仍为范围外 R002 `expected 299, got 323`。
- memory sync：review ledger、skill updates、tasks、tests summary 已更新。

## Git 提交门

- `git diff --cached --name-only`：空，未存在其他任务暂存内容。
- `docs/05-design/workflow-execution-design.md`、`tests/test_remaining_skill_project_status_contract.py`、`skills/art-asset-pipeline/SKILL.md`、`skills/go-backend-developer/SKILL.md`：均为整文件未追踪，包含上游任务内容，不能只暂存本任务 hunk。
- `skills/agent-harness-construction/SKILL.md`、`skills/using-shanforge/SKILL.md` 等已跟踪文件的工作区 diff 同时包含第一批或其他任务改动。
- `gitcommitzh` 结论：`blocked_unseparable_dirty_scope`；未执行 `git add` 或 `git commit`，避免混入范围外改动。
