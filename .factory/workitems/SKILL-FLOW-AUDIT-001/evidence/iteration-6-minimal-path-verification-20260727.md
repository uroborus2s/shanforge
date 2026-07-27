# Iteration 6 最小路径验证

- 时间：`2026-07-27T18:57:48+08:00`
- status：`passed_ready_for_review`
- 产品失败 / 错误 / 跳过：`0 / 0 / 0`

## 候选与合同

- 8 个整改 Skill 的 SHA-256 与验收修订逐项一致。
- 共享工作 Skill 回写契约 SHA-256 一致。
- WorkItem ledger：99 行 JSONL 可解析，最新事件 E099。
- `git diff --check`：通过。

## 冻结测试

```text
37 passed in 0.06s
All checks passed!
```

命令覆盖：

- 6 个完整相关测试文件；
- `test_work_skill_status_envelope_ownership.py` 的 3 个相关节点；
- 同范围 7 个测试文件的 Ruff。

首次在沙盒内重跑时，`uv` 因无权读取现有缓存失败；按规则在授权的沙盒外重跑，
pytest 与 Ruff 均 exit code 0。

## 旧套件漂移诊断

旧 20 文件清单在当前混合工作区为 `125 passed / 4 failed`。4 项分别属于：

- UI Skill 后续架构变化；
- 共享 memory 的有界当前态；
- 已关闭文档迁移任务的历史投影；
- 正式 workflow 文档后续版本。

这些不是 8 Skill 整改回归。以 HEAD 加局部候选的隔离副本复验，又暴露旧路径已
删除和后续架构未纳入 HEAD 的历史耦合。未修改这些范围外事实，改用验收修订中
冻结的 37 个相关测试节点。

## 结论

最小 Gate 的候选、公式和测试基线已可重放。作者状态为 `ready_for_review`，
仍需独立 reviewer 按冻结公式给出 8 Skill 双维度评分。
