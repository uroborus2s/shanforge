# Prompt Engineering Review Iteration 6

status: ready_for_review
blocked: no

本报告只评审当前工作区实际存在的 `skills/*/SKILL.md`。本轮未修改 skill、测试、ledger 或 memory；唯一写入文件为本报告。评分重点是触发边界、动作边界、输出契约、失败语义、证据要求、review / verification gate、子 agent / tool 边界，以及旧中心流程回退风险。

## 1. 扫描范围

实际扫描 skill 数量：36

完整文件清单：

1. `skills/agent-harness-construction/SKILL.md`
2. `skills/ai-first-engineering/SKILL.md`
3. `skills/ai-regression-testing/SKILL.md`
4. `skills/algorithmic-art/SKILL.md`
5. `skills/api-design/SKILL.md`
6. `skills/art-asset-pipeline/SKILL.md`
7. `skills/article-writing/SKILL.md`
8. `skills/brainstorming/SKILL.md`
9. `skills/browser-control/SKILL.md`
10. `skills/crawler4j-model-project/SKILL.md`
11. `skills/doc-coauthoring/SKILL.md`
12. `skills/document-templates/SKILL.md`
13. `skills/docx/SKILL.md`
14. `skills/executing-plans/SKILL.md`
15. `skills/frontend-patterns/SKILL.md`
16. `skills/gitcommitzh/SKILL.md`
17. `skills/humanizer/SKILL.md`
18. `skills/pdf/SKILL.md`
19. `skills/project-memory/SKILL.md`
20. `skills/python-uv-project/SKILL.md`
21. `skills/receiving-code-review/SKILL.md`
22. `skills/requesting-code-review/SKILL.md`
23. `skills/requirements-engineering/SKILL.md`
24. `skills/shadcn/SKILL.md`
25. `skills/skill-creator/SKILL.md`
26. `skills/stratix-admin-web/SKILL.md`
27. `skills/stratix-service/SKILL.md`
28. `skills/subagent-driven-development/SKILL.md`
29. `skills/systematic-debugging/SKILL.md`
30. `skills/tdd-workflow/SKILL.md`
31. `skills/ui-ux-pro-max/SKILL.md`
32. `skills/using-shanforge/SKILL.md`
33. `skills/verification-before-completion/SKILL.md`
34. `skills/webapp-testing/SKILL.md`
35. `skills/writing-plans/SKILL.md`
36. `skills/xlsx/SKILL.md`

辅助扫描事实：

- `find skills -mindepth 2 -maxdepth 2 -name SKILL.md -print`：36 个主 skill 文件。
- `wc -l skills/*/SKILL.md`：总计 4318 行。
- 旧中心流程扫描未命中 `factory-dispatch`、`factory-workitem-loop-gate`、`scripts/factory-`、`factory-pr-remote`、`REQUIRED NEXT SKILL`、`finishing-a-development-branch` 或 `docs/superpowers`。
- 相对 iteration-5，新增 `skills/art-asset-pipeline/SKILL.md`；总行数从 4601 降到 4318，说明 iteration-5 fixes 的入口压缩真实落地。

## 2. Prompt 评分

平均分：93.5

最低分：89（`agent-harness-construction`、`ai-first-engineering`、`article-writing`）

最高分：96（`systematic-debugging`）

低于 90 分数量：3

