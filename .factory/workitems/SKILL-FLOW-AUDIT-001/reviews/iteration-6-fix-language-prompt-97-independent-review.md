# Iteration 6 Fix Language Prompt 97 Independent Review

reviewer_type: same_thread_independent_reviewer
reviewer_id: codex-gpt5-independent-reviewer-2026-07-07
reviewer_independence_evidence: 未参与 `iteration-6-fix-language-prompt-97` implementation；本轮只读取任务文件、输入报告、实际 diff 和必要验证输出；未修改源码、测试、ledger 或 memory；唯一写入文件是本 review。

status: changes_requested
next_gate: fix_review_feedback

## Score

评分口径：沿用 iteration-6 中文语言评审和 Prompt 工程评审的全量 36 个 `skills/*/SKILL.md` 平均分口径；未修改 skill 沿用 iteration-6 独立评分，已修改 skill 重新按实际文本复评。

- 中文语言平均分：93.8 / 100。
- Prompt 工程平均分：94.2 / 100。
- Critical：0。
- Important：2。
- Minor：2。

结论：两个平均分均低于 97，且仍有 Important，因此必须 `changes_requested`。

## Findings

### Critical

无。

### Important

1. 全量 36 skill 平均分未达到 97。
   本轮只修 8 个目标 skill。按 iteration-6 基线分数计算，即使这 8 个目标 skill 全部打到 100，中文平均分最高约 95.1，Prompt 平均分最高约 95.3，仍低于 97。作者自评分 97.1 / 97.2 没有说明改用不同评分集合，不能作为独立复评通过依据。

2. 完整 workflow pytest 当前失败。
   `uv run pytest -p no:cacheprovider ...` 覆盖 flow report 中的完整 workflow 测试列表时，结果为 exit code 1，`122 passed, 1 failed`。失败点是 `tests/test_independent_review_gate.py::test_requesting_code_review_forbids_same_thread_approved`，仍断言 `skills/requesting-code-review/SKILL.md` 包含已被本轮合并删除的短句 `禁止把同线程复核写成 approved`。单文件复现同样 exit code 1。

### Minor

1. `skills/tdd-workflow/SKILL.md` 已删除原报告点名的重复短句，但仍保留两处相近的双 gate 语义：第 32 行和第 73 行。语义未削弱，不阻塞流程，但语言压缩目标没有完全干净。

2. `skills/art-asset-pipeline/SKILL.md` 已用短表压缩 `tmp/` / `approved/` / `manifest.json` 规则，但后续工作流、输出文件、验证要求中仍多次重复同组规则。语义清楚，不阻塞 Required Fix 7，但不支持 97 分语言目标。

## Required Fixes Checklist

1. `agent-harness-construction`：已处理。实际文本补齐 `work_item`、`ledger_event`、`needs_user_input` 例子，并明确 Codex skill 写作归 `skill-creator`。
2. `ai-first-engineering`：已处理。实际文本补齐 `work_item`、`ledger_event`，并把 `blocked` / `needs_user_input` 拆成两个分支。
3. `article-writing`：已处理。实际文本补齐 `work_item`、`ledger_event`、`verification`，补 `needs_user_input`，并明确发布型长文与工作文档边界。
4. `using-shanforge`：已处理。Bug / 验证失败先路由到 `systematic-debugging`，根因确认和修复方案确认后才进入 TDD / 回归，状态词已对齐。
5. `frontend-patterns`：已处理。状态词改为 `ready_for_review | blocked | needs_user_input`，并明确 `design_decision` 只是 `needs` 值。
6. `tdd-workflow`：已处理但有 Minor。原点名重复句已删除；双 gate 语义仍有两处相近表达。
7. `art-asset-pipeline`：已处理但有 Minor。短表已存在，最终包泄漏规则清楚；重复表达仍偏多。
8. `requesting-code-review`：部分处理，阻塞。skill 文本已合并同线程作者自检表达并保留独立性硬门，但现有 `tests/test_independent_review_gate.py` 未同步，完整 workflow 测试失败。

## Verification Commands

- 完整读取 review task：`sed -n '1,260p' .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/iteration-6-fix-language-prompt-97-independent-review-task.md`，exit code 0。
- 读取全部 Inputs：8 个输入文件均读取成功，exit code 0。
- 检查 review input 列出的实际 diff：`git diff -- ...`，exit code 0；未跟踪文件 `skills/art-asset-pipeline/SKILL.md`、`tests/test_task_workflow_semantics.py` 已直接读取。
- `python3 skills/skill-creator/scripts/quick_validate.py skills/<affected-skill>`，8 个受影响 skill 均 exit code 0，输出 `Skill is valid!`。
- Targeted pytest：`uv run pytest -p no:cacheprovider tests/test_skill_flow_process_audit.py tests/test_task_workflow_semantics.py tests/test_bug_fix_root_cause_skill_rules.py tests/test_review_workflow_skills.py tests/test_verification_debugging_workflow_skills.py`，exit code 0，30 passed。
- Targeted ruff：`uv run ruff check --no-cache tests/test_skill_flow_process_audit.py tests/test_task_workflow_semantics.py tests/test_bug_fix_root_cause_skill_rules.py tests/test_review_workflow_skills.py tests/test_verification_debugging_workflow_skills.py`，exit code 0，All checks passed。
- Full workflow pytest list from flow report：exit code 1，123 collected，122 passed，1 failed。
- Isolated failing pytest：`uv run pytest -p no:cacheprovider tests/test_independent_review_gate.py`，exit code 1，4 passed，1 failed。
- Full workflow ruff list from flow report：exit code 0，All checks passed。
- `git diff --check`，exit code 0，无输出。
- Work item ledger JSONL parse：exit code 0，`.factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl: 94 JSONL records parsed`。
- Review ledger JSONL parse：exit code 0，`.factory/memory/review-ledger.jsonl: 81 JSONL records parsed`。
- 旧中心 gate / 旧远端脚本扫描：`rg -n 'factory-dispatch loop-gate|factory-workitem-loop-gate|scripts/factory-workitem-loop-gate|factory-pr-remote-open|factory-pr-remote-merge|REQUIRED NEXT SKILL|finishing-a-development-branch|docs/superpowers' skills .factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-s1-s6-dry-run-transcript.md`，exit code 1，无输出，表示未命中。
- 评分复算脚本：exit code 0；复算结果中文 93.83，Prompt 94.19；仅把 8 个目标 skill 设为 100 的理论上限为中文 95.11，Prompt 95.25。

## Residual Risks

- 当前工作区有大量既有 dirty / untracked 文件，包含 memory、ledger、skill、tests 和 workitem 文件；本 review 未回滚或清理。该风险不改变本轮结论，但提交前必须重新限定范围。
- 如果项目 owner 想改用“只评 8 个修复文件”的平均分口径，需要重写 gate 说明；当前任务和两份 iteration-6 评审报告都使用全量 36 skill 平均分，因此 97-point acceptance 被阻塞。
- Targeted tests 通过不能替代完整 workflow suite；当前已有单测失败，不能进入人工确认门。

## Recommendation

changes_requested。下一 gate 应为 `fix_review_feedback`，不是 `pending_human_confirmation`。
