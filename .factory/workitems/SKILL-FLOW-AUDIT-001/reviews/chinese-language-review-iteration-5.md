# Chinese Language Review Iteration 5

status: ready_for_review
blocked: no

本报告只评审当前工作区实际存在的 `skills/*/SKILL.md`。已删除 skill 不纳入评分；新增 skill 单独标注。未修改任何 skill、测试、ledger 或 memory。

## 1. 扫描范围

实际扫描数量：35

扫描依据：

- `rg --files skills | rg '/SKILL\.md$' | sort`
- `wc -l skills/*/SKILL.md`：总计 4601 行
- 旧中心 gate 扫描：未命中 `factory-dispatch`、`factory-workitem-loop-gate`、`scripts/factory-`、`REQUIRED NEXT SKILL`、`factory-pr-remote`、`docs/superpowers`

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

## 2. 逐项评分

平均分：92.1

最低分：85（`skill-creator`）

最高分：96（`api-design`）

低于 90 分数量：5

| Skill | Iteration 4 | Iteration 5 | Delta | 变化原因 |
|---|---:|---:|---:|---|
| agent-harness-construction | 91 | 91 | 0 | 中文结构稳定；英文括注和 `schema/action space/harness` 密度仍偏高。 |
| ai-first-engineering | 91 | 91 | 0 | 表达清楚；`Eval/Prompts` 等术语可接受但仍有中英切换。 |
| ai-regression-testing | 94 | 94 | 0 | 根因、回归和多路径语义自然，输出契约完整。 |
| algorithmic-art | 94 | 93 | -1 | 正文简洁；标题、`status: done`、`Blocked` 等英文状态词和中文状态包不完全一致。 |
| api-design | 96 | 96 | 0 | 决策表清楚，术语保留得当，主入口不教程化。 |
| article-writing | 92 | 92 | 0 | 语言自然；`Newsletters`、`Quality Gate` 等标题/括注仍可中文化。 |
| brainstorming | 92 | 92 | 0 | 结构清楚；文件保存和可视化伴侣段落仍偏长。 |
| browser-control | 91 | 92 | +1 | iteration-4 fixes 后补齐标准状态包和失败语义；CLI 示例仍较密。 |
| crawler4j-model-project | 89 | 90 | +1 | 状态包和 blocked 语义已补；CLI、旧命令和英文协议名仍密集。 |
| doc-coauthoring | 95 | 94 | -1 | 协作边界清楚；`status: done` 和 `Blocked` 与 Shanforge 状态词不完全一致。 |
| document-templates | 86 | 88 | +2 | metadata 与状态包已修正；主文件仍承载模板目录、迁移流程和路径映射。 |
| docx | 94 | 94 | 0 | 分支、写入、验证和失败处理清楚。 |
| executing-plans | 93 | 93 | 0 | gate 明确，状态包完整；流程项较密但可接受。 |
| frontend-patterns | 95 | 95 | 0 | 中文短句稳定，决策表清楚。 |
| gitcommitzh | 86 | 86 | 0 | 长度和重复仍是主要问题；授权、范围、message、回显规则多处复述。 |
| humanizer | 95 | 95 | 0 | 边界短、问题类型具体、输出清晰。 |
| pdf | 94 | 94 | 0 | 文件处理分支和风险语义清楚。 |
| project-memory | 95 | 95 | 0 | 读取门和事实源优先级表达稳定。 |
| python-uv-project | 88 | 90 | +2 | 已明确 Python Bug 由调试/TDD 接管，并补状态包；`Review Checklist` 和工具链清单仍偏长。 |
| receiving-code-review | 88 | 90 | +2 | 状态包和失败语义已补；memory sync 和输出位置仍在主入口展开较多。 |
| requesting-code-review | 88 | 90 | +2 | 状态包和 blocked 语义已补；独立性硬门仍有重复。 |
| requirements-engineering | 91 | 89 | -2 | 需求教材段落、INVEST、NFR 示例和角色口吻在主入口堆叠，语言入口偏重。 |
| shadcn | 94 | 93 | -1 | 边界清楚；`done/blocked`、`registry/preset/MCP` 等英文状态和术语较密。 |
| skill-creator | 85 | 85 | 0 | 主入口仍覆盖创建、改写、评估、benchmark、描述优化和打包。 |
| stratix-admin-web | 新增 | 91 | 新增 | 新 skill 语言直接，组件边界清楚；英文产品名/CLI 和状态包字段略不齐。 |
| stratix-service | 87 | 87 | 0 | 生产化矩阵、CLI 清单和安全门仍过长；状态包缺 `work_item` / `ledger_event`。 |
| subagent-driven-development | 92 | 92 | 0 | 子 agent 边界清楚；流程步骤较多但语义一致。 |
| systematic-debugging | 95 | 95 | 0 | 根因流程短句清楚，禁止项明确。 |
| tdd-workflow | 95 | 95 | 0 | Red/Green、根因和风险验证表达自然。 |
| ui-ux-pro-max | 95 | 94 | -1 | 主入口简洁；`done/blocked` 状态和英文标题仍未完全中文化。 |
| using-shanforge | 93 | 93 | 0 | 流程总控边界清楚；gate/status 词密度高但必要。 |
| verification-before-completion | 95 | 95 | 0 | 完成声明、证据和 exit code 关系表达清楚。 |
| webapp-testing | 94 | 94 | 0 | 与 browser-control 边界清楚，失败处理自然。 |
| writing-plans | 93 | 93 | 0 | 计划 gate 具体；`Plan Review` 等标题仍可中文化。 |
| xlsx | 94 | 94 | 0 | 文件处理分支、写入安全和验证表达简洁。 |

