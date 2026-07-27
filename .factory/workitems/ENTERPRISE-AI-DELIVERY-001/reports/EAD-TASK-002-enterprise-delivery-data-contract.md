# 企业交付数据模型与 Agent 输出契约

## 1. 文档信息

- Work item：`ENTERPRISE-AI-DELIVERY-001`
- Task：`EAD-TASK-002`
- 版本：`0.1.0`
- 状态：`ready_for_review`
- 来源：用户批准的最小试点路径
- 适用范围：咨询实施包、半自动 Agent、人工脱敏导入导出

## 2. 目标与边界

本契约让业务、运营、负责人、开发、测试和运维使用同一组稳定字段交换需求、估算、
验收、缺陷和周报信息。AI 只生成草稿、缺口和一致性检查结果；所有业务、技术、排期、
上线与关闭决定都由指定人员确认。

本轮不定义 Web 页面、数据库表、API、客户系统连接器或代码仓库集成。输入和输出均为
人工上传或下载的脱敏文档、表格及结构化文件。

## 3. 统一约定

### 3.1 字段级别

- `R`：必填；缺失时不得进入下一门禁。
- `C`：条件必填；条件成立但缺失时不得进入下一门禁。
- `O`：可选；不影响当前门禁。

### 3.2 公共信封

所有模型都必须包含以下字段。

| 字段 | 级别 | 规则 |
|---|---:|---|
| `schema_version` | R | 固定为 `ead-delivery-contract/v1` |
| `record_id` | R | 稳定 ID，格式 `<TYPE>-<YYYYMMDD>-<SEQ>`，创建后不可复用 |
| `record_revision_id` | R | 当前修订 ID，格式 `<record_id>@<version>` |
| `previous_revision_id` | C | `version` 大于 `0.1.0` 时指向前一修订 |
| `content_digest` | R | 按 3.4 节计算的 `sha256:<64 位小写十六进制>`，绑定被审核内容 |
| `record_type` | R | `requirement_intake`、`development_ready_package`、`estimate_breakdown`、`acceptance_record`、`defect_closure` 或 `weekly_dashboard` |
| `source_ref` | R | 脱敏来源文件名、工作表或人工录入批次，不保存生产链接 |
| `source_version` | R | 来源版本或导入批次号 |
| `redaction_status` | R | 仅允许 `redacted_confirmed`；其他值拒绝处理 |
| `owner_role` | R | 对内容负责的岗位 |
| `owner_actor_ref` | R | `human:<directory>:<opaque-id>` 稳定脱敏身份，不使用姓名或 AI run ID |
| `reviewer_roles` | R | 当前门禁确认岗位列表，不能包含 AI |
| `reviewer_actor_refs` | R | 对应评审人的 `human:*` 稳定身份列表；AI actor 禁止进入 |
| `status` | R | 使用对应模型状态机 |
| `version` | R | 从 `0.1.0` 开始；修改保留历史版本 |
| `related_ids` | R | 关联记录 ID 列表；没有关联时为空数组 |
| `evidence_refs` | R | 脱敏证据路径或记录 ID；没有证据时为空数组且不得关闭 |
| `data` | R | 当前 `record_type` 在第 4 节定义的业务字段对象，不允许把业务字段放在顶层 |
| `audit_events` | R | 追加式事件，包含 event ID、actor ref/role、from/to、时间和证据 |
| `created_at` / `updated_at` | R | ISO-8601 时间 |

### 3.3 统一规则

1. AI 输出必须标记 `ai_draft: true`、`generated_at` 和 `input_record_ids`。
2. 人工确认必须记录 `decision`、`decided_by_actor_ref`、`decided_by_role`、`decided_at`、
   `reviewed_revision_id`、`reviewed_content_digest` 和 `decision_note`。
3. 原始输入与 AI 草稿不可被覆盖；修订创建新的 `record_revision_id`，通过
   `previous_revision_id` 连接版本链，人工决策绑定被审修订和摘要。
4. `record_id`、`related_ids` 和 `evidence_refs` 构成跨模型追踪链。
5. 任何输入未标记 `redacted_confirmed` 时，Agent 只能返回拒绝原因，不能继续生成。
6. AI 不得自动改变优先级、估算承诺、验收结论、上线结论或缺陷关闭状态。

### 3.4 Revision digest

