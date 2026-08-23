# SKILL-FULL-OPTIMIZATION-001 独立逐 Skill 复评

- reviewer_type: `independent_subagent`
- reviewer_id: `codex-subagent:/root/full_skill_score_review`
- reviewer_independence_evidence: reviewer 未参与 T01–T06 实现或整改，未读取实现者会话历史；本轮重新读取 `independent-review-task.md` 的全部文件化输入、动态发现的 38 个 `skills/*/SKILL.md` 及直接路由资源，并运行只读验证。唯一写入为本 review 文件。
- author_self_check_score: `n/a`
- review_score: `95.0 / 100`（38 个 Skill 独立总分的算术平均值）
- review_status: `approved`
- next_gate_status: `return_to_orchestrator`
- reviewed_inventory: `38 / 38`
- severity_total: `C0 / I0 / M0`
- remediation_closure: `I-01–I-15 closed (15/15)`

## 评分口径

严格采用任务指定五维权重：需求符合度 30、架构一致性 20、测试充分性 20、代码质量 20、文档与记忆同步 10。单项通过线为 `>=90 / C0-I0`。分数来自当前文件与行为证据的独立判断，不复用 implementer 自评分；validator、pytest 和 Ruff 仅作为佐证，不替代对职责边界、失败语义、可移植性和直接路由资源的审查。

## 38/38 单项 Scorecard