## 3. 低于 90 分问题明细

### `document-templates`：88

啰嗦重复：

- 321 行主文件仍内联“默认最小文档包”“模板资产与输出路径”“重构/迁移流程”。这些内容更像 reference，不像触发入口。
- 4 大模块、根索引职责、旧结构迁移和校验命令在多个章节反复出现。

语义不清：

- “先做判断”列出项目状态、动作、模块和暴露面，但没有明确最小路径：只补单页、只校验、完整重构分别要停在哪里。
- “正式文档治理规则”和“输出要求”都涉及 doc-map / docs/index 同步，权威更新顺序不够集中。

表达不一致：

- 同一文件同时使用“默认工作流”“正式文档治理规则”“输出要求”“状态回写与失败语义”，读者需要在四处拼合完成条件。
- `docs-stratego source validate` 既像推荐动作，又像统一收口 gate；失败后的 `blocked` / `needs_user_input` 分支可以更集中。

中英混杂：

- `docs-stratego`、`public/private`、`source validate`、`source add/remove/sync/build` 可保留，但同段英文命令和中文解释混排偏密。
- 标题“Gate 资产”等半中文半英文表达可统一为“关口资产”或直接保留 `gate` 并解释一次。

### `gitcommitzh`：86

啰嗦重复：

- 390 行中，提交授权、范围审查、`git add .` 禁止、message 一致性、真实 hash 回显在多个章节重复。
- Slash 直调、授权规则、默认工作流、禁止行为、输出模板都在重复“未提交不得输出提交结果”。

语义不清：

- “代理完成一个产生文件改动的任务时必须使用”与用户临时约束“只允许写某文件/暂不提交”之间虽有例外，但没有放在最醒目的优先级位置。
- 普通 Git 场景、Shanforge work item 场景和只写草案场景交织，入口读者不易先判断当前分支。

表达不一致：

- `blocked`、`未提交`、`草案`、`已提交` 的输出边界清楚但散落；同一提交消息一致性规则在第 2、3、4、5 步重复。
- “先给出结构化说明，再执行提交”和“已授权时不得停在草案”需要合并成一个分支表。

中英混杂：

- `Slash`、`commit message`、`staged/unstaged`、`cached`、`hash`、`message` 与中文术语频繁切换。
- Git 专名可保留，但标题和解释句可统一为中文，例如“直接调用规则”“暂存/未暂存差异”“提交信息一致性”。

### `requirements-engineering`：89

啰嗦重复：