`content_digest` 的规范前像是以下唯一 JSON 结构，不允许额外顶层字段：

```json
{
  "schema_version": "ead-delivery-contract/v1",
  "record_id": "<stable-id>",
  "record_revision_id": "<record-id>@<version>",
  "previous_revision_id": "<previous-revision-or-empty>",
  "record_type": "<type>",
  "source_ref": "<redacted-source>",
  "source_version": "<source-version>",
  "redaction_status": "redacted_confirmed",
  "owner_role": "<role>",
  "owner_actor_ref": "human:<directory>:<opaque-id>",
  "related_ids": [],
  "evidence_refs": [],
  "data": {}
}
```

`data` 必须且只能包含当前 `record_type` 在第 4 节列出的业务字段；第 4 节表格中的字段路径
均解释为 `data.<field>`，业务字段不得同时复制到记录顶层。

前像明确排除 `content_digest` 自身，以及会在审核后追加或变化的 `status`、
`reviewer_roles`、`reviewer_actor_refs`、`audit_events`、`created_at`、`updated_at`、
所有 `decision*` 字段和 Agent run 元数据。

计算规则：

- `related_ids` 和 `evidence_refs` 先去重并按 Unicode code point 升序排列。
- 其他数组保持业务顺序。
- 对前像执行 RFC 8785 JCS 序列化，编码为 UTF-8。
- 计算 SHA-256，并写成 `sha256:<64 位小写十六进制>`。
- 修改任何前像字段都必须创建新 `record_revision_id`，连接 `previous_revision_id` 并重算摘要。
- 追加 `audit_events` 或改变 workflow `status` 不改变当前 revision digest。
- 人工决策或受审状态转移前必须重算摘要，并同时比较 `reviewed_revision_id` 和
  `reviewed_content_digest`；任一不匹配都返回 `REVISION_DIGEST_MISMATCH`，
  只允许追加拒绝审计事件，不得推进状态。

Golden fixture 位于
`evidence/EAD-TASK-002-contract-check.py` 的 `sample` 对象；其唯一预期摘要为：

```text
sha256:da62145fcaffa8f551b082fe2f0e4c31822ecca2a962c63807b746d8b4afdcd8
```

## 4. 数据模型

本节所有字段均位于公共信封的 `data` 对象中。

### 4.1 需求准入 `requirement_intake`

状态集合：`draft`、`needs_clarification`、`ready_for_business_review`、`accepted`、`rejected`

| 字段 | 级别 | 说明 |
|---|---:|---|
| `business_goal` | R | 要改善的业务结果 |
| `requester_role` | R | 提出需求的岗位 |
| `problem_statement` | R | 当前问题及影响 |
| `scope_in` | R | 本次包含范围 |
| `scope_out` | R | 明确排除范围 |
| `priority_proposal` | R | `P0`、`P1` 或 `P2`，仅为建议 |
| `affected_users` | R | 受影响角色或用户群 |
| `business_rules` | R | 已知口径和约束；没有时为空数组并进入澄清 |
| `acceptance_intent` | R | 业务方可观察的成功结果 |
| `dependencies` | R | 外部数据、团队或前置决定 |
| `open_questions` | R | 未决问题列表 |
| `target_date` | O | 期望日期，不等于承诺日期 |
| `attachments` | O | 脱敏附件引用 |

准入门禁：业务/运营确认目标、范围、口径和验收意图后，才能进入开发就绪整理。

### 4.2 开发就绪包 `development_ready_package`

状态集合：`draft`、`needs_business_input`、`needs_technical_input`、`ready_for_joint_review`、
`accepted_for_estimation`、`returned`

| 字段 | 级别 | 说明 |
|---|---:|---|
| `requirement_id` | R | 对应需求准入 ID |
| `user_stories` | R | 角色、目标、价值 |
| `functional_rules` | R | 可实现的业务规则 |
| `acceptance_criteria` | R | Given/When/Then 或等价可观察标准 |
| `exception_flows` | R | 异常、空态、权限不足和恢复行为 |
| `data_impact` | R | 新增、修改、只读或无数据影响 |
| `api_impact` | R | 新增、修改、只读或无接口影响 |
| `ui_impact` | R | 页面、终端、交互或 N/A 原因 |
| `permission_rules` | R | 可见、可操作、审批角色 |
| `non_functional_requirements` | R | 性能、安全、兼容性等可验证目标 |
| `test_scenarios` | R | 正常、异常和边界场景 |
| `release_constraints` | C | 涉及上线窗口、迁移或回滚时必填 |
| `unresolved_decisions` | R | 未决项；非空时不得接受估算 |

