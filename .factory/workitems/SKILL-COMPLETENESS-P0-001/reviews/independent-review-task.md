# Independent Review Task

你是 `SKILL-COMPLETENESS-P0-001` 的独立 reviewer。不要读取实现者会话历史；只读取本输入包列出的仓库事实。

## Inputs

- Requirements：`.factory/workitems/SKILL-COMPLETENESS-P0-001/brief.md`
- Plan：`.factory/workitems/SKILL-COMPLETENESS-P0-001/plan.md`
- Task brief：`.factory/workitems/SKILL-COMPLETENESS-P0-001/task-briefs/SKILL-COMPLETENESS-P0-001-T01-sequential-p0-remediation.md`
- Implementer report：`.factory/workitems/SKILL-COMPLETENESS-P0-001/reports/SKILL-COMPLETENESS-P0-001-implementation.md`
- Verification evidence：`.factory/workitems/SKILL-COMPLETENESS-P0-001/evidence/SKILL-COMPLETENESS-P0-001-verification.md`
- Architecture constraints：`AGENTS.md`、`.factory/memory/doc-map.md`、`docs/05-design/system-architecture.md`

## P0 实现范围

- `.factory/project.json`
- `config/software-factory.defaults.json`
- `docs/05-design/api-design.md`
- `docs/05-design/frontend-design.md`
- `docs/05-design/technical-selection.md`
- `docs/05-design/ux-ui-design.md`
- `docs/05-design/workflow-execution-design.md`
- `scripts/sync-codex-skills`
- `skills/art-asset-pipeline/SKILL.md`
- `skills/brainstorming/SKILL.md`
- `skills/document-templates/SKILL.md` 中未暂存的 P0 布局解析变更
- `skills/requirements-engineering/SKILL.md`
- `tests/test_brainstorming_skill.py`
- `tests/test_task_workflow_semantics.py`
- `tests/test_work_skill_status_envelope_ownership.py`
- `tests/test_skill_formal_document_resolution.py`
- `tests/test_skill_inventory_integrity.py`
- `tests/test_sync_codex_skills.py`
- `.factory/workitems/SKILL-COMPLETENESS-P0-001/**`

## 并发排除

当前 index 中 `TEST-GOVERNANCE-001` 已暂存其独立测试治理改动。不要把该 WorkItem、`docs/06-delivery/test-plan.md`、测试模板资产、`verification-before-completion`、测试治理用例或 `agent-session.md` 评为本任务产物。`skills/document-templates/SKILL.md` 的测试案例/报告模板入口 hunk 属于并发任务；本任务只评审已有登记优先和新项目回退语义。

## Job

1. 核对五项 P0 是否完整、顺序和范围是否符合 brief。
2. 检查 skill-first 架构、复用 Skill 路径语义、候选资产生命周期和配置事实。
3. 检查测试是否验证行为/不变量，而非换成新的文本或整文件快照。
4. 核对 verification evidence 与真实工作树；可运行只读验证，不修改实现。
5. 按 `skills/requesting-code-review/references/review-score-rubric.md` 输出结论。

## Output

使用 `apply_patch` 新建：

`.factory/workitems/SKILL-COMPLETENESS-P0-001/reviews/independent-review.md`

必须包含 `reviewer_type`、`reviewer_id`、`reviewer_independence_evidence`、五项评分、Critical/Important/Minor、验证和 Gate。Reviewer 不修改实现、ledger、memory 或 Git。