| Skill | Iteration 5 | Iteration 6 | Delta | 变化原因 |
|---|---:|---:|---:|---|
| agent-harness-construction | 91 | 89 | -2 | 边界仍清楚；但 Shanforge 状态包缺 `work_item` / `ledger_event`，和本轮修复后的标准不齐。 |
| ai-first-engineering | 91 | 89 | -2 | 建议型内容稳定；状态包仍缺 `work_item` / `ledger_event`，进入 work item 时证据链较弱。 |
| ai-regression-testing | 93 | 94 | +1 | 根因、防回归、多路径一致性和禁止兜底语义完整；状态词与验证类 skill 相容。 |
| algorithmic-art | 90 | 93 | +3 | 已补 Shanforge work item 状态包、`needs_user_input` 和验证要求。 |
| api-design | 95 | 95 | 0 | API 契约、风险分级和验证建议完整。 |
| art-asset-pipeline | N/A | 94 | N/A | 新增 skill；阶段确认、资源清单、证据和清理规则完整。 |
| article-writing | 92 | 89 | -3 | 写作边界清楚；但状态包缺 `work_item` / `ledger_event`，事实核查失败语义也比其他写作类 skill 略弱。 |
| brainstorming | 94 | 94 | 0 | 会话恢复、读取边界、brief、批准和状态回写清楚。 |
| browser-control | 93 | 93 | 0 | 本地浏览器、Browser、Chrome、Computer Use 和 `web.run` 边界清楚。 |
| crawler4j-model-project | 90 | 91 | +1 | 状态包和失败语义完整；主入口仍有较多版本事实和旧命令禁用项。 |
| doc-coauthoring | 89 | 93 | +4 | 已补 Shanforge 状态包、`needs_user_input` 和验证要求；与正式模板文档边界更清楚。 |
| document-templates | 89 | 93 | +4 | 入口已压缩，默认文档包和长模板下沉，最小路径与失败语义清楚。 |
| docx | 94 | 94 | 0 | 文件安全、验证和 partial / blocked 语义完整。 |
| executing-plans | 94 | 94 | 0 | inline 执行、review checkpoint、evidence 和 ledger gate 完整。 |
| frontend-patterns | 93 | 92 | -1 | 前端边界清楚；状态词仍是 `passed/partial/failed/blocked`，与流程总控标准状态略不一致。 |
| gitcommitzh | 88 | 95 | +7 | 已压缩提交门，明确直接用户限制优先；本地 commit 与远端 PR / push / merge 边界清楚。 |
| humanizer | 94 | 94 | 0 | 文本边界、事实安全、写入安全和状态包完整。 |
| pdf | 94 | 94 | 0 | 文件处理分支、权限边界、验证和失败处理完整。 |
| project-memory | 94 | 94 | 0 | 最小读取、事实源优先级和旧中心禁止项稳定。 |
| python-uv-project | 92 | 93 | +1 | Bug owner 已明确交给调试 / TDD；uv 工具链状态包完整。 |
| receiving-code-review | 92 | 94 | +2 | feedback triage、验证、memory sync 和 `needs_user_input` 语义完整。 |
| requesting-code-review | 92 | 95 | +3 | 独立性硬门、N/A 门、review ledger 和人工确认边界完整。 |
| requirements-engineering | 93 | 94 | +1 | 教程内容已下沉，需求状态、baseline 影响和批准边界清楚。 |
| shadcn | 90 | 93 | +3 | 已补 work item 状态包；项目配置、registry、preset 和覆盖策略边界清楚。 |
| skill-creator | 86 | 95 | +9 | 长评估 / benchmark / 打包支线已变成明确请求才进入；旧脚本事实改为先核实。 |
| stratix-admin-web | 91 | 94 | +3 | 与 Stratix service / 普通前端 / UI 评审边界收口，状态包完整。 |
| stratix-service | 88 | 94 | +6 | 生产化矩阵、CLI 细节和加解密细节已下沉，按场景分级验证。 |
| subagent-driven-development | 93 | 95 | +2 | 子 agent 边界、并行 gate、证据、review input 和状态回写完整。 |
| systematic-debugging | 95 | 96 | +1 | 根因调查与修复分离最清楚；人工确认前不进入修复。 |
| tdd-workflow | 94 | 94 | 0 | TDD、根因确认和验证边界完整；有一处重复句但不影响行为。 |
| ui-ux-pro-max | 90 | 93 | +3 | 已补 Shanforge 状态包、`needs_user_input` 和验证要求。 |
| using-shanforge | 95 | 95 | 0 | 流程总控、提交门、远端 handoff 和子代理停止语义清楚。 |
| verification-before-completion | 95 | 95 | 0 | 新鲜命令、完整输出、exit code 和完成声明 gate 完整。 |
| webapp-testing | 94 | 94 | 0 | 与 browser-control 边界清楚，断言、截图、日志和失败语义完整。 |
| writing-plans | 94 | 94 | 0 | 计划、task brief、review handoff 和状态包完整。 |
| xlsx | 94 | 94 | 0 | 电子表格触发窄，写入安全和重读验证清楚。 |

## 3. 低于 90 分明细

### `agent-harness-construction`：89

触发边界：

- 触发范围聚焦 agent harness、工具 schema、观察格式和恢复路径，边界本身清楚。
- 与 `skill-creator` 有轻微重叠：两者都可能处理 prompt / tool / schema 质量；当前文件未明确“写 Codex skill 本身交给 `skill-creator`”。

动作边界：

- 明确不接管 Shanforge 阶段路由、review gate、人工确认和提交流程。
- 输出的是设计或评审包，不直接执行工具改造；这一点清楚。

输出契约：

- Shanforge 状态包缺 `work_item` 和 `ledger_event`。
- `outputs` / `evidence` / `needs` 有，但不能稳定接入 work item ledger。

失败语义：

- `blocked` 定义清楚。
- 缺少 `needs_user_input` 的具体触发例子，例如目标 agent、工具权限或安全边界需用户取舍时如何停。

旧流程风险：

- 未发现旧中心 gate 或旧脚本回退。
- 主要风险是作为 work item owner 时证据链不完整，不是旧流程回退。

### `ai-first-engineering`：89

