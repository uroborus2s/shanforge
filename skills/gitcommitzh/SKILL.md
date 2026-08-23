---
name: gitcommitzh
description: 审查 Git 工作区、暂存区和 diff，按当前任务范围生成中文变更说明和中文 commit message；用户明确授权提交时执行当前分支本地 commit。用户只要草案、明确暂不提交、只允许改文件，或 work item gate 未闭环时，不自动提交。远端 push、PR、merge、分支切换和历史改写不由本 skill 执行。
---

# Git 中文提交

用于把当前 Git 变更整理成可审阅的中文提交说明，并在范围清晰且已授权时执行本地提交。直接用户限制优先于自动提交触发。

## 触发边界

适用于：

- 用户要求总结当前 Git 改动、写中文提交说明或中文 commit message。
- 用户要求“总结后提交”“帮我 commit”“先看 diff 再提交”。
- 用户直接输入 `/gitcommitzh`。
- Shanforge work item 已满足 review、verification evidence、memory sync；只有真实待确认人工 Gate 存在时，才要求 `human_approved`，且用户未要求暂不提交。

不适用于：

- 用户要 push、建 PR、merge、同步远端或发布。
- 用户要创建、切换、删除分支。
- 用户要 `commit --amend`、`rebase`、`squash`、强推或其他历史改写。
- 当前任务仍缺 review、verification、memory sync，或存在尚未满足的真实人工确认 Gate。

gitcommitzh 不负责创建、推送或合并 PR；它只做当前分支本地 commit。远端动作交给对应 Git / GitHub 工作流。

## 分支表

| 场景 | 行为 |
|---|---|
| 只写草案 | 读取 status、diff 事实，输出结构化中文说明和拟写入 message；不执行 `git add` 或 `git commit`。 |
| 已授权提交 | 审查范围，必要时只 `git add -- <明确文件>`，展示最终 message，执行本地 commit，读取真实 hash 和实际 message 后回报。 |
| blocked | 范围不清、gate 缺失、暂存区混入范围外文件、Git 命令失败或用户限制冲突时停止；说明最小补充信息。 |

用户明确说“暂不提交”“只写草案”“只允许写某文件”时，优先级高于自动提交触发。

`/gitcommitzh` 无附加提交意图时默认只写草案；同一条消息含“提交 / commit / 执行提交”时视为已授权提交。

## 参考资料

- [中文提交模板](references/chinese-commit-patterns.md)
- [中文提交说明评审标准](references/commit-message-rubric.md)
- [PR 闭环与提交检查清单](references/pr-closure-checklist.md)

生成标题和正文时，优先沿用仓库最近提交风格；看不出稳定格式时使用 `<type>: <中文简短标题>`。

## PR 闭环与提交前置检查

当提交属于 Shanforge work item 时，提交前必须核对 [PR 闭环与提交检查清单](references/pr-closure-checklist.md)。
提交前必须先核对 work item、review、verification evidence、memory sync；存在真实人工确认 Gate 时再核对用户确认状态。

最小检查：

- 先重读当前 work item ledger 最新事件和 review ledger。`next_required_action` 为 `none` / `无` 时表示无后续动作；以 `create_exact_local_commit`、`create_local_commit` 或 `commit_current_scope` 开头时表示已进入提交转换，提交动作不是未解决动作。仅其他非空动作或阻塞状态会停止提交。
- work item ledger 已能说明当前任务状态、review 结论、verification evidence 和 memory sync。
- `.factory/memory/review-ledger.jsonl` 中的真实独立 review 记录已与 work item ledger 对齐。
- 若 ledger 或 review 显示 `pending_human_confirmation`，必须看到用户明确 `human_approved` 或同轮明确要求继续提交。
- 同一 `.factory/memory/` 文件混有其他任务条目时，只能暂存当前任务 hunk；无法拆分时停止。
- 禁止把未确认的 reviewer approved 当作提交闭环依据。
- 提交范围只包含当前任务相关代码、文档、测试和 `.factory/memory/` 同步文件。
- gitcommitzh 不负责创建、推送或合并 PR。