联合门禁：业务确认需求含义，开发确认可实现性，测试确认可验证性；任一方退回都不得估算。

### 4.3 估算拆解 `estimate_breakdown`

状态集合：`draft`、`needs_decomposition`、`ready_for_technical_review`、`confirmed`、`returned`

| 字段 | 级别 | 说明 |
|---|---:|---|
| `ready_package_id` | R | 已接受的开发就绪包 ID |
| `work_units` | R | 每项包含工作内容、owner 岗位和人日 |
| `assumptions` | R | 估算成立的前提 |
| `dependencies` | R | 人员、环境、接口或数据依赖 |
| `risk_buffer_days` | R | 风险缓冲及理由，可为 0 |
| `test_effort_days` | R | 测试与验收工作量 |
| `release_effort_days` | R | 发布、验证、回滚准备工作量 |
| `total_person_days` | R | 工作单元、测试、发布和缓冲之和 |
| `calculation_note` | R | 可复核的计算过程 |
| `resource_assumption` | R | 人数、技能和并行假设 |
| `confidence` | R | `low`、`medium` 或 `high` |
| `variance_reason` | C | 与历史或原估算偏差超过 20% 时必填 |

估算门禁：开发负责人确认拆解与假设，项目负责人确认资源和优先级；AI 不得把建议写成承诺日期。

### 4.4 验收记录 `acceptance_record`

状态集合：`draft`、`needs_test_input`、`ready_for_joint_review`、`approved_for_execution`、
`ready_for_result_review`、`accepted`、`rejected`

| 字段 | 级别 | 说明 |
|---|---:|---|
| `ready_package_id` | R | 对应开发就绪包 ID |
| `estimate_id` | R | 对应已确认估算 ID |
| `acceptance_scenarios` | R | 场景 ID、前置、动作和期望结果 |
| `required_evidence` | R | 每个场景的证据类型和采集责任岗位 |
| `environment` | R | 脱敏环境和版本 |
| `execution_results` | C | 进入结果评审前，逐场景记录实际结果 |
| `result_evidence_refs` | C | 进入结果评审前，逐场景关联证据 |
| `business_decision` | C | 进入 `accepted` 或 `rejected` 前必填 |
| `test_decision` | C | 进入 `accepted` 或 `rejected` 前必填 |
| `unresolved_failures` | R | 未通过场景；非空时不能进入 `accepted` |
| `release_check_ref` | C | 涉及上线时必填 |

验收门禁：业务确认业务结果，测试确认执行和证据；两者均绑定精确修订后才可接受。

### 4.5 缺陷闭环 `defect_closure`

状态集合：`reported`、`needs_reproduction`、`triaged`、`fixing`、`ready_for_verification`、
`verified`、`closed`、`reopened`

| 字段 | 级别 | 说明 |
|---|---:|---|
| `title` | R | 可定位问题的简短描述 |
| `severity` | R | `P0`、`P1`、`P2` 或 `P3` |
| `environment` | R | 脱敏环境标识和版本 |
| `preconditions` | R | 复现前置 |
| `reproduction_steps` | R | 可执行步骤 |
| `expected_result` | R | 期望行为 |
| `actual_result` | R | 实际行为 |
| `impact_scope` | R | 用户、业务和数据影响 |
| `root_cause` | C | 进入 `ready_for_verification` 前必填 |
| `fix_summary` | C | 进入 `ready_for_verification` 前必填 |
| `regression_scope` | C | 进入 `ready_for_verification` 前必填 |
| `verification_result` | C | 进入 `verified` 前必填 |
| `production_check` | C | 生产问题进入 `closed` 前必填 |
| `rollback_or_mitigation` | C | P0/P1 或影响生产时必填 |

关闭门禁：测试确认验证结果；生产问题还需运维确认生产检查。证据不完整只能退回或重开。

### 4.6 周报看板 `weekly_dashboard`

状态集合：`draft`、`needs_source_reconciliation`、`ready_for_owner_review`、`published`

