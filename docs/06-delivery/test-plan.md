# 测试策略与质量门

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `TEST-PLAN-001` |
| 正式版本 | `v3.1.0` |
| 来源候选 | `TASK-DELIVERY-001-R001` |
| 发布事务 | `DELIVERY-RELEASE-TX-R001-G001` |
| 负责人 | `HUMAN_QUALITY_SECURITY_LEAD` |
| 修改 / 审核 / 批准 | `AI_EXECUTOR` / 独立 Reviewer / `uroborus` |
| 状态 | 已批准并生效 |
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
| Skill consumer | 顶层 `skills/*/SKILL.md` | 38/38 结构和项目状态交接合同 |

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

## 4. 发布质量门

1. 正式输入、候选 manifest、计划、验证和 Review Decision 的 SHA-256 绑定一致。
2. pytest failed/skipped/not_run 均为 0；不能用旧结果替代本轮新鲜验证。
3. Ruff、format、mypy 和依赖锁检查全部通过。
4. 38 个顶层 Skill 全部通过 quick validation；`src/runtime/skills` 与 `src/settings/skills` 保持不存在。
5. fixed H、七种 disposition、exact-context permission、五字段 CAS、durable dispatch、provenance 和 10k/100k 性能攻击全部通过。
6. Critical/Important Finding 为 0；Review 不替代 verification，人类验收不替代正式发布授权。
7. Git、远端和部署结果必须由各自动作回执证明；没有回执时一律写“未执行”。

## 5. R002 已发布质量事实

R002 的权威运行结果位于 `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-IMPLEMENT-001-R002-post-release-verification.md`。该证据记录全仓 832/832、Ruff 0、format 299、mypy 0/236、Skill 38/38、候选攻击 17/17 和发布攻击 8/8。后续变更必须重新运行受影响验证，不得把这份历史证据当成未来变更的通过结果。

## 6. 风险与裁剪

- 文档-only 候选仍需验证 source CAS、链接、版本、禁止事实和 diff；不因为“不改代码”跳过全仓发布基线。
- 权限、CAS、持久化、发布事务和状态投影属于高风险范围，必须运行目标攻击和集成测试。
- 图形 UI 当前不在 R002 范围；替代验收是 access API、结构化响应、严格十五行文本和三入口集成。
- 生产部署尚未发生，因此没有线上 SLO、真实告警或生产回滚演练结果可供宣称。

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v3.0.0` | 2026-07-18 | 基于 R019 正式落档测试策略 | `uroborus` | `uroborus` | `uroborus` |
| `v3.1.0` | 2026-07-20 | 增加 R002 项目控制验证入口、发布质量门和证据边界 | `AI_EXECUTOR` | 独立 Reviewer | `uroborus` |
