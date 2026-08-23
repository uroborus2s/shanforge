# 事实收口与 GPT-5.6 模型路由实施计划

**目标：** 先获得事实一致、工作区干净、干净克隆全绿的 Shanforge 基线，再由 `gpt-5.6-sol` 统一设计、分级和控制任务，由 `gpt-5.6-terra` 或 `gpt-5.6-luna` 执行授权任务。

**架构：** 复用 `using-shanforge` 作为唯一控制面，不新增运行时。Sol 生成带风险、复杂度、执行模型和理由的路由包；执行 Skill 只消费路由包，Terra/Luna 不得重分级、自授权或自批完成。

**技术栈：** Markdown Skill 合同、JSONL ledger、pytest、Ruff、Git。

**工作项：** `MODEL-ROUTING-001`

**状态：** `plan_ready`

## 输入

- 用户批准目标：先统一事实源和干净基线，再实现 Sol/Terra/Luna 路由。
- 正式架构：`docs/05-design/system-architecture.md`。
- 正式流程：`docs/05-design/workflow-execution-design.md`。
- 当前测试与 Git 工作区。
- Codex 内置 GPT-5.6 模型选择回退资料；官方公开检索未返回三个精确变体页面。

## 范围

### 目标

- 统一当前产品、阶段、活动工作项和验证命令。
- 将现有变更归属为正式产物、可删除历史候选或本地缓存，留下可审计恢复备份。
- 当前工作区与干净克隆使用同一测试命令全绿。
- 固化 Sol 控制、Terra/Luna 执行、失败升级和无越权回退规则。

### 非目标

- 不新增模型网关、服务、数据库、依赖或中心 CLI。
- 不实现价格/配额优化器。
- 不执行远端或生产动作。

## 文件

| 类型 | 路径 | 职责 |
|---|---|---|
| 修改 | `.factory/project.json` | 对齐 skill-first 产品事实和当前阶段 |
| 修改 | `.factory/memory/agent-session.md` | 保存本工作项恢复入口 |
| 修改 | `.factory/memory/current-state.md` | 只保留当前活动任务和真实 Gate |
| 修改 | `.factory/memory/runtime-brief.md` | 对齐正式架构与唯一下一动作 |
| 修改 | `docs/05-design/workflow-execution-design.md` | 保存模型控制与执行正式合同 |
| 修改 | `docs/02-user-guide/user-guide.md` | 说明模型分级和使用边界 |
| 修改 | `skills/using-shanforge/SKILL.md` | Sol 唯一分级与路由 owner |
| 修改 | `skills/using-shanforge/agents/openai.yaml` | 暴露模型路由入口说明 |
| 修改 | `skills/writing-plans/SKILL.md` | 保留而不重算模型路由字段 |
| 修改 | `skills/writing-plans/references/task-brief-template.md` | 登记控制模型、风险、复杂度和执行模型 |
| 修改 | `skills/subagent-driven-development/SKILL.md` | Terra/Luna 只按路由包执行 |
| 测试 | `tests/test_model_tier_routing.py` | 覆盖 Sol/Terra/Luna 正反例和升级规则 |
| 修改 | `tests/test_*.py` | 仅修复已证实的过期合同断言 |
| 工作项 | `.factory/workitems/MODEL-ROUTING-001/**` | 计划、任务、证据、评审和 ledger |

## 任务

### T01：事实源与干净基线

- 目标：事实无冲突、当前工作区全绿、干净克隆全绿。
- 风险：`high`，因为涉及大量历史未提交事实和删除候选。
- 实现：先备份全部待删除未跟踪文件到 `/tmp`，再只保留正式文档、当前 ledger、必要测试夹具和本工作项。
- 验证：`uv run pytest -q`、正式 Ruff 范围、`git diff --check`、临时干净克隆复验。

### T02：Sol 控制与 Terra/Luna 执行

- 目标：Sol 负责总体设计、任务复杂度/风险分级、执行模型选择和升级；Terra/Luna 仅执行。
- 依赖：T01 全绿。
- 风险：`medium`，改变跨 Skill 公共流程合同但不引入运行时。
- Red：新增结构测试，证明当前合同缺少模型身份、确定性规则、执行限制和升级规则。
- Green：最小修改正式流程、`using-shanforge`、任务模板和执行 Skill。
- 验证：`uv run pytest -q tests/test_model_tier_routing.py` 加相邻流程测试。

### T03：集中质量与本地提交

- 目标：当前工作区和干净克隆全绿，独立只读评审无阻断项，精确本地提交后工作区干净。
- 依赖：T01、T02。
- 风险：`medium`。
- 验证：完整 pytest、正式 Ruff、Skill validator、JSONL、`git diff --check`、干净克隆复验。

## 集中质量门

- 计划独立评审：`N/A`；用户已明确架构方向，计划复用现有控制面。
- 批次代码评审：`pending`
- 批次验证：`pending`
- 本地提交：`pending`
- 远端：`not_authorized`

## 计划自审

- 规格覆盖：三项用户目标分别由 T01、T02、T03 覆盖。
- 占位符扫描：无占位交付。
- 可构建性：只使用现有 Markdown、pytest、Ruff 和 Git。
- 批次质量门：仅一套最终证据和评审。