| 字段 | 级别 | 说明 |
|---|---:|---|
| `period_start` / `period_end` | R | 周期边界 |
| `baseline_at` | R | 统计快照时间 |
| `requirement_counts` | R | 各状态需求数量及记录 ID |
| `estimate_variance` | R | 计划、实际和偏差原因 |
| `defect_counts` | R | 按等级、状态和超期统计 |
| `gate_waiting_items` | R | 等待人工确认的记录 ID、责任岗位和等待时长 |
| `delivered_outcomes` | R | 已验收业务结果及证据 |
| `risks_and_blockers` | R | 风险、影响、owner 和处理期限 |
| `next_week_commitments` | R | 已由负责人确认的下周事项 |
| `data_quality_notes` | R | 缺失、冲突和未纳入数据 |
| `source_record_ids` | R | 报表使用的全部稳定 ID |

发布门禁：项目负责人核对来源和偏差，确认后才能发布；AI 不得隐藏缺失数据或自动承诺下周事项。

### 4.7 封闭状态转移

未列出的 `from + event + to` 一律返回 `INVALID_STATE`，不修改记录。所有 guard 都必须由
`audit_events` 引用的人工决策和 `evidence_refs` 证明。

| Model | From | Event | Guard / evidence | To |
|---|---|---|---|---|
| `requirement_intake` | `draft` | `request_clarification` | 缺失字段或冲突列表非空 | `needs_clarification` |
| `requirement_intake` | `needs_clarification` | `submit_clarification` | 必填字段齐全，冲突已处置 | `ready_for_business_review` |
| `requirement_intake` | `draft` | `submit_business_review` | 必填字段齐全，`open_questions` 为空 | `ready_for_business_review` |
| `requirement_intake` | `ready_for_business_review` | `accept` | 业务 actor 决策绑定当前 revision/digest | `accepted` |
| `requirement_intake` | `ready_for_business_review` | `reject` | 业务 actor 决策含理由 | `rejected` |
| `requirement_intake` | `ready_for_business_review` | `return_for_clarification` | 退回理由和责任 actor 已记录 | `needs_clarification` |
| `development_ready_package` | `draft` | `request_business_input` | 业务缺口列表非空 | `needs_business_input` |
| `development_ready_package` | `draft` | `request_technical_input` | 技术缺口列表非空 | `needs_technical_input` |
| `development_ready_package` | `needs_business_input` | `submit_business_input` | 业务缺口已清零 | `draft` |
| `development_ready_package` | `needs_technical_input` | `submit_technical_input` | 技术缺口已清零 | `draft` |
| `development_ready_package` | `draft` | `submit_joint_review` | 必填字段齐全，未决项为空 | `ready_for_joint_review` |
| `development_ready_package` | `ready_for_joint_review` | `accept_for_estimation` | 业务、开发、测试 actor 均绑定当前 revision/digest | `accepted_for_estimation` |
| `development_ready_package` | `ready_for_joint_review` | `return` | 退回理由和责任 actor 已记录 | `returned` |
| `development_ready_package` | `returned` | `revise` | 新 revision 指向前一 revision | `draft` |
| `estimate_breakdown` | `draft` | `request_decomposition` | 工作单元或计算缺口非空 | `needs_decomposition` |
| `estimate_breakdown` | `needs_decomposition` | `submit_decomposition` | 工作单元可求和 | `draft` |
| `estimate_breakdown` | `draft` | `submit_technical_review` | 总人日等于明细、测试、发布和缓冲之和 | `ready_for_technical_review` |
| `estimate_breakdown` | `ready_for_technical_review` | `confirm` | 开发负责人和项目负责人绑定当前 revision/digest | `confirmed` |
| `estimate_breakdown` | `ready_for_technical_review` | `return` | 退回理由和责任 actor 已记录 | `returned` |
| `estimate_breakdown` | `returned` | `revise` | 新 revision 指向前一 revision | `draft` |
| `acceptance_record` | `draft` | `request_test_input` | 场景或证据定义缺口非空 | `needs_test_input` |
| `acceptance_record` | `needs_test_input` | `submit_test_input` | 场景和证据定义齐全 | `draft` |
| `acceptance_record` | `draft` | `submit_joint_review` | 场景可观察，环境和责任岗位已定义 | `ready_for_joint_review` |
| `acceptance_record` | `ready_for_joint_review` | `approve_execution` | 业务和测试 actor 绑定当前 revision/digest | `approved_for_execution` |
| `acceptance_record` | `ready_for_joint_review` | `return` | 退回理由和责任 actor 已记录 | `draft` |
| `acceptance_record` | `approved_for_execution` | `submit_results` | 每个场景都有结果和证据 | `ready_for_result_review` |
| `acceptance_record` | `ready_for_result_review` | `accept` | 业务和测试均通过，未通过场景为空 | `accepted` |
| `acceptance_record` | `ready_for_result_review` | `reject` | 未通过场景和处理意见已记录 | `rejected` |
| `acceptance_record` | `rejected` | `revise` | 新 revision 指向前一 revision | `draft` |
| `defect_closure` | `reported` | `request_reproduction` | 复现信息不完整 | `needs_reproduction` |
| `defect_closure` | `reported` | `triage` | 复现信息完整，严重级别已确认 | `triaged` |
| `defect_closure` | `needs_reproduction` | `submit_reproduction` | 步骤、期望、实际和环境齐全 | `triaged` |
| `defect_closure` | `triaged` | `start_fix` | 开发 owner 和影响范围已确认 | `fixing` |
| `defect_closure` | `fixing` | `submit_verification` | 根因、修复和回归范围齐全 | `ready_for_verification` |
| `defect_closure` | `ready_for_verification` | `verify` | 测试 actor 绑定验证证据 | `verified` |
| `defect_closure` | `ready_for_verification` | `return_to_fix` | 失败证据已记录 | `fixing` |
| `defect_closure` | `verified` | `close` | 测试通过；生产问题另有运维检查 | `closed` |
| `defect_closure` | `verified` | `reopen` | 新失败证据已记录 | `reopened` |
| `defect_closure` | `closed` | `reopen` | 回归或生产复发证据已记录 | `reopened` |
| `defect_closure` | `reopened` | `resume_fix` | 开发 owner 已确认 | `fixing` |
| `weekly_dashboard` | `draft` | `request_reconciliation` | 来源缺失或统计冲突非空 | `needs_source_reconciliation` |
| `weekly_dashboard` | `needs_source_reconciliation` | `submit_reconciliation` | 来源缺失和冲突已处置 | `draft` |
| `weekly_dashboard` | `draft` | `submit_owner_review` | 来源 ID 完整，数据质量缺口已披露 | `ready_for_owner_review` |
| `weekly_dashboard` | `ready_for_owner_review` | `publish` | 项目负责人绑定当前 revision/digest | `published` |
| `weekly_dashboard` | `ready_for_owner_review` | `return` | 退回理由和责任 actor 已记录 | `draft` |

