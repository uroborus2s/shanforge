# PR 闭环与提交检查清单

用于把 Shanforge work item 的 review、verification evidence、memory sync 和本地提交连接起来。

本清单只约束提交前检查。它不创建、不推送、不合并 PR。

## 输入

- work item ledger：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`
- review ledger：`.factory/memory/review-ledger.jsonl`
- review package：`.factory/workitems/<WORKITEM-ID>/reviews/`
- verification evidence：`.factory/workitems/<WORKITEM-ID>/evidence/`
- implementer report：`.factory/workitems/<WORKITEM-ID>/reports/`
- 当前任务 diff：`git diff -- <files>`
- 暂存区 diff：`git diff --cached -- <files>`
- 暂存区文件清单：`git diff --cached --name-only`

## 提交前必须确认

- 先重读当前 work item ledger 最新事件和 review ledger。`next_required_action` 为 `none` / `无` 时表示无后续动作；以 `create_exact_local_commit`、`create_local_commit` 或 `commit_current_scope` 开头时表示已进入提交转换，提交动作不是未解决动作。仅其他非空动作或阻塞状态会停止提交或完成声明。
- work item ledger 能说明当前状态。
- review package 存在，且阻塞级 review feedback 已处理。
- 真实独立 review 的 `reviewer_type / reviewer_id / reviewer_independence_evidence` 已记录。
- `approved` 只表示 reviewer 通过，不等于 `human_approved`。
- 若状态是 `pending_human_confirmation`，必须看到用户明确确认，或同轮明确要求继续提交。
- verification evidence 是本轮新鲜结果，包含命令、exit code、失败数量和真实输出摘要。
- 代码、文档、测试和 `.factory/memory/` 已同步。
- 同一 `.factory/memory/` 文件混有其他任务条目时，只能暂存当前任务 hunk；无法拆分时停止并拆成独立提交。
- 提交范围只覆盖当前任务相关文件。
- 排除无关脏改动、临时文件、其他 work item 产物和未核实生成物。

## Git 范围检查

提交前至少读取：

```bash
git status --short
git diff --stat
git diff --cached --stat
git diff -- <files>
git diff --cached -- <files>
git diff --cached --name-only
```

规则：

- 只使用明确文件列表暂存当前任务范围。
- 不使用会扩大范围的 `git add -A`。
- 未追踪文件必须先读取内容或 staged diff。
- 同一文件有 staged 与 unstaged diff 时，默认只提交 staged 内容。
- 无法判断范围时停止，不推测提交。

## 提交后回写

提交成功后回写或报告：

- commit hash。
- 实际提交信息。
- 纳入提交的文件列表。
- 未纳入的工作区改动。
- work item ledger 的提交事件。
- `.factory/memory/change-summary.md`、`tasks.summary.md`、`tests.summary.md` 的最新摘要。

## 禁止

- 禁止把本地 commit 描述成 PR 已合并。
- 禁止用提交替代 review、verification 或人工确认。
- 禁止把未确认的 reviewer approved 当作提交闭环依据。