触发边界：

- 适用于团队工程规则、评审标准、测试策略和协作模式，边界偏建议型。
- 与 `ai-regression-testing`、`requesting-code-review`、`document-templates` 的关系有排除项，但仍可能在“制定评审规则 / 测试规则”时压过更具体 skill。

动作边界：

- 明确不替代实施计划、正式文档、review 或人工确认。
- 作为建议型 skill，不直接写代码和 gate，边界可接受。

输出契约：

- Shanforge 状态包缺 `work_item` 和 `ledger_event`。
- `evidence` 只写“依据”，未要求落到 work item evidence 或审计路径。

失败语义：

- `blocked` / `needs_user_input` 只在同一句里概括，缺少可操作分支。
- 对“可以给局部规则”的 partial 语义表达清楚，但状态包没有 partial。

旧流程风险：

- 未发现旧中心 gate。
- 风险是工作项收口时只能靠外层包装补 ledger，不是流程回退。

### `article-writing`：89

触发边界：

- 长文、博客、指南、教程、时事通讯边界清楚。
- 与 `doc-coauthoring` 在提案、指南、项目说明上仍有轻微重叠；当前靠“不适用正式项目文档”分开，但工作文档和发布文章之间仍需用户意图判断。

动作边界：

- 明确不主动落盘，正式项目文档交给文档类 skill，事实核查不足时停止。
- 但“模仿特定创始人、运营者或品牌语气”需要更明确授权和来源边界，避免和 humanizer 的风格对齐职责混用。

输出契约：

- Shanforge 状态包缺 `work_item` 和 `ledger_event`。
- 交付契约没有标准 verification 字段；事实核查证据只能通过 `evidence` 概括。

失败语义：

- `blocked` 只覆盖关键事实、授权来源、目标读者和法律 / 品牌边界。
- 缺 `needs_user_input` 分支，例如缺目标读者、发布平台、语气参考但可以继续写大纲时应如何回写。

旧流程风险：

- 未发现旧中心 gate。
- 主要风险是进入 Shanforge work item 时状态包不完整。

## 4. 职责冲突或重叠

| Skill 对 | 重叠点 | 当前风险 | 最小边界建议 |
|---|---|---|---|
| `project-memory` vs `using-shanforge` | 会话恢复、work item 状态、ledger | 两者都读状态；子代理可能误进流程总控 | 当前 `using-shanforge` 已有 `SUBAGENT-STOP`，保留；`project-memory` 只恢复事实，`using-shanforge` 只路由。 |
| `using-shanforge` vs `systematic-debugging` / `tdd-workflow` / `ai-regression-testing` | Bug、测试失败、根因、回归 | 路由表的 bug 行未显式写 `systematic-debugging`，可能先触发 TDD 再阻塞 | 根因未知先 `systematic-debugging`；根因已确认后 `tdd-workflow`；防同类回归用 `ai-regression-testing`。 |
| `document-templates` vs `doc-coauthoring` | 技术规范、RFC、项目说明、设计说明 | 正式文档和协作草稿可能混 | 正式目录、模板、版本历史和结构校验归 `document-templates`；非模板化草稿和读者视角改写归 `doc-coauthoring`。 |
| `article-writing` vs `doc-coauthoring` | 指南、提案、长篇说明 | 发布型文章和工作文档可能误触 | 发布型公开长文归 `article-writing`；工作文档协作归 `doc-coauthoring`。 |
| `frontend-patterns` vs `ui-ux-pro-max` | 页面、组件、响应式、交互状态 | 设计质量和实现模式容易同时命中 | 视觉 / UX 判断归 `ui-ux-pro-max`；代码结构、状态管理和组件边界归 `frontend-patterns`。 |
| `frontend-patterns` vs `shadcn` | React / Tailwind 组件实现 | shadcn 项目中两者都能触发 | 有 `components.json`、registry、preset 或 shadcn 组件命令时优先 `shadcn`。 |
| `stratix-admin-web` vs `stratix-service` | Stratix 管理后台 | 前端页面和后端接口 / 配置生产化容易混 | 页面、组件、表格表单归 `stratix-admin-web`；后端接口、DI、配置、release gate 归 `stratix-service`。 |
| `stratix-admin-web` vs `frontend-patterns` / `ui-ux-pro-max` | 管理后台 UI | 普通后台 UI 可能误触 Stratix | 只有明确 Stratix admin 或仓库事实显示 web-admin 时用 `stratix-admin-web`。 |
| `browser-control` vs `webapp-testing` | 打开页面、截图、交互检查 | 一次性真实浏览器操作和可重复回归测试容易混 | 用户要本地浏览器 / Chrome / browser-use / 外部站点用 `browser-control`；localhost 可重复断言用 `webapp-testing`。 |
| `executing-plans` vs `subagent-driven-development` | 执行 approved plan | inline 和子代理执行都读 plan / ledger | 强耦合或不能派发子 agent 用 `executing-plans`；独立任务和同层并行用 `subagent-driven-development`。 |
| `gitcommitzh` vs `using-shanforge` | 提交门、人工确认、远端边界 | 自动提交触发和流程总控提交 gate 重叠 | `using-shanforge` 判断是否进入提交；`gitcommitzh` 只核实并执行本地 commit。 |
| `api-design` vs `requirements-engineering` | API 需求、验收、契约 | API 契约可能被写成需求，或需求替代契约设计 | 需求 owner 写用户价值和 AC；`api-design` 写 endpoint、schema、error、compatibility。 |
| `art-asset-pipeline` vs `algorithmic-art` / `ui-ux-pro-max` | 视觉资产、生成图、UI 视觉 | 美术资源包、代码生成艺术和 UI 评审可能混 | 开发资源包和确认图归 `art-asset-pipeline`；p5.js 代码作品归 `algorithmic-art`；界面质量评审归 `ui-ux-pro-max`。 |
| `python-uv-project` vs `systematic-debugging` / `tdd-workflow` | Python bug、pytest、ruff | Python 工程规范可能抢走根因 owner | Python bug owner 是调试 / TDD；`python-uv-project` 只约束 uv 和工具链。 |
| `agent-harness-construction` vs `skill-creator` | prompt、schema、tool 边界 | harness 评审和 skill 编写可能混 | 代理工具和观察面设计归 `agent-harness-construction`；Codex skill 文本、触发和打包归 `skill-creator`。 |