## 5. Agent 输出契约

所有 Agent 均返回：

```text
agent_run_id, agent_type, input_record_ids, output_record_ids,
status, missing_fields, conflicts, warnings, ai_draft,
generated_at, required_human_gate, failure
```

其中 `status` 只允许 `draft_generated`、`needs_input`、`conflict_detected`、`rejected_unredacted`
或 `failed`。Agent 不返回 `approved`、`confirmed`、`verified`、`closed` 或 `published`。

| Agent | 输入 | 输出 | 人审门禁 | 失败条件 |
|---|---|---|---|---|
| 需求准入 Agent | 脱敏需求记录、附件 | `requirement_intake` 草稿、缺口问题、优先级建议 | 业务/运营确认目标、范围、口径、验收意图 | 未脱敏；缺业务目标或来源；内容冲突无法定位 |
| 开发就绪 Agent | 已接受需求准入 | `development_ready_package` 草稿、影响清单、测试场景 | 业务、开发、测试联合确认 | 需求未接受；关键口径未决；权限或数据影响未知 |
| 估算辅助 Agent | 已接受开发就绪包、脱敏历史参考 | `estimate_breakdown` 草稿、假设和风险 | 开发负责人确认拆解，项目负责人确认资源 | 就绪包未接受；拆解不能求和；依赖或假设缺失 |
| 验收设计 Agent | 开发就绪包、估算拆解 | `acceptance_record` 草稿、证据清单、上线检查草稿 | 业务确认业务结果，测试确认可验证性 | AC 不可观察；环境或数据条件缺失；与需求冲突 |
| 缺陷闭环 Agent | 脱敏缺陷、日志摘要、验证记录 | `defect_closure` 草稿、缺口、疑似根因类别 | 开发确认根因与修复；测试/运维确认验证与关闭 | 无法复现；证据不足；P0/P1 无缓解或回滚信息 |
| 周报汇总 Agent | 当前周期已确认记录 | `weekly_dashboard` 草稿、差异和数据质量提示 | 项目负责人核对并发布 | 来源 ID 缺失；统计冲突；存在未披露的数据缺口 |

