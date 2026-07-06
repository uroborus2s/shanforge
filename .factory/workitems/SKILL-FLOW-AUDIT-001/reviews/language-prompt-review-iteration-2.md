# Language And Prompt Review Iteration 2

status: DONE

本报告只评审当前工作区实际存在的 `skills/*/SKILL.md`。历史报告仅作背景参考，评分按本轮读取到的当前文件重新给出；已删除的 skill 不纳入评分。

## 扫描范围

实际扫描数量：34

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

未纳入：`skills/backend-patterns/SKILL.md`、`skills/find-skills/SKILL.md`、`skills/web-artifacts-builder/SKILL.md` 以及其他已删除 skill。

## 评分总览

| Skill | 分数 |
|---|---:|
| agent-harness-construction | 86 |
| ai-first-engineering | 85 |
| ai-regression-testing | 80 |
| algorithmic-art | 72 |
| api-design | 82 |
| article-writing | 89 |
| brainstorming | 94 |
| browser-control | 93 |
| crawler4j-model-project | 92 |
| doc-coauthoring | 74 |
| document-templates | 86 |
| docx | 76 |
| executing-plans | 93 |
| frontend-patterns | 72 |
| gitcommitzh | 89 |
| humanizer | 80 |
| pdf | 76 |
| project-memory | 94 |
| python-uv-project | 90 |
| receiving-code-review | 91 |
| requesting-code-review | 92 |
| requirements-engineering | 91 |
| shadcn | 68 |
| skill-creator | 87 |
| stratix-service | 89 |
| subagent-driven-development | 89 |
| systematic-debugging | 95 |
| tdd-workflow | 78 |
| ui-ux-pro-max | 62 |
| using-shanforge | 94 |
| verification-before-completion | 95 |
| webapp-testing | 86 |
| writing-plans | 94 |
| xlsx | 82 |

最低分：62（`ui-ux-pro-max`）

最高分：95（`systematic-debugging`、`verification-before-completion`）

## 低于 90 分问题明细

### agent-harness-construction：86

- 啰嗦重复：核心模型、行动空间、观察、恢复和预算都是清单式表达，缺少执行路径，读者需要自己推导怎么落地。
- 语义不清：没有说明它在 Shanforge 中是用于设计工具、评审工具，还是改造 agent prompt。
- prompt 边界：触发语句偏宽，容易覆盖普通工具使用、架构设计和流程评审。
- 输出契约：没有产物路径、状态包、评分表或失败语义。
- 旧口径：保留较多英文括注，整体像通用 agent 教程，不像本项目 workflow skill。

### ai-first-engineering：85

- 啰嗦重复：团队原则、招聘信号和测试标准混在主入口，作为执行 prompt 时信息密度偏散。
- 语义不清：没有明确它产出流程建议、评审意见、工程规范，还是作为其他 skill 的背景原则。
- prompt 边界：触发“设计流程、评审和架构”较宽，可能与 `writing-plans`、`requesting-code-review`、`document-templates` 重叠。
- 输出契约：没有规定报告格式、状态回写、证据路径或何时 blocked。
- 旧口径：保留 Prompt/Eval 等英文括注，尚可接受，但整体不够 Shanforge 本地化。

### ai-regression-testing：80

- 啰嗦重复：Next.js、Vitest、Supabase、Redis、OpenAI 示例占据大量主入口篇幅，适合下沉到 references。
- 语义不清：策略、命令模板、测试代码样例和 bug-check 流程混在一起，主任务不够聚焦。
- prompt 边界：触发包含 `/bug-check`、沙盒模式和多路径一致性，容易与 `systematic-debugging`、`tdd-workflow` 重叠。
- 输出契约：缺少 Shanforge 状态包、evidence 路径和失败语义。
- 旧口径：直接点名 Claude Code、Gemini Cli、Codex，且保留 `.claude/commands/bug-check.md` 旧生态示例。

### algorithmic-art：72

