# 项目管理控制面集成方案

**项目名称：** shanforge
**文档状态：** 草案实施中
**主要读者：** 项目负责人 | 流程总控 | Skill 维护者 | Reviewer | QA
**上游输入：** 项目管理 Excel 模板理念 | `.factory/workitems/` | `.factory/memory/` | Superpowers 流程集成方案
**下游输出：** `.factory/pm/` 项目管理控制面 | 人类 HTML 状态页 | 流程总控读取规则
**最后更新：** 2026-07-05

## 1. 核心判断

项目管理 Excel 模板不应被当作新事实源照搬进仓库。它真正有价值的是一套管理逻辑：

1. 先定义项目目标、验收标准、假设和约束。
2. 再把目标拆成 WBS，而不是直接进入零散任务。
3. 每个工作包必须有责任人、审批人、辅助人和知会对象。
4. 风险在执行前登记，不能等失败后才解释。
5. 沟通、会议、状态报告形成固定节奏。
6. 范围、成本、进度和资源变化必须走变更记录。
7. 项目结束必须复盘目标、成本、时间、交付结果和经验。

这些规则适合成为 shanforge 的项目管理控制面。它不替代 AI 开发闭环，而是让人类能快速看清项目是否可控。

## 2. 与当前流程的关系

当前 shanforge 已经有执行闭环：

```text
using-shanforge
  -> project-memory
  -> brainstorming / requirements / writing-plans
  -> executing / subagent-driven-development
  -> requesting-code-review / receiving-code-review
  -> verification-before-completion / systematic-debugging
  -> human confirmation
  -> memory sync
```

项目管理控制面位于这条链路之上：

```text
PM 控制面
  -> 目标、WBS、里程碑、风险、变更、状态报告、人类看板

AI 执行闭环
  -> work item、plan、task brief、evidence、review、verification、ledger
```

两层通过 `work_item_id` 连接。

PM 控制面回答：

- 当前项目目标是什么。
- 当前 WBS 拆到哪些工作包。
- 每个工作包处于什么状态。
- 哪些风险、变更、阻塞和人工确认正在影响项目。
- 下一个管理动作是什么。

AI 执行闭环回答：

- 当前任务怎么实现。
- 哪些文件被修改。
- 哪些测试、评审和验证证据已经产生。
- 是否允许把任务推进到下一状态。

## 3. `.factory/pm/` 定位

`.factory/pm/` 是项目管理控制面的事实层。
HTML 是按需生成的展示结果，不是新的事实源。

```text
.factory/pm/
  README.md
  dashboard.md
  team-raci.md
  project-brief.md
  wbs.md
  milestones.md
  risk-register.jsonl
  communication-plan.md
  meeting-notes/
  status-reports/
  change-register.jsonl
  closure-report.md
  generated/status-dashboard.html
```

职责划分：

| 文件 | 职责 | AI 默认读取 |
|---|---|---|
| `dashboard.md` | 人类和 AI 都能快速读取的项目管理压缩视图 | 是 |
| `team-raci.md` | 角色、责任、审批、协作和知会关系 | 按需 |
| `project-brief.md` | 项目目标、范围、约束和验收口径 | 按需 |
| `wbs.md` | WBS 到 work item 的映射 | 按需 |
| `milestones.md` | 阶段里程碑和当前进度口径 | 按需 |
| `risk-register.jsonl` | 风险台账 | 按需 |
| `communication-plan.md` | 沟通对象、频率、渠道和触发条件 | 按需 |
| `meeting-notes/*.md` | 会议决议、行动项和影响 | 按需 |
| `status-reports/*.md` | 周期状态报告 | 按需 |
| `change-register.jsonl` | 变更台账 | 按需 |
| `closure-report.md` | 复盘和项目总结 | 按需 |
| `generated/status-dashboard.html` | 人类浏览器状态页，不作为事实源 | 否 |

`generated/status-dashboard.html` 只服务人类快速查看。
AI 不默认读取 HTML，因为 HTML 包含展示噪音。
生成模板放在 `skills/using-shanforge/references/status-dashboard-template.html`。

## 4. Excel 十表到 shanforge 的映射

| Excel 管理表 | shanforge 落点 | 说明 |
|---|---|---|
| 项目组成员 | `.factory/pm/team-raci.md` 或项目角色摘要 | 记录负责人、审批人、辅助人、知会人 |
| 项目策划 / 任务书 | `docs/04-project-development/01-governance/project-charter.md` + `.factory/pm/dashboard.md` | 正式目标进文档，当前摘要进 dashboard |
| WBS | `.factory/pm/wbs.md` + `.factory/workitems/<ID>/` | WBS 只管工作包，执行细节进 work item |
| 进度计划 | `.factory/pm/milestones.md` 或 dashboard 里程碑区 | 先用里程碑，不急着做复杂甘特图 |
| 风险管理 | `.factory/pm/risk-register.jsonl` | 风险是结构化台账 |
| 沟通计划 | `.factory/pm/communication-plan.md` | 记录谁需要什么信息、频率、渠道 |
| 会议纪要 | `.factory/pm/meeting-notes/` | 只记录决议、行动项和影响 |
| 状态报告 | `.factory/pm/status-reports/` | 周期性管理汇总 |
| 变更管理 | `.factory/pm/change-register.jsonl` | 变更必须关联影响和审批 |
| 项目总结 | `docs/04-project-development/09-evolution/retrospective.md` + `.factory/pm/closure-report.md` | 正式复盘进入演进文档 |

