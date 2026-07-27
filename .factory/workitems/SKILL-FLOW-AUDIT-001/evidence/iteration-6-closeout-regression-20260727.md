# SKILL-FLOW-AUDIT-001 关闭回读回归

- 时间：`2026-07-27T19:35:00+08:00`
- status：`root_cause_found`
- implementation_performed：`false`

## 复现

同一冻结 37 节点在本轮初次运行时为 `37 passed`。关闭事件写入后重新运行：

```text
1 failed, 36 passed
```

失败节点：

`test_all_work_skills_reference_the_shared_return_contract_once`

断言对象：`skills/stratix-service/SKILL.md`。

该文件修改时间为 `2026-07-27 19:28:21`，不属于冻结的 8 个候选 Skill。末行由标准
完整合同句变成缩短句，导致精确合同计数从 1 变为 0。

## 根因

最小验收修订只冻结了 8 个候选 Skill 的哈希，却把会读取全部工作 Skill 的
`test_remaining_skill_project_status_contract.py` 整文件纳入冻结套件。测试输入没有随
候选一起冻结，因此范围外 Skill 的并行修改能够在人工确认后改变 Gate 结果。

## 边界

没有修改或回退 `stratix-service`，也没有把其并行改动纳入本工作项。先等待根因人工
确认，再形成“扩范围修正该一行”或“把验收节点收紧为 8 Skill”的修复方案。
