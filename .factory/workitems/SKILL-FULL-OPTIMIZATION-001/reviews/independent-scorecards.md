# SKILL-FULL-OPTIMIZATION-001 独立逐 Skill 复评

- reviewer_type: `independent_subagent`
- reviewer_id: `codex-subagent:/root/full_skill_score_review`
- reviewer_independence_evidence: 本 reviewer 与上轮为同一独立 reviewer，未参与 T01–T06 实现、本轮整改或 Git 操作，也未读取实现者会话历史；本轮重新依据 `independent-review-task.md` 的文件化输入、当前最终可见的 38 个 `skills/*/SKILL.md`、直接路由资源、17 个整改 diff、相关测试与只读行为探针逐项复评。未复用实现者分数；唯一写入是本 review 文件。
- author_self_check_score: `n/a`
- review_score: `93.7 / 100`（38 个 Skill 独立总分算术平均值，`3559 / 38 = 93.6579`）
- review_status: `approved`
- next_gate_status: `return_to_orchestrator`
- reviewed_inventory: `38 / 38`
- severity_total: `C0 / I0 / M2`
- remediation_closure: `I-01–I-17 closed (17/17)；M-01 open，新增 M-02 open`

## 评分口径

严格采用任务指定五维权重：需求符合度 30、架构一致性 20、测试充分性 20、代码质量 20、文档与记忆同步 10。单项通过线为 `>=90 / C0-I0`；整体通过还要求平均分 `>=90` 且 Critical、Important 均为 0。分数来自当前文件、直接路由资源和可执行行为的独立判断；validator、pytest 与 Ruff 是基础证据，不替代对职责边界、失败语义、可移植性和跨资源一致性的审查。

## 38/38 单项 Scorecard

