# HUMAN-RESPONSE-CONTRACT-003-T01：实现修复定位与代码形状合同

## 状态与路由

- status: `completed`
- workflow_id: `execution-workflow`
- write_policy: `source_or_test_write`
- current_gate: `closed`
- control_model: `gpt-5.6-sol`
- task_complexity: `standard`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- execution_authorized: `true`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- requested_reasoning_effort: `medium`
- fork_turns: `none`

## 允许修改

- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/human-readable-status.md`
- `skills/using-shanforge/references/work-skill-return-contract.md`
- `skills/systematic-debugging/SKILL.md`
- `skills/tdd-workflow/SKILL.md`
- `docs/02-user-guide/user-guide.md`
- `tests/test_skill_progress_visibility_and_continuation.py`
- `tests/test_work_skill_status_envelope_ownership.py`
- `tests/test_verification_debugging_workflow_skills.py`

## 禁止修改

- 其他 Skill、测试、正式文档、其他工作项、memory、Git、远端和生产状态。

## 实现要求

- 修复说明结构化提供 `file`、`symbol`、`change`、`reason`、`verification`；没有函数边界时使用真实模块/配置项/章节。
- 所有 `source_or_test_write` 路由包含：禁止函数/方法体内定义局部函数；禁止抽取只有一个调用点且无独立职责的公共 helper。
- 框架强制入口、接口实现、回调注册或资源生命周期边界不是为了排版拆分的 helper；不得借例外包装一次转发。
- 测试验证字段结构和决策边界，不只匹配标题。

## 验证

```bash
uv run pytest -q tests/test_skill_progress_visibility_and_continuation.py tests/test_work_skill_status_envelope_ownership.py tests/test_verification_debugging_workflow_skills.py
uv run ruff check tests/test_skill_progress_visibility_and_continuation.py tests/test_work_skill_status_envelope_ownership.py tests/test_verification_debugging_workflow_skills.py
```

## 返回

- `ready_for_review | blocked`
- 修改文件、Red/Green、Ruff、diff check 和 concerns；不得提交。

## 实现结果

- Red：`3 failed, 27 passed`；Green：`30 passed`。
- Ruff、限定 diff check：通过。
- `change_locations` 与 `code_shape_check` 已进入总控、共享合同、调试/TDD 和用户指南候选。
