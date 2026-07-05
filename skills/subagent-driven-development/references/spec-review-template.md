# Spec Review

用于确认实现是否完全符合 task brief。目标是防止做少、做多或做错。

## Inputs

- 完整 task brief：
- Implementer report：
- evidence：
- 相关 diff：
- 相关文件：

## 核心规则

- 不要相信实现报告。
- 读取实际 diff。
- 读取实际代码和测试。
- 对照 task brief 逐项核查。
- 只判断是否符合规格，不先做代码审美判断。

## 检查项

- 缺失需求：是否有 task brief 要求但未实现的内容。
- 额外工作：是否加入未要求的功能、抽象、路径或行为。
- 误解需求：是否解决了相似但错误的问题。
- 验收证据：evidence 中的命令和结果是否真实支撑任务。
- 文件范围：是否修改了允许范围外的文件。

## 输出格式

```markdown
## Spec Review

**Status:** approved | changes_requested

**Issues:**
- [file:line] <问题> - <为什么偏离 task brief>

**Verified:**
- <核查过的需求或文件>
```

没有问题时写 `approved`。任何缺失需求、额外工作或误解需求都必须写 `changes_requested`。
