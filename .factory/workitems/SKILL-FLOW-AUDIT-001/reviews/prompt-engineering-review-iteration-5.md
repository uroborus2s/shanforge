# Prompt Engineering Review Iteration 5

status: DONE
blocked: no

本报告只评审当前工作区实际存在的 `skills/*/SKILL.md`。本轮未修改 skill、测试、ledger 或 memory；唯一写入文件为本报告。分数按当前 prompt 质量重新评分：触发边界、动作边界、输出契约、失败语义、证据要求、旧流程风险，以及是否会自批完成、跳过 review 或跳过验证。

## 1. 扫描范围

实际扫描 skill 数量：35

完整文件清单：

1. `skills/agent-harness-construction/SKILL.md`
2. `skills/ai-first-engineering/SKILL.md`
3. `skills/ai-regression-testing/SKILL.md`
4. `skills/algorithmic-art/SKILL.md`
5. `skills/api-design/SKILL.md`
6. `skills/article-writing/SKILL.md`
7. `skills/brainstorming/SKILL.md`
8. `skills/browser-control/SKILL.md`
9. `skills/crawler4j-model-project/SKILL.md`
10. `skills/doc-coauthoring/SKILL.md`
11. `skills/document-templates/SKILL.md`
12. `skills/docx/SKILL.md`
13. `skills/executing-plans/SKILL.md`
14. `skills/frontend-patterns/SKILL.md`
15. `skills/gitcommitzh/SKILL.md`
16. `skills/humanizer/SKILL.md`
17. `skills/pdf/SKILL.md`
18. `skills/project-memory/SKILL.md`
19. `skills/python-uv-project/SKILL.md`
20. `skills/receiving-code-review/SKILL.md`
21. `skills/requesting-code-review/SKILL.md`
22. `skills/requirements-engineering/SKILL.md`
23. `skills/shadcn/SKILL.md`
24. `skills/skill-creator/SKILL.md`
25. `skills/stratix-admin-web/SKILL.md`
26. `skills/stratix-service/SKILL.md`
27. `skills/subagent-driven-development/SKILL.md`
28. `skills/systematic-debugging/SKILL.md`
29. `skills/tdd-workflow/SKILL.md`
30. `skills/ui-ux-pro-max/SKILL.md`
31. `skills/using-shanforge/SKILL.md`
32. `skills/verification-before-completion/SKILL.md`
33. `skills/webapp-testing/SKILL.md`
34. `skills/writing-plans/SKILL.md`
35. `skills/xlsx/SKILL.md`

辅助扫描事实：

- `wc -l skills/*/SKILL.md`：总计 4601 行。
- 相对 iteration-4，新增 `skills/stratix-admin-web/SKILL.md`。
- 旧中心流程扫描未发现 `factory-dispatch`、`factory-workitem-loop-gate`、`scripts/factory-`、`factory-pr-remote-*`、`REQUIRED NEXT SKILL`、`finishing-a-development-branch` 或 `docs/superpowers` 回归；唯一相关命中是 `project-memory` 中“不得把旧中心命令、动作注册表或全局脚本当成新流程主控”的禁止项。
- `ledger_event` 缺失 12 个 skill；其中 `gitcommitzh`、`skill-creator`、`stratix-service` 更影响 Shanforge 工作项收口。
- `work_item` 缺失 11 个 skill；多数是通用创作或建议型 skill，但进入 work item 时仍会降低状态一致性。
- `blocked` 只在 `project-memory` 主文件中没有明确状态语义；因它主要负责恢复和同步，风险较低。

## 2. Prompt 评分

平均分：92.2

最低分：86（`skill-creator`）

最高分：95（`api-design`、`systematic-debugging`、`using-shanforge`、`verification-before-completion`）

低于 90 分数量：5

