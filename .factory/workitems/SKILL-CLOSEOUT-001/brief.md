# SKILL-CLOSEOUT-001

## 目标

收口已独立批准 Skill 候选在后续共享事实更新后暴露的两处非隔离验收回归，不回滚新任务事实，不扩大到其他未归属 Skill。

## 已确认根因

1. `tests/test_project_test_governance.py` 把 `FLOW-TASK-013` 候选误写成整行唯一值，无法容纳后续合法候选并存。
2. `tests/test_project_memory_skill.py` 把当前活跃工作项硬编码为 `FLOW-CONTRACT-001 / FLOW-TASK-*`；后续 EAD 状态同步同时遗漏固定历史回源入口。

用户已于 2026-07-27 明确确认以上根因。

## 边界

- 保留 `PROJECT-ARTIFACTS-001` 与 EAD 当前业务状态。
- 只修验收隔离和 current-state 固定回源合同。
- 不修改 `docs/06-delivery/test-plan.md`、EAD ledger、其他 Skill、产品代码或远端状态。
- 实施前等待用户确认修复任务。
