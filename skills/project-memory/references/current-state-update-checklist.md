# Current State 更新清单

更新 `.factory/memory/` 时只写已观察到的事实。

## 必查

- 本轮真实改动文件。
- 已运行测试和真实结果。
- 已生成 evidence、review 或 ledger 文件。
- 当前 work item 的最新状态。
- 是否存在未提交或用户已有改动。

## 必同步

- 同步 `tasks.summary.md`：任务进展、缺口、下一顺位。
- 同步 `tests.summary.md`：新增测试、验证命令、失败或跳过原因。
- 同步 `skill-updates.summary.md`：skill 规则或结构变化。
- 必要时同步 `change-summary.md`：面向后续会话的变更摘要。
- 必要时同步 `doc-map.md`：新增正式文档或 summary 映射。

## 禁止

- 不要把计划中未执行的动作写成已完成。
- 不要把“准备执行”“应该执行”写成已经通过。
- 不要覆盖与本任务无关的历史事实。
- 不要把临时推测写进 current-state。
- 不要把实现者自评写成 review 通过。

## 推荐记录格式

```markdown
- 2026-07-05：新增 `skills/project-memory/`，将 `factory-agent-session` 的会话恢复、读取范围、ledger 模板和 current-state 更新清单拆入 skill references。新增 `tests/test_project_memory_skill.py` 固定结构约束；定向验证 `<命令>` `<结果>`。
```
