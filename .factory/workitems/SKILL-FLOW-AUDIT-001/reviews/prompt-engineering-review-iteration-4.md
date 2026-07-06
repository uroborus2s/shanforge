# Prompt Engineering Review Iteration 4

status: DONE
blocked: no

本报告只评审当前工作区实际存在的 `skills/*/SKILL.md`。未修改任何 skill 文件。分数按本轮任务卡重点重新评分：触发边界、指令优先级、tool / skill / 子 agent 边界、输出契约、失败语义、证据要求、自批 / 跳 review / 旧流程风险。相对 iteration-3 的 delta 是本轮评分减去 `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/language-prompt-review-iteration-3.md` 中的分数，不表示一定发生了文件内容修改。

## 扫描范围

实际扫描数量：34

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
25. `skills/stratix-service/SKILL.md`
26. `skills/subagent-driven-development/SKILL.md`
27. `skills/systematic-debugging/SKILL.md`
28. `skills/tdd-workflow/SKILL.md`
29. `skills/ui-ux-pro-max/SKILL.md`
30. `skills/using-shanforge/SKILL.md`
31. `skills/verification-before-completion/SKILL.md`
32. `skills/webapp-testing/SKILL.md`
33. `skills/writing-plans/SKILL.md`
34. `skills/xlsx/SKILL.md`

辅助扫描事实：

- `wc -l skills/*/SKILL.md`：总计 4338 行。
- 旧中心流程禁词扫描：未发现 `factory-dispatch`、`factory-workitem-loop-gate`、`scripts/factory-`、`REQUIRED NEXT SKILL` 等旧 gate；唯一命中是 `using-shanforge` 中合法说明“工作 skill 完成时只返回状态包，不写下一步 skill”。
- `ledger_event` 字段缺失扫描命中 17 个 skill；其中一部分是通用创作 / 工具 skill，可接受但会降低 Shanforge 状态一致性。
- `blocked` 缺失扫描命中 6 个 skill：`browser-control`、`crawler4j-model-project`、`project-memory`、`python-uv-project`、`receiving-code-review`、`requesting-code-review`。其中 `project-memory` 是恢复 skill，缺显式 blocked 语义风险较低。

## 评分总览

| Skill | Iteration 3 | Iteration 4 | Delta | 变化原因 |
|---|---:|---:|---:|---|
| agent-harness-construction | 92 | 91 | -1 | 主体清楚；Shanforge 状态包缺 `work_item` / `ledger_event`。 |
| ai-first-engineering | 91 | 91 | 0 | 边界和输出稳定；仍是建议型 skill，不承担执行 gate。 |
| ai-regression-testing | 92 | 93 | +1 | 根因、回归和多路径一致性语义清楚，输出包完整。 |
| algorithmic-art | 94 | 90 | -4 | 创作边界好；但状态仍是 `done`，缺 Shanforge 统一状态包。 |
| api-design | 95 | 95 | 0 | 触发、风险分级、输出契约完整。 |
| article-writing | 93 | 92 | -1 | 写作边界好；状态包缺 `work_item` / `ledger_event`。 |
| brainstorming | 93 | 94 | +1 | 读取边界、状态回写和不自选下一步更清楚。 |
| browser-control | 93 | 89 | -4 | 工具路由强；缺状态包和失败状态，browser-use 固定命令有时效风险。 |
| crawler4j-model-project | 90 | 88 | -2 | 版本边界清楚；缺输出契约和 blocked 语义，旧命令密度高。 |
| doc-coauthoring | 93 | 89 | -4 | 文档协作清楚；与正式文档 owner 重叠，输出用 `done`。 |
| document-templates | 88 | 87 | -1 | 仍是长入口，metadata 仍有英文 D3，状态包缺 `work_item` / `ledger_event`。 |
| docx | 93 | 94 | +1 | 触发窄、失败语义和验证要求完整。 |
| executing-plans | 93 | 94 | +1 | task gate、review checkpoint、状态包完整。 |
| frontend-patterns | 94 | 93 | -1 | 边界清楚；与 UI/UX、shadcn、webapp testing 仍需靠触发语区分。 |
| gitcommitzh | 88 | 88 | 0 | 安全门强；390 行重复，自动提交触发语偏重。 |
| humanizer | 93 | 94 | +1 | 事实边界、写入安全和状态包完整。 |
| pdf | 93 | 94 | +1 | 触发窄、失败语义和验证路径完整。 |
| project-memory | 94 | 94 | 0 | 最小读取和事实源优先级稳定。 |
| python-uv-project | 89 | 88 | -1 | 工程规范强；触发过宽，缺状态包和 blocked 语义。 |
| receiving-code-review | 90 | 88 | -2 | 核实反馈原则强；缺固定 `工作结果` 状态包。 |
| requesting-code-review | 90 | 89 | -1 | 独立性硬门强；缺标准状态包和 blocked 语义。 |
| requirements-engineering | 92 | 93 | +1 | 场景、版本、baseline 和状态边界完整。 |
| shadcn | 94 | 90 | -4 | 组件边界清楚；输出仍是 `done`，与 UI/UX / frontend 验证需靠外部路由。 |
| skill-creator | 87 | 86 | -1 | 主入口仍覆盖创建、评审、评估、打包和描述优化；旧工具事实未收口。 |
| stratix-service | 89 | 88 | -1 | 版本探测意识好；生产矩阵压过普通任务，状态包缺 `work_item` / `ledger_event`。 |
| subagent-driven-development | 91 | 93 | +2 | 子 agent 边界、串行执行、状态回写和不得自批更完整。 |
| systematic-debugging | 95 | 95 | 0 | 根因先行、停止条件和状态包完整。 |
| tdd-workflow | 94 | 94 | 0 | Red/Green、根因和风险分级验证完整。 |
| ui-ux-pro-max | 95 | 90 | -5 | UI/UX 边界清楚；输出仍是 `done`，缺 work item 状态字段。 |
| using-shanforge | 94 | 94 | 0 | 流程总控边界强；`SUBAGENT-STOP` 对本类子任务有效。 |
| verification-before-completion | 95 | 95 | 0 | 完成声明、证据、exit code 和状态包完整。 |
| webapp-testing | 94 | 94 | 0 | 与 browser-control 边界清楚，验证和失败处理完整。 |
| writing-plans | 94 | 94 | 0 | 计划 gate、review handoff 和状态包完整。 |
| xlsx | 93 | 94 | +1 | 触发窄、文件安全和验证语义完整。 |

