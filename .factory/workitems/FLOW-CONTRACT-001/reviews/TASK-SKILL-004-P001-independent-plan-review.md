# TASK-SKILL-004-P001 独立计划评审

- reviewer：`/root/task_skill_004_plan_review`
- decision：`changes_requested`
- score：`91 / 100`
- Critical：0
- Important：1
- Minor：1
- UI N/A：accepted

## I-001

计划缺少逐 Skill 专业契约防回退断言；owner 测试可能在误删 status、needs、blocked/needs_user_input 或真实人工/权限语义时仍通过。

## M-001

正式统一任务包使用 `task_id/task_type`，计划工作结果包使用 `skill`；共享 reference 必须解释两者关系，禁止借去重顺手归一化专业输出包。

## 已接受边界

- 精确 32 个范围与同构尾块成立。
- `using-shanforge` 独占状态信封合理。
- Markdown reference 不构成中心 dispatcher/registry/runtime manager。
- 仅可安全分离时执行 `gitcommitzh`。
