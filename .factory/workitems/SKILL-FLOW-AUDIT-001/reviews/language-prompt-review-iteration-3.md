# Language And Prompt Review Iteration 3

status: DONE
blocked: no

本报告只评审当前工作区实际存在的 `skills/*/SKILL.md`。已删除 skill 不纳入评分。分数按本轮读取到的当前文件重新给出；delta 为本轮分数减去 iteration-2 分数，不表示一定由某一次文件修改直接造成。

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

## 评分总览

| Skill | Iteration 2 | Iteration 3 | Delta |
|---|---:|---:|---:|
| agent-harness-construction | 86 | 92 | +6 |
| ai-first-engineering | 85 | 91 | +6 |
| ai-regression-testing | 80 | 92 | +12 |
| algorithmic-art | 72 | 94 | +22 |
| api-design | 82 | 95 | +13 |
| article-writing | 89 | 93 | +4 |
| brainstorming | 94 | 93 | -1 |
| browser-control | 93 | 93 | 0 |
| crawler4j-model-project | 92 | 90 | -2 |
| doc-coauthoring | 74 | 93 | +19 |
| document-templates | 86 | 88 | +2 |
| docx | 76 | 93 | +17 |
| executing-plans | 93 | 93 | 0 |
| frontend-patterns | 72 | 94 | +22 |
| gitcommitzh | 89 | 88 | -1 |
| humanizer | 80 | 93 | +13 |
| pdf | 76 | 93 | +17 |
| project-memory | 94 | 94 | 0 |
| python-uv-project | 90 | 89 | -1 |
| receiving-code-review | 91 | 90 | -1 |
| requesting-code-review | 92 | 90 | -2 |
| requirements-engineering | 91 | 92 | +1 |
| shadcn | 68 | 94 | +26 |
| skill-creator | 87 | 87 | 0 |
| stratix-service | 89 | 89 | 0 |
| subagent-driven-development | 89 | 91 | +2 |
| systematic-debugging | 95 | 95 | 0 |
| tdd-workflow | 78 | 94 | +16 |
| ui-ux-pro-max | 62 | 95 | +33 |
| using-shanforge | 94 | 94 | 0 |
| verification-before-completion | 95 | 95 | 0 |
| webapp-testing | 86 | 94 | +8 |
| writing-plans | 94 | 94 | 0 |
| xlsx | 82 | 93 | +11 |

最低分：87（`skill-creator`）

最高分：95（`api-design`、`systematic-debugging`、`ui-ux-pro-max`、`verification-before-completion`）

低于 90 分数量：5（iteration-2 为 21）

平均分：92.3（iteration-2 为 85.2）

总体判断：相对 iteration-2 明显改善。主要改善来自入口中文化、输出契约补齐、旧生态措辞清理和教程内容压缩。剩余问题集中在少数长入口和几个输出协议不统一的工程类 skill。

## 低于 90 分问题明细

### 啰嗦 / 重复

- `document-templates`（88）：默认最小文档包、模板资产映射、迁移流程仍放在主入口，306 行主文件承担了 reference 职责。
- `gitcommitzh`（88）：387 行，提交范围、暂存区、message 一致性、禁止项和提交后回显规则多处重复。规则强，但阅读成本仍高。
- `skill-creator`（87）：创建、改写、翻译、评审、评估、benchmark、打包全部在主入口，187 行仍像完整操作手册。
- `stratix-service`（89）：219 行，版本探测、生产化矩阵、配置安全、CLI 命令和评审清单都在主文件；简单 Stratix 评审会被重流程拖住。
- `python-uv-project`（89）：项目结构、日常开发、迁移、编码、测试和 review checklist 全部展开，作为入口略重。

### 语义不清

- `document-templates`：metadata 仍写 “Software project lifecycle document system for D3”，正文又是 `docs-stratego` 4 大模块文档系统；D3 含义未解释。
- `skill-creator`：当前可用的评估工具、`eval-viewer/generate_review.py`、`package_skill.py` 和 `.skill` 打包事实没有在入口说明是否仍是现行能力。
- `stratix-service`：同时覆盖生成应用、插件、管理后台、skill 自测和生产上线证明；“测试 skill 时必须跑两个临时项目”与普通业务实现/评审场景边界不够分明。
- `python-uv-project`：作为工程规范 skill 很清楚，但缺少与 `systematic-debugging`、`tdd-workflow` 的优先级说明；遇到 Python bug 时容易不清楚谁先接管。

### Prompt 边界

- `document-templates`：正式文档初始化、历史迁移、增量补文档、聚合站点集成都在一个入口，容易覆盖普通文档协作任务。
- `gitcommitzh`：本地提交边界清楚，但 Shanforge work item 闭环检查与普通 Git 提交流程交织，非 work item 场景阅读负担偏高。
- `skill-creator`：触发范围覆盖创建、修改、评审、评估、描述优化和打包，建议把评估/打包作为按需分支或 references。
- `stratix-service`：生产化验证矩阵过强，缺少按“解释/评审/小修/新项目/上线”分级的执行强度。
- `python-uv-project`：触发描述覆盖几乎所有 Python 开发，容易压过更具体的 bug、TDD、API 或 CLI skill。

