# PM 看板按需渲染

本文件供 `using-shanforge` 在人类要求查看项目状态时读取。

## 原则

- 不新增独立 `project-management` skill。
- `using-shanforge` 已是流程总控，直接负责按需生成状态看板。
- `.factory/pm/` 保存事实。
- `references/status-dashboard-template.html` 保存 HTML 模板。
- `.factory/pm/generated/status-dashboard.html` 是生成结果，不是事实源。

## 读取

按需读取：

1. `.factory/pm/dashboard.md`
2. `.factory/pm/project-brief.md`
3. `.factory/pm/team-raci.md`
4. `.factory/pm/wbs.md`
5. `.factory/pm/milestones.md`
6. `.factory/pm/risk-register.jsonl`
7. `.factory/pm/change-register.jsonl`
8. `.factory/pm/communication-plan.md`
9. `.factory/pm/meeting-notes/`
10. `.factory/pm/status-reports/`
11. `.factory/pm/closure-report.md`
12. `.factory/workitems/*/ledger.jsonl`

## Excel 十模块

| 模块 | PM 文件 |
|---|---|
| 项目组成员 | `.factory/pm/team-raci.md` |
| 项目策划 / 任务书 | `.factory/pm/project-brief.md` |
| WBS | `.factory/pm/wbs.md` |
| 进度计划 | `.factory/pm/milestones.md` |
| 风险管理 | `.factory/pm/risk-register.jsonl` |
| 沟通计划 | `.factory/pm/communication-plan.md` |
| 会议纪要 | `.factory/pm/meeting-notes/` |
| 状态报告 | `.factory/pm/status-reports/` |
| 变更管理 | `.factory/pm/change-register.jsonl` |
| 项目总结 | `.factory/pm/closure-report.md` |

## 输出

默认生成：

```text
.factory/pm/generated/status-dashboard.html
.factory/pm/generated/pm-details.html
.factory/pm/generated/workitems.html
```

链接规则：

- 首页链接必须指向渲染后的 HTML 视图，不直接打开 `.md`、`.jsonl` 原文。
- 首页必须包含项目甘特图、项目任务看板、评审链路总览、WBS 和 PM 十模块入口。
- 项目甘特图显示任务推进阶段，不作为工时估算事实。
- 项目任务看板至少区分：待独立评审、待人工确认、已通过 / 切片通过、后续 / 风险。
- 评审链路总览必须按任务、轮次、评审类型、结果、评分、下一动作展示，并链接到 work item 详情页内的评审锚点。
- Excel 十模块标题链接到 `generated/pm-details.html#<module>`。
- WBS / work item 链接到 `generated/workitems.html#<workitem-id>`。
- 风险标题链接到 `generated/pm-details.html#risks`。
- 变更标题链接到 `generated/pm-details.html#changes`。
- 状态报告、会议纪要和项目总结链接到 `generated/pm-details.html` 对应锚点。
- PM 详情页和 work item 详情页内部把源路径作为文字展示，不作为默认点击目标。
- Work item 详情页必须把每个任务渲染成任务摘要、事件时间线、评审链路和评审结果详情。
- 每一轮评审结果必须有人能读懂的结论、评分、阻塞项、修复状态和下一 gate；禁止只展示原始 JSONL 或 Markdown 文本。
- 使用相对链接，保证 `file://` 方式打开时可跳转。

生成后只把路径返回给人类。AI 后续仍读 `.factory/pm/dashboard.md` 和台账，不读 HTML。
