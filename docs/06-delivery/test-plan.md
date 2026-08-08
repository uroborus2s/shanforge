# 测试策略与质量门

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `TEST-PLAN-001` |
| 正式版本 | `v3.1.0` |
| 当前修订 | `FLOW-TASK-013` 候选，未发布 |
| 来源候选 | `TASK-DELIVERY-001-R001` |
| 发布事务 | `DELIVERY-RELEASE-TX-R001-G001` |
| 负责人 | `HUMAN_QUALITY_SECURITY_LEAD` |
| 正式版修改 / 审核 / 批准 | `AI_EXECUTOR` / 独立 Reviewer / `uroborus` |
| 候选审核 / 批准 | 未执行 / 未执行 |
| 状态 | `v3.1.0` 已生效；当前修订仅为 `ready_for_review` 候选 |
| 上游 | PRD、R020 正式设计、R002 正式实现 |
| 下游 | 自动测试、WorkItem evidence、发布与交付 Gate |

## 1. 文档目标

固定 Shanforge 的测试层级、风险选择、发布质量门和 R002 项目控制增量的稳定验证入口。单次运行日志、失败堆栈和临时夹具仍进入 WorkItem evidence，不在本页复制。

## 2. 测试层级

| 层级 | 范围 | 重点 |
|---|---|---|
| Schema / Contract | Agent App、Workflow、Project Control、Response、Evidence | 字段、枚举、版本、边界和失败关闭 |
| Domain / Use Case | workflow、memory、project disposition、Gate CAS | 业务不变量和状态转换 |
| Runtime / Adapter | reducer、verification budget、provenance、provider | 确定性、预算、持久化和错误语义 |
| Composition / Integration | access → application → domain → runtime → settings | 五层装配、三入口、端口 owner 和无越层 |
| Security / Policy | permission、approval、writeset、eligibility | 越权、侧信道、旧资格和未授权动作拒绝 |
| Performance | 10,000 task / 100,000 event | 1000 行、8 MiB、3000 ms 上限与无额外全库扫描 |
| Skill consumer | 顶层 `skills/*/SKILL.md` | 全部结构和项目状态交接合同 |

## 3. R002 稳定验证入口

| 需求范围 | 目标测试 |
|---|---|
| `REQ-VIS-001..004` | `tests/test_project_control_contracts.py`、`position.py`、`disposition.py`、`integration.py` |
| `REQ-VIS-005/008` | `tests/test_project_control_evidence.py`、`disposition.py` |
| `REQ-VIS-006/007`、`REQ-ASYNC-016` | `tests/test_project_control_response.py`、`integration.py` |
| `REQ-VIS-009` | `tests/test_project_control_provenance.py` |
| `REQ-ASYNC-015`、`NFR-VIS-004` | `tests/test_project_control_verification.py`、`integration.py` |
| 五层和消费者 | `tests/test_application_boundaries.py`、`test_composition_container.py`、Skill 工作流回归 |

完整回归使用 `uv run pytest -q`。静态门使用 `uv run ruff check src tests`、`uv run ruff format --check src tests` 和 `uv run mypy src`。依赖与差异卫生使用 `uv lock --check` 和 `git diff --check`。

## 4. 在审修订：项目级测试治理（未发布）

正式测试使用稳定测试 ID；一次运行只新增 WorkItem evidence，不重复创建测试定义。追踪方向固定为 `需求 -> 任务 -> 测试 -> 证据`。

### 4.1 测试登记

| 测试 ID | 人类可读名称 | 需求 ID | 任务 ID | 可执行入口 | Evidence | 结果 | 环境 ID |
|---|---|---|---|---|---|---|---|
| `TEST-BB-001` | Shanforge 整体黑盒流程评估 | `REQ-AI-WORKFLOW-053` | `FLOW-TASK-012` | `.venv/bin/python -m pytest -q tests/test_black_box_workflow_eval.py` | `.factory/workitems/FLOW-CONTRACT-001/evidence/FLOW-TASK-012-review-fix-verification.md` | `passed`（13/13） | `TEST-ENV-PYTEST` |
| `TEST-UI-001` | 项目快照页面结构与导航回归 | `REQ-PKI-008` | `FLOW-TASK-011` | `.venv/bin/python -m pytest -q tests/test_project_site_renderer.py tests/test_prd_project_knowledge_requirements.py` | `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-IMPLEMENT-003-P001-review-remediation.md` | `passed`（入口 18/18；扩展证据 102/102） | `TEST-ENV-STATIC` |
| `TEST-API-001` | 项目知识索引契约回归 | `REQ-PKI-004` | `TASK-IMPLEMENT-003-P001` | `.venv/bin/python -m pytest -q tests/test_project_knowledge_contracts.py` | `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-IMPLEMENT-003-P001-T06-verification.md` | `passed`（入口 5/5） | `TEST-ENV-PYTEST` |
| `TEST-REL-001` | Shanforge 发布回归 | `REQ-AI-WORKFLOW-037` | `TASK-IMPLEMENT-001-ai-workflow-platform-implementation` | `.venv/bin/python -m pytest -q && .venv/bin/ruff check src tests && .venv/bin/ruff format --check src tests && .venv/bin/mypy src && uv lock --check && git diff --check` | `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-IMPLEMENT-001-R002-post-release-verification.md` | `passed`（R002 发布证据） | `TEST-ENV-PYTEST` |