最低分：86（`skill-creator`）

最高分：95（`api-design`、`systematic-debugging`、`verification-before-completion`）

低于 90 分数量：10（iteration-3 为 5）

平均分：91.6（iteration-3 为 92.3）

总体判断：没有发现旧中心 gate 回退或明确自批批准风险。iteration-4 下调主要来自本轮更严格检查“Shanforge 状态包、失败语义和 tool / skill 边界一致性”，不是因为旧流程大面积回潮。

## 低于 90 分明细

### `browser-control`：89

- 触发边界：与 `webapp-testing` 的边界写得较清楚；但 description 强调“优先走 browser-use CLI”，在 Codex Browser / Chrome 插件已可用时容易让工具选择显得固定。
- 动作边界：安全确认规则完整；但没有 Shanforge work item 场景下的状态回写边界。
- 输出契约：只有用户可读汇报格式，没有 `work_item`、`status`、`outputs`、`evidence`、`ledger_event`、`needs`。
- 失败语义：登录、验证码、权限等只写在“未完成项”，没有 `blocked` / `needs_user_input` 状态。
- 旧流程风险：未发现旧 factory gate；主要风险是本地 CLI 命令事实随环境变化。

### `crawler4j-model-project`：88

- 触发边界：触发词非常具体，但 “必须使用” 覆盖创建、迁移、调试、校验、打包、发布，强度偏高。
- 动作边界：0.4.0 / core-native-v2 当前事实写得清楚；但版本事实硬编码较多，需要更强调先探测当前安装版本。
- 输出契约：没有统一状态包；创建、迁移、发布失败后的输出格式不固定。
- 失败语义：缺 `blocked` / `needs_user_input` 定义；CLI 不存在、版本不符、校验失败、发布链路缺凭据时状态不清。
- 旧流程风险：旧命令和旧 spec 被列为禁止项，方向正确；但旧口径密度高，主入口仍像迁移备忘录。

### `doc-coauthoring`：89

- 触发边界：与 `document-templates`、`article-writing` 都有相邻边界；不适用场景写了，但在“提案 / 技术规范 / RFC”上仍可能和正式文档 owner 重叠。
- 动作边界：协作式写作动作清楚；但作为 `using-shanforge` 路由表中的文档候选 owner 时，缺 work item gate。
- 输出契约：使用 `status: done | blocked`，没有 `ready_for_review`、`work_item`、`ledger_event`。
- 失败语义：只有 `blocked`，缺 `needs_user_input` 和 partial 状态；事实冲突时如何暂停不够固定。
- 旧流程风险：未发现旧流程风险；主要是状态词与流程总控不一致。

