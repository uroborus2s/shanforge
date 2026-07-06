---
name: requirements-engineering
description: "需求工程方法论技能。指导如何编写高质量的用户故事、验收标准、非功能需求和需求分析。requirements-analyst 代理必须参考此技能。"
---

# 需求工程方法论

## 触发

- 一句话需求、work item brief 或已批准设计需要转成可验收需求。
- 需要编写或修正用户故事、验收标准、非功能需求。
- 需要把需求同步成 Shanforge 可执行输入。

## 输入

优先使用当前对话和 `project-memory` 会话卡。缺少关键信息时，读取：

- `.factory/workitems/<WORKITEM-ID>/brief.md`
- `.factory/workitems/<WORKITEM-ID>/ledger.jsonl`
- 相关 `.factory/memory/*summary.md`
- 必要时按 `.factory/memory/doc-map.md` 单文件回源正式文档

## 输出位置

- 需求草案或 brief：`.factory/workitems/<WORKITEM-ID>/brief.md`
- 正式 PRD：`docs/04-project-development/03-requirements/prd.md` 或用户指定路径
- 任务 ledger：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`
- Memory summary：`.factory/memory/prd.summary.md`、`.factory/memory/tasks.summary.md`

未获用户确认的需求只能写成 `draft` 或 `ready_for_review`，不得写成已批准事实。

## 四类场景和影响分析

- `new_project`：先形成 Project baseline 输入包，再写第一批需求；没有 baseline 时不得直接拆实现任务。
- `add_requirement`：写 Requirement 输入包，并做 baseline 影响分析。
- `change_requirement`：定位原 Requirement，按需求版本规则追加版本历史，再做影响分析。
- `fix_bug`：作为 bug 需求管理；bug 需求必须先有复现和根因，再写修复需求和回归验收。

## 需求版本规则

- 新增需求默认从 `0.1.0` 草稿开始。
- 变更需求必须保留原需求事实，不直接覆盖旧结论。
- 修改正式需求时必须追加版本历史，写明变更原因、日期、作者、审核和批准状态。
- reviewer `approved` 和用户 `human_approved` 前，不得把需求状态写成已批准。

## baseline 影响分析

每个需求都要判断是否影响：

- 领域边界。
- 总体架构。
- 数据库。
- API。
- UI baseline。

有影响时输出 baseline 变更建议，并反向关联当前需求；无影响时写明 `无 baseline 影响`。

## 领域模块映射

- 需求必须映射到一个或多个领域模块。
- 涉及数据库、API 或跨模块交互时，必须写清模块 owner 和接口边界。
- 不能绕过领域模块直接改数据库、API 或 UI baseline。

## 用户故事写作规范

**格式：** 作为 <角色>，我希望 <功能>，以便 <价值>

**INVEST 原则检查：**
- **I**ndependent（独立）：不依赖其他故事即可实现
- **N**egotiable（可协商）：是意图而非合同
- **V**aluable（有价值）：为用户提供业务价值
- **E**stimable（可估算）：开发团队能评估工作量
- **S**mall（小型）：一个迭代内可完成
- **T**estable（可测试）：有明确的验收标准

## 验收标准写作规范

每个 REQ 必须有可测试的验收标准：

```
AC-1: 给定 [前置条件]，当 [操作]，则 [预期结果]
```

**示例：**
```
REQ-001: 用户登录
AC-1: 给定已注册用户，当输入正确邮箱和密码并点击登录，则跳转到首页并显示用户名
AC-2: 给定已注册用户，当输入错误密码 5 次，则账户锁定 15 分钟
AC-3: 给定未注册邮箱，当尝试登录，则显示"账户不存在"提示
```

## 需求优先级定义

| 优先级 | 定义 | 时间要求 |
|--------|------|---------|
| P0 | 必须：没有则产品不可用 | 第一迭代 |
| P1 | 应该：核心体验所需 | 第二迭代 |
| P2 | 可以：锦上添花 | 后续迭代 |

## 非功能需求编写指南

每个 NFR 必须有可度量的目标值：

| NFR 类型 | 应包含 | 示例 |
|---------|--------|------|
| 性能 | 响应时间、吞吐量、并发数 | API 响应 < 200ms (P95) |
| 安全 | 认证方式、加密标准、合规要求 | 密码 bcrypt 加 salt |
| 可用性 | SLA、恢复时间 | 99.9% 月可用性 |
| 可扩展性 | 用户数、数据量增长 | 支持 10 万注册用户 |
| 兼容性 | 浏览器、设备、OS | Chrome 90+, Safari 15+ |

## AI 摘要生成规则

从完整 PRD 生成 `.factory/memory/prd.summary.md` 时：

1. **只保留 ID + 一句话描述 + 优先级 + 状态**
2. **对每个 REQ 保留关键约束**（1-2 行）
3. **保留 NFR 的度量目标**
4. **总行数控制在 100 行以内**
5. **不包含背景描述、示例、详细说明**

## 按需模板

- 一句话需求、已批准设计或 work item brief 需要转成 PRD 时，读取 [PRD 模板](references/prd-template.md)。

## Shanforge 默认流程

1. 确认需求来源、场景类型和 work item id。
2. 区分事实、假设和待确认问题。
3. 写用户故事、REQ、AC、NFR、非目标和风险。
4. 写需求版本规则、baseline 影响分析、领域模块映射和 baseline 变更建议。
5. 用 INVEST 和可测试性检查需求。
6. 标记未确认项；不清楚时输出 `needs_user_input`。
7. 按 PRD 模板或 work item brief 路径保存产物。
8. 同步 `.factory/memory/prd.summary.md` 和 `.factory/memory/tasks.summary.md`，只写已观察到的事实。
9. 向 `.factory/workitems/<WORKITEM-ID>/ledger.jsonl` 写入需求事件。
10. 输出状态包，只写 `needs`，不决定下一步 skill。

## 状态边界

- 本 skill 可以把需求推进到 `requirements_ready`、`ready_for_review`、`needs_user_input` 或 `blocked`。
- 本 skill 不得把工作项写成 `approved`、`done`、`human_approved`。
- reviewer `approved` 和用户 `human_approved` 必须由后续评审和人工确认门产生。
- 需求未确认时，不得进入计划或实现口径。

状态包格式：

```text
工作结果：
- work_item: <ID>
- skill: requirements-engineering
- status: requirements_ready | ready_for_review | needs_user_input | blocked
- outputs:
  - .factory/workitems/<WORKITEM-ID>/brief.md
  - docs/04-project-development/03-requirements/prd.md
- evidence:
  - <requirements checklist or review note>
- ledger_event: <event id>
- needs:
  - user_confirmation | review | plan | none
```

`needs` 只是状态回写，不是下一步 skill 决策。流程路由由 `using-shanforge` 判断。