| Skill | Iteration 4 | Iteration 5 | Delta | 变化原因 |
|---|---:|---:|---:|---|
| agent-harness-construction | 91 | 91 | 0 | 边界清楚；状态包仍缺 `work_item` / `ledger_event`。 |
| ai-first-engineering | 91 | 91 | 0 | 建议型边界稳定；状态包仍是轻量格式。 |
| ai-regression-testing | 93 | 93 | 0 | 根因、防回归和多路径一致性强；状态词与 Shanforge 工作 skill 不完全统一。 |
| algorithmic-art | 90 | 90 | 0 | 创作边界清楚；仍使用 `done`，缺 work item 状态字段。 |
| api-design | 95 | 95 | 0 | 触发、契约、风险分级和证据要求完整。 |
| article-writing | 92 | 92 | 0 | 写作边界清楚；状态包仍缺 `work_item` / `ledger_event`。 |
| brainstorming | 94 | 94 | 0 | 读取边界、批准边界、状态包和不自选下一步清楚。 |
| browser-control | 89 | 93 | +4 | iteration-4 修复已补标准状态包、`blocked` 和 `needs_user_input`。 |
| crawler4j-model-project | 88 | 90 | +2 | iteration-4 修复已补状态包和失败语义；主入口仍偏长。 |
| doc-coauthoring | 89 | 89 | 0 | 短入口清楚；仍用 `done`，缺标准 Shanforge 状态包。 |
| document-templates | 87 | 89 | +2 | metadata 和状态包已修；默认文档包、模板映射和迁移流程仍压在主入口。 |
| docx | 94 | 94 | 0 | 文件处理分支、写入安全和验证失败语义完整。 |
| executing-plans | 94 | 94 | 0 | inline 执行 gate、review checkpoint 和状态回写完整。 |
| frontend-patterns | 93 | 93 | 0 | 前端实现边界稳定；与 UI/UX、shadcn 仍需靠触发语区分。 |
| gitcommitzh | 88 | 88 | 0 | 本地提交安全门强；自动提交触发和长重复仍未压缩。 |
| humanizer | 94 | 94 | 0 | 文本边界、事实安全和状态包完整。 |
| pdf | 94 | 94 | 0 | 文件安全、验证和失败处理完整。 |
| project-memory | 94 | 94 | 0 | 最小读取和事实源优先级稳定；自身缺明确 blocked 语义但风险低。 |
| python-uv-project | 88 | 92 | +4 | iteration-4 修复已明确 Bug 流程交给调试/TDD，并补状态包。 |
| receiving-code-review | 88 | 92 | +4 | iteration-4 修复已补标准状态包、`blocked` 和 `needs_user_input`。 |
| requesting-code-review | 89 | 92 | +3 | iteration-4 修复已补状态包和失败语义；独立性硬门仍略重复。 |
| requirements-engineering | 93 | 93 | 0 | 场景、baseline、版本和批准边界完整。 |
| shadcn | 90 | 90 | 0 | 组件边界清楚；仍用 `done`，缺 work item 状态字段。 |
| skill-creator | 86 | 86 | 0 | 主入口仍覆盖创建、评审、评估、benchmark、描述优化和打包。 |
| stratix-admin-web | N/A | 91 | N/A | 新增 skill；边界清楚但缺 `ledger_event`，与 Stratix/前端/UI skills 需靠路由区分。 |
| stratix-service | 88 | 88 | 0 | 版本探测强；生产化矩阵、CLI 清单和普通任务默认强度仍过重。 |
| subagent-driven-development | 93 | 93 | 0 | 子 agent 边界、证据、review input 和状态回写完整。 |
| systematic-debugging | 95 | 95 | 0 | 根因先行、停止条件和状态包完整。 |
| tdd-workflow | 94 | 94 | 0 | Red/Green、根因和风险分级验证完整。 |
| ui-ux-pro-max | 90 | 90 | 0 | UI/UX 边界清楚；仍用 `done`，缺 work item 状态字段。 |
| using-shanforge | 94 | 95 | +1 | 新增远端 PR / push / merge handoff 入口，降低本地提交冒充远端闭环风险。 |
| verification-before-completion | 95 | 95 | 0 | 完成声明、exit code、证据和失败语义完整。 |
| webapp-testing | 94 | 94 | 0 | 与 browser-control 边界清楚，失败处理和 evidence 要求完整。 |
| writing-plans | 94 | 94 | 0 | 计划、task brief、review handoff 和状态包完整。 |
| xlsx | 94 | 94 | 0 | 触发窄、文件安全、验证和失败语义完整。 |

## 3. 低于 90 分明细

### `doc-coauthoring`：89