### `document-templates`：87

- 触发边界：description 仍是英文且含未解释的 D3；正文是 `docs-stratego` 4 大模块，入口语义不统一。
- 动作边界：正式文档治理清楚；但 317 行主入口承担模板映射、迁移流程和目录参考职责，长背景会压过关键动作。
- 输出契约：状态包缺 `work_item` 和 `ledger_event`；`document_ready` 与通用工作 skill 状态协议没有完全对齐。
- 失败语义：`blocked` 定义存在；但缺 partial / needs_user_input 的具体分支，例如只校验、只补单页、工具不可用。
- 旧流程风险：明确禁止旧仓库脚本，未见旧 factory gate；风险是迁移流程和工具命令太多，容易被当成默认重流程。

### `gitcommitzh`：88

- 触发边界：本地提交边界清楚；但“代理完成一个产生文件改动的任务且 gate 满足时也必须使用”容易和任务卡“只允许写入某文件 / 不提交”的临时约束冲突，需要强调直接用户约束优先。
- 动作边界：不 push、不建 PR、不改写历史写得很强；Shanforge gate 与普通 Git 场景交织，阅读成本高。
- 输出契约：提交成功 / 未提交模板完整；但作为工作 skill 没有统一 `work_item/status/outputs/evidence/ledger_event/needs` 状态包。
- 失败语义：`blocked` 语义很完整。
- 旧流程风险：未发现旧 gate；主要问题是 390 行中范围门、message 一致性门、提交后回显门重复。

### `python-uv-project`：88

- 触发边界：覆盖 Python 项目、uv、pytest、ruff、mypy、FastAPI、Typer、Django、CLI、服务端、自动化脚本，容易压过更具体的调试、TDD、API 或 CLI skill。
- 动作边界：uv 工程规范清楚；但遇到 Python bug 时没有明确“先由 `systematic-debugging` / `tdd-workflow` 接管，本 skill 只提供 uv 约束”。
- 输出契约：没有 Shanforge 状态包。
- 失败语义：没有 `blocked` / `needs_user_input` 语义；依赖安装失败、非 uv 项目迁移争议、测试失败时回写不固定。
- 旧流程风险：未发现旧流程风险。

### `receiving-code-review`：88

- 触发边界：review feedback、PR 评论、外部 reviewer 建议覆盖清楚。
- 动作边界：先核实再修改、pushback、N/A 处理都清楚；每项反馈单独处理的约束正确。
- 输出契约：只有输出位置和完成状态描述，没有固定 `工作结果` 状态包。
- 失败语义：缺 `blocked` / `needs_user_input` 状态，例如反馈不清、reviewer 未接受 N/A、验证失败时状态不固定。
- 旧流程风险：未发现旧流程风险；主要风险是缺状态包导致流程总控难以机械读取结果。

### `requesting-code-review`：89

- 触发边界：实现完成、review checkpoint、PR 前、`ready_for_review` 触发清楚。
- 动作边界：独立性硬门强，same-thread 自检不能 approved 的风险控制到位。
- 输出契约：输出 review 文件和 ledger 事件，但没有标准 `工作结果` 状态包。
- 失败语义：缺 `blocked` / `needs_user_input` 定义；缺 task brief、report、evidence、diff、子 agent 未授权时如何状态回写不够固定。
- 旧流程风险：未发现旧流程风险；无自批批准风险。

### `skill-creator`：86

- 触发边界：同时覆盖创建、修改、评审、评估、benchmark、description optimization、打包，触发面仍偏宽。
- 动作边界：中文、隔离评审、含义保留清单正确；但主入口仍把评估运行、评分员、查看器、打包都内联，容易压过“改一个 skill”的最小路径。
- 输出契约：有状态包，但缺 `work_item` / `ledger_event`；评估产物和 review 产物路径不固定。
- 失败语义：`blocked` 定义存在；但评估工具不可用、目标 CLI 无法跑子代理、打包脚本不存在时的状态不够具体。
- 旧流程风险：没有旧 factory gate；但 `eval-viewer/generate_review.py`、`package_skill.py`、`.skill` 打包事实看起来像旧工具链，需核实是否仍是当前能力。

