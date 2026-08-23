# 全量逐 Skill 优化评分实施计划

> **给执行者：** 按 T01 → T02 → T03 → T04 → T05 → T06 顺序执行；合格 Skill 记录 `no_change_required`，不得为制造 diff 改写。

**目标：** 对动态发现的 38 个 Skill 完成逐项审计、必要优化、验证和独立 100 分制评分。

**架构：** 以 `skills/*/SKILL.md` 与其实际引用资源为事实源，不建立数量注册表。自动检查只证明命名、引用和可执行不变量；语义质量由逐项审计和独立 reviewer scorecard 判断。

**技术栈：** Markdown、Python 标准库、pytest、Ruff、系统 `quick_validate.py`、Git。

**工作项：** `SKILL-FULL-OPTIMIZATION-001`

**状态：** `ready_for_commit`

## 输入

- 已批准输入：`.factory/workitems/SKILL-FULL-OPTIMIZATION-001/brief.md`
- 当前任务：`.factory/workitems/SKILL-FULL-OPTIMIZATION-001/task-briefs/`
- 评分基准：`skills/requesting-code-review/references/review-score-rubric.md`
- Skill 设计基准：系统 `skill-creator/SKILL.md`

## 范围

### 目标

- 动态清点 38/38 Skill，逐项形成基线结论和优化状态。
- 只修正有证据的触发、职责、流程、错误语义、引用、脚本或验证缺口。
- 为 38/38 Skill 输出独立 reviewer 单项分数与 C/I/M。

### 非目标

- 不要求 38 个 Skill 都产生 diff。
- 不新增中心注册表、平台运行时、依赖或整文件快照。
- 不执行远端或发布动作。

## 文件

| 类型 | 路径 | 职责 |
|---|---|---|
| 新建 | `.factory/workitems/SKILL-FULL-OPTIMIZATION-001/reports/baseline-audit.md` | 38 项初始审计与问题分组 |
| 新建 | `.factory/workitems/SKILL-FULL-OPTIMIZATION-001/reports/optimization-results.md` | 逐项修改/不修改理由和验证结果 |
| 新建 | `.factory/workitems/SKILL-FULL-OPTIMIZATION-001/evidence/verification.md` | 自动验证和完整回归证据 |
| 新建 | `.factory/workitems/SKILL-FULL-OPTIMIZATION-001/reviews/independent-scorecards.md` | 独立 reviewer 的 38 张单项 scorecard |
| 条件修改 | `skills/*/SKILL.md` 及其已存在资源 | 仅修复审计确认的问题 |
| 条件测试 | `tests/test_skill_*.py` 与相关现有测试 | 只补有行为价值的动态不变量 |
| 记忆 | `.factory/memory/{agent-session.md,current-state.md,tasks.summary.md,tests.summary.md,skill-updates.summary.md,review-ledger.jsonl}` | 批次阶段与最终评分摘要 |

## 边界

- 层级：`system`
- 领域：Skill 治理与质量
- 接口归属方：每个 Skill 的 frontmatter、专业工作流和本地资源仍由该 Skill 自己拥有。
- 下游依赖：Codex 动态发现、Shanforge 流程路由、现有测试。
- 禁止耦合：不得创建中心 Skill 内容注册表或把所有专业输出统一成同一模板。

## 任务

### T01：审计基线与评分输入

- 目标和验收结果：读取 38 个 `SKILL.md` 及被其路由的必要资源，生成 38 行基线审计；每项包含触发/边界、工作流、错误语义、资源、验证和初始 finding。
- 依赖：brief 已批准。
- 实现：只写 WorkItem 报告；不修改 Skill。
- 验证：38 个目录全部出现且唯一，全部 `quick_validate.py` 可执行，报告无遗漏和占位。
- 风险：`medium`

### T02：流程与质量控制组（12 项）

