# 项目压缩运行卡

- 生成时间：2026-07-19 08:36:54
- 负责人：uroborus
- 项目：shanforge
- 当前阶段：DESIGN R020 FORMAL DESIGN RELEASED / POST-RELEASE VERIFIED
- 当前模式：cli_direct
- 技术画像：抽象 Agent 平台规划画像
- 技术栈：Python 3.14+ / uv / Markdown docs / .factory memory / typed contracts / settings-layer composition
- 活跃工作项：2
- 阻塞项：0
- 开放风险：0
- 最近交接包：`.factory/workitems/FLOW-CONTRACT-001/task-briefs/TASK-DESIGN-001-ai-collaboration-workflow-design.md`
- 最近快照：R020 已由 `uroborus` 批准完整内容并正式发布。49 项事务激活，docs 37/7，真实离线 pytest 287/287，Ruff/CAS/syntax/diff check 通过；第 3/8 步“设计重基线”完成，无开放人工 Gate。Git、远端和部署未执行。
- 备注：Hermes-inspired abstract agent platform

## AI 最小读取顺序

1. 先读本文件 `/.factory/memory/runtime-brief.md`
2. 再读 `/.factory/memory/role-charter.project.md`
3. 再读 `/.factory/memory/doc-map.md`
4. 再读 `/.factory/project.json`、`/.factory/memory/project-index.md`、`/.factory/memory/current-state.md`
5. 再读 `/.factory/memory/motivation-state.md`、`/.factory/memory/autonomy-rules.md`、`/.factory/memory/evolution-baseline.md`
6. 再读当前阶段相关 summary；禁止默认直读阶段 `docs/`
7. 只有当 summary 不足以支撑当前任务时，才允许按 `doc-map.md` 单文件回源正式文档

## 当前阶段优先摘要

- `.factory/memory/traceability.summary.md`
- `.factory/memory/graph/traceability.json`

## 当前焦点

- 本节首项为当前有效焦点：`FLOW-CONTRACT-001 / TASK-DESIGN-001 / R020-G001` 已正式发布并完成发布后验证；下一动作由流程总控基于正式 R020 进入下一项目阶段。下列 R010 条目仅为历史压缩背景。

- 当前正式需求基线是 `docs/04-project-development/03-requirements/prd.md` `v3.1.0`；正式需求矩阵为 `v3.1.0`，文档索引为 `v1.1.0`。
- `TASK-REQ-002-R014` 已获独立 AI 复审 `approved / 100` 和 `uroborus` 人工批准，`REQ-CHANGE-WF-CTL-010-001` 已完整并入原 `WF-CTL-010`。
- R014 固定项目进度查询的确定性快照、代码生成会话摘要/HTML/十表 Excel、事实资格、状态与派生算法、AI 工具计划、137 字段、权限、性能和跨格式验收。
- 受控下游入口：`.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-REQ-002-R014-release-manifest.json`；清单绑定冻结机器合同、人工批准和正式版本，已批准人工候选归档后默认禁止读取。
- `TASK-DESIGN-001-P006` 计划 SHA-256 `bdeff4bb6c06f61329e1f9f423f4d1dba165082ec8141d974d7706191bbe3c5e`；同一独立 AI Reviewer Popper 复审 `approved / 96`，P005 六项问题全部关闭。
- 用户已批准 P006 精确哈希；R008 工作包 A 至 F 已完成，Catalog 为 4006 条记录和 77 条需求覆盖。
- Reviewer Arendt 对 R009 的只读复审为 `changes_requested / 66`，确认 5 项关闭并独立复现 `I-003`、`I-006` 两个验证假通过。
- R010 精确校验 13 条 canonical edge、9 个 ActionSpec 上游引用和 11 个接口；56 个 fixture 由 56 个 evaluator 执行 183 条语义断言，69 个 mutation 各有唯一 operator、目标和已发布语义探针绑定。
- R010 56/56、69/69、9 个定向攻击、全部旧 profile、需求影响、158 项暂存发布和三处失败恢复通过。
- 当前状态 `design_ready_for_same_reviewer_rereview`。下一动作由 AI 冻结最终四哈希并交同一 Reviewer Arendt 只读复审；通过后停在人类四哈希确认门。
- 当前会话未提交、未 Push、未创建 PR、未 Merge、未部署；PR 仍须用户单独明确批准。

## 必要时回源的正式文档

- `docs/04-project-development/03-requirements/prd.md`
- `docs/04-project-development/10-traceability/requirements-matrix.md`
- `docs/04-project-development/10-traceability/document-index.md`

## 必守规则

- 不跳阶段。
- 代码类工作必须走 PR 闭环后再关单。
- 任何已接受变更都要同步代码、文档、测试、`.factory/memory/`。
- 遇到阻塞、空转或质量漂移时，优先交回 `using-shanforge` 判断唯一下一步，并由对应 skill 产出状态、证据和 `needs`。
- 发现问题时优先做模式级修复，再把有效做法沉淀到 `evolution-baseline.md`。
- 任务单位是人天，最小精度 0.5，但不是默认拆分步长。
- 禁止默认把阶段 `docs/` 列入“先读”。
- 禁止每次开工都全文读取 `docs/`、`user-guide`、演进长文或设计长文。
- 禁止跳过 `.factory/memory/*` 而直接回源人类文档。
- 禁止把正式文档回源候选理解为默认运行时输入。
- 禁止把 skill 当成动作注册表或命令目录；流程路由由 `using-shanforge` 判断，旧中心命令和全局流程脚本已退场。
- 进入实现前必须回源核对 `docs/04-project-development/04-design/technical-selection.md` 的正式事实。

## 当前推荐动作

- 先用 `project-memory` 恢复最小上下文、当前 work item 和 ledger。
- 再交给 `using-shanforge` 判断唯一下一步 skill。
- 若要提交，必须先满足 review、verification、memory sync 和人工确认，再使用 `gitcommitzh`。