- 用户故事、INVEST、验收标准、优先级、NFR 和 AI 摘要规则都放在主入口，像需求教程。
- “未批准不得写成批准事实”在输出位置、版本规则和状态边界中重复。

语义不清：

- description 写“requirements-analyst 代理必须参考此技能”，角色绑定口吻比当前其他 skill 更旧；普通使用者不清楚是否仅供某代理使用。
- `requirements_ready`、`ready_for_review`、`user_confirmation` 与 Shanforge 通用状态词的关系需要更明确。

表达不一致：

- `baseline`、`PRD`、`REQ`、`AC`、`NFR` 混用，部分已解释，部分默认读者知道。
- 输出位置同时写 brief、正式 PRD、ledger、memory summary，但不同任务是否都必须写没有收口。

中英混杂：

- `INVEST`、`REQ`、`AC`、`NFR`、`baseline`、`human_approved`、`AI 摘要` 密集出现。
- `Chrome 90+, Safari 15+` 等示例可留在 reference，主入口只需说明“兼容性需可度量”。

### `skill-creator`：85

啰嗦重复：

- 创建、改写、压缩、翻译、评审、评估、benchmark、描述优化、打包全部在主入口展开。
- “中文、闭环、隔离”“作者不能自批”“独立 reviewer”在强制原则、高层流程、评估流程和改进流程中重复。

语义不清：

- `eval-viewer/generate_review.py`、`generate_review.py`、`package_skill.py`、`.skill` 打包是否仍是当前仓库事实不清楚。
- “运行测试用例必须启动两个子代理任务”更像完整 benchmark 流程，不适合所有小改 skill 的默认路径。

表达不一致：

- 前半部分要求主文件精简、reference 下沉，后半部分又把评估、查看器、描述优化和打包步骤内联。
- 状态包缺 `work_item` / `ledger_event`，和多数 Shanforge 工作 skill 的状态包不一致。

中英混杂：

- `Skill Creator`、`Evaluation`、`Benchmark`、`Assertion`、`Description Optimization`、`SKILL.md`、`body` 等英文概念密集。
- 英文术语可保留一次，但标题和流程句应中文化，避免在同一段里连续切换。

### `stratix-service`：87

啰嗦重复：

- 生产化测试矩阵、版本探测、执行流程、配置安全门、常用 CLI、编码规则、环境事实和评审清单都在主入口。
- `STRATIX_SENSITIVE_CONFIG`、加解密、runtime injection、release gate 在多个章节重复强调。

语义不清：

- “测试 skill 时必须同时跑两个临时项目”是 skill 自测/生产证明要求，不适合普通业务小修默认执行。
- “结论：可上线 | blocked | needs_user_input”与状态包里的 `ready_for_review | blocked | needs_user_input` 不一致。

表达不一致：

- 管理后台前端已新增 `stratix-admin-web`，但本文件仍把 `app web-admin` 和 `stratix generate admin-page/admin-crud` 放在后端 service 主入口，边界需要重新收口。
- 输出契约缺 `work_item` 和 `ledger_event`，与 iteration-4 已修复的其他工程 skill 不齐。

中英混杂：

- `production manifest`、`release gate`、`runtime injection`、`preset`、`template`、`doctor`、`controller/service/repository` 连续出现。
- 这些是 Stratix 专名或命令，但主入口可以只保留中文解释和少量代表命令，完整 CLI 下沉到 reference。

## 4. 最常见的 10 个中文表达问题

1. 主 `SKILL.md` 仍承担 reference 职责，把模板清单、CLI 清单、迁移流程和完整教程放进入口。
2. 同一 gate 在“原则、默认流程、禁止、完成状态、输出模板”多处重复，且措辞略有差异。
3. 状态词未完全统一：`done`、`passed`、`partial`、`requirements_ready`、`document_ready`、`ready_for_review` 混用。
4. `Blocked`、`Review Checklist`、`Quality Gate`、`Plan Review`、`Description Optimization` 等标题可中文化但未统一。
5. 工具名、命令名和抽象英文概念混在同一解释句中，导致入口意图比必要程度更难读。
6. 普通任务、Shanforge work item、skill 自测/benchmark、生产上线四类场景混写，默认执行强度不清。
7. 部分 description 触发面过宽，容易压过更具体 skill，例如 Python、Stratix、需求和文档类入口。
8. 失败语义虽比 iteration-4 前更完整，但部分文件仍把 `blocked`、`needs_user_input` 和 partial 分散在正文末尾。
9. 教材式示例仍偏多，尤其是需求写作、提交工作流、文档目录和技能评估流程。
10. 少量文件仍缺 `work_item` / `ledger_event` 字段，导致“状态包”表达不如其他 skill 一致。

