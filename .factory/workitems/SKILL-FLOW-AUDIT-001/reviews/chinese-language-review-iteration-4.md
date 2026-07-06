# Chinese Language Review Iteration 4

status: DONE
blocked: no

本报告只评审当前工作区实际存在的 `skills/*/SKILL.md`。已删除 skill 不纳入评分。分数按本轮读取到的当前文件重新给出；delta 为本轮分数减去 iteration-3 分数。

## 扫描范围

实际扫描数量：34

扫描命令依据：`find skills -mindepth 2 -maxdepth 2 -name SKILL.md -print | sort`

当前 `skills/*/SKILL.md` 总行数：4338

文件清单：

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

## 评分总览

平均分：92.1

最低分：85（`skill-creator`）

最高分：96（`api-design`）

低于 90 分数量：8

| Skill | Iteration 3 | Iteration 4 | Delta | 主要原因 |
|---|---:|---:|---:|---|
| agent-harness-construction | 92 | 91 | -1 | 英文括注和 `harness/schema/action space` 密度仍偏高。 |
| ai-first-engineering | 91 | 91 | 0 | 中文清楚，保留少量必要英文术语。 |
| ai-regression-testing | 92 | 94 | +2 | 入口更短，根因、回归、多路径边界表达清楚。 |
| algorithmic-art | 94 | 94 | 0 | 结构简洁，英文基本是必要工具名。 |
| api-design | 95 | 96 | +1 | 决策表清晰，少教程化内容。 |
| article-writing | 93 | 92 | -1 | 仍有 `Newsletters`、`Quality Gate` 等中英标题混用。 |
| brainstorming | 93 | 92 | -1 | 文件保存、状态判断和视觉伴侣段落略重。 |
| browser-control | 93 | 91 | -2 | 工具名堆叠较多，输出格式未和状态包统一。 |
| crawler4j-model-project | 90 | 89 | -1 | CLI 与旧命令清单密集，缺完成状态和失败输出契约。 |
| doc-coauthoring | 93 | 95 | +2 | 短入口，边界和验证要求清楚。 |
| document-templates | 88 | 86 | -2 | metadata 全英文，主文件仍承担模板目录和迁移 reference。 |
| docx | 93 | 94 | +1 | 分支、写入、验证和状态包清楚。 |
| executing-plans | 93 | 93 | 0 | 规则清楚，重复在可接受范围内。 |
| frontend-patterns | 94 | 95 | +1 | 决策表和风险分级精简。 |
| gitcommitzh | 88 | 86 | -2 | 授权、范围、提交、回显、禁止项多处重复。 |
| humanizer | 93 | 95 | +2 | 文字审稿边界短而明确。 |
| pdf | 93 | 94 | +1 | 文件处理分支清楚，风险说明具体。 |
| project-memory | 94 | 95 | +1 | 读取门和事实源优先级表达稳定。 |
| python-uv-project | 89 | 88 | -1 | 触发范围偏宽，缺 Shanforge 状态包。 |
| receiving-code-review | 90 | 88 | -2 | “表演式同意”重复，缺统一状态包。 |
| requesting-code-review | 90 | 88 | -2 | 独立性硬门多处复述，缺统一状态包。 |
| requirements-engineering | 92 | 91 | -1 | 需求教材段落仍偏多，metadata 仍有角色绑定口吻。 |
| shadcn | 94 | 94 | 0 | 中英混用主要是工具专名，可接受。 |
| skill-creator | 87 | 85 | -2 | 创建、评审、评估、benchmark、打包仍在主入口。 |
| stratix-service | 89 | 87 | -2 | 生产化矩阵和 CLI 清单过长，默认强度不分场景。 |
| subagent-driven-development | 91 | 92 | +1 | 子 agent 边界和状态回写更清楚。 |
| systematic-debugging | 95 | 95 | 0 | 根因流程短句清晰。 |
| tdd-workflow | 94 | 95 | +1 | 取消固定覆盖率口径后更自然。 |
| ui-ux-pro-max | 95 | 95 | 0 | 主入口保持精简。 |
| using-shanforge | 94 | 93 | -1 | 路由表必要，但状态词和 gate 仍有重复。 |
| verification-before-completion | 95 | 95 | 0 | 完成声明和证据关系表达清楚。 |
| webapp-testing | 94 | 94 | 0 | 边界清楚，示例适量。 |
| writing-plans | 94 | 93 | -1 | 计划字段要求密集，少量英文审查项。 |
| xlsx | 93 | 94 | +1 | 分支、写入和验证表达简洁。 |