- 啰嗦重复：算法哲学、概念种子、p5.js、交互查看器和品牌模板要求层层铺开，入口像创作长提示词。
- 语义不清：“算法哲学运动”“概念 DNA”等表达抽象，实际交付标准不够硬。
- prompt 边界：强制“先写哲学再实现”可能覆盖用户只要一个简单 p5 草图的场景。
- 输出契约：只粗略说明 `.md/.html/.js`，没有文件命名、验证、失败或状态回写。
- 旧口径：要求理解 Anthropic 品牌标识，且使用“大师级实现”等宣传式口吻，不适合 Shanforge 中文 skill。

### api-design：82

- 啰嗦重复：大量 REST 教程、状态码、分页、认证、速率限制示例放在主文件。
- 语义不清：没有区分“设计新 API”“评审已有 API”“修 API bug”时的不同动作。
- prompt 边界：触发范围覆盖 API 设计、错误处理、版本控制和公共 API，容易和后端/需求/测试流程重叠。
- 输出契约：没有要求输出 API contract、OpenAPI 片段、决策记录、review 结论或状态包。
- 旧口径：英文括注较多，但无明显旧生态依赖。

### article-writing：89

- 啰嗦重复：整体简洁，但结构指南和质量门禁可进一步压缩。
- 语义不清：没有说明何时只给草稿、何时落盘、何时进入文档协作流程。
- prompt 边界：触发“长篇内容”较宽，和 `doc-coauthoring`、`document-templates` 存在边界重叠。
- 输出契约：缺少交付格式、事实核查证据和失败语义。
- 旧口径：`origin: ECC` 未解释来源价值，对当前项目读者无帮助。

### doc-coauthoring：74

- 啰嗦重复：三阶段协作流程写得像完整教程，包含大量用户引导话术。
- 语义不清：没有和 Shanforge 的 brief、requirements、document-templates 分清职责。
- prompt 边界：默认先“提议工作流”，但用户直接要求写文档时可能拖慢交付。
- 输出契约：没有固定输出路径、状态包、evidence、ledger 或 blocked 语义。
- 旧口径：多处使用 Claude、“新鲜 Claude”、共享文档和 alt-text 叙事，不适合当前 Codex/Shanforge 中性口径。

### document-templates：86

- 啰嗦重复：默认文档包和模板映射列表过长，主入口承担了 reference 的工作。
- 语义不清：标题写 `docs-stratego`，description 又写 D3，项目名和文档系统边界不够统一。
- prompt 边界：文档初始化、重构、校验、聚合站点集成都在同一入口，执行者需要自行裁剪。
- 输出契约：输出要求有任务分类，但缺少状态包、evidence、ledger 和 blocked 格式。
- 旧口径：metadata 仍是英文，部分旧生命周期目录映射痕迹较重。

### docx：76

- 啰嗦重复：docx-js、XML、修订、批注等实现细节过多，主入口像速查手册。
- 语义不清：读取、创建、编辑、审阅和修订处理的流程没有分支化。
- prompt 边界：触发非常宽，只要提到报告/备忘录/模板就可能抢占普通文档写作任务。
- 输出契约：验证只提 validate，缺少视觉渲染检查、输出文件清单、失败语义和状态包。
- 旧口径：要求默认使用 “Claude” 作为修订作者，且建议全局 `npm install -g docx`。

### frontend-patterns：72

- 啰嗦重复：大量 React 代码示例、hook 示例、动画和 a11y 示例堆在主入口。
- 语义不清：没有明确它是实现指导、代码评审清单还是架构建议。
- prompt 边界：触发覆盖所有前端开发，容易压过项目既有设计系统和 UI 规则。
- 输出契约：缺少产物、检查结果、状态回写和失败标准。
- 旧口径：示例强绑定 React/Jest/Framer Motion，且包含自造数据拉取 hook，容易诱导重复造轮子。

### gitcommitzh：89

- 啰嗦重复：提交范围、授权、message 一致性和禁止项反复出现，主入口 375 行偏重。
- 语义不清：规则本身清楚，但 work item 闭环检查与普通 Git 提交流程混在一起，首次触发阅读成本高。
- prompt 边界：本地提交边界明确，低风险。
- 输出契约：契约很强，是加分项。
- 旧口径：无明显旧生态口径；主要问题是重复和入口过长。

### humanizer：80

