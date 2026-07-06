# PRD 模板

用于把一句话需求或已批准设计转换成可追踪需求。输出可以写入正式 PRD，也可以先写入 `.factory/workitems/<WORKITEM-ID>/brief.md`。

## 标题区

- 项目：
- Work item：
- 状态：draft | ready_for_review | approved
- 来源：用户输入 | brainstorming 规范 | review 反馈 | bug 根因
- 关联文档：

## 版本信息

| 项目 | 内容 |
|---|---|
| 文档编号 |  |
| 文档类型 | 需求文档 |
| 当前版本 | `0.1.0` |
| 当前状态 | draft |
| 最近更新 |  |

## 版本历史

| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `0.1.0` | 初版 |  |  | 待审核 | 待批准 |

## 场景分类

- 场景：new_project | add_requirement | change_requirement | fix_bug
- baseline 影响：无 | 领域 | 架构 | 数据库 | API | UI
- 关联原需求：
- bug 复现与根因：

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

## 领域模块映射

- 领域模块：
- 模块 owner：
- 接口边界：
- 数据库 / API / UI 影响：

## baseline 变更建议

- 是否需要 baseline 变更：
- 变更类型：领域 | 架构 | 数据库 | API | UI
- 建议 work item：
- 反向关联需求：

## 风险

- 事实缺口：
- 依赖：
- 回滚：

## Memory 同步

- 更新 `.factory/memory/prd.summary.md`：只保留 ID、优先级、状态和关键约束。
- 更新 `.factory/memory/tasks.summary.md`：记录进入计划或实现的下一步。
- 不把未批准需求写成已确认事实。
