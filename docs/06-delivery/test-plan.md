# 测试策略与质量门

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `TEST-PLAN-001` |
| 正式版本 | `v3.2.0` |
| 当前修订 | 无 |
| 来源候选 | `TEST-GOVERNANCE-CLOSURE-001` |
| 负责人 | `HUMAN_QUALITY_SECURITY_LEAD` |
| 修改 | `AI_EXECUTOR` |
| 审核 / 批准 | 独立 Reviewer / uroborus |
| 状态 | 已批准并生效 |
| 上游 | PRD、Skill-first 系统架构、工作流执行设计 |
| 下游 | 自动测试、WorkItem evidence、测试报告与发布 Gate |

## 1. 文档目标与产品边界

固定 Shanforge 当前 Skill 工程的测试层级、可执行入口、结果语义和发布质量门。Shanforge 不提供仓内 `src/` 平台运行时；已退役平台的 Project Control、五层装配和 OpenAPI 路由测试不属于当前测试范围，不得作为现行入口恢复。

单次运行日志、失败堆栈、测试结果和聚合报告进入当前 WorkItem evidence；本页只保存稳定策略和测试登记。

## 2. 当前测试层级

| 层级 | 当前范围 | 重点 |
|---|---|---|
| Skill contract | `skills/*/SKILL.md`、references、模板与 scripts | 结构、触发边界、输入输出、状态和失败关闭 |
| Workflow semantics | 会话路由、WorkItem、Gate、Review、Verification、Commit | 状态转换、授权边界和交接合同 |
| Project facts | `.factory/`、正式文档、追踪与恢复摘要 | 单一事实源、路径存在性、JSON/JSONL 和可恢复性 |
| Deterministic helpers | 各 Skill 自带 `scripts/` | 标准库行为、确定性输出和错误语义 |
| Consumer integration | Skill 之间的声明式协作合同 | owner、模型路由、无越权和相邻流程回归 |
| Static quality | Python 测试与脚本 | Ruff、diff 卫生和无无关生成物 |

UI、API、性能或安全专项只在目标项目真实存在对应暴露面时启用；不为了填表恢复不存在的 Shanforge 平台能力。

## 3. 当前稳定验证入口

| 范围 | 可执行入口 |
|---|---|
| Skill 结构与边界 | `tests/test_remaining_skill_project_status_contract.py`、`tests/test_skill_flow_process_audit.py` |
| 会话与任务工作流 | `tests/test_full_project_session_workflow_routing.py`、`tests/test_task_workflow_semantics.py` |
| Sol / Terra / Luna 路由 | `tests/test_model_tier_routing.py` |
| 项目记忆与事实源 | `tests/test_project_memory_skill.py`、`tests/test_doc_factory_restructure.py` |
| 测试治理 | `tests/test_project_test_governance.py` |
| 案例/报告文档有效性 | `uv run python skills/document-templates/scripts/validate_test_documents.py --repo-root . --catalog docs/06-delivery/test-cases.md` |
| 完整回归 | `uv run pytest -q` |
| 静态门 | `uv run ruff check .`、`git diff --check` |

所有正式引用的 `tests/test_*.py` 必须存在。删除或重命名测试时，同一变更必须更新本计划、案例目录和治理测试；不得保留“以后再恢复”的失效入口。

## 4. 项目级测试治理

正式测试使用稳定测试 ID；一次运行只新增 WorkItem evidence，不重复创建测试定义。追踪方向固定为 `需求 -> 任务 -> 测试 -> 证据`。

### 4.1 测试登记