## 低于 90 分问题明细

### 啰嗦 / 重复

- `document-templates`（86）：317 行主文件仍包含默认最小文档包、模板资产到输出路径映射、历史迁移流程和站点集成规则。主入口承担了 reference 角色。
- `gitcommitzh`（86）：390 行中，提交授权、范围核查、`git add .` 禁止、message 一致性、真实 hash 回显在多个章节重复出现。
- `skill-creator`（85）：创建、改写、中文化、评审、评估、benchmark、描述优化、打包全部留在主入口，像操作手册而不是触发入口。
- `stratix-service`（87）：版本探测、双临时项目测试、生产化验证矩阵、CLI 命令、配置安全和评审清单都在主文件，简单评审也会被重流程拖住。
- `requesting-code-review`（88）：`same_thread` 不能 approved、`needs_independent_review`、独立 reviewer 元数据等规则在含义清单、独立性硬门和禁止项中重复。
- `receiving-code-review`（88）：核心原则中“禁止表演式同意”重复出现，默认流程、输出位置和 memory sync 都在主入口展开。
- `python-uv-project`（88）：项目结构、日常命令、交付前命令、配置、编码、测试、迁移和 review checklist 全部展开；作为入口仍偏重。
- `crawler4j-model-project`（89）：旧命令删除清单、模块协议、目录、硬限制、宿主验收和评审清单都在主入口，工具事实密度过高。

### 语义不清

- `document-templates`：metadata 写 “Software project lifecycle document system for D3”，正文却是 `docs-stratego` 的 4 大模块文档系统；D3 没有解释。
- `skill-creator`：`eval-viewer/generate_review.py`、`generate_review.py`、`package_skill.py`、`.skill` 打包是否仍是当前工具事实不清楚。
- `stratix-service`：“测试 skill 时必须同时跑两个临时项目”更像评估本 skill 的要求，不适合普通 Stratix 业务实现默认执行。
- `python-uv-project`：修 Bug 时要求根因先行，但没有说清与 `systematic-debugging`、`tdd-workflow` 同时触发时谁主谁辅。
- `crawler4j-model-project`：创建、迁移、Core/SDK 源码开发、宿主安装、发布验收都混在一个执行面，读者需要自行判断当前分支。

### 表达不一致

- `python-uv-project`：没有标准 Shanforge 状态包，和多数新文件的 `work_item / ledger_event / needs` 格式不一致。
- `receiving-code-review`：只写“完成状态”，没有 `status / outputs / evidence / ledger_event / needs` 模板。
- `requesting-code-review`：只写 `review_status`、`next_gate_status`，未对齐工作 skill 状态包。
- `document-templates`：状态包缺 `work_item` 和 `ledger_event`，`status: document_ready` 也和其他 skill 的 `ready_for_review` 口径不完全一致。
- `gitcommitzh`：普通 Git 提交、Shanforge work item 收尾、slash 直调三套口径交织，读者需要反复切换上下文。
- `skill-creator`：前半部分强调主文件精简和 references，下半部分仍把评估和打包细节放在主文件，前后标准不一致。
- `stratix-service`：输出结论写 `可上线 | blocked | needs_user_input`，状态包又写 `ready_for_review | blocked | needs_user_input`，口径不统一。

### 中英混杂

- `document-templates`：description 全英文，且含未解释的 D3；标题虽中文化，但入口元数据仍不符合当前中文 skill 风格。
- `skill-creator`：`Description Optimization`、`Evaluation`、`Benchmark`、`Assertion`、`SKILL.md` 编写教程等英文概念密集，且部分可中文化。
- `stratix-service`：`runtime injection`、`release gate`、`production manifest`、`preset`、`template`、`doctor` 等英文串联过密；部分是工具名，部分可改中文说明。
- `crawler4j-model-project`：`Hosted UI`、`DevLink`、`manifest lock`、`workflow/component`、`runtime surface` 等术语密集，没有分层解释。
- `gitcommitzh`：`slash`、`staged / unstaged`、`cached`、`message`、`hash` 等 Git 术语可保留，但同一段落中英文切换频繁。
- `python-uv-project`：`Review Checklist` 标题和 `lint`、`fallback` 等英文保留过多；可改成中文标题，工具名保留原文。

## Top 10 共性问题