| # | Skill | 能力摘要 | 需求 /30 | 架构 /20 | 测试 /20 | 质量 /20 | 文档 /10 | 总分 | C/I/M | 结论 | 独立证据 | 剩余优化方向 |
|---:|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| 1 | agent-harness-construction | 设计 agent 行动空间、工具和观察/恢复格式 | 29 | 19 | 19 | 19 | 10 | 96 | 0/0/0 | 通过 | 主文件明确行动、观察、恢复边界；inventory、flow-audit 与状态合同回归通过 | 增加工具失败和观察缺失的行为级负例 |
| 2 | ai-first-engineering | 定义 AI-first 团队运营、授权和质量边界 | 29 | 19 | 18 | 19 | 9 | 94 | 0/0/0 | 通过 | 适用边界、授权强度和回写契约一致；通用合同回归通过 | 增加非 AI-first 团队不触发的负例 |
| 3 | ai-regression-testing | 设计假设回归、路径漂移和契约遗漏测试 | 29 | 19 | 19 | 19 | 9 | 95 | 0/0/0 | 通过 | 根因与回归职责清楚；专项 references 和 bug-fix 合同测试一致 | 增加 sandbox/真实路径差异的可执行 fixture |
| 4 | algorithmic-art | 生成可复现、交互式原创 p5.js 算法艺术 | 28 | 19 | 18 | 20 | 10 | 95 | 0/0/0 | 通过 | `viewer.html` 已移除固定品牌和 Google Fonts；主文件与模板明确 CDN starter 及离线内联要求 | 增加离线 vendored p5.js 的浏览器 smoke fixture |
| 5 | api-design | 设计/评审 REST/HTTP 契约、错误和版本兼容 | 29 | 19 | 19 | 19 | 10 | 96 | 0/0/0 | 通过 | 主文件和直接 references 对兼容性、幂等、分页、错误模型一致 | 增加游标分页与错误模型示例契约测试 |
| 6 | art-asset-pipeline | 经风格与清单 Gate 生产应用/游戏资源包 | 29 | 19 | 18 | 19 | 10 | 95 | 0/0/0 | 通过 | 双 Gate、确认权限和交付包边界明确；状态合同回归通过 | 增加清单未确认时禁止批量生产的负例 |
| 7 | article-writing | 基于来源、品牌语气和读者目标创作长文 | 29 | 19 | 18 | 19 | 9 | 94 | 0/0/0 | 通过 | 适用/排除范围、事实来源和项目化回写规则清楚 | 增加时效性事实检索与引用行为测试 |
| 8 | brainstorming | 在当前项目状态上澄清范围、比较方案并产出 brief | 29 | 19 | 18 | 19 | 10 | 95 | 0/0/0 | 通过 | `visual-companion.md` 定义并统一使用 `<skill-dir>`；启动、停止和资产路径不依赖仓库 cwd | 增加任意 cwd 下伴侣启动/停止集成 fixture |
| 9 | browser-control | 用本地真实浏览器执行导航、交互、截图与状态回读 | 28 | 18 | 18 | 19 | 10 | 93 | 0/0/0 | 通过 | browser-use/本地 Web 测试边界、副作用确认和证据回读清楚 | 增加 browser-use 缺失和登录态不可用的失败路径测试 |
| 10 | crawler4j-model-project | 按 crawler4j 0.4.0 协议创建、迁移、校验和打包模块 | 29 | 19 | 18 | 19 | 10 | 95 | 0/0/0 | 通过 | 三份直接 references 与版本、manifest、Hosted UI/DevLink 路由一致 | 增加旧 TaskScript 到 core-native-v2 的端到端 fixture |
| 11 | doc-coauthoring | 协同起草、改写和评审 RFC/提案/技术文档 | 29 | 19 | 18 | 19 | 10 | 95 | 0/0/0 | 通过 | 最少提问、读者验证和局部状态包边界明确 | 增加输入互相冲突时的澄清/停止负例 |
| 12 | document-templates | 建立、整理和升级通用软件项目正式文档体系 | 28 | 19 | 19 | 19 | 10 | 95 | 0/0/0 | 通过 | catalog、repository structure 和技术模板已通用化，Shanforge 为条件 profile；质量模板统一 `<skill-dir>` | 增加非 Shanforge 项目的生成快照 fixture |
| 13 | docx | 读取、编辑、修订、渲染并验证 DOCX | 29 | 19 | 20 | 19 | 9 | 96 | 0/0/0 | 通过 | `accept_changes.py` 对超时、非法 DOCX 和残留修订闭合失败；行为守卫覆盖成功/失败分支 | 扩展残留修订检查到 header/footer 等 story parts |
| 14 | executing-plans | 当前会话内按批准计划连续开发并批次收口 | 29 | 20 | 18 | 19 | 9 | 95 | 0/0/0 | 通过 | 仅返回本职结果包，不生成项目级下一动作或状态信封；owner 负例通过 | 增加多批次中断恢复 fixture |
| 15 | frontend-patterns | 约束前端组件边界、状态、性能和可访问性 | 29 | 19 | 18 | 19 | 10 | 95 | 0/0/0 | 通过 | 技术栈跟随、组件复用和 a11y 规则清晰；合同回归通过 | 增加既有设计系统优先级与 a11y 回归 fixture |
| 16 | gitcommitzh | 审查 diff/暂存区并在授权后生成中文本地提交 | 29 | 19 | 19 | 19 | 10 | 96 | 0/0/0 | 通过 | 提交门、任务范围隔离、人工 Gate 与 push/PR 排除边界一致 | 增加混合脏工作区只提交任务范围的集成 fixture |
| 17 | go-developer | 约束 Gin+GORM+Logrus+Consul 组合栈开发 | 29 | 19 | 18 | 19 | 10 | 95 | 0/0/0 | 通过 | 严格组合触发与五份工程 references 一致；专项测试覆盖 | 增加只命中单库时不触发的负例 |
| 18 | humanizer | 去除文本 AI 痕迹并保持事实、语气和含义 | 28 | 19 | 18 | 19 | 9 | 93 | 0/0/0 | 通过 | 触发边界、禁止虚构经历和项目化 partial 语义清楚 | 增加不改事实、引文和代码的样例回归 |
| 19 | java-developer | Java/Spring Boot 开发、评审、重构和工程文档 | 29 | 19 | 18 | 19 | 10 | 95 | 0/0/0 | 通过 | 阶段判断与三份工程 references 一致；专项测试覆盖 | 增加非 Spring Java 与替代框架的路由负例 |
| 20 | pdf | 读取、生成、表单填写、OCR、渲染和验证 PDF | 29 | 19 | 20 | 19 | 9 | 96 | 0/0/0 | 通过 | `forms.md` 全部命令使用 `<skill-dir>`；bbox 失败非零、图片目录自动创建，P0 行为测试通过 | 增加真实可填写/扫描 PDF 双分支 fixture |
| 21 | project-memory | 有界恢复项目状态、同步 ledger/memory 并防重复执行 | 29 | 20 | 18 | 19 | 9 | 95 | 0/0/0 | 通过 | 明确只投影 owner 已生成的 envelope，不自行生成 `next_required_action`；职责负例通过 | 增加 ledger 与 memory 冲突时的恢复 fixture |
| 22 | python-uv-project | 统一 Python 项目 uv 环境、依赖和工具链规范 | 29 | 19 | 18 | 19 | 9 | 94 | 0/0/0 | 通过 | uv 职责与 debugging/TDD 边界清楚；工具链合同回归通过 | 增加 pip/requirements 迁移和无 lockfile fixture |
| 23 | receiving-code-review | 核实、分诊、整改并闭合 review feedback | 28 | 20 | 19 | 19 | 9 | 95 | 0/0/0 | 通过 | triage 为 `state_or_gate_write`、整改 TaskCard 为 `source_or_test_write`，权限与流程不再矛盾 | 增加 triage 到整改 TaskCard 的端到端回流测试 |
| 24 | release-deployment | 在显式生产授权下部署、观察或回滚并留回执 | 28 | 19 | 18 | 19 | 10 | 94 | 0/0/0 | 通过 | 只回写发布证据/gate 输入，不生成项目级下一动作；授权边界明确 | 增加成功、回滚和授权缺失的行为测试 |
| 25 | requesting-code-review | 组织独立任务/PR review、评分和质量门 | 29 | 20 | 19 | 19 | 9 | 96 | 0/0/0 | 通过 | 主文件和独立评审模板均规定 approved 默认返回 orchestrator，仅真实人工 Gate 才暂停 | 增加真实人工 Gate 与普通 approved 的模板快照测试 |
| 26 | requirements-engineering | 把想法/brief/变更转为可验收、可追踪需求 | 29 | 20 | 18 | 19 | 9 | 95 | 0/0/0 | 通过 | 只返回需求结果和 needs，总控拥有下一动作；追踪契约完整 | 增加跨需求冲突和变更影响 fixture |
| 27 | shadcn | 在含 components.json 的项目添加、更新和定制组件 | 28 | 19 | 19 | 19 | 10 | 95 | 0/0/0 | 通过 | 主文件恢复 `Updating Components`，cli/customization 锚点可达且 smart merge 流程完整 | 增加已定制组件升级的真实 diff fixture |
| 28 | stratix-admin-web | Stratix 管理后台 CRUD、组件抽取和前端规范 | 29 | 19 | 18 | 19 | 9 | 94 | 0/0/0 | 通过 | 严格 Stratix 触发、CRUD 边界和公共组件阈值明确 | 增加普通 admin 项目不触发的负例 |
| 29 | stratix-service | Stratix 后端服务、插件、Kysely 和工具链开发 | 29 | 19 | 18 | 19 | 10 | 95 | 0/0/0 | 通过 | 五份直接 references 与 CLI、配置和分层契约一致 | 增加 preset/插件迁移的真实 fixture |
| 30 | subagent-driven-development | 按 TaskCard 隔离子代理实现并汇总批次 | 29 | 20 | 18 | 19 | 9 | 95 | 0/0/0 | 通过 | 只回本职执行结果，不重复项目状态信封或下一动作；owner 负例通过 | 增加并行冲突和子代理失败汇总 fixture |
| 31 | systematic-debugging | 先复现和追踪数据流，再形成根因与最小修复点 | 29 | 19 | 18 | 19 | 10 | 95 | 0/0/0 | 通过 | 四阶段根因流程与 tracing reference 一致；专项停止条件测试覆盖 | 增加多次假设失败后重审架构的行为 fixture |
| 32 | tdd-workflow | 以 Red/Green、根因和风险分级完成开发验证 | 29 | 19 | 19 | 19 | 10 | 96 | 0/0/0 | 通过 | 三份直接 references 与主流程一致；debugging/verification 专项测试覆盖 | 增加测试先绿、错误失败原因和高风险 Gate 负例 |
| 33 | ui-ux-pro-max | 跨 Web/移动/桌面完成 UI/UX、动效和设计交付 | 28 | 19 | 17 | 19 | 10 | 93 | 0/0/0 | 通过 | 11 份平台 references、样例和 skill-local 搜索脚本均可达 | 增加中文查询质量、持久化输出和 a11y 验收 fixture |
| 34 | using-shanforge | 作为流程总控判断模式、唯一下一 Skill 和状态信封 | 29 | 20 | 19 | 19 | 9 | 96 | 0/0/0 | 通过 | `codex-tools.md` 映射当前协作工具，移除失效 close/global-config 指令；总控 owner 唯一 | 增加平台工具清单变化的自动漂移检测 |
| 35 | verification-before-completion | 用新鲜命令、exit code 和 evidence 约束完成声明 | 29 | 20 | 19 | 19 | 9 | 96 | 0/0/0 | 通过 | 仅判断验证声明覆盖范围，不生成项目 completion/remaining/next-action；完整回归通过 | 增加长任务新鲜度过期和部分验证负例 |
| 36 | webapp-testing | 用 Playwright/既有栈验证本地 Web 应用和交互证据 | 28 | 19 | 20 | 19 | 9 | 95 | 0/0/0 | 通过 | `with_server.py` 不用未消费 PIPE，检测早退并按进程组清理；高输出/子树行为测试通过 | 增加 Windows 子进程树清理 fixture |
| 37 | writing-plans | 将批准输入拆为可验收 plan、TaskCard 和批次门 | 29 | 20 | 18 | 19 | 9 | 95 | 0/0/0 | 通过 | 只返回计划候选和 needs，不生成总控下一动作；状态合同回归通过 | 增加跨模块计划依赖环检测 fixture |
| 38 | xlsx | 读取、修改、重算并验证 Excel/CSV 工作簿 | 29 | 19 | 20 | 19 | 9 | 96 | 0/0/0 | 通过 | XLSX validator 检查 ZIP/XML 必备结构；recalc 使用隔离 profile 且超时失败；P0 行为测试通过 | 增加 LibreOffice 实际公式重算与宏保持集成 fixture |

