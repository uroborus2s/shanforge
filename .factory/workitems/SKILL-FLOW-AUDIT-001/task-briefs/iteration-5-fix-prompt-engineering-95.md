# SKILL-FLOW-AUDIT-001 Iteration 5 Prompt Engineering Fix to 95+

## 目标

把 [prompt-engineering-review-iteration-5.md](../reviews/prompt-engineering-review-iteration-5.md) 中指出的问题修到下一轮 Prompt 工程评审预期 95 分以上。

此任务必须在 `iteration-5-fix-chinese-language-95` 完成后执行，基于它的改动继续补齐 prompt 契约，不得回退前一任务。

## 必读输入

- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/prompt-engineering-review-iteration-5.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/chinese-language-review-iteration-5.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/task-briefs/iteration-5-fix-chinese-language-95.md`
- 前一任务产出的 report / evidence / review input

## 允许修改

- `skills/doc-coauthoring/SKILL.md`
- `skills/document-templates/SKILL.md`
- `skills/gitcommitzh/SKILL.md`
- `skills/skill-creator/SKILL.md`
- `skills/stratix-service/SKILL.md`
- `skills/stratix-admin-web/SKILL.md`
- `skills/algorithmic-art/SKILL.md`
- `skills/shadcn/SKILL.md`
- `skills/ui-ux-pro-max/SKILL.md`
- 直接对应的结构测试
- 本任务自己的 report / evidence / review input
- `.factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl`

不要修改 memory；由主线程统一同步。

## 修复要求

1. 低于 90 分的 `doc-coauthoring`、`document-templates`、`gitcommitzh`、`skill-creator`、`stratix-service` 必须补齐触发边界、动作边界、输出契约、失败语义、证据要求。
2. `doc-coauthoring` 补 Shanforge work item 状态包：`ready_for_review | blocked | needs_user_input`，同时保留非 work item 的轻量交付口径。
3. `gitcommitzh` 补标准 `工作结果` 包，且不扩大到 push / PR / merge。
4. `skill-creator` 补 `work_item` / `ledger_event`，把旧工具链事实改成“存在才使用，不存在则记录 blocked 或跳过原因”。
5. `stratix-service` 补 `work_item` / `ledger_event`，统一 `ready_for_review | blocked | needs_user_input`，去掉“可上线”与状态包并存的歧义。
6. `stratix-admin-web` 补 `ledger_event`，明确只有 Stratix admin 页面开发才优先于普通前端 skill。
7. 对 `algorithmic-art`、`shadcn`、`ui-ux-pro-max` 做最小状态包补丁；不要重写完整主入口。

## 验证

至少运行：

```bash
uv run pytest tests/test_skill_creator_skill_principles.py tests/test_pr_commit_workflow_rules.py tests/test_stratix_service_skill.py tests/test_stratix_admin_web_skill.py tests/test_sf_sp_010_documentation_navigation.py tests/test_skill_flow_process_audit.py
uv run ruff check tests/test_skill_creator_skill_principles.py tests/test_pr_commit_workflow_rules.py tests/test_stratix_service_skill.py tests/test_stratix_admin_web_skill.py tests/test_sf_sp_010_documentation_navigation.py tests/test_skill_flow_process_audit.py
git diff --check
```

## 输出

- `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-5-fix-prompt-engineering-95-report.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-5-fix-prompt-engineering-95-verification.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/iteration-5-fix-prompt-engineering-95-review-input.md`
- ledger event：`iteration-5-fix-prompt-engineering-95:implementation`