- 啰嗦重复：24 类 AI 写作特征、示例和评分表都放主文件，像完整教材。
- 语义不清：“注入灵魂”“允许一些混乱”等表达主观，容易导致风格漂移。
- prompt 边界：触发“去 AI 痕迹”清楚，但没有区分编辑、审稿、重写、只标注问题。
- 输出契约：输出格式只有重写文本和可选总结，缺少保留事实、引用限制和失败语义。
- 旧口径：来源说明可接受，但 `allowed-tools`、metadata 和外部仓库来源不符合本仓其他 skill 风格。

### pdf：76

- 啰嗦重复：pypdf、pdfplumber、reportlab、qpdf、OCR 示例堆在主入口。
- 语义不清：读取、合并、拆分、生成、OCR、加密等任务没有清晰分支。
- prompt 边界：只要提到 PDF 就触发，和文档生成、OCR、表格抽取任务边界粗。
- 输出契约：缺少 render-and-verify、输出文件清单、不可提取文本时的 blocked 语义。
- 旧口径：无明显旧生态依赖，但仍是通用工具速查口径。

### shadcn：68

- 啰嗦重复：rules、patterns、workflow、quick reference 和 detailed references 全英文堆叠。
- 语义不清：`Current Project Context` 使用注入式 `!npx...` 片段，执行者不清楚它是示例还是必须已注入的上下文。
- prompt 边界：触发非常宽，包含 shadcn 项目管理、组件搜索、debug、preset 切换和 UI composing。
- 输出契约：没有中文状态包、失败语义、验证要求或 Shanforge evidence。
- 旧口径：英文主文件、`user-invocable: false`、allowed-tools 语法和 `npx shadcn@latest` 动态口径都与当前中文规范不一致。

### skill-creator：87

- 啰嗦重复：创建、改写、评估、benchmark、描述优化、打包全部放在主入口。
- 语义不清：既要求中文闭环，又保留 eval-viewer、package_skill.py 和多子代理评估流程，当前可用性不够明确。
- prompt 边界：触发覆盖创建、修改、评估和优化，任务跨度较大。
- 输出契约：有原则和流程，但缺少统一状态包、产物路径和 blocked 格式。
- 旧口径：保留旧 eval viewer、评分员子代理和 `.skill` 打包口径，需确认是否仍是 Shanforge 当前事实。

### stratix-service：89

- 啰嗦重复：版本探测、生产化测试、CLI、配置安全门和运行时现实都在主文件，信息量偏大。
- 语义不清：面向 Stratix 生成应用、插件、管理后台、生产验证和 skill 自测，场景跨度较大。
- prompt 边界：强制生产化测试矩阵很重，简单评审或小修时可能过度执行。
- 输出契约：没有 Shanforge 状态包和标准 evidence 路径。
- 旧口径：已经明确排除旧 `@stratix/cli` 和 tasks preset，旧口径控制较好。

### subagent-driven-development：89

- 啰嗦重复：含义保留清单、默认流程、边界、禁止和完成状态有少量重复。
- 语义不清：“连续执行，不在每个任务之间问是否继续”和“继续下一个任务前必须由 using-shanforge 确认”存在张力。
- prompt 边界：子 agent 执行、review input、memory sync 都清楚，但同线程 fallback 语义可再明确。
- 输出契约：状态包完整，是加分项。
- 旧口径：无明显旧生态口径。

### tdd-workflow：78

- 啰嗦重复：TDD 原则、Jest/Vitest、Next API、Playwright、mock、CI 示例过多。
- 语义不清：80% 覆盖率、E2E 覆盖“所有关键流程”等硬要求没有风险分级，容易不适合小修。
- prompt 边界：和 `systematic-debugging`、`ai-regression-testing` 重叠明显。
- 输出契约：缺少 Shanforge 状态包，只有 reference 模板提示。
- 旧口径：强绑定 npm/Jest/Playwright/Supabase/OpenAI 示例，不够项目中立。

### ui-ux-pro-max：62

- 啰嗦重复：703 行主入口包含数据库概览、规则库、CLI 教程、设计系统持久化、app UI 检查表等，严重过载。
- 语义不清：Web、mobile app、design intelligence、search database、implementation checklist 多个角色混在一起。
- prompt 边界：触发覆盖 UI 的 plan/build/create/review/fix/optimize/refactor，几乎所有视觉任务都会被吞掉。
- 输出契约：缺少中文状态包、产物路径、验证要求和失败语义。
- 旧口径：英文主文件、app-only scope notice 与 web 触发混杂，和当前中文 Shanforge skill 风格差异最大。