## I-01–I-15 关闭核验

| Finding | 状态 | 独立核验依据 |
|---|---|---|
| I-01 algorithmic-art 中立性/自包含声明 | closed | `templates/viewer.html` 无 Anthropic/Google Fonts；模板与主文件明确 CDN starter 和离线内联义务 |
| I-02 brainstorming 可移植性 | closed | `visual-companion.md` 定义 `<skill-dir>`，启动、停止、frame/helper 路径全部使用该占位 |
| I-03 document-templates 项目特化 | closed | catalog、repository structure、technical design 已改为通用规则；`.factory` 仅为条件 Shanforge profile |
| I-04 document-templates 质量命令路径 | closed | 三份 05-quality 模板均定义并使用 `<skill-dir>/scripts/validate_test_documents.py` |
| I-05 docx 错误成功 | closed | `accept_changes.py` 超时/非零/非法 ZIP/残留修订均返回 Error；`test_docx_accept_changes_fails_on_timeout_and_unaccepted_output` 覆盖 |
| I-06 项目状态信封 owner 漂移 | closed | 九个相关工作 Skill 不再生成项目级 next/completion envelope；仅 `using-shanforge` 为 owner，合同回归通过 |
| I-07 receiving-code-review 写权限矛盾 | closed | triage 与整改 TaskCard 的 write policy、授权和验证责任已明确分支 |
| I-08 review 无条件人工 Gate | closed | 主文件和 `independent-review-task-template.md` 均规定 approved 默认 `return_to_orchestrator` |
| I-09 pdf 表单资源路径 | closed | `forms.md` 定义 `<skill-dir>`，全部脚本命令含正确 `.py` 路径 |
| I-10 pdf 失败码/输出目录 | closed | bbox FAILURE 非零；converter 先创建目录；对应行为测试通过 |
| I-11 shadcn 断链 | closed | `SKILL.md#updating-components` 存在，`cli.md`/`customization.md` 路由可达 |
| I-12 using-shanforge 工具映射 | closed | `codex-tools.md` 列出当前 spawn/send/followup/wait/list/interrupt 工具，无 `close_agent` 或全局配置修改 |
| I-13 webapp-testing 进程清理 | closed | server 继承标准流、检测早退、POSIX 进程组 TERM/KILL 清理；高输出/进程树测试通过 |
| I-14 xlsx validator | closed | `office/validate.py` 对真实 XLSX 解包并验证必备 ZIP/XML 结构，拒绝破损包 |
| I-15 xlsx profile/超时 | closed | `recalc.py` 使用 `TemporaryDirectory` 隔离 LibreOffice profile，timeout 返回 error；行为测试通过 |