### `stratix-service`：88

- 触发边界：覆盖 app、plugin、worker、sync、gateway、管理后台、配置安全门、DI 等，强度较大；普通 Stratix 评审也会被完整生产矩阵拖住。
- 动作边界：先探测版本的原则正确；但“测试 skill 时必须同时跑两个临时项目”应下沉到 skill 自测，而不是普通业务任务默认路径。
- 输出契约：有输出契约，但 Shanforge 状态包缺 `work_item` / `ledger_event`。
- 失败语义：`blocked` 语义完整。
- 旧流程风险：旧 `@stratix/cli`、tasks preset 等作为禁用口径可接受；风险是旧口径密度高，主入口像版本迁移说明。

## 职责重叠和冲突对

| Skill 对 | 重叠点 | 当前风险 | 最小边界建议 |
|---|---|---|---|
| `document-templates` vs `doc-coauthoring` | 技术规范、RFC、设计说明、项目说明 | `using-shanforge` 路由表把两者并列为文档 owner；正式文档和协作草稿状态容易混用 | `document-templates` 只管正式生命周期文档和目录治理；`doc-coauthoring` 只管非模板化草稿 / 改写 / 读者视角检查。 |
| `doc-coauthoring` vs `article-writing` | 提案、指南、长篇说明 | 长文草稿可能误触文档协同或文章写作 | `article-writing` 只管发布型长文；`doc-coauthoring` 管需要与用户迭代成文的工作文档。 |
| `frontend-patterns` vs `ui-ux-pro-max` | 页面、组件、交互、响应式 | 一个偏实现模式，一个偏设计质量；触发都能覆盖 UI 改动 | UI 设计判断先 `ui-ux-pro-max`；代码结构、状态和组件实现先 `frontend-patterns`。 |
| `frontend-patterns` vs `shadcn` | React/Tailwind 组件实现 | shadcn 项目中两者都可能触发 | 存在 `components.json` 或 registry/preset/组件 add/update 时优先 `shadcn`；普通前端模式用 `frontend-patterns`。 |
| `browser-control` vs `webapp-testing` | 打开页面、截图、检查交互 | 一次性浏览器操作和可重复回归验证容易混 | 用户要本地浏览器 / 登录态 / 外部站点用 `browser-control`；localhost 可重复断言用 `webapp-testing`。 |
| `systematic-debugging` vs `tdd-workflow` | Bug 修复、测试失败 | 根因调查和 Red/Green 实现顺序可能混 | 根因不明先 `systematic-debugging`；根因清楚后用 `tdd-workflow` 落测试和最小修复。 |
| `tdd-workflow` vs `ai-regression-testing` | Bug 防回归测试 | 都要求根因和回归断言 | `tdd-workflow` 管新行为 / 修复循环；`ai-regression-testing` 管 AI 易漏的多路径一致性和同类 bug 防线。 |
| `python-uv-project` vs `systematic-debugging` / `tdd-workflow` | Python bug、pytest 失败、ruff/mypy | Python skill 触发过宽，可能抢走根因 / TDD owner | Python bug 先由调试 / TDD owner 决定流程；`python-uv-project` 只约束 uv 命令、项目结构和工具链。 |
| `executing-plans` vs `subagent-driven-development` | 执行已批准 plan | inline 执行和子 agent 执行边界清楚，但都读 plan / ledger | 继续保留：强耦合或平台不能子 agent 用 `executing-plans`；独立任务批处理用 `subagent-driven-development`。 |
| `project-memory` vs `using-shanforge` | 会话恢复、ledger、当前阶段 | 两者都读状态；若忽略 `using-shanforge` 的 `SUBAGENT-STOP` 会误路由子任务 | 保持现状：`project-memory` 只恢复事实；`using-shanforge` 只做流程路由，特定子代理忽略它。 |
| `gitcommitzh` vs `using-shanforge` | 提交门、human approval、ledger | 自动提交触发和流程总控提交门重复 | `using-shanforge` 决定是否进入提交；`gitcommitzh` 只核实并执行本地提交，直接用户“暂不提交 / 只允许写文件”优先。 |
| `api-design` vs `requirements-engineering` | API 需求、契约、验收 | API 契约可能被写进需求或设计 | 需求 owner 写用户价值和 AC；`api-design` 写 endpoint/schema/error/compatibility 契约。 |
| `docx` / `pdf` / `xlsx` vs `document-templates` | 文档交付物 | 正式文档内容和文件格式处理可能混 | 正式项目文档结构归 `document-templates`；具体 Word/PDF/Excel 文件读写验证归对应 artifact skill。 |

