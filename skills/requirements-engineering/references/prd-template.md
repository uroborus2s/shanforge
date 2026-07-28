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

## 需求分析

- analysis_mode: embedded
- analysis_locator: `prd.md#需求分析`
- 需求优先级与依赖：
- 可行性与关键约束：
- 风险与未决问题：
- 对设计与测试的影响：

跨域、高风险、依赖复杂或需要独立评审时，把 `analysis_mode` 改为
`standalone`，并将 `analysis_locator` 指向独立 `requirements-analysis.md`。

## 目标

用 2-4 句说明要解决的问题、目标用户和业务价值。

## 非目标

- 明确本轮不做什么。
- 避免把后续扩展混入当前任务。

## 需求列表

用户故事建议格式：

```markdown
作为 <角色>，我希望 <功能>，以便 <价值>
```

INVEST 检查：

- Independent：不依赖其他故事即可实现。
- Negotiable：表达意图，不写成实现合同。
- Valuable：能说明用户或业务价值。
- Estimable：开发团队能评估工作量。
- Small：一个迭代内可完成。
- Testable：有明确验收标准。

优先级：

- P0：必须，没有则产品不可用。
- P1：应该，核心体验所需。
- P2：可以，后续增强。

```markdown
REQ-XXX: <一句话需求>
- 优先级：P0 | P1 | P2
- 状态：draft | approved | changed
- 说明：<必要业务约束>
- AC-1: 给定 <前置条件>，当 <动作>，则 <可观察结果>
- AC-2: 给定 <异常条件>，当 <动作>，则 <错误或恢复结果>
```

AC 示例：

```markdown
REQ-001: 用户登录
- AC-1: 给定已注册用户，当输入正确邮箱和密码并点击登录，则跳转到首页并显示用户名。
- AC-2: 给定已注册用户，当输入错误密码 5 次，则账户锁定 15 分钟。
```

## 非功能需求

NFR 必须有可度量目标，例如响应时间、吞吐量、认证方式、恢复时间、兼容环境或数据规模。兼容性可以写成“支持目标浏览器与版本”，不要只写“兼容主流浏览器”。

```markdown
NFR-XXX: <可度量的非功能目标>
- 类型：性能 | 安全 | 可用性 | 兼容性 | 可维护性
- 指标：<明确阈值或验收信号>
- 验证：<测试、review 或运行证据>
```

NFR 示例：

```markdown
NFR-001: 登录接口性能
- 类型：性能
- 指标：P95 响应时间小于 200ms
- 验证：压测报告或集成测试记录
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