1. 少数主 `SKILL.md` 仍把 reference、命令手册、模板清单和评审清单全部塞在入口。
2. 状态包尚未统一，常见缺口是 `work_item`、`ledger_event`、`needs` 和失败语义。
3. 工程类 skill 触发范围偏宽，容易压过更具体的调试、TDD、API、文档或 UI skill。
4. 普通任务、Shanforge work item、skill 自测三类场景混写，默认执行强度不清。
5. 中英混杂主要集中在标题、metadata 和工具链说明；工具名可保留，但解释句应中文化。
6. 同一 gate 在“含义保留清单、默认流程、禁止、完成状态”中重复出现，且措辞有轻微差异。
7. `done`、`passed`、`ready_for_review`、`document_ready`、`fixed` 等状态词没有完全收口。
8. 部分文件仍像教材，例如用户故事、INVEST、完整 CLI 命令、完整目录树；入口应只留路由和关键门。
9. 旧口径大多已变成禁用说明，但旧命令、旧工具和旧包名密度仍让当前入口显得不够干净。
10. 少量 metadata 仍是英文或旧角色口吻，影响 skill 发现阶段的中文一致性。

## 相对 iteration-3 的总体变化

- 平均分：92.3 -> 92.1，基本持平。
- 低于 90 分数量：5 -> 8，增加的主要原因不是新增严重问题，而是本轮按“中文语言一致性”更严格扣了状态包缺失、主入口重复和中英混杂。
- 明显改善：`doc-coauthoring`、`humanizer`、`ai-regression-testing` 更像精简入口；`api-design`、`frontend-patterns`、`tdd-workflow` 保持高质量。
- 明显退步：`document-templates`、`gitcommitzh`、`skill-creator`、`stratix-service` 仍未把长清单下沉；`receiving-code-review`、`requesting-code-review` 因状态包不统一被扣分。
- 已删除 skill 未纳入本轮评分；当前扫描数量仍为 34。

## 最小下一步修复清单

1. `skills/document-templates/SKILL.md`：把 description 改成中文，删除或解释 D3；把默认文档包和模板映射下沉到 references；状态包补 `work_item`、`ledger_event`。
2. `skills/gitcommitzh/SKILL.md`：合并提交范围、message 一致性、提交执行、提交后回显四类重复规则；保留“只总结”和“执行提交”两个分支即可。
3. `skills/skill-creator/SKILL.md`：主入口只留创建/改写/评审主流程；评估、benchmark、描述优化、打包移到 references，并核实现有脚本名。
4. `skills/stratix-service/SKILL.md`：把生产化测试矩阵和常用 CLI 下沉；按解释、评审、小修、新项目、上线五类场景分级验证。
5. `skills/python-uv-project/SKILL.md`：补标准状态包；明确 Python bug 场景先由 `systematic-debugging` 或 `tdd-workflow` 接管，本 skill 只提供 uv 约束。
6. `skills/receiving-code-review/SKILL.md`：删除重复原则，补 `工作结果` 状态包，保留逐项 triage 和验证要求。
7. `skills/requesting-code-review/SKILL.md`：把独立性硬门去重，补标准状态包；`same_thread` 规则只保留一处权威表述。
8. `skills/crawler4j-model-project/SKILL.md`：补输出契约和 blocked 语义；旧命令清单、完整 CLI 和宿主验收细节移到 references。
9. 全局小修：把 `Review Checklist`、`Quality Gate`、`Description Optimization` 等可中文化标题统一改中文；工具名、命令名和 API 名保留英文。
10. 全局状态词小修：为非文件处理类 skill 统一 `ready_for_review | blocked | needs_user_input`，需要结果型状态时只放入 `needs` 或 evidence 摘要。

## 不建议修改

- 不需要强行翻译 `uv`、`pytest`、`ruff`、`Playwright`、`shadcn/ui`、`browser-use`、`OpenAPI`、`p5.js`、`Chrome`、`Codex` 等工具专名。
- 不需要把所有短入口都补成大型 Shanforge 流程说明；短入口目前是优势。
- 不需要恢复已删除 skill，也不应把已删除 skill 纳入评分。

## 状态回写

```text
工作结果：
- work_item: SKILL-FLOW-AUDIT-001
- skill: humanizer
- status: ready_for_review
- outputs:
  - .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/chinese-language-review-iteration-4.md
- evidence:
  - read task brief chinese-language-review-iteration-4.md
  - read language-prompt-review-iteration-3.md
  - read skill-flow-completeness-test-iteration-3.md
  - scanned 34 current skills/*/SKILL.md files
  - compared iteration-4 scores against iteration-3 scores
- ledger_event: none
- needs:
  - review
```