- 触发边界：与 `document-templates`、`article-writing` 仍有重叠，尤其是提案、技术规范、RFC、决策记录和项目说明。
- 动作边界：正文说明“不是模板库，也不是流程总控”是对的；但在 Shanforge work item 中如何进入 review、ledger 或人工确认没有固定边界。
- 输出契约：只写 `status: done | blocked`，没有 `work_item`、`ledger_event`、`needs_user_input` 或 `ready_for_review`。
- 失败语义：只有 `blocked`；缺“事实可补但需要用户确认”的 `needs_user_input` 分支，也缺 partial 语义。
- 证据要求：列了输入文件、用户确认、引用来源、检查记录；但没有要求 evidence 落到 work item 路径。
- 旧流程风险：未发现旧 factory gate；主要风险是 `done` 状态在 work item 中绕过 review 语义。

### `document-templates`：89

- 触发边界：metadata 已中文化且聚焦正式文档体系；仍覆盖章程、需求、架构、API、测试、发布、运维、交接、用户指南等大量文档，容易压过 `doc-coauthoring`。
- 动作边界：正式文档治理规则清楚；但 321 行主入口仍包含默认最小文档包、模板资产映射和迁移流程，长背景压过“按需读取 references”的关键动作。
- 输出契约：iteration-4 修复已补 `work_item` 和 `ledger_event`；但输出路径和校验命令对“只补单页文档”的轻任务仍偏重。
- 失败语义：`blocked` / `needs_user_input` 已清楚；风险是工具校验不可用时容易把文档任务整体阻塞，而不是输出可审阅的局部文档。
- 证据要求：要求 `docs-stratego validate` 或核查说明，证据方向正确。
- 旧流程风险：明确“不再调用旧仓库脚本”；未见旧中心 gate。剩余风险是旧生命周期迁移细节仍在主入口，读感像迁移手册。

### `gitcommitzh`：88

- 触发边界：本地提交触发语很完整；但“代理完成一个产生文件改动的任务且 gate 满足时也必须使用”仍容易与用户临时约束冲突，例如“只写一个文件、不要提交”。
- 动作边界：不 push、不建 PR、不改写历史写得很强；但普通 Git 提交、Shanforge 提交门、slash 直调和提交后回显交织，阅读成本高。
- 输出契约：提交说明和提交结果模板很完整；但作为 Shanforge skill 缺标准 `工作结果` 包，缺 `work_item/status/outputs/evidence/ledger_event/needs`。
- 失败语义：`blocked` 语义完整，范围不清、gate 缺失、hook 失败和暂存冲突都有覆盖。
- 证据要求：diff、cached diff、真实 hash、`git log -1 --format=%B` 等证据要求强。
- 旧流程风险：未发现旧 factory gate；主要风险是提交门与 `using-shanforge` 重复，且自动提交触发若未强调“直接用户约束优先”，会误执行。

### `skill-creator`：86

- 触发边界：同时覆盖创建、修改、改进、评审、评估、benchmark、description optimization 和打包，触发面仍偏宽。
- 动作边界：中文、闭环、隔离评审原则正确；但主入口仍内联测试运行、评分员、查看器、描述优化和打包，容易压过“改一个 skill”的最小路径。
- 输出契约：有状态包，但缺 `work_item` / `ledger_event`；评估产物、review 产物和 benchmark 产物路径不固定。
- 失败语义：`blocked` 定义存在；但目标 CLI 不可用、子 agent 不能运行、`generate_review.py` / `package_skill.py` 不存在、浏览器查看器无法打开时状态不够具体。
- 证据要求：要求测试、eval 或自检记录；但评估脚本、`timing.json`、`grading.json`、`benchmark.json` 是否仍是当前工具事实未被入口核实。
- 旧流程风险：没有旧 factory gate；但 `eval-viewer/generate_review.py`、`package_skill.py`、`.skill` 打包事实像旧工具链，需要核实或下沉 references。

### `stratix-service`：88

