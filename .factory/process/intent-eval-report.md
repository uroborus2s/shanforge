# Intent 回放评估

- 时间：2026-04-03 19:25:17
- 总样本：13
- 通过：13
- 失败：0
- 命中率：100.00%
- 状态：`success`

## 结果

- `intent-empty-init`：通过 | 动作：`init` | 工具：`codex` | safe：`policy_denied`
- `intent-historical-onboarding`：通过 | 动作：`historical-project-onboarding` | 工具：`codex` | safe：`policy_denied`
- `intent-managed-docs-upgrade`：通过 | 动作：`state-doctor` | 工具：`opencode` | safe：`success`
- `intent-managed-next-step`：通过 | 动作：`state-doctor` | 工具：`gemini` | safe：`success`
- `intent-managed-design-kickoff`：通过 | 动作：`command-profiles` | 工具：`codex` | profile：`design-kickoff`
- `intent-managed-daily-profile`：通过 | 动作：`command-profiles` | 工具：`codex` | profile：`daily-close` | safe：`policy_denied` | approval_request：`pending_approval`
- `intent-managed-daily-workflow`：通过 | 动作：`workflow-runner` | 工具：`codex` | workflow：`daily_close` | safe：`policy_denied` | approval_request：`pending_approval`
- `intent-skill-without-candidate`：通过 | 动作：`skill-delete-approval` | 工具：`codex`
- `intent-skill-next-eval`：通过 | 动作：`skill-eval` | 工具：`codex` | skill：`skills-drafts/intent-governance-coach` | skill_op：`eval`
- `intent-skill-approval-request`：通过 | 动作：`skill-approval` | 工具：`codex` | skill：`skills-drafts/intent-governance-coach` | skill_op：`approval_request`
- `intent-skill-promote`：通过 | 动作：`skill-promote` | 工具：`codex` | skill：`skills-drafts/intent-governance-coach` | skill_op：`promote`
- `intent-skill-delete-approval`：通过 | 动作：`skill-delete-approval` | 工具：`codex` | skill：`skills-drafts/intent-governance-coach` | skill_op：`delete_first_publish`
- `intent-skill-delete-approved-rollback`：通过 | 动作：`skill-rollback` | 工具：`codex` | skill：`skills-drafts/intent-governance-coach` | skill_op：`delete_first_publish`

## 下一步

- 继续增加回放样本，覆盖更多自然语言变体。

## 对话摘要

- 状态：success
- 总样本：13
- 通过：13
- 失败：0
- 命中率：100.0
- 摘要：intent 回放通过 13/13，命中率 100.00%。