### webapp-testing：86

- 啰嗦重复：整体不长，但示例脚本仍可压缩。
- 语义不清：和 `browser-control` 的边界不够明确，特别是本地页面检查和截图任务。
- prompt 边界：默认“编写原生 Python Playwright 脚本”，可能在已有 Playwright/JS 项目中违背项目现有测试栈。
- 输出契约：没有状态包、截图/日志/evidence 路径规范或失败语义。
- 旧口径：无明显旧生态口径。

### xlsx：82

- 啰嗦重复：较短，但常用操作指南和示例仍偏教程化。
- 语义不清：读取、分析、格式化、修改现有文件和生成新文件没有严格分支。
- prompt 边界：`.csv`、结构化数据分析和 Excel 文件处理混在一起，可能与通用数据分析任务重叠。
- 输出契约：缺少文件安全策略、公式验证、多 sheet 验证、输出摘要和状态包。
- 旧口径：建议依赖缺失时 `pip install`，与本仓 `uv` 口径冲突。

## Top 10 共性问题

1. 主 `SKILL.md` 承担太多 reference 职责，教程、代码样例、模板和长清单没有下沉。
2. 输出契约不统一，很多 skill 没有 `status / outputs / evidence / ledger_event / needs`。
3. 触发条件偏宽，退出条件和“不使用本 skill”的条件不足。
4. Shanforge 流程边界不一致，通用知识型 skill 很少说明和 work item、ledger、memory 的关系。
5. 英文或旧生态口径残留，集中在 `shadcn`、`ui-ux-pro-max`、`doc-coauthoring`、`docx`。
6. 框架绑定示例过多，容易把 Next.js、Jest、Supabase、Python Playwright 等误当默认事实。
7. 一些 skill 把价值观、原则或教材内容当执行 prompt，缺少可执行步骤和完成标准。
8. 验证语义不一致，流程类 skill 要求 evidence，工具类 skill 常常只给命令示例。
9. 部分规则过度刚性，没有按任务风险分级，例如固定覆盖率、完整生产矩阵或强制特定工具。
10. 重复门禁多，尤其提交、评审、测试和验证相关规则在多个段落反复出现。

## 最小修复优先级

### P0：先修会误导触发或旧口径最重的入口

1. `ui-ux-pro-max`：把主文件压到“触发、边界、CLI 最小用法、输出契约、验证门”，规则库迁入 references；全量中文化。
2. `shadcn`：中文化主入口，删除注入式 `!npx...` 片段，明确 CLI 只是候选命令；补状态包和失败语义。
3. `doc-coauthoring`：去 Claude 口径，改成“独立读者/独立模型”；明确何时只协作起草、何时落盘、何时交给 document-templates。
4. `algorithmic-art`：删除 Anthropic 品牌和宣传式措辞；把“哲学创作”降为可选路径；补 `.md/.html/.js` 输出和验证契约。

### P1：压缩教程型 skill，补统一契约

1. `frontend-patterns`、`tdd-workflow`、`ai-regression-testing`：保留原则和决策表，代码示例移入 references；按风险分级触发测试强度。
2. `pdf`、`docx`、`xlsx`：把工具速查改成任务分支；补输出文件清单、验证步骤、失败语义和安全写入规则。
3. `api-design`、`humanizer`：把长例子和模式库下沉，主入口只留执行流程、评审清单和输出格式。
4. `skill-creator`、`stratix-service`：保留核心流程，旧 eval/生产矩阵/包管理口径改为按需 reference。

### P2：清理重复和边界小问题

1. `gitcommitzh`：合并重复的范围、授权、message 一致性和禁止项。
2. `subagent-driven-development`：统一“连续执行”和“继续前总控确认”的语义。
3. `agent-harness-construction`、`ai-first-engineering`、`article-writing`：补最小输出契约和“不适用场景”。
4. `webapp-testing`：明确与 `browser-control` 的选择边界，并允许复用项目既有 Playwright 栈。

## 状态回写

```text
status: DONE
outputs:
  - .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/language-prompt-review-iteration-2.md
```