| # | Skill | 能力摘要 | 需求 /30 | 架构 /20 | 测试 /20 | 质量 /20 | 文档 /10 | 总分 | C/I/M | 结论 | 独立证据 | 剩余优化方向 |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|
| 1 | agent-harness-construction | 设计 agent 行动空间、工具定义与观察/恢复格式 | 29 | 19 | 18 | 19 | 10 | 95 | 0/0/0 | 通过 | 主文件覆盖行动、观察、失败与恢复边界；inventory、flow-audit 和状态合同回归通过 | 增加工具失败与观察缺失的行为级负例 |
| 2 | ai-first-engineering | 定义 AI-first 团队授权、工程运营与质量边界 | 29 | 19 | 18 | 19 | 9 | 94 | 0/0/0 | 通过 | 适用范围、授权强度、评审责任和回写契约一致；通用合同测试通过 | 增加非 AI-first 团队不触发的负例 |
| 3 | ai-regression-testing | 设计假设回归、路径漂移与契约遗漏测试 | 29 | 19 | 18 | 19 | 9 | 94 | 0/0/0 | 通过 | 根因、同模型假设和真实路径回归职责清楚；debugging 合同测试通过 | 增加 sandbox/真实路径差异的可执行 fixture |
| 4 | algorithmic-art | 生成可复现、交互式原创 p5.js 算法艺术 | 28 | 19 | 18 | 19 | 9 | 93 | 0/0/0 | 通过 | 模板移除固定品牌/字体，主文件明确 CDN starter 与离线内联义务；I-01 关闭 | 增加离线 vendored p5.js 浏览器 smoke fixture |
| 5 | api-design | 设计/评审 REST/HTTP 契约、错误与版本兼容 | 29 | 19 | 18 | 19 | 10 | 95 | 0/0/0 | 通过 | 主文件与直接 references 对兼容、幂等、分页、错误模型一致 | 增加游标分页和错误模型的可执行契约样例 |
| 6 | art-asset-pipeline | 经风格样张与资源清单 Gate 生产应用/游戏资源包 | 29 | 19 | 18 | 19 | 9 | 94 | 0/0/0 | 通过 | 双 Gate、确认权限和交付包边界明确；状态 owner 合同通过 | 增加清单未确认时禁止批量生产的负例 |
| 7 | article-writing | 基于来源、品牌语气与读者目标创作长文 | 28 | 19 | 17 | 19 | 9 | 92 | 0/0/0 | 通过 | 适用/排除范围、事实来源和项目化回写清楚 | 增加时效事实检索、引用和不确定性行为测试 |
| 8 | brainstorming | 在项目状态上澄清范围、比较方案并形成 brief | 29 | 19 | 19 | 18 | 10 | 95 | 0/0/0 | 通过 | 主入口改为 `[可视化伴侣](visual-companion.md)`；复制 Skill 到临时安装目录并从另一 cwd 解析资源的测试通过，I-02 关闭 | 增加伴侣服务真实启动/停止与资产落盘集成 fixture |
| 9 | browser-control | 用本地真实浏览器执行导航、交互、截图与回读 | 28 | 18 | 18 | 19 | 9 | 92 | 0/0/0 | 通过 | browser-use、本地 Web 测试边界、副作用确认和证据回读清楚 | 增加 browser-use 缺失和登录态不可用失败测试 |
| 10 | crawler4j-model-project | 按 crawler4j 0.4.0 协议创建、迁移、校验和打包模块 | 29 | 19 | 18 | 19 | 9 | 94 | 0/0/0 | 通过 | 直接 references 与 core-native-v2、manifest、Hosted UI/DevLink 路由一致 | 增加旧 TaskScript 到 core-native-v2 的端到端 fixture |
| 11 | doc-coauthoring | 协同起草、改写和评审 RFC/提案/技术文档 | 28 | 19 | 18 | 19 | 9 | 93 | 0/0/0 | 通过 | 最少提问、读者验证、事实约束和局部状态包边界清楚 | 增加输入冲突时澄清/停止的负例 |
| 12 | document-templates | 建立、整理和升级通用软件项目正式文档体系 | 28 | 18 | 18 | 19 | 9 | 92 | 0/0/1 | 通过 | 主入口与 verification 均使用 `<skill-dir>/scripts/validate_test_documents.py`，稳定 ID 统一为 `TEST-*`，I-04/I-17 关闭；但 `02-user-guide/index.md` 的新链接在正式输出映射后仍指向不存在的 `docs/08-handover/` | 让资产源与物化输出同时自洽，例如把 user-guide 模板与 index 同目录维护，或在物化阶段重写并验证链接 |
| 13 | docx | 读取、编辑、修订、渲染并验证 DOCX | 29 | 19 | 19 | 19 | 8 | 94 | 0/0/0 | 通过 | `accept_changes.py` 对超时、非法 DOCX 与残留修订 fail closed，行为守卫覆盖；I-05 关闭 | 扩展残留修订检查到 header/footer 等 story parts |
| 14 | executing-plans | 当前会话内按批准计划连续开发并批次收口 | 29 | 19 | 18 | 19 | 9 | 94 | 0/0/0 | 通过 | 仅回本职结果包，不生成项目级下一动作；owner 回归通过 | 增加多批次中断恢复 fixture |
| 15 | frontend-patterns | 约束前端组件边界、状态、性能与可访问性 | 29 | 19 | 17 | 19 | 9 | 93 | 0/0/0 | 通过 | 技术栈跟随、组件复用和 a11y 规则清楚；通用合同回归通过 | 增加设计系统优先级和 a11y 行为 fixture |
| 16 | gitcommitzh | 审查 diff/暂存区并在授权后生成中文本地提交 | 28 | 18 | 18 | 19 | 10 | 93 | 0/0/0 | 通过 | 主文件、提交清单和总控统一定义 `none/无` 终态及三类 commit action 前缀，不再把提交转换本身当阻塞；合同测试覆盖三份文件，I-16 关闭 | 增加解析真实 ledger 状态矩阵并执行 dry-run 路由的行为测试 |
| 17 | go-developer | 约束 Gin+GORM+Logrus+Consul 组合栈开发 | 29 | 19 | 18 | 19 | 9 | 94 | 0/0/0 | 通过 | 严格四件套触发与工程 references 一致；专项测试通过 | 增加只命中单库时不触发的负例 |
| 18 | humanizer | 去除文本 AI 痕迹并保持事实、语气与含义 | 28 | 19 | 17 | 19 | 9 | 92 | 0/0/0 | 通过 | 触发边界、禁止虚构经历和项目化 partial 语义清楚 | 增加不改事实、引文和代码的样例回归 |
| 19 | java-developer | Java/Spring Boot 开发、评审、重构与工程文档 | 29 | 19 | 18 | 19 | 9 | 94 | 0/0/0 | 通过 | 阶段判断与工程 references 一致；专项测试覆盖 | 增加非 Spring Java 与替代框架路由负例 |
| 20 | pdf | 读取、生成、表单填写、OCR、渲染和验证 PDF | 29 | 19 | 19 | 19 | 9 | 95 | 0/0/0 | 通过 | `forms.md` 使用 `<skill-dir>`；bbox 失败非零、输出目录自动创建，行为测试通过；I-09/I-10 关闭 | 增加真实可填写/扫描 PDF 双分支 fixture |
| 21 | project-memory | 有界恢复项目状态、同步 ledger/memory 并防重复执行 | 29 | 20 | 17 | 19 | 9 | 94 | 0/0/0 | 通过 | 只投影 owner 信封，不自行生成项目级下一动作；职责回归通过 | 增加 ledger 与 memory 冲突时的恢复 fixture |
| 22 | python-uv-project | 统一 Python 项目 uv 环境、依赖和工具链规范 | 29 | 19 | 17 | 19 | 9 | 93 | 0/0/0 | 通过 | uv 职责与 debugging/TDD 边界清楚；工具链合同回归通过 | 增加 pip/requirements 迁移和无 lockfile fixture |
| 23 | receiving-code-review | 核实、分诊、整改并闭合 review feedback | 28 | 19 | 18 | 19 | 10 | 94 | 0/0/0 | 通过 | 最终状态包已加入 `implementation`，与 triage 第 13/98 行及 write-policy 分流一致；专项合同测试通过，I-07 关闭 | 增加 triage 产物到整改 TaskCard 的端到端回流 fixture |
| 24 | release-deployment | 在显式生产授权下部署、观察或回滚并留回执 | 28 | 19 | 17 | 19 | 9 | 92 | 0/0/0 | 通过 | 只回写发布证据/gate 输入，不生成项目级下一动作；生产授权边界明确 | 增加成功、回滚与授权缺失行为测试 |
| 25 | requesting-code-review | 组织独立任务/PR review、评分与质量门 | 29 | 20 | 18 | 19 | 9 | 95 | 0/0/0 | 通过 | 独立性、评分与 approved 默认回总控规则一致；I-08 关闭 | 增加真实人工 Gate 与普通 approved 的模板快照测试 |
| 26 | requirements-engineering | 把想法/brief/变更转为可验收、可追踪需求 | 29 | 20 | 17 | 19 | 9 | 94 | 0/0/0 | 通过 | 只返回需求结果与本地 needs，总控拥有下一动作；追踪契约完整 | 增加跨需求冲突和变更影响 fixture |
| 27 | shadcn | 在含 components.json 的项目添加、更新和定制组件 | 28 | 19 | 18 | 19 | 10 | 94 | 0/0/0 | 通过 | Updating Components 使用 `npx shadcn@latest add <component> --diff` 或项目运行器等价命令，与 `cli.md` 一致；跨文件负例测试通过，I-11 关闭 | 增加已定制组件更新的真实 CLI diff fixture |
| 28 | stratix-admin-web | Stratix 管理后台 CRUD、组件抽取和前端规范 | 29 | 19 | 17 | 19 | 9 | 93 | 0/0/0 | 通过 | 严格 Stratix 触发、CRUD 边界和公共组件阈值明确；专项测试通过 | 增加普通 admin 项目不触发的负例 |
| 29 | stratix-service | Stratix 后端服务、插件、Kysely 与工具链开发 | 29 | 19 | 18 | 19 | 9 | 94 | 0/0/0 | 通过 | 直接 references 与 CLI、配置、分层契约一致；专项测试通过 | 增加 preset/插件迁移的真实 fixture |
| 30 | subagent-driven-development | 按 TaskCard 隔离子代理实现并汇总批次 | 29 | 20 | 17 | 19 | 9 | 94 | 0/0/0 | 通过 | 只回本职执行结果，不重复项目状态信封；owner 回归通过 | 增加并行冲突和子代理失败汇总 fixture |
| 31 | systematic-debugging | 先复现和追踪数据流，再形成根因与最小修复点 | 29 | 19 | 18 | 19 | 9 | 94 | 0/0/0 | 通过 | 四阶段根因流程与 tracing reference 一致；停止条件测试通过 | 增加多次假设失败后重审架构的行为 fixture |
| 32 | tdd-workflow | 以 Red/Green、根因和风险分级完成开发验证 | 29 | 19 | 19 | 19 | 9 | 95 | 0/0/0 | 通过 | 直接 references 与主流程一致；debugging/verification 专项测试覆盖 | 增加测试先绿、错误失败原因和高风险 Gate 负例 |
| 33 | ui-ux-pro-max | 跨 Web/移动/桌面完成 UI/UX、动效和设计交付 | 28 | 19 | 16 | 19 | 9 | 91 | 0/0/0 | 通过 | 平台 references、样例与 skill-local 搜索脚本均可达；专项测试通过 | 增加中文查询质量、持久化输出和 a11y 验收 fixture |
| 34 | using-shanforge | 作为流程总控判断模式、唯一下一 Skill 与状态信封 | 28 | 20 | 18 | 19 | 9 | 94 | 0/0/0 | 通过 | 工具映射保持有效；提交门与 gitcommitzh/清单统一 terminal sentinel 和 commit action 语义，I-12/I-16 关闭 | 增加从 approved、verification、memory sync 到 commit 的黑盒状态转换 fixture |
| 35 | verification-before-completion | 用新鲜命令、exit code 和 evidence 约束完成声明 | 29 | 20 | 18 | 19 | 9 | 95 | 0/0/0 | 通过 | 第 93 行明确把 `<skill-dir>` 替换为 document-templates 实际安装目录并运行完整 uv 命令；跨 Skill 路径合同测试通过，I-04 关闭 | 增加把默认资产复制到临时目标项目后实际运行 validator 的集成测试 |
| 36 | webapp-testing | 用 Playwright/既有栈验证本地 Web 应用与交互证据 | 28 | 18 | 18 | 19 | 9 | 92 | 0/0/1 | 通过 | Windows 正常路径调用原生 `taskkill /PID <pid> /T /F`，单元测试验证树终止命令；POSIX 高输出/进程组测试继续通过，I-13 主缺口关闭 | `taskkill` 非零时当前仍回退为仅 terminate shell 并继续报告 stopped；应 fail closed、记录 stderr，并补失败分支测试 |
| 37 | writing-plans | 将批准输入拆为可验收 plan、TaskCard 与批次门 | 29 | 20 | 17 | 19 | 9 | 94 | 0/0/0 | 通过 | 只返回计划候选与本地 needs，不生成总控下一动作；状态合同回归通过 | 增加跨模块计划依赖环检测 fixture |
| 38 | xlsx | 读取、修改、重算并验证 Excel/CSV 工作簿 | 29 | 19 | 19 | 19 | 9 | 95 | 0/0/0 | 通过 | `main()` 对 error 结果 exit 1；缺文件、soffice 不可用和 timeout 三条 subprocess 测试及真实缺文件探针均为非零，I-14/I-15 关闭 | 增加真实 LibreOffice 公式重算、errors_found 与宏保持集成 fixture |

