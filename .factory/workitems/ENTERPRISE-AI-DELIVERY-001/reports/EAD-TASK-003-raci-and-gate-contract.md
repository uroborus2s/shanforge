# 企业 AI 交付多岗位 RACI 与流程门禁契约

## 1. 文档信息

- Work item：`ENTERPRISE-AI-DELIVERY-001`
- Task：`EAD-TASK-003`
- 版本：`0.1.0`
- 状态：`approved_pending_customer_confirmation`
- 生效状态：`pending_customer_confirmation`
- 前置契约：`EAD-TASK-002-enterprise-delivery-data-contract.md`

## 2. 适用边界

本契约是第一家客户试点的通用岗位模板，不绑定真实姓名。客户确认前，所有
`human:<directory>:<opaque-id>` 映射均为空，流程必须返回
`ROLE_AUTHORITY_UNCONFIRMED`，不得把候选 RACI 当成已生效授权。

AI Agent 只负责生成草稿、发现缺口、检查状态和汇总证据。Shanforge 只负责保存
record、revision、digest、actor、decision 和 evidence；二者都不能成为 RACI 的
`A`，也不能替代人工 reviewer。

## 3. 角色

| Role ID | 中文岗位 | 决策边界 |
|---|---|---|
| `business_owner` | 业务负责人 | 业务目标、范围、业务口径和最终业务验收 |
| `operations_owner` | 运营负责人 | 一线操作规则、运营影响、日常反馈和使用准备 |
| `project_owner` | 项目负责人 | 优先级、资源冲突、跨岗位协调、周报和升级 |
| `development_owner` | 开发负责人 | 技术可行性、任务拆解、估算、实现和根因 |
| `test_owner` | 测试负责人 | 测试设计、结果验证、回归范围和质量结论 |
| `release_owner` | 运维/发布负责人 | 环境、发布窗口、上线检查、回滚和生产关闭 |

每个 Role ID 必须映射一个稳定的 `human:*` actor。一个 actor 可以承担多个角色，
但必须逐角色确认；同一门禁要求职责分离时不得由同一 actor 同时提交和批准。

## 4. RACI

符号：`R` 执行，`A` 最终负责，`C` 事前协商，`I` 事后知会，`A/R` 同时承担。
每行必须恰好一个 `A`，且至少一个 `R`。

| ID | 活动 | 业务 | 运营 | 项目负责人 | 开发 | 测试 | 运维/发布 |
|---|---|---|---|---|---|---|---|
| RAC-01 | 确认业务目标、范围和验收意图 | A | R | C | C | C | I |
| RAC-02 | 确认运营口径和一线影响 | C | A/R | C | C | I | I |
| RAC-03 | 确认优先级和资源顺位 | C | C | A/R | C | I | I |
| RAC-04 | 确认技术影响和开发就绪 | C | C | I | A/R | R | C |
| RAC-05 | 拆解并确认估算 | I | I | C | A/R | C | C |
| RAC-06 | 设计测试与验收场景 | C | C | I | C | A/R | C |
| RAC-07 | 实施、代码自检和根因分析 | I | I | I | A/R | C | C |
| RAC-08 | 验证测试结果和回归范围 | C | I | I | C | A/R | C |
| RAC-09 | 确认业务验收结果 | A | R | C | I | R | I |
| RAC-10 | 执行上线、回滚和生产检查 | I | I | C | R | C | A/R |
| RAC-11 | 确认 P0/P1 缺陷优先级与缓解 | C | R | A | R | C | R |
| RAC-12 | 关闭已验证生产缺陷 | I | C | I | C | R | A/R |
| RAC-13 | 核对并发布周报 | C | R | A/R | C | C | C |
| RAC-14 | 升级跨岗位阻塞和决策冲突 | C | C | A/R | C | C | C |

## 5. 六类门禁

所有门禁都必须先：

1. 读取当前 record 和 `record_revision_id`。
2. 重算 T02 `content_digest` 并比对 `reviewed_content_digest`。
3. 校验 `A` 和所需 `R` 的 `human:*` actor 映射。
4. 校验决策 actor 对应当前 RACI 角色，且不是 AI actor。
5. 校验 guard 和 evidence；任一失败不推进状态。

| Gate | Source record | From | Event | Human A | Guard / evidence | To | Failure |
|---|---|---|---|---|---|---|---|
| GATE-REQ | `development_ready_package` | `ready_for_joint_review` | `accept_for_estimation` | `development_owner` | `requirement_intake=accepted`；业务、开发、测试 actor 均绑定当前 revision/digest；未决项为空 | `accepted_for_estimation` | `ROLE_AUTHORITY_UNCONFIRMED` / `MISSING_GATE_EVIDENCE` / `REVISION_DIGEST_MISMATCH` |
| GATE-EST | `estimate_breakdown` | `ready_for_technical_review` | `confirm` | `development_owner` | 明细可求和；假设、依赖、缓冲、资源和偏差原因完整；项目负责人已确认优先级 | `confirmed` | `ESTIMATE_NOT_EXPLAINABLE` / `ROLE_AUTHORITY_UNCONFIRMED` / `REVISION_DIGEST_MISMATCH` |
| GATE-TEST | `acceptance_record` | `ready_for_joint_review` | `approve_execution` | `test_owner` | 开发就绪包和估算已确认；场景可观察；环境、数据、证据类型和责任岗位齐全 | `approved_for_execution` | `TEST_INPUT_INCOMPLETE` / `ROLE_AUTHORITY_UNCONFIRMED` / `REVISION_DIGEST_MISMATCH` |
| GATE-REL | `acceptance_record` | `ready_for_result_review` | `accept` | `business_owner` | 业务与测试 actor 均通过；所有场景有结果和证据；未通过场景为空；涉及上线时有发布检查和回滚 | `accepted` | `ACCEPTANCE_FAILED` / `RELEASE_EVIDENCE_MISSING` / `REVISION_DIGEST_MISMATCH` |
| GATE-DEF | `defect_closure` | `verified` | `close` | `release_owner` | 测试验证通过；生产问题有运维检查；P0/P1 有缓解、根因、回归和回滚证据 | `closed` | `DEFECT_EVIDENCE_INCOMPLETE` / `ROLE_AUTHORITY_UNCONFIRMED` / `REVISION_DIGEST_MISMATCH` |
| GATE-WEEK | `weekly_dashboard` | `ready_for_owner_review` | `publish` | `project_owner` | 来源 record ID 完整；统计冲突已处置；数据缺口披露；下周事项已由对应 owner 确认 | `published` | `SOURCE_CONFLICT` / `ROLE_AUTHORITY_UNCONFIRMED` / `REVISION_DIGEST_MISMATCH` |

