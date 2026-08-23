# 38 个 Skill 优化结果

## 结果口径

- 清单来自 `skills/*/SKILL.md`，共 38 项。
- `optimized` 表示关闭了基线 finding；`no_change_required` 表示逐项复核后无证据支持改写。
- 本表是 implementer 结果，不替代 T06 独立评分。

## 逐项结果

| Skill | 结果 | 关闭项 / 保留能力 | 验证 |
|---|---|---|---|
| agent-harness-construction | no_change_required | 保留行动空间、观察格式、恢复与失败语义 | validator + full regression |
| ai-first-engineering | no_change_required | 保留 AI-first 团队工程运营边界 | validator + full regression |
| ai-regression-testing | no_change_required | 保留假设回归、多路径一致性与风险验证 | validator + full regression |
| algorithmic-art | optimized | `ALG-M1` + `I-01`：补 `needs_user_input`；模板移除固定品牌/外部字体并明确 p5.js 联网与离线交付边界 | portability contract + validator + full regression |
| api-design | no_change_required | 保留 API 契约、兼容性、分页与错误设计能力 | validator + full regression |
| art-asset-pipeline | no_change_required | 保留候选确认、资源清单与生产包双 Gate | validator + full regression |
| article-writing | no_change_required | 保留来源、语气、结构与长文事实边界 | validator + full regression |
| brainstorming | optimized | `I-02`：可视化伴侣资源统一从 `<skill-dir>` 解析，不依赖目标项目 cwd | portability contract + validator + workflow tests |
| browser-control | no_change_required | 保留浏览器路由、副作用确认与结果回读 | validator + browser tests |
| crawler4j-model-project | optimized | `CRAWLER-M1`：按需资料改为可点击 Markdown 链接 | contract test + crawler tests + validator |
| doc-coauthoring | optimized | `DOC-M1`：轻量状态加入 `needs_user_input` | contract test + validator |
| document-templates | optimized | `I-03/I-04`：通用目录/技术设计去除单项目必备项，Shanforge 状态目录拆为条件 profile，质量模板使用 `<skill-dir>` | cross-project/portability contracts + validator + full regression |
| docx | optimized | `DOCX-I1/M1` + `I-05`：skill-local 路径与 `partial`；接受修订超时/无效输出 fail closed，并回读确认修订标记已清除 | failure contract + validator + full regression |
| executing-plans | optimized | `I-06`：只返回执行本职结果与本地 `needs`，项目状态信封交回总控 | owner contract + workflow tests + validator |
| frontend-patterns | no_change_required | 保留组件、状态、性能与可访问性约束 | validator + full regression |
| gitcommitzh | optimized | `GIT-I1`：`human_approved` 仅用于真实人工 Gate | contract test + validator |
| go-developer | no_change_required | 保留 Gin/GORM/Logrus/Consul 严格触发与工程流程 | validator + Go skill tests |
| humanizer | optimized | `HUM-M1`：项目状态加入 `partial` | contract test + validator |
| java-developer | no_change_required | 保留 Java/Spring 分阶段路由与 references | validator + Java skill tests |
| pdf | optimized | `PDF-I1/M1` + `I-09/I-10`：全部表单命令继承 `<skill-dir>`；bbox 失败非零，转换自动创建输出目录 | failure/portability contracts + validator + full regression |
| project-memory | optimized | `I-06`：只投影总控已生成的项目状态，不在本职结果中生成项目级下一动作 | owner contract + workflow tests + validator |
| python-uv-project | no_change_required | 保留 uv 工具链、迁移与 Python 工程约束 | validator + full regression |
| receiving-code-review | optimized | `I-06/I-07`：triage 的 `state_or_gate_write` 与整改的 `source_or_test_write` 分流，且不返回总控字段 | owner/review routing contracts + validator + workflow tests |
| release-deployment | optimized | `REL-M1` + `I-06`：明确专业回执与共享任务信封分工，不决定项目级下一动作 | owner contract + validator |
| requesting-code-review | optimized | `I-06/I-08`：移除总控字段；独立 review approved 默认回总控，仅真实人工 Gate 才等待确认 | review gate contracts + validator + workflow tests |
| requirements-engineering | optimized | `I-06`：只返回需求事实、本地状态与 `needs`，不决定项目级下一动作 | owner contract + validator + workflow tests |
| shadcn | optimized | `SHADCN-I1/M1` + `I-11`：最小按需读取与 `needs_user_input`；补齐被引用的 Updating Components 工作流 | anchor/portability contract + validator |
| stratix-admin-web | no_change_required | 保留严格触发、CRUD 与公共组件抽取门槛 | validator + Stratix tests |
| stratix-service | optimized | `STRATIX-I1`：补共享项目化回写契约 | contract tests + Stratix tests + validator |
| subagent-driven-development | optimized | `I-06`：子 agent/主执行器只回本职结果，本地 `needs` 与项目状态 owner 分离 | owner contract + validator + workflow tests |
| systematic-debugging | no_change_required | 保留根因调查、停止条件与 owner 交接 | validator + workflow tests |
| tdd-workflow | no_change_required | 保留 Red/Green、根因门与风险分级验证 | validator + workflow tests |
| ui-ux-pro-max | optimized | `UI-I1`：搜索脚本入口改用 `<skill-dir>` | portability test + UI/UX tests + validator |
| using-shanforge | optimized | `I-12`：Codex 协作工具表只列当前可用动作，不修改用户全局配置，不引用失效 skill | tool-map contract + validator + workflow tests |
| verification-before-completion | optimized | `I-06`：只验证声明与证据覆盖范围，项目位置/完成层级/停止原因/剩余工作由总控生成 | owner contract + validator + workflow tests |
| webapp-testing | optimized | `WEB-I1/M1` + `I-13`：路径/状态契约；服务器不再用未消费 PIPE，检测早退并终止完整进程组 | process failure contract + validator + full regression |
| writing-plans | optimized | `I-06`：计划 Skill 只返回候选计划与本地 `needs`，不决定项目级下一动作 | owner contract + validator + workflow tests |
| xlsx | optimized | `XLSX-I1/M1` + `I-14/I-15`：补真实 XLSX 结构校验；重算使用隔离 LibreOffice profile，超时 fail closed | failure contract + validator + full regression |

## 汇总

- `optimized`：24。
- `no_change_required`：14。
- 基线 finding：C0 / I8 / M10。
- 首轮独立评分：38/38，`89.1 / C0-I23-M0`，合并为 15 个 Important finding。
- P0 整改：15/15 已实现并通过完整回归；最终 C/I/M 与单项分数仍由同一独立 reviewer 复评判定。