## Findings

### Critical

- none

### Important

- none

### Minor

- none；低于满分的非阻塞增强项已逐行写入“剩余优化方向”。

## Verification

- 动态 inventory：`38/38` 个 `skills/*/SKILL.md` 已逐项复评，名称唯一、无遗漏。
- `.venv/bin/python -m pytest -q -p no:cacheprovider`：首次复评运行发现 session-card/ledger 的当前投影时序漂移；总控按 owner 同步后新鲜重跑 exit `0`，`262 passed, 4 subtests passed in 2.23s`。
- `.venv/bin/ruff check .`：exit `0`，`All checks passed!`。
- 对动态发现且包含 `SKILL.md` 的目录逐个运行 `/Users/uroborus/.codex/skills/.system/skill-creator/scripts/quick_validate.py`：exit `0`，`38/38` valid。
- `git diff --check`：exit `0`，无输出。
- 文件化证据中的 P0 脚本失败合同 `6 passed`、受影响 Skill 回归 `70 passed`、旧契约迁移复测 `65 passed` 与当前实现相符；本 reviewer 已核对对应脚本和测试，而非复用其分数。

## Gate

`return_to_orchestrator`

38/38 Skill 均达到 `>=90 / C0-I0`，I-01–I-15 全部关闭，当前不存在真实人工 Gate。本 review 不修改 Skill、测试、ledger、memory 或 Git，也不把 WorkItem 标记为 done。
