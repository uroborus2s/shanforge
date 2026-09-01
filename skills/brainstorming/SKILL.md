---
name: brainstorming
description: "创造性工作进入需求、设计、计划或实现前使用；基于 shanforge 当前阶段、work item 状态和用户意图，澄清范围、比较方案、形成可审阅 brief 或设计输入。"
---

# 头脑风暴

把一个想法收敛成可进入需求、设计或计划的输入。它只负责创意澄清、方案探索、设计批准前的输入质量。

## 核心原则

- 先看当前阶段和 work item，再决定是否需要头脑风暴。
- 没有项目化意图时，只做会话澄清或轻量分析；不落盘、不创建 work item、不写 ledger。
- 不把所有请求强行转换成从零开始的设计流程。
- 不靠提示词硬门控项目流转；流转依据是 `.factory/memory/`、work item 状态、ledger 和用户批准。
- 设计未获批准前，不得把同一个 work item 推进到计划或实现。
- 如果 work item 已在 `PLAN`、`IMPLEMENTATION`、`TESTING` 或更后阶段，只在出现新增范围、重大歧义或用户要求重新设计时使用本 skill。

## 上下文输入边界

本 skill 默认**不直接展开读取项目背景文件清单**。

优先使用当前对话、`project-memory` 输出的会话卡、当前 work item brief 和 ledger 中已经压缩过的信息。若这些输入已经能说明当前阶段、work item、用户目标和禁止动作，不再读取 `.factory/memory/` 源文件。

上下文不足时，先交给 `project-memory` 恢复最小会话卡，而不是在本 skill 里重复读取：

```text
阶段：<stage>
工作项：<WORKITEM-ID 或 none>
已读摘要：<summary names>
禁止动作：<do-not-repeat / do-not-skip gates>
相关输入：<brief / ledger / direct files>
```

只在以下情况才增量读取文件：

- 当前 work item 已知，且需要查看 `.factory/workitems/<WORKITEM-ID>/brief.md` 或 `ledger.jsonl`。
- 用户本轮直接要求修改或核对某个文件。
- 会话卡明确指出某个 summary 存在事实缺口。
- 需要把已批准的头脑风暴结果写回对应 summary。

读取前先说明原因和预期产出。不得为了“稳妥”读取 `role-charter.project.md`、`doc-map.md`、`project.json`、`current-state.md`、`tasks.summary.md` 等一组背景文件。需要正式事实时，由 `project-memory` 的相关性判断门按单文件回源。

## 触发判断

使用本 skill：

- 用户提出新功能、新产品、新组件、新交互、新流程或行为修改。
- 当前 work item 还没有清晰目标、范围、非目标或成功标准。
- 需求、设计或计划前发现关键假设未确认。
- 实现中出现范围变化，需要回到用户意图层重新确认。
- 用户直接要求 brainstorming、头脑风暴、方案比较、先想清楚。

不要使用本 skill：

- work item 已有批准的 brief、计划和测试策略，用户只是要求继续执行。
- 用户要求修复已定位 bug，且问题不涉及需求重定义。
- 用户只要求代码评审、提交、运行测试、同步记忆或解释现有事实。
- 当前应该由 `project-memory` 恢复上下文，或由 `writing-plans` / 实现类 skill 执行已批准计划。

## 工作项状态判断

| 当前状态 | 本 skill 动作 | 状态回写 |
|---|---|---|
| 无项目化意图的一次性分析 | 直接输出轻量澄清、方案比较或建议 | `status: done`；`needs: none`；不落盘 |
| 无 work item 或仅有一句话想法 | 澄清目标、约束、成功标准；形成 work item brief 草稿 | `status: needs_user_input`；`needs: work_item_registration` |
| `BRAINSTORM` 或 brief 不完整 | 一次一个问题补齐 brief；提出 2-3 个方案 | `status: needs_user_input \| ready_for_review`；`needs: approval \| review` |
| 已有 brief，缺需求结构 | 不重启头脑风暴；记录需求结构缺口 | `status: ready_for_review`；`needs: requirements` |
| 已有需求，缺设计决策 | 只澄清设计分歧；记录设计缺口 | `status: ready_for_review`；`needs: design` |
| 设计已批准，缺计划 | 不继续提问；记录计划缺口 | `status: ready_for_review`；`needs: plan` |
| 已在实现或测试 | 只处理范围变更；否则退出并说明无需头脑风暴 | `status: blocked \| needs_user_input`；`needs: none \| scope_decision` |

流程路由由 `using-shanforge` 根据阶段、work item 状态和 ledger 判断。本 skill 只回写 brief、批准状态、outputs、evidence、ledger_event 和 `needs`。

## 默认流程

