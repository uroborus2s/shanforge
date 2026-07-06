# 远端 PR / push / merge handoff

本文件定义 Shanforge 本地提交之后的最小远端 handoff 契约。它不替代 `gitcommitzh`，也不把远端动作塞进本地提交 skill。

## Owner

- 流程 owner：`using-shanforge`，只负责判断是否可以进入远端 handoff、状态词是否准确、evidence 是否齐备。
- 本地提交 owner：`gitcommitzh`，只负责本地 commit，不负责创建、推送或合并 PR。
- 远端执行 owner：可用的 Git/GitHub 工作流、Codex App 原生控件、GitHub app / `gh` / `git push` 操作者，或用户指定的人类 owner。

## 输入

- work item ID、任务范围和允许提交/远端操作的文件范围。
- 本地 commit hash、当前分支、远端名称和目标 base branch。
- review 结论、verification evidence、memory sync evidence 和 `human_approved`。
- PR 标题/正文或更新说明；merge 还需要目标 PR URL 或编号。

## 本地提交前提

- `gitcommitzh` 已完成当前任务范围内的本地提交，并记录真实 commit hash。
- 当前 work item ledger、review ledger、verification evidence 和 memory sync 已齐备。
- 无 `next_required_action`、`changes_requested`、`pending_human_confirmation` 或未解决 blocker。
- 若当前 checkout 无法 push 或创建 PR，必须转为 handoff，不得冒充远端已完成。

## 可用远端工具

- Codex App 原生 Create branch / push / PR 控件。
- GitHub app 或 GitHub plugin workflow。
- `gh pr create`、`gh pr view`、`gh pr merge` 等 GitHub CLI 命令。
- `git push`。
- 用户明确指定的人类远端执行流程。

使用任何工具前都要确认权限、目标分支和目标仓库。工具不可用时输出 `remote_handoff_blocked`。

## Evidence

远端 evidence 至少包含实际观察到的其中一组：

- push：remote、branch、commit hash、命令或工具结果、exit code。
- PR 创建/更新：PR URL 或编号、head branch、base branch、commit hash、工具结果。
- merge：PR URL 或编号、merge commit / squash commit / rebase commit hash、合并方式、工具结果。
- handoff：handoff owner、handoff 输入包、未执行原因、用户可执行下一步。

没有这些 evidence 时，不得使用 `remote_push_done`、`remote_pr_opened` 或 `remote_merge_done`。

## 失败语义

- `remote_handoff_blocked`：本地前提、权限、远端目标或工具缺失，尚未尝试远端动作。
- `remote_failed`：已尝试远端动作但失败，必须记录命令/工具、exit code 或错误摘要。
- `remote_conflict`：远端分支、PR 或 merge 出现冲突，需要人工或后续修复。
- `remote_checks_failed`：PR checks 失败，不能合并。

失败状态不是完成状态；只能说明下一步阻塞或交接。

## 状态词

- `remote_handoff_ready`
- `remote_handoff_blocked`
- `remote_push_done`
- `remote_pr_opened`
- `remote_pr_updated`
- `remote_merge_done`
- `remote_failed`
- `remote_conflict`
- `remote_checks_failed`

## 禁止冒充规则

- 禁止把本地 commit 写成 push、PR 或 merge 已完成。
- 禁止把 dry-run、计划、PR 描述草稿或建议命令写成远端 evidence。
- 禁止在没有 PR URL / 编号时声明 PR 已创建。
- 禁止在没有真实远端工具结果和 commit hash 时声明已推送。
- 禁止在没有 merge evidence 时声明已合并。
- 禁止让 `gitcommitzh` 承担远端 PR / push / merge owner。