## 6. 失败返回

失败时必须返回结构化对象：

| 字段 | 说明 |
|---|---|
| `code` | `UNREDACTED_INPUT`、`MISSING_REQUIRED_FIELD`、`MISSING_ACTOR_ID`、`AI_REVIEWER_FORBIDDEN`、`BROKEN_REVISION_CHAIN`、`REVISION_DIGEST_MISMATCH`、`SOURCE_CONFLICT`、`INVALID_STATE`、`INSUFFICIENT_EVIDENCE` 或 `PROCESSING_ERROR` |
| `message` | 面向人的简明原因 |
| `record_ids` | 受影响记录 |
| `field_paths` | 缺失或冲突字段 |
| `recoverable` | 是否可补充后重试 |
| `required_action` | 负责岗位需要补充或确认的动作 |

失败不得触发状态前进；重复运行使用同一输入版本时必须保留原记录并生成新的 `agent_run_id`。

## 7. 端到端追踪

最小链路：

```text
REQ-* -> DRP-* -> EST-* -> ACC-* -> 验收证据
  └------------------------------> DEF-*（发现缺陷时）
REQ-*/DRP-*/EST-*/ACC-*/DEF-* -> WEEK-*
```

- 需求准入记录通过 `related_ids` 关联开发就绪包。
- 开发就绪包关联估算，估算关联具有稳定 ID 的验收记录。
- 验收记录关联逐场景结果和证据；失败场景可关联缺陷。
- 缺陷关联受影响需求、开发就绪包、验收记录、版本和验证证据。
- 周报列出所有来源记录 ID，统计值必须能回查。

## 8. 非功能与治理要求

| ID | 要求 | 验证信号 |
|---|---|---|
| `NFR-EAD-001` | 100% 输入具有 `source_ref`、`source_version` 和 `redaction_status` | 字段检查无缺失 |
| `NFR-EAD-002` | 100% AI 输出标记 `ai_draft: true` 和人工门禁 | Agent 输出检查无缺失 |
| `NFR-EAD-003` | 100% 状态前进保留人工决策与证据引用 | 抽样记录可回查 |
| `NFR-EAD-004` | 6 类模型之间通过稳定 ID 追踪 | 任一周报统计可回到来源记录 |
| `NFR-EAD-005` | 未脱敏输入拒绝率为 100% | 反例检查返回 `UNREDACTED_INPUT` |
| `NFR-EAD-006` | 100% 人工决策绑定稳定 actor、revision 和 content digest | 审计字段检查无缺失 |
| `NFR-EAD-007` | 所有状态前进都匹配封闭转移表 | 非法转移负例返回 `INVALID_STATE` |

## 9. Baseline 影响

- 领域：定义企业交付咨询试点的数据语义，不改变 Shanforge 产品领域代码。
- 架构：无。
- 数据库：无；本轮不设计持久化表。
- API：无；本轮不设计对外接口。
- UI：无；本轮不开发工作台。
- 后续如决定产品化持久化或集成，必须另建 work item 并重新评审数据库、API、权限和 UI baseline。

## 10. 验收追踪

| Task AC | 契约证据 |
|---|---|
| AC-1 | 第 3.2 节公共信封与第 4 节六类状态机 |
| AC-2 | 第 3.1 节字段级别与第 4 节字段表 |
| AC-3 | 第 5 节六类 Agent 输出契约 |
| AC-4 | 第 2、3.3、5、8 节脱敏和非直连边界 |
| AC-5 | 第 3.2、4.4、7 节验收稳定 ID 与追踪链 |

## 11. 待评审项

- 字段集合是否足够支撑 2 个真实需求和一批 P0/P1 缺陷的试点。
- T03 是否需要在 RACI 中把“业务”和“运营”拆成两个独立决策角色。
- T04 是否需要客户提供脱敏历史估算样本以建立偏差基线。
