# Current State 更新清单

更新 `.factory/memory/` 时只写已观察到的事实。

## 事实源优先级

- 正式文档和 work item ledger 高于 memory summary。
- summary 不复制完整正文；只写 ID、状态、当前 gate、关键约束和索引。
- summary 与正式文档冲突时，以正式文档和 ledger 为准。
- HTML 和 cache 都是非事实投影；不得从 `.factory/cache/site/current/index.html` 反推正式事实。

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

## 非活跃任务降级

- 已关闭任务在下一次 memory sync 从 `current-state.md` 降级到 `tasks.summary.md` 或对应 work item ledger。
- `current-state.md` 只保留活跃任务、真实阻塞项、最近事实、唯一下一动作和历史回源入口。
- 历史回源固定保留 `.factory/workitems/<WORKITEM-ID>/ledger.jsonl` 和 `.factory/memory/tasks.summary.md`；任务专属链接只能追加，不能替代。
- 最近事实最多保留 5 条。
- `current-state.md` 不超过 16 KiB 和 80 行；超过任一阈值必须先压缩。
- ledger、evidence、review 和 report 永不因降级删除；禁止用压缩当前态代替执行审计。

## 条件读取链自查

- 当前对话中的新鲜会话卡足够时，读取 memory 文件数必须为 0。
- 不能只读 `.factory/memory/current-state.md` 就判断权威任务状态。
- 不得固定读取 `agent-session.md`、`runtime-brief.md`、`current-state.md` 三件套。
- 每次扩展读取前先写明事实缺口，一次只读取一个最小片段，够用即停。

## 禁止

- 不要把计划中未执行的动作写成已完成。
- 不要把“准备执行”“应该执行”写成已经通过。
- 不要覆盖与本任务无关的历史事实。
- 不要把临时推测写进 current-state。
- 不要把实现者自评写成 review 通过。

## 推荐记录格式

```markdown
- 2026-07-05：新增 `skills/project-memory/`，将旧会话脚本的会话恢复、读取范围、ledger 模板和 current-state 更新清单拆入 skill references。新增 `tests/test_project_memory_skill.py` 固定结构约束；定向验证 `<命令>` `<结果>`。
```
