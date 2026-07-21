# TASK-SKILL-004-P001 独立实现评审输入

- reviewer requirement：fresh-context、未参与计划或实现、只读、不得修改文件或 Git。
- plan：`.factory/workitems/FLOW-CONTRACT-001/plans/TASK-SKILL-004-P001.md`
- brief：`.factory/workitems/FLOW-CONTRACT-001/task-briefs/TASK-SKILL-004-work-skill-status-envelope-owner.md`
- implementation report：`.factory/workitems/FLOW-CONTRACT-001/reports/TASK-SKILL-004-P001-implementer-report.md`
- verification：`.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-SKILL-004-P001-verification.md`
- black-box：`.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-SKILL-004-P001-black-box-transcript.md`
- target tests：`tests/test_remaining_skill_project_status_contract.py`、`tests/test_work_skill_status_envelope_ownership.py`
- implementation owner：`skills/using-shanforge/SKILL.md`、`skills/using-shanforge/references/work-skill-return-contract.md`
- consumers：测试中冻结的精确 32 个 `skills/*/SKILL.md`。
- formal design：`docs/05-design/workflow-execution-design.md` 的统一任务包段。

## 必审问题

1. 四字段是否只由总控项目状态信封生成。
2. 32 个消费者的专业正文、原状态枚举和真实 Gate 是否未改变。
3. 共享 Markdown 合同是否保持为轻量契约，没有中心化运行时机制。
4. direct/lightweight 与项目化流程是否仍正确分流。
5. RED/GREEN、黑盒、相邻回归和范围外失败归因是否真实。

实现者状态：`ready_for_independent_review`，未自批 `approved`。

## Iteration 2

- 首轮结果：`changes_requested / 92 / C0 I1 M0`。
- `I-001`：三处本职结果模板已改为本地 `status/needs` 占位符；正式设计把状态说明标成非封闭枚举。
- finding RED/GREEN：`1 failed / 4 deselected -> 1 passed / 4 deselected`。
- 当前目标：`9 passed`；Skill 相邻 `141 passed`；流程相邻 `30 passed`；目标 Ruff/format、using validator、diff check 通过。
- author status：`ready_for_same_reviewer_rereview`，未自批 `approved`。
