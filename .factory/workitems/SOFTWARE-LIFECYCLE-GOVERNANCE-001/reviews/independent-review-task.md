# SOFTWARE-LIFECYCLE-GOVERNANCE-001 独立批次评审输入

## Inputs

- Work item：`.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/brief.md`
- Review type：`independent batch review`
- Plan：`.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/plan.md`
- Task briefs：`.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/task-briefs/`
- Ledger：`.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/ledger.jsonl`
- Implementer report：`.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/reports/SOFTWARE-LIFECYCLE-GOVERNANCE-001-implementation-summary.md`
- Verification evidence：`.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/evidence/SOFTWARE-LIFECYCLE-GOVERNANCE-001-verification.md`
- Diff package：当前 `HEAD 91460c2` 之后的工作区 diff 与本 WorkItem 未跟踪文件。

## 评审范围

- `.factory/project-knowledge/artifact-source-registry.json`
- `contracts/openapi/openapi.yaml`（删除）
- `contracts/schemas/design-artifact-manifest.schema.json`（删除）
- `contracts/schemas/openapi-shanforge-rules.schema.json`（删除）
- `design/ux-ui/design-manifest.yaml`（删除）
- `design/ux-ui/tokens.json`（删除）
- `docs/03-developer-guide/interface-reference.md`
- `docs/04-product/requirements-matrix.md`
- `docs/05-design/*.md` 中本候选已修改文件
- `docs/06-delivery/test-plan.md`
- `docs/06-delivery/test-cases.md`
- `docs/document-index.md`
- `tests/test_lifecycle_governance.py`
- `tests/test_project_test_governance.py`
- `tests/test_full_project_session_workflow_routing.py`
- `.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/**`
- `.factory/memory/agent-session.md`、`current-state.md`、`tasks.summary.md`

## Job

1. 核对用户要求：正式设计唯一事实源、完整生命周期输入输出/Gate 矩阵、跨文档一致性校验和干净克隆准备。
2. 核对重写后的设计是否保留所有当前 Skill-first 合同，同时确实删除旧 Python 平台、OpenAPI/UI 附件的现行资格。
3. 核对生命周期矩阵是否可执行，尤其是简单任务、复杂任务、Spike/原型、TDD、Bug、Review、候选验证、提交与发布边界。
4. 核对 `TEST-BB-002` 是否可能出现假绿、漏扫、脆弱解析或仅堆关键字。
5. 核对版本、来源候选、批准状态、索引、需求追踪、ledger 与 memory 是否一致；特别评估用户授权是否足以支持当前正式状态标记。
6. 核对删除附件确实无当前 consumer，且 source registry 没有残留活动 root。
7. 只读，不修改任何文件。先列 findings，再给 score 和 `approved | changes_requested`。

## Output

返回完整 Independent Review 内容；由 Sol 写入 `.factory/workitems/SOFTWARE-LIFECYCLE-GOVERNANCE-001/reviews/independent-review.md`。

- `reviewer_type: independent_subagent`
- `reviewer_id`: 真实 canonical agent id
- `reviewer_independence_evidence`: Terra/high、`fork_turns=none`、未参与 T01–T03、只读
- Critical / Important / Minor 分级，带文件与行号。
- `approved` 只有在 Critical=0、Important=0 时成立，默认 `return_to_orchestrator`；本候选无人工 Gate。