变更先按影响选择单元/契约、整体黑盒、UI 测试、API 测试和发布回归。某层级不适用时必须记录 `N/A` 与原因，不能把未运行写成通过。

### 4.2 当前测试环境基线

| 环境 ID | 场景 | 启动命令 | 端口 | 健康检查 | 关闭方式 |
|---|---|---|---|---|---|
| `TEST-ENV-PYTEST` | Python 单元、契约、进程内 API 和整体黑盒 | `N/A`：pytest 在测试进程内导入并调用被测代码 | `N/A`：测试进程不监听网络端口 | `.venv/bin/python -m pytest --collect-only -q` | `N/A`：pytest 进程退出即释放资源 |
| `TEST-ENV-STATIC` | 静态项目 HTML | `.venv/bin/python -m shanforge --project-root . project snapshot --html --json` | `N/A`：只生成并读取本地静态文件 | `test -s .factory/cache/site/current/index.html` | `N/A`：没有常驻进程，快照是可重建缓存 |

所有 UI/API evidence 必须写测试 ID、启动命令、实际端口或带原因的 `N/A`、健康检查、关闭结果、失败数和未运行项。通用项目模板位于 `skills/document-templates/references/test-environment-template.md`。

## 5. 发布质量门

1. 正式输入、候选 manifest、计划、验证和 Review Decision 的 SHA-256 绑定一致。
2. pytest failed/skipped/not_run 均为 0；不能用旧结果替代本轮新鲜验证。
3. Ruff、format、mypy 和依赖锁检查全部通过。
4. 顶层 Skill 全部通过 quick validation；`src/runtime/skills` 与 `src/settings/skills` 保持不存在。
5. fixed H、七种 disposition、exact-context permission、五字段 CAS、durable dispatch、provenance 和 10k/100k 性能攻击全部通过。
6. Critical/Important Finding 为 0；Review 不替代 verification，人类验收不替代正式发布授权。
7. Git、远端和部署结果必须由各自动作回执证明；没有回执时一律写“未执行”。

## 6. R002 已发布质量事实

R002 的权威运行结果位于 `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-IMPLEMENT-001-R002-post-release-verification.md`。该证据记录全仓 832/832、Ruff 0、format 299、mypy 0/236、Skill 38/38、候选攻击 17/17 和发布攻击 8/8。后续变更必须重新运行受影响验证，不得把这份历史证据当成未来变更的通过结果。

## 7. 风险与裁剪

- 文档-only 候选仍需验证 source CAS、链接、版本、禁止事实和 diff；不因为“不改代码”跳过全仓发布基线。
- 权限、CAS、持久化、发布事务和状态投影属于高风险范围，必须运行目标攻击和集成测试。
- 图形 UI 当前不在 R002 范围；替代验收是 access API、结构化响应、严格十五行文本和三入口集成。
- 生产部署尚未发生，因此没有线上 SLO、真实告警或生产回滚演练结果可供宣称。

## 8. 测试案例、运行结果与报告标准（候选）

### 8.1 三类内容严格分离

| 内容 | 稳定格式 | 保存位置 | 是否进入知识索引 | 回答的问题 |
|---|---|---|---|---|
| 测试案例定义 | `TestCaseCatalog/v1` YAML | `tests/specifications/*.testcases.yaml` | 是 | 应该测什么、为什么测、怎样判定 |
| 单次运行结果 | `TestRunResult/v1` JSON | 当前 WorkItem 的 `evidence/test-results/` | 否 | 这一次实际发生了什么 |
| 聚合测试报告 | `TestReport/v1` JSON | 当前 WorkItem 的 `evidence/test-reports/` | 否 | 本次运行整体质量如何 |

