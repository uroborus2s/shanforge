# T04 评审反馈响应

## Fixed

### T04-I1

Fixed. 任务简报提取器现在：

- 识别中文、英文和无显式 `- 任务：` 字段的注册任务简报。
- 规范化 `1. 目标`、`15. 完成定义` 等编号标题。
- 映射 `Goal`、`Inputs`、`Required Outputs`、`Acceptance Criteria`、
  `Verification` 等既有英文标题。
- 对局部 `TASK-SKILL-001` 使用父工作项限定的稳定任务身份，避免不同工作项静默碰撞。
- 将任务简报来源升级为 `markdown-v3`，强制旧贡献重新投影。

Verified:

- 真实注册语料：`138 total / 138 work_item / 138 with_any_semantics`。
- 字段覆盖：`goal=129`、`work_items=64`、`deliverables=71`、
  `completion_conditions=93`、`verification=88`。
- 全量 CLI 快照：`parsed=146`，成功生成 361 个变化页面并复用 1731 个页面。

### T04-I2

Fixed. 删除根据任务标题拼接的三段推测性套话。缺正式任务语义时分别显示：

- 当前任务简报尚未登记任务目的。
- 当前任务简报尚未登记具体工作。
- 当前任务简报尚未登记交付结果。
- 当前任务简报尚未登记完成条件。

Verified:

- `test_task_detail_uses_explicit_missing_states_without_inventing_semantics`：通过。
- 真实 Chrome 桌面和移动端：任务四区块存在，控制台错误为 0。

### T04-I3

Fixed. 两份设计文档恢复前一正式版本，将 T04 内容登记为同文档的未发布候选；审核和批准
字段明确写为待独立复审、待用户确认，不再提前宣告正式发布。

Verified:

- `data-design.md` 正式版本保持 `v1.3.0`，候选版本为 `v1.4.0`。
- `frontend-design.md` 正式版本保持 `v1.5.1`，候选版本为 `v1.6.0`。
- 两个 T04 版本均未进入“正式版本历史（仅已发布）”。

### T04-R2-I1

Fixed. 任务简报和 Ledger 现在共用 `_qualified_task_id`：

- Ledger 同时识别 `task` 与 `task_id`，并读取 `work_item` 作为父级限定范围。
- 局部 `TASK-SKILL-001` 在两侧都投影为
  `FLOW-CONTRACT-001-TASK-SKILL-001` 这类父工作项限定身份。
- 全局 canonical 任务 ID 不改名。
- Ledger 来源升级为 `jsonl-event-v6`，保证旧贡献不会绕过新身份规则。

Verified:

- 新增 SQLite 索引级回归：brief + Ledger 只生成一个实体，状态为 `in_progress`，
  同时含任务简报 `goal`。
- 真实 source registry 注册的 138 份任务简报生成 138 个全局唯一实体 ID，且全部至少
  有一类正式任务语义。
- 项目知识目标回归：`69 passed`。
- 固定 CLI：`parsed=36`、`rendered=23`、`reused=2062`，成功发布最后有效站点。
