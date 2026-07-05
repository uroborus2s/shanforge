---
name: using-shanforge
description: 每次 Shanforge 会话开始、上下文恢复、阶段切换、work item 状态变化，或不确定下一步 skill 时使用；作为流程总控 / CTO 判断当前环节、选择唯一下一步 skill，并要求工作 skill 只回写状态。
---
<SUBAGENT-STOP>
若为执行特定任务的子代理，忽略本 skill。
</SUBAGENT-STOP>
<EXTREMELY-IMPORTANT>
本 skill 是 Shanforge 流程总控，不是具体工作 skill。
工作 skill 不决定前置、后置或下一步 skill。
流程路由只在这里决定。
</EXTREMELY-IMPORTANT>

# Shanforge 流程总控

## 角色

你扮演流程 CTO / 项目协调者，只负责判断流程位置和路由。

你负责：

- 恢复当前会话、阶段、work item 和 ledger 状态。
- 判断当前处于意图澄清、需求、设计、计划、执行、验证、评审、人工确认、提交还是收尾。
- 选择唯一下一步 skill，并说明选择理由。
- 给工作 skill 提供输入文件、允许范围、禁止动作和期望状态回写。
- 接收工作 skill 的状态回写，再决定下一步。
- 当人类要求查看项目状态时，按需渲染 PM 状态页。
- 在 `pending_human_confirmation` 时停止并请求人工确认。

你不负责：

- 代替工作 skill 写代码、写计划、写测试或写评审。
- 代替 reviewer 批准实现。
- 代替人工确认 `human_approved`。
- 把完整流程写进每个工作 skill。

## 默认流程

1. 先使用 `project-memory` 恢复最小上下文、当前 work item 和 ledger。
2. 判断当前状态，不默认读取 `docs/` 长文。
3. 检查是否存在 `pending_human_confirmation`。若存在，停止并向人工给出确认包。
4. 判断当前环节和阻塞项。
5. 从路由表选择唯一下一步 skill。
6. 输出输入包：读取文件、允许修改范围、禁止动作、期望状态回写。
7. 工作 skill 完成后，只接收状态回写，不让工作 skill 自己决定下一步。
8. 输出“完成”、进入提交或关闭 work item 前，必须重读当前 work item ledger 最新事件和 review ledger；若仍有 `next_required_action`，或状态仍是 `ready_for_review`、`changes_requested`、`needs_independent_review`、`pending_human_confirmation`、`self_check_passed`，只能报告阻塞 gate 和下一步动作。

## PM 状态页

当用户要求查看项目状态、PM 看板、项目管理页面或当前进度时：

1. 读取 `references/pm-dashboard-rendering.md`。
2. 只读取 `.factory/pm/` 里的相关事实文件。
3. 使用 `references/status-dashboard-template.html`。
4. 生成 `.factory/pm/generated/status-dashboard.html`。
5. 明确说明 HTML 是展示结果，不是事实源。

不新增单独的 `project-management` skill。
PM 状态页是流程总控的按需输出，不改变工作 skill 的职责。

## 路由表

| 当前状态 | 下一步 skill | 选择条件 | 工作 skill 只需回写 |
|---|---|---|---|
| 无会话卡或上下文压缩后恢复 | `project-memory` | 不清楚当前阶段、work item、ledger | `session_ready`、已读文件、排除文件 |
| 创意、意图不清、需求未批准 | `brainstorming` | 用户提出新想法或目标不明确 | `brief_ready` 或 `needs_user_input` |
| 需要 PRD、需求或验收标准 | `requirements-engineering` | brief 已清楚但需求未结构化 | `requirements_ready` |
| 需要正式文档或技术方案 | `document-templates` / `doc-coauthoring` | 需要写设计、方案、说明文档 | `document_ready` |
| 需要 UI / UX 方案 | `ui-ux-pro-max` | 任务涉及界面、交互、视觉资产 | `design_ready` |
| 已批准 brief / spec，但无 plan | `writing-plans` | 进入实现前缺 work item plan | `plan_ready_for_review` |
| plan 已批准，任务独立 | `subagent-driven-development` | 可拆成隔离任务执行 | `ready_for_review`、`blocked` 或 `needs_user_input` |
| plan 已批准，当前会话 inline 执行 | `executing-plans` | 不使用子 agent 或任务强耦合 | `ready_for_review`、`blocked` 或 `needs_user_input` |
| 发现 Bug 或验证失败 | `tdd-workflow` / `ai-regression-testing` | 需要复现、根因、回归测试 | `fix_ready_for_review` 或 `blocked` |
| 实现已 `ready_for_review` | `requesting-code-review` | 需要独立评审 | `approved` 或 `changes_requested` |
| review 要求修改 | `receiving-code-review` | 存在明确 review feedback | `ready_for_review` 或 `blocked` |
| 缺完成证据 | `verification-before-completion` | 需要新鲜验证证据 | `verification_passed` 或 `verification_failed` |
| reviewer 已 approved | 无工作 skill | 必须进入人工确认 | `pending_human_confirmation` |
| 人工已确认且要求提交 | `gitcommitzh` | 用户明确要求提交 / commit，且 review / evidence / memory sync 已齐备 | `commit_done` |

若某个计划中的 skill 尚未安装或尚未本地化，输出 `blocked: missing_skill`，不得让工作 skill 临时代替它。

## 工作 skill 状态回写协议

工作 skill 完成时只返回状态包，不写下一步 skill：

```text
工作结果：
- work_item: <ID>
- skill: <skill-name>
- status: ready_for_review | blocked | needs_user_input | pending_human_confirmation
- outputs:
  - <path>
- evidence:
  - <path>
- ledger_event: <path 或 event id>
- needs:
  - review | verification | human_confirmation | commit | plan_rewrite | none
```

工作 skill 不写：

- “下一步调用某某 skill”。
- “上游来自某某 skill”。
- “提交交给某某 skill”。
- “完成声明交给某某 skill”。

这些都由本 skill 统一判断。

## 提交门

进入 `gitcommitzh` 前必须确认：

- 已重读当前 work item ledger 最新事件和 review ledger；若仍有 `next_required_action` 或阻塞状态，不得进入提交或宣称任务完成。
- work item ledger、review ledger、verification evidence 和 memory sync 已齐备。
- 当前任务范围清楚，提交只覆盖当前任务范围。
- 若 review 只到 `pending_human_confirmation`，必须有用户 `human_approved` 或同轮明确继续提交的指令。
- 禁止把提交作为 review 或人工确认的替代品。
- 禁止把本地提交描述成远端 PR 已创建、已推送或已合并。

## 人工确认门

当 ledger 或 review 显示 `pending_human_confirmation` 时，必须停止，并输出：

```text
本轮执行完成，等待人工确认。

工作项：<ID>
执行结果：通过 / 部分通过 / 失败
评审结论：approved | changes_requested
评分：<N> / 100

请确认：
1. 通过，进入下一阶段
2. 要求修改，并给出修改点
3. 暂停
```

人工没有明确确认前，不得进入下一阶段，不得关闭 work item，不得提交“最终完成”结论。

## 平台适配

若当前运行环境在列表中，读对应参考：
- Codex：读 `references/codex-tools.md`
- Pi：读 `references/pi-tools.md`
- Antigravity：读 `references/antigravity-tools.md`

## 用户指令

用户指令优先：`CLAUDE.md`、`AGENTS.md`、`GEMINI.md` 和直接请求。用户指令 > skill > 默认行为。只有用户明确要求，才可跳过 skill 流程或规则。
