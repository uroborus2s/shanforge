# Iteration 6 隔离关闭门修复阻塞证据

- Work item：`SKILL-FLOW-AUDIT-001`
- Task：`iteration-6-hermetic-closeout-repair`
- 时间：`2026-07-27T20:05:00+08:00`
- 状态：`blocked`

## 验证目标

确认 8 个冻结候选是否都有只读取候选、共享回写合同或当前 WorkItem 固定输入的
现有独立 pytest 节点。

## 新鲜检查

```bash
rg -l 'agent-harness-construction|article-writing' tests
uv run pytest --collect-only -q tests/test_skill_flow_process_audit.py
```

真实结果：

- `agent-harness-construction` 与 `article-writing` 的行为断言只存在于
  `test_prompt_review_target_skills_have_work_item_status_packages`。
- 该节点还读取 `doc-coauthoring`、`algorithmic-art`、`shadcn` 和
  `ui-ux-pro-max`，因此不是冻结 8 Skill 的隔离输入。
- pytest 收集成功，`6 tests collected`，没有两个候选各自的专属节点。

## 已满足候选

- `using-shanforge`
- `frontend-patterns`
- `tdd-workflow`
- `art-asset-pipeline`
- `requesting-code-review`
- `ai-first-engineering`

上述候选已有只读自身或共享合同的现有节点。

## 结论

批准方案的异常流程明确规定：候选缺少现有独立测试节点时停止，不得用全仓或聚合
测试替代。当前不修改 `tests/**`，也不把聚合节点伪装成隔离门。