| 测试 ID | 人类可读名称 | 需求 ID | 任务 ID | 可执行入口 | Evidence | 结果 | 环境 ID |
|---|---|---|---|---|---|---|---|
| `TEST-BB-001` | Shanforge 整体合同回归 | `REQ-SF-002` | `MODEL-ROUTING-001-T01` | `uv run pytest -q` | `.factory/workitems/MODEL-ROUTING-001/evidence/MODEL-ROUTING-001-T01-verification.md` | `passed`（228 + 4 subtests） | `TEST-ENV-PYTEST` |
| `TEST-UI-001` | 项目快照页面结构与导航回归 | `REQ-SF-007` | `PM-DASHBOARD-005-T01` | `uv run pytest -q tests/test_using_shanforge_snapshot.py` | `.factory/workitems/PM-DASHBOARD-005/evidence/PM-DASHBOARD-005-T01-round-7-verification.md` | `passed`（工作区回归） | `TEST-ENV-STATIC` |
| `TEST-API-001` | 项目事实与恢复契约回归 | `REQ-SF-003` | `MODEL-ROUTING-001-T01` | `uv run pytest -q tests/test_project_memory_skill.py tests/test_doc_factory_restructure.py` | `.factory/workitems/MODEL-ROUTING-001/evidence/MODEL-ROUTING-001-T01-verification.md` | `passed`（工作区回归） | `TEST-ENV-PYTEST` |
| `TEST-REL-001` | Shanforge 发布回归 | `REQ-SF-004` | `MODEL-ROUTING-001-T01` | `uv run pytest -q && uv run ruff check . && git diff --check` | `.factory/workitems/MODEL-ROUTING-001/evidence/MODEL-ROUTING-001-T01-verification.md` | `passed`（提交前候选） | `TEST-ENV-PYTEST` |

登记中的结果是所引用历史 evidence 的事实，不代表当前变更已通过。当前候选必须生成新鲜结果和报告。

### 4.2 当前测试环境基线

| 环境 ID | 场景 | 启动命令 | 端口 | 健康检查 | 关闭方式 |
|---|---|---|---|---|---|
| `TEST-ENV-PYTEST` | Python 单元、契约和整体黑盒 | `N/A`：pytest 在测试进程内读取 Skill 与项目事实 | `N/A`：测试进程不监听网络端口 | `uv run pytest --collect-only -q` | `N/A`：pytest 进程退出即释放资源 |
| `TEST-ENV-STATIC` | 项目快照静态 HTML 合同 | `N/A`：pytest 直接调用 Skill 自带快照脚本 | `N/A`：只生成并读取本地静态文件 | `uv run pytest --collect-only -q tests/test_using_shanforge_snapshot.py` | `N/A`：没有常驻进程，临时目录由测试清理 |

通用环境模板位于 `skills/document-templates/references/test-environment-template.md`。有真实服务时必须记录启动、健康检查和关闭；无服务时必须使用带原因的 `N/A`。

## 5. 测试案例、运行结果与报告合同

### 5.1 三类内容分离

| 内容 | 事实 owner | 回答的问题 |
|---|---|---|
| 测试案例定义 | [`docs/06-delivery/test-cases.md`](./test-cases.md) 与对应测试脚本 | 应该测什么、为什么测、怎样判定 |
| 单次运行结果 | 当前 WorkItem evidence | 这一次实际发生了什么 |
| 人类可读测试报告 | 当前 WorkItem reports/evidence | 本次整体质量、缺口、风险和发布建议是什么 |

普通开发任务不创建长期正式测试报告页面。阶段验收、发布候选或用户明确要求时，使用 `skills/document-templates/assets/templates/05-quality/test-report.md` 生成当前 WorkItem 报告。

### 5.2 测试案例必填内容

案例至少包含稳定 ID、版本、名称、定义状态、目标、需求/验收追踪、层级、优先级、风险、Owner、前置条件、测试数据或 fixture、操作与预期成对步骤、环境、自动化入口、证据要求、后置/清理条件和标签。

定义状态只有 `draft / active / deprecated / retired`，不能在案例定义中写 `passed` 或 `failed`。当前项目正式目录位于 `docs/06-delivery/test-cases.md`，通用模板位于 `skills/document-templates/assets/templates/05-quality/test-cases.md`。

### 5.3 案例运行结果七态