## 5. 流程接入规则

### 5.1 会话开始

`using-shanforge` 的项目恢复顺序调整为：

1. 读取 `.factory/memory/runtime-brief.md`。
2. 读取 `.factory/memory/current-state.md`。
3. 读取 `.factory/pm/dashboard.md`。
4. 读取当前 work item 的 `ledger.jsonl`。
5. 只在需要时读取 `.factory/pm/wbs.md`、风险台账或变更台账。

这样人类管理状态进入流程总控，但不会迫使 AI 读取全部项目管理长文档。

### 5.2 计划阶段

`writing-plans` 产出 work item plan 后，PM 控制面只记录管理摘要：

- WBS 编号。
- work item ID。
- 当前状态。
- 计划输出。
- 关键依赖。
- 目标完成门。

实现步骤、代码路径、测试命令仍留在 `.factory/workitems/<ID>/plan.md`。

### 5.3 执行阶段

执行类 skill 不直接维护 PM 状态页。它们只写：

- work item ledger。
- evidence。
- report。
- review brief。
- memory summary。

PM 控制面由 `using-shanforge` 在需要时从这些产物汇总。
工作 skill 不关心 PM 状态页，也不决定下一环节。

### 5.4 评审、验证和人工确认

PM 控制面必须区分四种状态：

| 状态 | 含义 |
|---|---|
| `ready_for_review` | 实现者完成，等待独立评审 |
| `approved` | reviewer 通过，但不等于人工确认 |
| `pending_human_confirmation` | 等待人工确认能否进入下一阶段 |
| `human_approved` | 人工确认通过 |

这能避免把 reviewer 的技术通过误当成人类项目确认。

### 5.5 变更和风险

出现以下情况必须更新 PM 控制面：

- 用户改变目标、范围、流程或验收要求。
- 发现 skill 不按流程执行。
- 发现模板、reference、测试或 review 存在系统性缺口。
- 任务重复执行、上下文压缩失真或读文档范围失控。
- 任何工作项从 `approved` 回退到 `changes_requested`。

## 6. 人类 HTML 状态页

人类查看不应去翻 JSONL、ledger 和多层 Markdown。应提供一个静态 HTML 看板：

```text
.factory/pm/generated/status-dashboard.html
```

页面定位：

- 首页给项目负责人看。
- 不作为事实源。
- 可以直接用浏览器打开。
- 由 `using-shanforge` 在人类要求查看项目状态时按需生成。
- 使用 `skills/using-shanforge/references/status-dashboard-template.html` 模板。
- 按 `skills/using-shanforge/references/pm-dashboard-rendering.md` 的读取规则渲染。

首版页面应包含：

1. 项目摘要：项目名、阶段、更新时间、总体状态。
2. 管理门禁：计划、执行、评审、验证、人工确认、PR / 提交。
3. WBS / work item 表：ID、目标、状态、下一动作、证据。
4. 风险区：风险等级、影响、责任人、缓解措施、状态。
5. 变更区：变更原因、影响范围、审批状态。
6. 最近状态报告：本轮完成、未完成、阻塞、下一步。
7. 链接区：跳转到 work item、evidence、review、正式文档。

设计原则：

- 用表格和状态徽标，不用长篇叙述。
- 默认展示当前项目状态，历史细节折叠。
- 状态颜色只表达管理语义：正常、待评审、待人工确认、阻塞、高风险。
- 页面可离线打开，不依赖服务端。

## 7. Skill 边界

不新增单独的 `project-management` skill。

原因：

- `using-shanforge` 已经是流程总控。
- PM 状态页只是总控的按需视图。
- 新增 skill 会让流程入口变多，增加维护成本。
- 工作 skill 应只完成专业任务并回写状态。

固定边界：

- `using-shanforge`：判断当前环节、读取 PM 事实、渲染人类状态页。
- `.factory/pm/`：保存 PM 事实和生成结果。
- `skills/using-shanforge/references/`：保存 HTML 模板和渲染规则。
- 工作 skill：只写 output、evidence、report、ledger 和状态包。
- Reviewer：只判断技术质量，不代替人工项目确认。

## 8. 当前实施切片

当前先落最小可用切片：

1. 新增本方案文档。
2. 新增 `.factory/pm/dashboard.md`。
3. 新增 Excel 十表对应的 PM 事实文件。
4. 新增 `.factory/pm/generated/status-dashboard.html`。
5. 新增 `using-shanforge` 的 HTML 模板和渲染规则。
6. 新增风险和变更台账。
7. 将本方案加入开发过程导航和 memory 摘要。

暂不做：

- Excel 双向导入导出。
- 甘特图编辑器。
- 数据库存储。
- 独立前端应用。
- 自动生成器脚本。
- 新增项目管理专用 skill。

如果 HTML 生成变成高频重复工作，再把确定性渲染逻辑做成 `using-shanforge` 的 helper code。
