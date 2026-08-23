---
name: requirements-engineering
description: "需求工程技能。用于把想法、work item brief、已批准设计、变更请求或 bug 根因转成可验收的用户故事、验收标准、非功能需求和需求影响分析。"
---

# 需求工程

用于把不完整输入整理成可评审、可追踪、可实现的需求。默认只写当前阶段需要的需求材料，不把草案写成批准事实。

## v1.2.0 运行时路由合同

- `SB-CLARIFY`、`SB-REQUIREMENT` 进入 `requirements-workflow`，`write_policy: project_fact_write`。
- 写入前，route 必须有已存在且非空的 `work_item_id`、`task_card_id`，以及精确 `allowed_paths`、
  `forbidden_actions`、`current_gate`、`write_policy`；只写 allowlist 内需求事实，并追加 ledger 和 evidence。
- 返回 `status`、`outputs`、`evidence`、`ledger_event`、`gate`、`next_required_action`；缺身份、批准输入
  或事实冲突时返回 `blocked` 或 `needs_user_input`。

## 触发

- 一句话需求、work item brief 或已批准设计需要转成可验收需求。
- 需要编写或修正用户故事、验收标准、非功能需求。
- 新增、变更或修复需求需要做 baseline 影响分析。
- 需要把需求同步成 Shanforge 可执行输入。

## 输入

优先使用当前对话和 `project-memory` 会话卡。缺少关键信息时，读取：

- `.factory/workitems/<WORKITEM-ID>/brief.md`
- `.factory/workitems/<WORKITEM-ID>/ledger.jsonl`
- 相关 `.factory/memory/*summary.md`
- 必要时按 `.factory/memory/doc-map.md` 单文件回源正式文档

## 输出位置

- 需求草案或 brief：`.factory/workitems/<WORKITEM-ID>/brief.md`
- 正式 PRD：用户指定路径，或 `.factory/memory/doc-map.md` 为 PRD 登记的正式路径；尚无登记的新项目先由 `document-templates` 建立最小布局和映射
- 任务 ledger：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`
- Memory summary：`.factory/memory/prd.summary.md`、`.factory/memory/tasks.summary.md`

未获用户确认的需求只能写成 `draft`、`requirements_ready` 或 `ready_for_review`，不得写成已批准事实。

## 轻量分析与项目化任务

需求工程有两种执行形态：

- **轻量需求分析**：用户只要会话里的结构化答案；不创建任务卡、不写 ledger、不更新 memory。
- **项目化需求任务**：需求来自 WorkItem、系统拆分、后续设计 / 开发 / 测试输入，或需要跨会话追踪；必须创建任务卡并保存产物。

两种形态的输出契约一致，至少覆盖：

- 目标
- 用户角色
- 主流程
- 异常流程
- 业务规则
- 安全 / 权限要求
- 验收标准
- 未决问题

项目化需求任务额外写清任务 ID、父 WorkItem、状态、依赖、产物路径、ledger event 和后续任务。

## 四类场景

- `new_project`：先形成 Project baseline 输入包，再写第一批需求；没有 baseline 时不得直接拆实现任务。
- `add_requirement`：写 Requirement 输入包，并做 baseline 影响分析。
- `change_requirement`：定位原 Requirement，按需求版本规则追加版本历史，再做影响分析。
- `fix_bug`：先由调试结果判定事实 owner。只有业务目标、范围或验收标准错误才变更 Requirement；设计错误回设计，
  实现错误回代码，测试预期错误回测试。不得把每个 Bug 自动升级成需求变更。
- bug 需求必须先有复现和根因；缺少任一项时保持调查状态，不进入需求批准。

## 必写分析

需求分析载体：

- 分析内容始终必做；每次项目化需求工程都声明
  `analysis_mode = embedded | standalone` 和可回读的 `analysis_locator`。
- `embedded`：默认把依赖、优先级、可行性、风险和设计/测试影响写入 PRD
  的“需求分析”章节或已批准需求包，并把章节路径写入 `analysis_locator`。
- `standalone`：跨域、高风险、依赖复杂或需要独立评审时，生成
  `requirements-analysis.md`，并把文件路径写入 `analysis_locator`。
- Gate 校验分析内容和定位，不按固定文件名判断需求分析是否完成。

需求版本规则：

- 新增需求默认从 `0.1.0` 草稿开始。
- 变更需求必须保留原需求事实，不直接覆盖旧结论。
- 修改正式需求时必须追加版本历史，写明变更原因、日期、作者、审核和批准状态。
- reviewer `approved` 和用户 `human_approved` 前，不得把需求状态写成已批准。

baseline 影响分析：

- 判断是否影响领域边界、总体架构、数据库、API 或 UI baseline。
- 有影响时输出 baseline 变更建议，并反向关联当前需求。
- 无影响时写明 `无 baseline 影响`。

领域模块映射：

- 需求必须映射到一个或多个领域模块。
- 涉及数据库、API 或跨模块交互时，必须写清模块 owner 和接口边界。
- 不能绕过领域模块直接改数据库、API 或 UI baseline。

## 按需模板

一句话需求、已批准设计或 work item brief 需要转成 PRD 时，读取 [PRD 模板](references/prd-template.md)。

模板里承接：

- 用户故事和 INVEST 检查。
- AC 写法和示例。
- P0 / P1 / P2 优先级。
- NFR 类型、示例和可度量目标。
- `.factory/memory/prd.summary.md` 摘要规则。

## Shanforge 默认流程

1. 确认需求来源、场景类型和 work item id。
2. 区分事实、假设和待确认问题。
3. 写用户故事、REQ、AC、NFR、非目标和风险。
4. 选择 `analysis_mode`，写 `analysis_locator`，完成需求分析。
5. 写需求版本规则、baseline 影响分析、领域模块映射和 baseline 变更建议。
6. 用模板中的检查项确认需求可测试。
7. 标记未确认项；不清楚时输出 `needs_user_input`。
8. 按 PRD 模板或 work item brief 路径保存产物。
9. 同步 `.factory/memory/prd.summary.md` 和 `.factory/memory/tasks.summary.md`，只写已观察到的事实。
10. 向 `.factory/workitems/<WORKITEM-ID>/ledger.jsonl` 写入需求事件。
11. 输出状态包，只写 `needs`，不决定下一步 skill。

## 状态边界

- `requirements_ready` 表示需求内容已足够进入评审或计划输入核查。
- `ready_for_review` 表示已产出正式 PRD 或可审阅需求包，等待独立 review。
- 两者都不是 `approved`，也不是用户确认。
- 本 skill 可以输出 `requirements_ready`、`ready_for_review`、`needs_user_input` 或 `blocked`。
- 本 skill 不得把工作项写成 `approved`、`done`、`human_approved`。
- 需求未确认时，不得进入计划或实现口径。

状态包格式：

```text
工作结果：
- work_item: <ID>
- skill: requirements-engineering
- status: requirements_ready | ready_for_review | needs_user_input | blocked
- outputs:
  - .factory/workitems/<WORKITEM-ID>/brief.md
  - <用户指定或 .factory/memory/doc-map.md 登记的正式 PRD 路径>
- evidence:
  - <requirements checklist or review note>
- ledger_event: <event id>
- needs:
  - user_confirmation | review | plan | none
```

`needs` 只是状态回写，不是下一步 skill 决策。流程路由由 `using-shanforge` 判断。

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