| 状态 | 中文含义 | 是否算通过 |
|---|---|---|
| `passed` | 已执行且全部满足预期 | 是 |
| `failed` | 已执行但断言或验收不满足 | 否 |
| `error` | 测试基础设施或执行过程异常 | 否 |
| `blocked` | 前置条件、依赖或权限阻断 | 否 |
| `skipped` | 本轮按明确条件跳过 | 否 |
| `not_run` | 已计划但本轮未执行 | 否 |
| `cancelled` | 测试执行被取消 | 否 |

每条结果记录案例 ID、run ID、环境别名、精确候选、状态、缺陷 ID（如有）和证据引用。`skipped / not_run / cancelled / blocked` 必须写原因，不能推导为通过。

### 5.4 批次验证结论

批次结论只使用 `passed / partial / failed / blocked`：

- `passed`：全部必需检查通过，且无未运行项。
- `partial`：已完成部分检查，但仍有未运行项或残余验证缺口。
- `failed`：至少一个已运行必需检查失败。
- `blocked`：环境、权限或依赖导致必需验证无法开始或继续。

案例七态与批次四态不可混用。报告的七态计数来自案例结果，批次结论由准出条件和未运行项确定。

### 5.5 自动有效性与聚合一致性

- 案例目录定稿时运行 `validate_test_documents.py --repo-root . --catalog <path>`，检查索引/详情一致、必填字段、枚举和 pytest 自动化节点。
- 里程碑、发布候选或用户明确要求的 WorkItem 报告定稿时运行 `validate_test_documents.py --report <path>`，检查精确候选、七态总数、批次四态和 GO/NO-GO。
- 校验失败属于质量门失败；不得通过手工修改聚合结论绕过案例结果。

## 6. 发布质量门

1. 候选必须绑定不可变 commit 或 digest，测试报告、review 和发布动作指向同一候选。
2. 首个候选运行完整必需发布测试；阻断缺陷修复后冻结最终候选，再运行一次完整必需发布测试。
3. 最终候选的必需测试 `failed/error/blocked/not_run/cancelled` 均为 0；`skipped` 必须有已接受理由。
4. `uv run pytest -q`、`uv run ruff check .` 和 `git diff --check` 使用本轮新鲜结果通过。
5. 正式测试引用均可解析到当前文件；JSON/JSONL 和 Skill 自带确定性脚本按变更影响验证。
6. 正式案例目录和适用的人类可读报告通过 `validate_test_documents.py`。
7. Critical/Important Finding 为 0；Review、Verification 和人工批准互不替代。
8. Git、远端和部署结果只按真实回执报告；未执行时明确写未执行。

## 7. 轻量测试闭环（2026-08-08 已批准生效）

- 设计阶段定义范围、层级、环境、数据、自动化入口、准入准出和报告结构；脚本与运行结果分别在开发、测试阶段完成。
- 案例目录引用 fixture 和断言入口，不复制大段请求 body、响应或日志。
- 每个修复只复测原失败案例、根因案例和受影响调用方/契约；最终候选再跑完整必需发布测试。
- 普通任务使用紧凑命令结果；阶段、发布或本 WorkItem 明确要求时才生成完整人类可读报告。
- 报告不得记录完整内部 URL、IP、端口、账号、密码、令牌、DSN、个人信息或原始敏感日志。

## 8. 风险与裁剪

- 文档和 Skill 合同变更至少运行受影响治理测试、完整 pytest、Ruff 和 diff 卫生检查。
- UI/API/性能/安全层级只有真实暴露面时才启用，不使用 `N/A` 表格制造不存在的系统。
- 无法自动化的检查必须写人工步骤、Owner、未运行原因和残余风险。
- 历史 evidence 只证明历史候选，不替代当前候选验证。

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v3.0.0` | 2026-07-18 | 基于 R019 正式落档测试策略 | `uroborus` | `uroborus` | `uroborus` |
| `v3.1.0` | 2026-07-20 | 增加 R002 项目控制验证入口、发布质量门和证据边界 | `AI_EXECUTOR` | 独立 Reviewer | `uroborus` |
| `v3.2.0` | 2026-08-23 | 发布正式案例目录、自动化入口有效性校验和七态报告聚合门 | `AI_EXECUTOR` | 独立 Reviewer | `uroborus` |