## 6. 门禁职责分离

| Gate | 提交者 | 批准者 | 不允许 |
|---|---|---|---|
| GATE-REQ | `business_owner`、`development_owner`、`test_owner` 各自提交确认 | `development_owner` 完成最终技术准入 | AI actor 代签；缺任一角色确认 |
| GATE-EST | `development_owner` 提交估算 | `development_owner` 确认技术估算，`project_owner` 另行确认资源顺位 | AI 把建议日期写成承诺 |
| GATE-TEST | `development_owner` 提交可测版本和证据 | `test_owner` 批准验收执行 | 开发 actor 同时冒充测试批准者 |
| GATE-REL | `test_owner` 提交结果，`release_owner` 提交上线检查 | `business_owner` 接受业务结果 | 无测试证据上线；AI 自动验收 |
| GATE-DEF | `development_owner` 提交根因与修复，`test_owner` 提交验证 | `release_owner` 关闭生产缺陷 | 开发 actor 单方关闭生产 P0/P1 |
| GATE-WEEK | 各 owner 提交来源记录 | `project_owner` 发布 | 隐藏缺失数据；AI 自动承诺 |

若同一 actor 同时承担提交者和批准者角色：

- GATE-TEST、GATE-REL、GATE-DEF 必须拒绝并返回 `SEGREGATION_OF_DUTIES_VIOLATION`。
- 其他 Gate 必须在 `decision_note` 明确角色合并原因，由 `project_owner` 追加风险确认。

## 7. AI 与 Shanforge 边界

### AI Agent 可以

- 根据脱敏输入生成 record 草稿、缺失问题和冲突列表。
- 检查必填字段、状态转移、revision/digest 和 evidence 完整性。
- 生成 RACI 建议、周报草稿和升级提醒。

### AI Agent 不可以

- 写入 `human:*` actor 身份或伪造人工 decision。
- 成为 `A`、最终 reviewer、业务验收人或上线批准人。
- 自动接受需求、确认估算、批准提测、验收、关闭缺陷或发布周报。

### Shanforge 负责

- 保存每次 record revision、digest、decision 和 audit event。
- 在 actor、状态、证据或 digest 不满足时 fail closed。
- 提供可导出的脱敏 evidence 包，不连接客户生产系统或代码仓库。

## 8. 失败返回

| Code | 条件 | 恢复动作 |
|---|---|---|
| `ROLE_AUTHORITY_UNCONFIRMED` | 角色未映射稳定 human actor，或客户未确认岗位决策权 | 客户确认角色映射 |
| `ROLE_CONFLICT` | 一个活动出现多个 `A` 或没有 `A/R` | 修正 RACI |
| `AI_DECISION_FORBIDDEN` | AI actor 试图承担 A、reviewer 或决策人 | 改由授权 human actor |
| `SEGREGATION_OF_DUTIES_VIOLATION` | 提交和批准角色必须分离但 actor 相同 | 指定独立批准人 |
| `MISSING_GATE_EVIDENCE` | guard 所需 record、decision 或 evidence 缺失 | 补证据后重试 |
| `REVISION_DIGEST_MISMATCH` | 决策绑定的 revision/digest 不是当前内容 | 创建新 revision 并重新审核 |

所有失败只追加拒绝审计事件，不推进 source record。

## 9. 客户最小确认包

正式启用前只需客户确认以下 6 项：

1. 为六个 Role ID 指定稳定脱敏 `human:*` actor。
2. 确认业务与运营是不同岗位，或明确允许同一 actor 兼任并记录原因。
3. 确认 `project_owner` 对优先级、资源冲突和周报发布最终负责。
4. 确认 `business_owner` 最终接受业务结果，`test_owner` 独立确认质量。
5. 确认 `release_owner` 负责上线、回滚、生产检查和生产缺陷关闭。
6. 确认下列强制 actor 分离；任一重合都不得激活模板：
   - GATE-TEST：`development_owner != test_owner`
   - GATE-REL：`business_owner != test_owner`
   - GATE-REL：`business_owner != release_owner`
   - GATE-DEF：`release_owner != development_owner`
   - GATE-DEF：`release_owner != test_owner`

确认前：

- 文档状态保持 `pending_customer_confirmation`。
- 可以用于访谈、演练和角色映射，不得作为真实授权执行生产动作。

## 10. T04 输入

客户确认角色映射后，T04 使用：

- 六个 Role ID 到脱敏 actor 的映射。
- 六类 Gate 的生效版本。
- 2 个真实脱敏需求和一批 P0/P1 缺陷的资料清单。
- 试点周期、基线测量、访谈人员和退出条件。
