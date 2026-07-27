# EAD-TASK-002 Review Response

## Fixed

- `I1`：公共信封新增稳定 actor ref、revision ID、前一修订、内容摘要和追加式审计事件；
  人工决策绑定 actor、revision 和 digest。
- `I2`：用 45 条 `model/from/event/guard/to` 封闭转移替代箭头表达，补齐退回、
  验收返工和 `closed -> reopened -> fixing`。
- `I3`：新增具有公共信封和独立状态机的 `acceptance_record`，追踪链改为
  `REQ -> DRP -> EST -> ACC -> evidence/DEF -> WEEK`。
- `I4`：task brief 明确授权 5 个 memory 文件，并要求共享文件只暂存 EAD hunk。
- `M1`：新增可执行 stdlib 检查脚本，覆盖身份、版本、6 类模型、45 条转移和 4 个非法转移负例。
- `I5`：固定 `canonical_review_payload` 字段、排除项、集合排序、RFC 8785 JCS、
  SHA-256 格式和 revision/digest mismatch 拒绝规则。
- `M2`：新增 actor 缺失、AI reviewer、版本断链、未脱敏和 digest mismatch
  5 个治理负例，并验证 audit 追加不改变摘要、业务字段改变必然改变摘要。
- `I6`：公共信封正式增加固定 `schema_version` 和唯一 `data` 对象；第 4 节字段统一解释为
  `data.<field>`，canonical payload 与 validator 使用同一结构，并增加固定 golden digest。

## Verified

- `python3 .../EAD-TASK-002-contract-check.py`：
  `models=6 agents=6 audit_fields=12 transitions=45 state_negative_cases=4
  governance_negative_cases=5`。
- `uv run ruff check .../EAD-TASK-002-contract-check.py`：`All checks passed!`
- Golden digest：`sha256:da62145fcaffa8f551b082fe2f0e4c31822ecca2a962c63807b746d8b4afdcd8`。
- Ledger JSONL：逐行解析通过。
- `git diff --check`：通过。

## 未改变

- 整体黑盒、UI、API 和发布回归继续采用 reviewer 已接受的 N/A。
- 未新增 Web、数据库、API、客户生产系统或代码仓库设计。