## I-01–I-17 整改复核

| Finding | 状态 | 独立核验依据 |
|---|---|---|
| I-01 algorithmic-art 中立性/自包含声明 | closed | 模板无固定品牌或 Google Fonts；联网 starter 与离线交付边界明确 |
| I-02 brainstorming 可移植性 | closed | 主入口改为相对 Markdown 链接；安装目录复制后从另一 cwd 解析资源的测试通过 |
| I-03 document-templates 项目特化 | closed | 目录、catalog 与技术模板已通用化，Shanforge 是条件 profile |
| I-04 document-templates 质量命令路径 | closed | document-templates 主入口与 verification 跨 Skill 路由均使用实际安装目录下的 `<skill-dir>/scripts/validate_test_documents.py`，合同测试覆盖 |
| I-05 docx 错误成功 | closed | timeout、非法 ZIP、残留修订均 fail closed，专项行为测试通过 |
| I-06 项目状态信封 owner 漂移 | closed | 相关工作 Skill 不再生成项目级 next/completion envelope；owner 合同测试通过 |
| I-07 receiving-code-review 写权限矛盾 | closed | 最终状态包加入 `implementation`，triage 结果与 write-policy 分流可一致表达 |
| I-08 review 无条件人工 Gate | closed | approved 默认 `return_to_orchestrator`，仅真实人工 Gate 暂停 |
| I-09 pdf 表单资源路径 | closed | `forms.md` 命令使用 `<skill-dir>` 且脚本后缀完整 |
| I-10 pdf 失败码/输出目录 | closed | bbox 失败非零，转换器先创建输出目录，行为测试通过 |
| I-11 shadcn 断链 | closed | 锚点命令改为 `shadcn@latest add <component> --diff`，与 cli/customization 一致并有负例测试 |
| I-12 using-shanforge 工具映射 | closed | 当前协作工具映射完整，无失效 `close_agent` 或全局配置修改 |
| I-13 webapp-testing 进程清理 | closed | Windows 主路径使用 `taskkill /T /F` 终止原生进程树，POSIX 继续使用进程组；两条平台分支均有定向测试。taskkill 失败语义作为 M-02 保留 |
| I-14 xlsx validator | closed | stdlib ZIP/XML 校验接受基本真实 XLSX 并拒绝破损包 |
| I-15 xlsx profile/超时 | closed | CLI 对 error 结果 exit 1；缺文件、soffice 不可用与 timeout 均有 subprocess 级非零测试，真实缺文件探针 exit 1 |
| I-16 gitcommitzh/using-shanforge 提交门自阻塞 | closed | 三份提交合同统一 `none/无` 与合法 commit action 前缀，提交转换不再被当作未解决动作；专项合同测试通过 |
| I-17 document-templates 测试 ID 分裂 | closed | 核心追踪规则、requirements matrix、test environment 和质量模板统一为 `TEST-*`；跨资源负例测试通过 |

