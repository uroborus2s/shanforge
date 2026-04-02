# Intent 回放评估

- 时间：2026-04-02 18:26:58
- 总样本：7
- 通过：7
- 失败：0
- 命中率：100.00%
- 状态：`success`

## 结果

- `intent-empty-init`：通过 | 动作：`init` | 工具：`codex` | safe：`policy_denied`
- `intent-historical-onboarding`：通过 | 动作：`historical-project-onboarding` | 工具：`codex` | safe：`policy_denied`
- `intent-managed-docs-upgrade`：通过 | 动作：`docs-standard-upgrade` | 工具：`opencode` | safe：`success`
- `intent-managed-next-step`：通过 | 动作：`state-doctor` | 工具：`gemini` | safe：`success`
- `intent-managed-design-kickoff`：通过 | 动作：`command-profiles` | 工具：`codex` | profile：`design-kickoff`
- `intent-managed-daily-profile`：通过 | 动作：`command-profiles` | 工具：`codex` | profile：`daily-close` | safe：`policy_denied` | approval_request：`pending_approval`
- `intent-managed-daily-workflow`：通过 | 动作：`workflow-runner` | 工具：`codex` | workflow：`daily_close` | safe：`policy_denied` | approval_request：`pending_approval`

## 下一步

- 继续增加回放样本，覆盖更多自然语言变体。

## 对话摘要

- 状态：success
- 总样本：7
- 通过：7
- 失败：0
- 命中率：100.0
- 摘要：intent 回放通过 7/7，命中率 100.00%。