1. **确认状态**：基于会话卡或当前输入说明阶段、work item、是否需要头脑风暴；缺上下文时先交给 `project-memory`。
2. **识别范围**：如果请求包含多个独立子系统，先建议拆成多个 work item。
3. **一次一个问题**：优先选择题；问题聚焦目的、约束、成功标准或关键决策。
4. **提出 2-3 种方案**：先给推荐方案，再说明权衡。
5. **展示设计或 brief**：简单任务写成短 brief；复杂任务分架构、组件、数据流、错误处理、测试和文档同步。
6. **取得用户批准**：只把会改变目标、范围、验收或不可逆取舍的关键选择合并为一次用户确认；普通章节确认不得制造 Gate。
7. **落盘**：按“文件保存位置”写入 work item、正式文档和 memory。
8. **自审**：检查占位、矛盾、歧义、范围漂移和未同步项。
9. **状态回写**：输出状态回写包，包含 brief、批准状态、产物路径、证据、ledger_event 和 `needs`。

## 文件保存位置

首选 work item 目录：

```text
.factory/workitems/<WORKITEM-ID>/
  brief.md
  ledger.jsonl
  design-assets/
    brainstorm/<SESSION-ID>/
```

保存规则：

- 小改动和单个功能的头脑风暴结果写入 `.factory/workitems/<WORKITEM-ID>/brief.md`。
- 过程事件、用户批准、视觉选择和状态回写事件写入 `.factory/workitems/<WORKITEM-ID>/ledger.jsonl`。
- 项目级发现、产品定位或全局范围变化，优先更新当前 work item brief；确需成为正式事实时，由 `project-memory` 按目标项目 `.factory/memory/doc-map.md` 的 owner 映射回源并更新对应正式页面，同时同步根导航和文档索引。
- 需要正式需求时，把 `needs` 标记为 `requirements`，由流程总控决定后续处理。
- 需要正式设计时，把 `needs` 标记为 `design`，由流程总控决定后续处理。
- 视觉探索中间文件放在 `.factory/workitems/<WORKITEM-ID>/design-assets/brainstorm/<SESSION-ID>/`。
- 被采纳的真实设计交付物登记到 `.factory/memory/doc-map.md` 指向的设计文档或其资产目录，并刷新 `.factory/memory/design-assets.summary.md`。
- 目标项目尚无正式文档映射时，先由 `document-templates` 建立最小文档布局和登记，再写正式产物；不得从本 skill 硬编码目录结构。

## Brief 模板

```markdown
# <WORKITEM-ID> Brief

## 目标

## 非目标

## 背景与当前状态

## 用户意图

## 方案比较

## 已批准方案

## 成功标准

## 影响范围

## 需要同步的文档、测试和 memory

## 未决问题
```

## 自审清单

落盘后快速检查：

1. 是否还有 `TBD`、`TODO`、占位章节或含糊词。
2. 目标、非目标、方案、成功标准是否互相矛盾。
3. 范围是否适合一个 work item；不适合就拆分。
4. 需求是否可能被两种方式理解；若是，选定一种并明写。
5. 是否写清批准状态、产物路径、证据、ledger_event、`needs` 和未决问题。
6. 是否同步 `.factory/memory/tasks.summary.md`、`current-state.md` 或相关 summary。

作者自检不能把状态推进到 `approved` 或 `done`。涉及 skill、流程或代码改动时，只能推进到 `ready_for_review`，再交给独立 reviewer。

## 可视化伴侣

可视化伴侣是浏览器辅助工具，不是默认模式。

只在用户看图比读文字更容易理解时提供，例如界面稿、布局、架构图、流程图或视觉方案对比。概念问题、范围问题、文本方案比较和技术权衡继续在终端处理。

第一次确实需要视觉表达时，单独发送：

> 接下来这部分可能看图更清楚。我可以边聊边在浏览器标签页里做界面稿、图表和对比。它会把临时文件保存到当前 work item 的 design-assets 目录，也可能消耗较多上下文额度。要我打开吗？

这条消息必须单独发送。用户同意后，继续前先读 [可视化伴侣](visual-companion.md)。

## 状态回写包

```text
工作结果：
- work_item: <WORKITEM-ID 或 待登记>
- skill: brainstorming
- status: ready_for_review | needs_user_input | blocked
- brief: <summary 或 .factory/workitems/<WORKITEM-ID>/brief.md>
- approval:
  - approved: <yes/no>
  - points: <批准点或 none>
- outputs:
  - <brief/docs/memory paths>
- evidence:
  - <conversation summary 或 evidence paths>
- ledger_event: <.factory/workitems/<WORKITEM-ID>/ledger.jsonl event id 或 path>
- needs:
  - work_item_registration | approval | requirements | design | plan | review | none
```

## 关键纪律

- 一次只问一个问题。
- 能用选择题就用选择题。
- 方案比较必须有推荐和理由。
- 坚持 YAGNI，不把未请求功能塞进设计。
- 保留用户明确批准的决策，不在后续自行改写。
- 发现当前阶段、work item 或 ledger 与对话记忆冲突时，以 `.factory/memory/`、ledger、git 事实和 evidence 为准。
- `needs` 只是状态回写，不是 skill 路由决策；流程路由由 `using-shanforge` 判断。

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