## 自批、跳 review、旧流程风险

- 自批风险：未发现工作 skill 主动把自身实现写成 `approved` 的口径。`requesting-code-review`、`subagent-driven-development`、`writing-plans`、`brainstorming`、`project-memory` 明确禁止作者自批。
- 跳 review 风险：流程类 skill 基本都有 review gate；风险集中在通用创作 / 工具 skill 使用 `status: done`，进入 Shanforge work item 时可能绕开 `ready_for_review` 语义。
- 跳验证风险：`verification-before-completion`、`tdd-workflow`、`systematic-debugging`、`webapp-testing`、文件处理类 skill 都有验证要求。`browser-control`、`crawler4j-model-project`、`python-uv-project` 的失败 / 验证状态需要补固定回写。
- 旧流程风险：未发现旧 `factory-*` gate 或旧中心脚本回退。剩余旧口径主要是禁用说明或可能过时的工具事实：`skill-creator` 的评估 / 打包脚本、`stratix-service` 的旧包口径、`crawler4j-model-project` 的旧命令列表。

## 相对 iteration-3 的关键变化

- 文件数量：34 -> 34，无新增 / 删除。
- 平均分：92.3 -> 91.6。下降来自本轮提高状态包和失败语义权重。
- 低于 90：5 -> 10。新增低分主要是 `browser-control`、`doc-coauthoring`、`requesting-code-review` 以及部分通用 UI / 工具类状态协议问题。
- 旧流程：iteration-3 已指出旧 gate 基本清理；本轮扫描仍未发现旧中心 gate 回退。
- 流程完整性：`skill-flow-completeness-test-iteration-3.md` 中的 Critical 仍与本报告相关：缺 S1-S6 真实黑盒行为回放 evidence。该问题不是单个 prompt 分数能完全关闭。
- 远端闭环：iteration-3 完整性报告指出 PR / push / merge 没有 Shanforge owner。本轮 `gitcommitzh` 仍正确禁止冒充远端状态，但远端 handoff 契约仍未定义。

## 最小下一步修复清单

只列真正值得改的项：

1. 给 `crawler4j-model-project`、`python-uv-project`、`receiving-code-review`、`requesting-code-review` 补标准 `工作结果` 状态包和 `blocked` / `needs_user_input` 语义。
2. 给 `browser-control` 增加最小 Shanforge 状态包；保留当前用户可读汇报格式，不要重写浏览器工具路由。
3. 把 `document-templates` 的英文 D3 metadata 改成当前中文说明；把默认文档包和模板映射清单下沉到 references；状态包补 `work_item` / `ledger_event`。
4. 把 `skill-creator` 的评估、benchmark、description optimization、打包流程下沉到 references；核实 `eval-viewer/generate_review.py`、`package_skill.py`、`.skill` 是否仍是当前事实。
5. 压缩 `gitcommitzh` 的重复提交门和回显门；明确“直接用户约束优先于自动提交触发”。
6. 把 `stratix-service` 的“双临时项目生产矩阵”标成 skill 自测 / 上线证明分支；普通解释、评审、小修默认只做版本探测 + 目标验证。
7. 明确三组优先级：`document-templates` vs `doc-coauthoring`、`browser-control` vs `webapp-testing`、`python-uv-project` vs `systematic-debugging` / `tdd-workflow`。
8. 定义远端 PR / push / merge 的最小 handoff 契约：owner、输入、状态、evidence、禁止冒充规则。不要塞进 `gitcommitzh`，也不要新增中心 `factory-*` gate。

## 状态回写

```text
工作结果：
- work_item: SKILL-FLOW-AUDIT-001
- skill: prompt-engineering-review
- status: ready_for_review
- outputs:
  - .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/prompt-engineering-review-iteration-4.md
- evidence:
  - read .factory/workitems/SKILL-FLOW-AUDIT-001/task-briefs/prompt-engineering-review-iteration-4.md
  - read .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/language-prompt-review-iteration-3.md
  - read .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-3.md
  - scanned 34 current skills/*/SKILL.md files
  - ran structural scans for old factory gates, status fields, blocked semantics and approval terms
- ledger_event: none
- needs:
  - review
```