- Skill：`brainstorming`、`executing-plans`、`project-memory`、`receiving-code-review`、`requesting-code-review`、`requirements-engineering`、`subagent-driven-development`、`systematic-debugging`、`tdd-workflow`、`using-shanforge`、`verification-before-completion`、`writing-plans`。
- 目标和验收结果：逐项关闭 T01 findings；无 finding 项记录 `no_change_required`。
- 验证：对应 validator、流程合同测试和受影响定向测试通过。
- 风险：`medium`

### T03：工程与平台组（13 项）

- Skill：`agent-harness-construction`、`ai-first-engineering`、`ai-regression-testing`、`api-design`、`crawler4j-model-project`、`frontend-patterns`、`go-developer`、`java-developer`、`python-uv-project`、`shadcn`、`stratix-admin-web`、`stratix-service`、`webapp-testing`。
- 目标和验收结果：逐项关闭 T01 findings，保留技术栈特有边界，不把通用工程建议复制到每项。
- 验证：对应 validator、资源引用和受影响定向测试通过。
- 风险：`medium`

### T04：内容、资产与工具组（13 项）

- Skill：`algorithmic-art`、`art-asset-pipeline`、`article-writing`、`browser-control`、`doc-coauthoring`、`document-templates`、`docx`、`gitcommitzh`、`humanizer`、`pdf`、`release-deployment`、`ui-ux-pro-max`、`xlsx`。
- 目标和验收结果：逐项关闭 T01 findings，保留文件格式、浏览器、资产与发布授权边界。
- 验证：对应 validator、脚本/引用可达性和受影响定向测试通过。
- 风险：`medium`

### T05：批次验证与作者结果表

- 目标和验收结果：生成 38 项 optimization result；运行全部 validator、完整 pytest、Ruff、JSON/JSONL、脚本语法和 Git hygiene。
- 首个候选：完整必需测试；失败进入同范围定向根因修复。
- 最终候选：再次运行完整必需测试，写入唯一 verification evidence。
- 风险：`medium`

### T06：独立逐项评分与整改闭环

- 目标和验收结果：独立 reviewer 只读评分 38/38 Skill；每项列五维分、总分、C/I/M、结论和证据。
- 通过线：每项 `>=90 / C0-I0`；否则由实现者核实 feedback、最小整改、受影响复测并交同 reviewer 复评。
- 集中 Gate：全部 38 项通过后才能进入提交和 memory 关闭。
- 风险：`medium`

## 测试策略

- 基线：38 个 `quick_validate.py`；现有完整 pytest。
- 定向：只运行受修改 Skill 对应测试和动态引用/合同守卫。
- 批次：`uv run pytest -q -p no:cacheprovider`、`uv run ruff check .`。
- 资源：解析所有本地 Markdown 链接与 Skill 路由资源，检查存在性；修改脚本时运行语法和行为测试。
- 独立 forward test：仅对审计判定为复杂/高风险或 reviewer 要求的 Skill 使用隔离临时目录。

## 文档同步

- 正式文档：只有审计发现正式 Skill 能力事实漂移时才修改并回源 owner。
- memory：T01 基线、批次 ready_for_review、独立终审和关闭时同步最小摘要。
- 工作项：所有逐项结果、验证和 scorecard 保存在本 WorkItem。

## 集中质量门

- 计划独立评审：`N/A`（中风险，作者自审；用户要求的是最终逐 Skill 独立评分）。
- 批次代码评审：`approved`（同 reviewer 复评 38/38，`95.0 / C0-I0-M0`）
- 批次验证：`passed`（最终候选 `262 passed / 4 subtests passed`，Ruff 与 38/38 validator 通过）
- 本地提交：`pending`
- 记忆同步：`passed`

## 计划自审

- 规格覆盖：38 项被三个互斥分组完整覆盖，T05/T06 覆盖验证和独立评分。
- 占位符扫描：无未定义交付物或“后续补充”步骤。
- 类型一致性：Skill 名称来自当前文件系统，分组总数 `12 + 13 + 13 = 38`。
- 可构建性：所有产物路径、验证命令和通过线明确。
- 批次质量门：单套 evidence、单套独立 scorecard、同 reviewer 整改复评。