## 5. 相对 iteration-5 的变化

- 文件数量：35 -> 36。新增 `skills/art-asset-pipeline/SKILL.md`。
- 总行数：4601 -> 4318。长入口压缩有效，尤其是 `gitcommitzh`、`skill-creator`、`stratix-service`、`document-templates`。
- 平均分：92.2 -> 93.5。
- 低于 90 分数量：5 -> 3。
- 最大提升：`skill-creator` 86 -> 95；`gitcommitzh` 88 -> 95；`stratix-service` 88 -> 94。
- `doc-coauthoring`、`algorithmic-art`、`shadcn`、`ui-ux-pro-max` 已补 Shanforge work item 状态包，不再是辅助 owner 一致性缺口。
- `document-templates` 和 `requirements-engineering` 已把教程、模板和示例下沉，主入口更像流程入口。
- `stratix-service` 与 `stratix-admin-web` 的后端 / 前端 owner 边界已收口。
- 旧中心流程风险继续为低：主 skill 扫描未见旧 factory gate、旧远端脚本或旧 superpowers 回退。
- 本轮负向变化来自评分基线变严：iteration-5 fixes 已把多数 work item owner 补齐状态包，因此 `agent-harness-construction`、`ai-first-engineering`、`article-writing` 的 `work_item` / `ledger_event` 缺口更显眼。

## 6. 最小下一步修复清单

只列真正值得改的项：

1. `skills/agent-harness-construction/SKILL.md`：Shanforge 状态包补 `work_item` 和 `ledger_event`；补 `needs_user_input` 例子；明确 Codex skill 写作交给 `skill-creator`。
2. `skills/ai-first-engineering/SKILL.md`：Shanforge 状态包补 `work_item` 和 `ledger_event`；把 `blocked` / `needs_user_input` 分成两个可执行分支。
3. `skills/article-writing/SKILL.md`：Shanforge 状态包补 `work_item`、`ledger_event` 和 verification 字段；补 `needs_user_input` 语义；明确发布型长文与工作文档的边界。
4. `skills/using-shanforge/SKILL.md`：在 bug / 测试失败路由行显式加入 `systematic-debugging`，避免根因未知时先落到 TDD 再反弹。
5. `skills/frontend-patterns/SKILL.md`：若作为 Shanforge work item owner，补 `needs_user_input` 状态或说明 `design_decision` 只作为 `needs` 而非状态。
6. 暂不改 `gitcommitzh`、`skill-creator`、`stratix-service`、`document-templates`：iteration-5 fixes 已达到当前 prompt 质量目标，继续压缩收益低。

## 风险摘要

Critical：无。

Important：

- 3 个辅助 skill 的 Shanforge 状态包仍缺 `work_item` / `ledger_event`，如果直接作为 work item owner，会削弱 ledger / evidence 可追踪性。

Minor：

- bug 路由表未显式列 `systematic-debugging`，但 TDD 本身会在根因未确认时阻止修复，当前不是跳过根因 gate 的风险。
- 少数建议 / 评审类 skill 使用 `passed/partial/failed/blocked`，和流程总控标准状态词存在轻微不一致。