同一能力的案例集中保存在一个目录级 catalog，不采用“一条测试一个文件”。运行结果
和报告按 WorkItem 留作可审计证据，但不登记为长期项目事实源，避免历史运行无限进入
常驻上下文和 SQLite。

### 8.2 测试案例必填内容

每个案例必须包含稳定 ID 和版本、中文标题、定义状态、测试目标、测试类型、层级、
优先级、风险、Owner、追踪、前置条件、测试数据、操作/预期成对步骤、后置条件、
环境、自动化状态和标签。

追踪固定分为需求、验收标准、设计文档、UI 页面、API operation、开发任务六类；
需求至少一项，另外五类至少一项。测试数据逐项标明 `sensitive`，避免秘密进入日志。
测试数据值只允许 JSON 标量或对象，不接受数组。
定义状态只有 `draft / active / deprecated / retired`，不能在案例中写 `passed` 或
`failed`；案例已登记只表示“测试定义已登记 / 尚未执行”。

### 8.3 单次结果七态

| 状态 | 中文含义 | 是否算通过 |
|---|---|---|
| `passed` | 已执行且全部满足预期 | 是 |
| `failed` | 已执行但断言或验收不满足 | 否 |
| `error` | 测试基础设施或执行过程异常 | 否 |
| `blocked` | 前置条件、依赖或权限阻断 | 否 |
| `skipped` | 本轮按明确条件跳过 | 否 |
| `not_run` | 已计划但本轮尚未执行 | 否 |
| `cancelled` | 执行开始前后被取消 | 否 |

结果必须记录案例 ID/版本、run ID、带时区起止时间、环境 ID、Git commit、运行时、
逐步实际结果和证据。步骤编号从 1 连续递增；证据路径只能位于当前 WorkItem evidence
目录，必须带 64 位 SHA-256。整体状态由步骤按
`error > failed > blocked > cancelled > passed/skipped/not_run` 确定；后三种状态要求
全部步骤同态。`passed` 还要求至少一个步骤、每步引用证据且证据真实登记。
测试定义、历史结果或人工描述都不能推导出 `passed`。

### 8.4 报告聚合规则

报告只引用已经通过 result validator 的结果，逐项绑定 result ID、case ID、七态、
证据路径和 SHA-256。`total` 和七个状态计数由引用结果确定性计算；自报数字、缺失
结果、重复 result ID、状态漂移或证据 hash 漂移都会使报告失败。报告不以文字总结
覆盖机器计数。报告与所有被引用结果必须使用同一个 `run_id`，禁止跨运行批次拼接。

### 8.5 固定命令与只读站点

稳定案例由目标项目自身的合同测试验证。Shanforge 不再提供仓内 test-case validator，
也不维护 SQLite 测试投影。
质量页和文档详情必须将其显示为测试定义，只有明确传入且通过校验的当前报告才能显示
运行结果。

## 9. 轻量测试闭环（2026-08-08 已批准生效）

本节覆盖第 4、7、8 节中与本节冲突的候选字段和逐次全仓要求；无需为普通开发任务生成完整治理材料。

- 设计阶段完成测试范围、层级、角色权限矩阵、接口案例、环境 / 数据、自动化入口、进入 / 退出条件和报告结构；
  脚本实现与运行结果分别在开发、测试阶段完成。
- 案例目录只保留稳定 ID、目标 / 追踪、角色或认证态、输入 fixture 引用、预期断言引用、层级和自动化入口。
  接口 body 与预期状态码、schema、业务码、副作用和幂等结果由测试脚本断言，不复制大段 JSON。
- 单次运行结果只保留案例 ID、状态、缺陷 ID 和证据引用；最终报告只保留精确候选、环境别名、结果汇总、
  失败 / 阻塞 / 跳过、缺陷历史、残余风险和证据引用。
- 报告不得记录完整测试服务地址、IP、端口、账号、密码、令牌、DSN、个人信息或原始敏感日志；只使用环境和账号别名。
- 首个发布候选运行完整必需发布测试并集中登记缺陷；每个修复只复测原失败案例、根因案例和受影响调用方 / 契约；
  阻断缺陷全部关闭后冻结最终候选，再运行一次完整必需发布测试。V4 或项目明确规定时才运行字面全仓测试。

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v3.0.0` | 2026-07-18 | 基于 R019 正式落档测试策略 | `uroborus` | `uroborus` | `uroborus` |
| `v3.1.0` | 2026-07-20 | 增加 R002 项目控制验证入口、发布质量门和证据边界 | `AI_EXECUTOR` | 独立 Reviewer | `uroborus` |
