# Iteration 4 Fix Language And Prompt Contracts

## Goal

修复中文语言评审和 prompt 工程评审共同指出的高价值问题。只做最小有效修复，不重写整套 skill。

## Inputs

- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/chinese-language-review-iteration-4.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/prompt-engineering-review-iteration-4.md`

## Allowed Files

- `skills/document-templates/SKILL.md`
- `skills/requesting-code-review/SKILL.md`
- `skills/receiving-code-review/SKILL.md`
- `skills/python-uv-project/SKILL.md`
- `skills/browser-control/SKILL.md`
- `skills/crawler4j-model-project/SKILL.md`
- 直接相关测试文件。

## Required Fixes

1. 给缺口 skill 补最小 `工作结果` 状态包，至少包含 `work_item`、`status`、`outputs`、`evidence`、`ledger_event`、`needs`。
2. 给 `blocked` / `needs_user_input` 缺口补失败语义。
3. 修 `document-templates` 英文 description / D3 口径，补 `work_item` / `ledger_event`。
4. 明确 `python-uv-project` 在 Python bug 场景只提供 uv / 工具链约束，根因流程由 `systematic-debugging` / `tdd-workflow` 接管。
5. 不处理 `gitcommitzh`、`skill-creator`、`stratix-service` 的长入口压缩；这三个属于后续单独清理，避免本轮范围过大。

## Verification

至少运行：

```bash
uv run pytest tests/test_review_workflow_skills.py tests/test_skill_flow_process_audit.py tests/test_bug_fix_root_cause_skill_rules.py tests/test_browser_control_skill.py tests/test_crawler4j_model_skill_integration.py tests/test_sf_sp_010_documentation_navigation.py
uv run ruff check tests/test_review_workflow_skills.py tests/test_skill_flow_process_audit.py tests/test_bug_fix_root_cause_skill_rules.py tests/test_browser_control_skill.py tests/test_crawler4j_model_skill_integration.py tests/test_sf_sp_010_documentation_navigation.py
```

## Output

写入：

- `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-4-fix-language-prompt-contracts-report.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-4-fix-language-prompt-contracts-verification.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/iteration-4-fix-language-prompt-contracts-review-input.md`

## Forbidden

- 不得修改未列入 allowed files 的 skill。
- 不得改动 flow completeness evidence。
- 不得提交。
- 不得把本任务写成 approved 或 done。