## 5. 相对 iteration-4 的变化

- 文件数量：34 -> 35。新增 `skills/stratix-admin-web/SKILL.md`。
- 总行数：4338 -> 4601。增加主要来自新增 skill 和 iteration-4 fixes 对状态包/失败语义的补充。
- 平均分：92.1 -> 92.1，整体持平。
- 低于 90 分数量：8 -> 5。下降原因是 `browser-control`、`python-uv-project`、`receiving-code-review`、`requesting-code-review`、`document-templates` 等文件补齐了状态包或失败语义。
- 明显改善：`document-templates` 去掉旧 D3 metadata 并补状态包；`python-uv-project` 明确 Bug owner；`receiving-code-review`、`requesting-code-review`、`browser-control`、`crawler4j-model-project` 补齐状态包。
- 仍未改善：`gitcommitzh`、`skill-creator`、`stratix-service` 的主入口压缩尚未做；这是当前最主要的语言债。
- 新增风险：`stratix-admin-web` 作为新入口总体清楚，但和 `stratix-service` 在 `web-admin/admin-page/admin-crud` 上还有边界重复。

分数下降项说明：

- `requirements-engineering`：本轮按“教程化堆叠”权重重新评分，INVEST/NFR/AC 示例放在主入口的成本更突出。
- `algorithmic-art`、`doc-coauthoring`、`shadcn`、`ui-ux-pro-max`：正文质量未恶化；小幅扣分来自 `done/Blocked` 和英文标题状态词与当前 Shanforge 状态包风格不完全一致。

## 6. 最小下一步修复清单

只列真正值得改的项：

1. `skills/skill-creator/SKILL.md`：把评估、benchmark、描述优化、打包流程下沉到 references；核实 `eval-viewer/generate_review.py`、`generate_review.py`、`package_skill.py` 和 `.skill` 是否仍是当前事实。
2. `skills/gitcommitzh/SKILL.md`：合并授权、范围、message 一致性和提交后回显规则；用一个分支表区分“只写草案 / 已授权提交 / blocked”。
3. `skills/stratix-service/SKILL.md`：把生产化双项目矩阵、完整 CLI 和环境加解密细节下沉；普通后端小修默认只保留版本探测、最小实现和目标验证。
4. `skills/document-templates/SKILL.md`：把默认文档包和模板路径映射下沉到 references；主入口只保留判断、最小工作流、治理规则和状态回写。
5. `skills/requirements-engineering/SKILL.md`：把 INVEST、AC 示例、NFR 示例和优先级教材下沉；description 去掉旧角色绑定口吻。
6. `skills/stratix-service/SKILL.md` 与 `skills/stratix-admin-web/SKILL.md`：收口 `web-admin/admin-page/admin-crud` 边界，避免后端 service 入口继续承担后台前端开发规则。
7. 全局小修：把可中文化标题统一成中文；工具名、命令名、API 名保留英文，但解释句用中文短句。

## 状态回写

```text
工作结果：
- work_item: SKILL-FLOW-AUDIT-001
- skill: chinese-language-review
- status: ready_for_review
- outputs:
  - .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/chinese-language-review-iteration-5.md
- evidence:
  - read .factory/workitems/SKILL-FLOW-AUDIT-001/task-briefs/chinese-language-review-iteration-5.md
  - read iteration-4 Chinese language review, prompt engineering review, independent review and fix summary
  - scanned 35 current skills/*/SKILL.md files
  - compared iteration-5 scores against iteration-4 Chinese language scores
- ledger_event: none
- needs:
  - review
```