### 输出契约

- `python-uv-project`：缺少 Shanforge 状态包、`blocked`/`needs_user_input` 语义和 evidence 字段。
- `crawler4j-model-project`（90，未低于 90 但接近）：规则清楚，但没有统一状态包；对创建、迁移、打包、发布失败时的输出格式不足。
- `document-templates`：已有状态包，但缺少 `ledger_event`，memory/doc-map 同步条件也没有进入状态包。
- `requesting-code-review`（90，未低于 90 但接近）：独立评审门很强，但缺少像其他流程 skill 一样的标准状态包代码块。
- `receiving-code-review`（90，未低于 90 但接近）：输出位置明确，但完成状态没有标准化为 `status / outputs / evidence / ledger_event / needs`。

### 旧口径 / 英文措辞

- `document-templates`：description 全英文且含 D3；标题和正文已中文化，但 metadata 仍不符合当前中文 skill 风格。
- `skill-creator`：保留旧评估查看器、`.skill` 打包和评分员子代理工作流；需核实后下沉或更新。
- `stratix-service`：旧 `@stratix/cli`、tasks preset 等多为明确禁用口径，不算错误，但旧口径密度高，主入口显得像迁移备忘录。
- `browser-control`、`using-shanforge` 中的 Codex/Chrome/Browser 英文是工具名，当前可接受。

## Top 10 剩余共性问题

1. 少数主 `SKILL.md` 仍承担 reference 职责，尤其是长模板清单、命令矩阵和评估流程。
2. 输出状态包还没有完全统一，部分 skill 缺 `ledger_event`、`work_item`、`needs` 或失败语义。
3. 工程类 skill 的触发边界仍偏宽，容易与更具体的调试、TDD、API、文档或 UI skill 重叠。
4. 风险分级已经变好，但少数 skill 仍把重验证矩阵写成默认路径。
5. metadata 中文化不彻底，`document-templates` 仍有英文 description 和未解释产品名。
6. “旧口径”大多已变成禁用说明，但在 `stratix-service`、`crawler4j-model-project` 这类迁移 skill 中密度偏高。
7. 普通场景与 Shanforge work item 场景的输出要求有时混写，增加非 work item 使用成本。
8. 一些流程 skill 的状态词不完全一致，例如 `done`、`passed`、`ready_for_review`、`document_ready` 混用。
9. 部分按需 references 已被正确引用，但主入口没有明确“读到哪里就够了”的退出条件。
10. 少数 skill 的工具事实具有时效性，入口需要更强调“先探测当前版本，再执行候选命令”。

## 最小下一步修复清单

### P0：把低于 90 的 5 个入口拉过线

1. `skills/skill-creator/SKILL.md`：保留创建/改写主流程；把评估、benchmark、description optimization、打包移到 references；核实 `eval-viewer/generate_review.py`、`package_skill.py` 和 `.skill` 是否仍是现行事实。
2. `skills/document-templates/SKILL.md`：把 description 改成中文，解释或删除 D3；把默认文档包和模板映射清单下沉到 references；状态包补 `ledger_event` 和 memory/doc-map 同步条件。
3. `skills/gitcommitzh/SKILL.md`：合并重复的范围门、message 一致性门、提交执行门和提交后回显门；普通 Git 场景与 Shanforge work item 场景分成两个短分支。
4. `skills/python-uv-project/SKILL.md`：补标准状态包与 blocked 语义；明确 Python bug 先走 `systematic-debugging`/`tdd-workflow`，本 skill 只提供 uv 与项目结构约束。
5. `skills/stratix-service/SKILL.md`：把生产化测试矩阵和常用 CLI 下沉到 references；按解释、评审、小修、新项目、上线分级验证。

### P1：修接近 90 的契约不齐

1. `skills/crawler4j-model-project/SKILL.md`：补输出契约和 blocked 语义，不必大改内容。
2. `skills/requesting-code-review/SKILL.md`：补标准状态包代码块，保留独立性硬门。
3. `skills/receiving-code-review/SKILL.md`：把完成状态改成固定 `status / outputs / evidence / ledger_event / needs`。

### P2：小幅压缩即可

1. `skills/brainstorming/SKILL.md`：保留流程，但压缩文件保存位置和状态判断表。
2. `skills/browser-control/SKILL.md`：输出格式可改成状态包 + 用户可读摘要双模式。
3. `skills/using-shanforge/SKILL.md`：状态词表统一到一处，减少路由表和提交门重复。

## 状态回写

```text
工作结果：
- work_item: SKILL-FLOW-AUDIT-001
- skill: language-prompt-review
- status: ready_for_review
- outputs:
  - .factory/workitems/SKILL-FLOW-AUDIT-001/reviews/language-prompt-review-iteration-3.md
- evidence:
  - read task brief and iteration-2 fix report
  - scanned 34 current skills/*/SKILL.md files
  - compared scores against language-prompt-review-iteration-2.md
- needs:
  - review
```