## 工作流

### 1. 审查范围

至少读取：

- `git status --short`
- `git diff --stat`
- `git diff --cached --stat`
- 本次候选文件的 `git diff -- <files>`
- 已暂存候选的 `git diff --cached -- <files>`

规则：

- 默认只提交当前任务范围，不按整个工作区提交。
- 当前任务范围来自用户本轮要求、指定文件、当前 plan / todo 和 diff 内容。
- 暂存区只能作为候选参考；仍需核查是否属于当前任务。
- 暂存区含范围外文件时停止；不要自行 reset 或重排用户暂存区。
- 同一文件同时有 staged 与 unstaged diff 时，默认只提交 staged 内容。
- 未追踪文件必须先读取内容或 staged diff。
- 禁止默认使用 `git add .`、`git add -A` 或 `git commit -am`。
- 只有用户明确要求“提交全部改动”，或已确认全部改动属于同一任务，才允许考虑全量提交。

### 2. 写中文说明

输出结构：

- 提交范围：纳入文件、排除文件、暂存状态。
- 变更概览：2 到 5 条中文完整句，说明类型和目的。
- 详细改动：按文件或主题说明改了什么、为什么改、影响是什么。
- 风险与验证：只写真实执行过的验证；未执行就写未执行和原因。
- 提交信息：标题、正文、拟写入 Git 的完整 message。

如果后续执行提交，说明中的标题和正文就是唯一 message 来源。

### 3. 执行本地提交

仅在已授权提交且范围清晰时执行：

- 需要暂存时，只运行 `git add -- <明确文件列表>`。
- 提交前读取 `git diff --cached --name-only`，确认暂存区与本次范围一致。
- 先展示“最终写入 Git 的提交信息原文”，再执行非交互式 `git commit`。
- `git commit` 必须逐字复用已展示的标题和正文。
- 提交后读取 `git rev-parse --short HEAD` 和 `git log -1 --format=%B`。
- 只有拿到真实短 hash 和实际 message 后，才能输出“已提交”。

禁止在本 skill 内创建、切换、删除分支，禁止 push、PR、merge 和历史改写。

## 输出模板

未提交时：

```md
## 提交范围
- ...

## 变更概览
- ...

## 详细改动
- `path/to/file`: ...

## 风险与验证
- 风险：...
- 验证：...

## 提交信息
- 类型：...
- 标题：...
- 正文：...

### 拟写入 Git 的提交信息原文
标题：
<拟写入标题原文>

正文：
<拟写入正文原文>
```

已提交时：

```md
## 提交结果
- 状态：已提交
- 提交号：<真实短 hash>
- 纳入文件：...

### 最终写入 Git 的提交信息原文（提交前已展示，提交后回显）
标题：
<最终写入标题原文>

正文：
<最终写入正文原文>

### Git 实际提交信息回显
标题：
<Git 中实际写入的标题>

正文：
<Git 中实际写入的正文>
```

Shanforge 状态包：

```text
工作结果：
- work_item: <WORKITEM-ID or none>
- skill: gitcommitzh
- status: committed | draft_only | blocked | needs_user_input
- outputs:
  - <commit hash or message draft>
- evidence:
  - <git status/diff/log 命令摘要>
- ledger_event: <event id or none>
- needs:
  - none | user_input | review | verification | human_confirmation
```

## blocked 语义

`blocked` 表示本地提交不能安全执行或不能安全生成最终结论，例如：

- 提交范围无法和当前任务对应。
- 暂存区含范围外内容。
- work item、review、verification evidence、memory sync 缺失，或真实人工 Gate 所需的 `human_approved` 缺失。
- 用户直接限制与自动提交触发冲突。
- hook、权限、冲突或 Git 命令失败。

blocked 时输出已读取事实、阻塞原因和需要用户补充的最小信息。不要输出“已提交”样式的结果区块。

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
