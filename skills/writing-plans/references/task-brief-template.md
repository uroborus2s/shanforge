# 任务简报

## 工作项

- 工作项：
- 任务：
- 状态：`draft | ready_for_review | approved | changes_requested`
- 上游计划：
- 流水账：

## 目标

用 1-3 句说明本任务必须完成的可观察结果。

## 输入

- 已批准计划：
- 相关规格 / 需求 / 设计：
- 必读文件：
- 可选参考：

## 允许修改

- `exact/path`

## 禁止修改

- 与本任务无关的文件。
- 用户已有未归属本任务的脏改动。
- 分层边界外的实现。

## 实施步骤

1. 写红灯测试。
2. 运行并确认失败。
3. 写最小实现。
4. 运行并确认通过。
5. 写验证证据。
6. 写实现报告。
7. 更新流水账和记忆摘要。

## 验证命令

```bash
<命令>
```

期望输出：

```text
<期望输出>
```

## 输出报告

- 验证证据：`.factory/workitems/<WORKITEM-ID>/evidence/task-N.md`
- 实现报告：`.factory/workitems/<WORKITEM-ID>/reports/task-N.md`
- 评审输入简报：`.factory/workitems/<WORKITEM-ID>/reviews/task-N-brief.md`
- 流水账事件：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`

## 完成口径

实现者只能写 `ready_for_review`。`approved` 必须来自独立评审。