- 触发边界：覆盖 Stratix 应用、插件、worker、sync、gateway、管理后台配套、配置安全、DI、preset 等，强度偏高；普通解释或小修也会触发重流程。
- 动作边界：“先探测版本和 CLI 能力”正确；但“测试 skill 时必须同时跑两个临时项目”和完整生产矩阵不应是普通业务任务默认路径。
- 输出契约：交付说明完整；Shanforge 状态包缺 `work_item` 和 `ledger_event`，且“结论：可上线 | blocked | needs_user_input”与状态包 `ready_for_review` 并存。
- 失败语义：`blocked` 对 CLI、官方模板、runtime injection、release gate/start 等失败覆盖充分。
- 证据要求：版本、命令、stderr、配置安全门、production manifest、release gate、start、runtime injection 证据很强，但对小任务过重。
- 旧流程风险：旧 `@stratix/cli` 和 `tasks` preset 只作为禁用口径出现，方向正确；风险是旧口径密度高，主入口像版本迁移说明。

## 4. 冲突或职责重叠 Skill 对

| Skill 对 | 重叠点 | 当前风险 | 最小边界建议 |
|---|---|---|---|
| `document-templates` vs `doc-coauthoring` | 技术规范、RFC、项目说明、决策记录 | 正式文档体系和协作草稿可能混用状态 | `document-templates` 只管正式目录、模板、版本历史和校验；`doc-coauthoring` 管非模板化草稿、改写和读者视角检查。 |
| `doc-coauthoring` vs `article-writing` | 提案、指南、长篇说明 | 长文可能误触文档协作或发布型文章 | `article-writing` 管发布型长文；`doc-coauthoring` 管工作文档协作。 |
| `frontend-patterns` vs `ui-ux-pro-max` | 页面、组件、响应式、交互状态 | 一个偏实现，一个偏设计质量；UI 改动常同时命中 | 设计判断和视觉质量先 `ui-ux-pro-max`；代码结构、组件边界、状态实现先 `frontend-patterns`。 |
| `frontend-patterns` vs `shadcn` | React/Tailwind 组件实现 | shadcn 项目中两者都能触发 | 有 `components.json`、registry、preset、组件 add/update 时优先 `shadcn`。 |
| `stratix-admin-web` vs `stratix-service` | Stratix 管理后台、admin-page、admin CRUD | 前端页面和后端/CLI 生产化验证可能互相抢 owner | 后端、配置、CLI、release gate 归 `stratix-service`；管理后台页面、公共 UI、表格表单交互归 `stratix-admin-web`。 |
| `stratix-admin-web` vs `frontend-patterns` / `ui-ux-pro-max` | 管理后台 UI 实现和评审 | Stratix admin 页面可能同时触发普通前端和 UI/UX skill | Stratix admin 开发默认 `stratix-admin-web`；非 Stratix 前端用 `frontend-patterns`；纯视觉评审用 `ui-ux-pro-max`。 |
| `browser-control` vs `webapp-testing` | 打开页面、截图、检查交互 | 一次性浏览器操作和可重复回归验证容易混 | 用户要求本地浏览器/Chrome/browser-use 或外部站点用 `browser-control`；localhost 可重复断言用 `webapp-testing`。 |
| `systematic-debugging` vs `tdd-workflow` | Bug、测试失败、修复实现 | 根因调查和 Red/Green 实现顺序可能混 | 根因不明先 `systematic-debugging`；根因明确后用 `tdd-workflow` 写失败测试和最小实现。 |
| `tdd-workflow` vs `ai-regression-testing` | 防回归测试 | 都要求根因和回归断言 | `tdd-workflow` 管单次开发红绿循环；`ai-regression-testing` 管 AI 易漏的多路径一致性。 |
| `python-uv-project` vs `systematic-debugging` / `tdd-workflow` | Python bug、pytest、ruff、mypy | Python 工程 skill 可能抢走根因 owner | Python bug owner 是调试/TDD；`python-uv-project` 只约束 uv 命令和工具链。 |
| `executing-plans` vs `subagent-driven-development` | 执行已批准 plan | inline 和子 agent 执行都读 plan/ledger | 强耦合或不能派发子 agent 用 `executing-plans`；独立任务批处理用 `subagent-driven-development`。 |
| `project-memory` vs `using-shanforge` | 会话恢复、ledger、当前阶段 | 两者都读状态，子任务可能误触流程总控 | `project-memory` 只恢复事实；`using-shanforge` 只做路由，且执行特定任务的子代理按 `SUBAGENT-STOP` 忽略。 |
| `gitcommitzh` vs `using-shanforge` | 提交门、人工确认、远端边界 | 自动提交触发和流程总控提交门重复 | `using-shanforge` 决定是否进入提交；`gitcommitzh` 只核实并执行本地提交；直接用户限制优先。 |
| `api-design` vs `requirements-engineering` | API 需求、验收、契约 | API 契约可能被写成需求，或需求替代契约设计 | 需求 owner 写用户价值和 AC；`api-design` 写 endpoint、schema、error、compatibility。 |
| `docx` / `pdf` / `xlsx` vs `document-templates` | 文档交付物和正式文档内容 | 正式文档结构和文件格式处理可能混 | 正式项目文档结构归 `document-templates`；具体 Word/PDF/Excel 文件读写验证归 artifact skill。 |

