# PRD 模板

用于把一句话需求或已批准设计转换成可追踪需求。输出可以写入正式 PRD，也可以先写入 `.factory/workitems/<WORKITEM-ID>/brief.md`。

## 标题区

- 项目：
- Work item：
- 状态：draft | ready_for_review | approved
- 来源：用户输入 | brainstorming 规范 | review 反馈 | bug 根因
- 关联文档：

## 目标

用 2-4 句说明要解决的问题、目标用户和业务价值。

## 非目标

- 明确本轮不做什么。
- 避免把后续扩展混入当前任务。

## 需求列表

```markdown
REQ-XXX: <一句话需求>
- 优先级：P0 | P1 | P2
- 状态：draft | approved | changed
- 说明：<必要业务约束>
- AC-1: 给定 <前置条件>，当 <动作>，则 <可观察结果>
- AC-2: 给定 <异常条件>，当 <动作>，则 <错误或恢复结果>
```

## 非功能需求

```markdown
NFR-XXX: <可度量的非功能目标>
- 类型：性能 | 安全 | 可用性 | 兼容性 | 可维护性
- 指标：<明确阈值或验收信号>
- 验证：<测试、review 或运行证据>
```

## 影响范围

- 代码：
- 文档：
- 测试：
- `.factory/memory/`：

## 风险

- 事实缺口：
- 依赖：
- 回滚：

## Memory 同步

- 更新 `.factory/memory/prd.summary.md`：只保留 ID、优先级、状态和关键约束。
- 更新 `.factory/memory/tasks.summary.md`：记录进入计划或实现的下一步。
- 不把未批准需求写成已确认事实。