## Findings

### Critical

- none

### Important

- none

### Minor

1. **M-01 / document-templates：模板链接只在源资产布局中可达，物化后仍断链。** `assets/templates/02-user-guide/index.md:13` 改为 `../08-handover/user-guide.md`，源包检查通过；但 `repository-structure.md:228` 将目标文件映射到 `docs/02-user-guide/user-guide.md`，index 物化到 `docs/02-user-guide/index.md` 后该链接会指向不存在的 `docs/08-handover/user-guide.md`。应让源与输出共用相对关系，或由可验证物化步骤重写链接。
2. **M-02 / webapp-testing：Windows 树终止失败分支仍会报告成功。** `with_server.py:53-54` 在 `taskkill` 非零时只 `process.terminate()`，未证明 child tree 已退出；失败探针观察到无异常并继续。建议记录 taskkill stderr、fail closed，并补非零/timeout 分支测试。

## Verification

- `.venv/bin/python -m pytest -q -p no:cacheprovider`：评分文件落盘后新鲜重跑 exit `0`，`269 passed, 4 subtests passed in 2.43s`；失败 `0`、error `0`、skip `0`。
- `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_brainstorming_skill.py tests/test_pr_commit_workflow_rules.py tests/test_skill_portability_and_local_contracts.py tests/test_skill_script_failure_contracts.py`：exit `0`，`34 passed in 0.89s`。
- `.venv/bin/ruff check .`：exit `0`，`All checks passed!`。
- 对动态发现的 38 个 Skill 逐个运行 `.venv/bin/python /Users/uroborus/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>`：exit `0`，`38/38` valid。
- 定向测试首次使用 `uv run pytest ...` 时因 sandbox 无权读取 `~/.cache/uv/sdists-v9/.git` 失败；改用仓库 `.venv` 后同一测试集合新鲜通过。该环境型失败未当作内容结果。
- `git diff --check`：exit `0`，无输出。
- 主 `SKILL.md` Markdown 本地链接检查：`99 checked / 0 missing`；全部 Skill Markdown：`242 checked / 0 missing`。M-01 是物化后路径语义，不是源树缺文件。
- Python 源码只读 AST 解析：`45/45`。
- inventory：动态发现 `38` 个唯一 Skill 名，逐项与 scorecard 对齐。
- scorecard 结构自检：`38` 行、`38` 个唯一 Skill、五维逐行求和一致，总分 `3559`、平均 `93.6579`、单项低于 90 为 `0`。
- XLSX CLI 探针：`python3 skills/xlsx/scripts/recalc.py /tmp/shanforge-rereview-nonexistent.xlsx` 输出 error JSON，实际 exit `1`，I-15 关闭。
- Windows 清理失败探针：模拟 `taskkill` exit `1` 后函数无异常、只调用 shell terminate，形成 M-02；未把正常路径测试外推到失败语义。
- 文档物化路径探针：source link `../08-handover/user-guide.md` 从 `docs/02-user-guide/index.md` 解析为 `docs/08-handover/user-guide.md`，与登记映射 `docs/02-user-guide/user-guide.md` 不同，形成 M-01。
- 写范围审计：本 reviewer 只通过 `apply_patch` 更新 `reviews/independent-scorecards.md`；未修改候选 Skill、测试、memory、ledger 或执行 Git 操作。

## Gate

`return_to_orchestrator`

38/38 Skill 均达到 `>=90 / C0-I0`，整体平均分 `93.7`，I-01–I-17 全部关闭，当前为 `C0/I0/M2`。两个 Minor 已给出可执行优化方向但不阻塞本轮独立 review；输入包不存在真实人工 Gate，故 approved 默认返回流程总控。本 review 不把 WorkItem 标记为 done。