## 5. 相对 Iteration 4 的变化

- 文件数量：34 -> 35。新增 `stratix-admin-web`。
- 平均分：91.6 -> 92.2。上升主要来自 iteration-4 fixes 补齐状态包、失败语义和远端 handoff。
- 低于 90 分数量：10 -> 5。`browser-control`、`crawler4j-model-project`、`python-uv-project`、`receiving-code-review`、`requesting-code-review` 已脱离低分区。
- `document-templates` 从 87 升到 89：metadata 和状态包已修，但主入口仍过长。
- `using-shanforge` 从 94 升到 95：远端 PR / push / merge handoff 降低了本地 commit 冒充远端闭环的风险。
- `gitcommitzh`、`skill-creator`、`stratix-service` 维持低分：iteration-4 fixes 明确没有覆盖这些长入口压缩。
- 旧流程风险继续下降：未发现旧中心 factory gate 回归。
- 残留系统性问题：部分通用创作 / UI skill 仍使用 `done`，在普通任务可接受，但进入 Shanforge work item 时会降低 review gate 一致性。

## 6. 最小下一步修复清单

只列真正值得改的项：

1. `skills/gitcommitzh/SKILL.md`：压缩重复提交门；补标准 `工作结果` 状态包；明确“直接用户要求暂不提交 / 只允许写文件”优先于自动提交触发。
2. `skills/skill-creator/SKILL.md`：把评估、benchmark、描述优化和打包下沉到 references；核实 `eval-viewer/generate_review.py`、`package_skill.py`、`.skill` 是否仍是当前事实；状态包补 `work_item` / `ledger_event`。
3. `skills/stratix-service/SKILL.md`：把生产化双项目矩阵和完整 CLI 清单下沉；按解释、评审、小修、新项目、上线五类场景分级验证；状态包补 `work_item` / `ledger_event`。
4. `skills/document-templates/SKILL.md`：把默认最小文档包、模板资产映射和迁移流程移动到 references；主入口只保留判断、边界、治理规则、状态包和按需读取索引。
5. `skills/doc-coauthoring/SKILL.md`：补 Shanforge work item 状态包，使用 `ready_for_review | blocked | needs_user_input`，并保留普通非 work item 的轻量交付格式。
6. `skills/stratix-admin-web/SKILL.md`：补 `ledger_event` 字段；明确它优先于 `frontend-patterns` 的条件是 Stratix admin 页面开发，不是所有后台 UI 评审。
7. 全局小修：`algorithmic-art`、`shadcn`、`ui-ux-pro-max` 如进入 Shanforge work item，应补 `work_item` / `ledger_event` 和 `needs_user_input`；不必重写完整主入口。

## 状态回写

```text
工作结果：
- work_item: SKILL-FLOW-AUDIT-001
- skill: prompt-engineering-review
- status: ready_for_review
- outputs:
  - .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/prompt-engineering-review-iteration-5.md
- evidence:
  - read .factory/workitems/SKILL-FLOW-AUDIT-001/task-briefs/prompt-engineering-review-iteration-5.md
  - read .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/prompt-engineering-review-iteration-4.md
  - read .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/chinese-language-review-iteration-4.md
  - read .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/iteration-4-fixes-independent-review.md
  - read .factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-4-fix-summary-report.md
  - scanned 35 current skills/*/SKILL.md files
  - ran structural scans for old factory gates, work_item, ledger_event, blocked, needs_user_input and status terms
- ledger_event: none
- needs:
  - review
```
