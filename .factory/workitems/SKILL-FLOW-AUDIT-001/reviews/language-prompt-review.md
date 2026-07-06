# 中文语言与 Prompt 质量评审

只读评审已完成，未修改文件。评审范围仅包括仓库内 `skills/*/SKILL.md`，并参考允许读取的 `.factory/memory/runtime-brief.md` 与 `.factory/memory/skill-updates.summary.md`。

## 评分总览

| Skill | 分数 |
|---|---:|
| agent-harness-construction | 86 |
| ai-first-engineering | 84 |
| ai-regression-testing | 78 |
| algorithmic-art | 80 |
| api-design | 83 |
| article-writing | 90 |
| backend-patterns | 76 |
| brainstorming | 92 |
| browser-control | 93 |
| crawler4j-model-project | 91 |
| doc-coauthoring | 78 |
| document-templates | 86 |
| docx | 82 |
| executing-plans | 91 |
| find-skills | 76 |
| frontend-patterns | 77 |
| gitcommitzh | 88 |
| humanizer | 84 |
| pdf | 80 |
| project-memory | 92 |
| python-uv-project | 90 |
| receiving-code-review | 91 |
| requesting-code-review | 88 |
| requirements-engineering | 86 |
| shadcn | 78 |
| skill-creator | 89 |
| stratix-service | 92 |
| subagent-driven-development | 89 |
| systematic-debugging | 94 |
| tdd-workflow | 80 |
| ui-ux-pro-max | 72 |
| using-shanforge | 93 |
| verification-before-completion | 94 |
| web-artifacts-builder | 78 |
| webapp-testing | 84 |
| writing-plans | 92 |
| xlsx | 83 |

## 低于 90 分的关键问题

- `agent-harness-construction`：偏概念清单，缺少输入、输出和完成标准。建议补“何时使用 / 产出什么 / 如何判断工具设计合格”三段。
- `ai-first-engineering`：像团队原则文章，不像可执行 skill。建议压缩价值观，增加评审输出格式和适用边界。
- `ai-regression-testing`：示例代码过多，且强绑定 Next.js/Vitest/Supabase。建议主文件保留策略和触发，框架示例移入 `references/`。
- `algorithmic-art`：英文口径和宣传式措辞不自然，且模板依赖说明不够稳。建议改成中文短句，删除宣传式要求，明确最终文件清单。
- `api-design`：内容完整但教程化，缺少“执行时输出什么”。建议把长示例下沉，只保留 API 评审清单、决策表和输出模板。
- `backend-patterns`：代码样例过多，且默认引入 Repository/Service 等抽象，容易诱导过度工程。建议改成“先复用项目现有模式”，把模式示例放 references。
- `doc-coauthoring`：仍有 Claude 口径，且“让新鲜 Claude 测试”不适合所有环境。建议改为“独立读者/独立模型”，明确何时写文件、何时只协作起草。
- `document-templates`：路径和模板列表过长，主文件负担重；metadata 仍是英文。建议主文件只留判断流程和输出要求，模板映射移入 reference。
- `docx`：工具细节实用，但“使用 Claude 作为作者”、全局 `npm install -g` 和 XML 操作规则不够项目中立。建议改为可配置作者、优先本地依赖，并补最终验证输出。
- `find-skills`：依赖外部 `npx skills` 生态和安装量判断，和当前 Codex skill 安装机制边界不清。建议对齐本环境的 skill/tool 安装流程，安装前必须确认。
- `frontend-patterns`：教程代码太多，示例有自造 hook 和性能建议，容易覆盖项目既有模式。建议压成 React 评审/实现检查表，复杂示例移走。
- `gitcommitzh`：规则严谨但重复很多，尤其提交前/提交后门禁多次出现。建议合并授权规则、范围规则和提交一致性规则。
- `humanizer`：内容有价值，但主文件像完整写作教材。建议把 24 类模式移入 reference，主文件保留处理流程、评分表和最常见模式。
- `pdf`：工具速查清楚，但缺少 render-and-verify 或布局质量门，输出格式也弱。建议补“读取/生成/修改 PDF 后必须如何验证”的最小闭环。
- `requirements-engineering`：结构太短，缺少 Shanforge 输出路径、状态回写和需求审批边界。建议补 PRD/AC/NFR 的产物位置与完成状态。
- `shadcn`：几乎全英文，且包含动态注入式 `!npx...` 口径，不适合当前仓中文规范。建议中文化，删除不可执行注入片段，保留 CLI 路由和关键规则。
- `skill-creator`：总体好，但评估流程仍偏重旧 eval viewer/子代理假设。建议明确“当前环境可用工具优先”，把长评估步骤移入 reference。
- `subagent-driven-development`：有“连续执行”和“继续前交还 using-shanforge 确认”的轻微冲突。建议统一为“单任务完成后回写，由总控决定是否继续批量”。
- `tdd-workflow`：过长且框架绑定，80% 覆盖率硬要求过粗。建议改成风险分级测试策略，长 Jest/Playwright 示例移入 references。
- `ui-ux-pro-max`：最大问题是英文主文件、超长数据库说明、重复 checklist，触发和执行流程被淹没。建议中文化主入口，只保留 search 脚本用法、设计系统流程和交付检查。
- `web-artifacts-builder`：仍是 claude.ai artifact 口径，且建议“通常避免预先测试”与本项目验证文化冲突。建议改成通用 Web artifact，交付前至少跑最小渲染检查。
- `webapp-testing`：可执行性不错，但强调 Python Playwright，和现有浏览器/插件工具边界不清。建议补“何时用 browser-control，何时用本 skill”。
- `xlsx`：实用但简略，安装依赖、覆盖文件、格式保留和公式验证边界不够。建议补安全写入、公式/多 sheet 验证、输出摘要模板。

## Top 10 问题模式

1. 主 `SKILL.md` 过长，把教程、代码样例、模板和数据库内容塞进入口。
2. 英文口径残留明显，尤其 `ui-ux-pro-max`、`shadcn`、部分 artifact/Claude 表述。
3. 输出契约不统一：很多 skill 没写清最终产物、状态包、证据和失败语义。
4. 触发条件写得宽，退出条件写得少，容易误触发。
5. 职责边界混乱：部分工作 skill 仍暗示自己决定下一步流程。
6. 示例强绑定特定框架，容易误导不同技术栈项目。
7. 重复门禁过多，尤其 review、提交、验证相关规则在多个段落反复出现。
8. 教程型 skill 缺少“先复用仓内既有模式”的约束。
9. 一些旧生态口径未清理，如 Claude、claude.ai、外部 `npx skills`。
10. 部分中文表达像直译，术语括注过多，阅读阻力偏高。
