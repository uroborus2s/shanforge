# 需求分析条件化与任务分层实施计划

> **给执行者：** 计划评审通过后，把状态交还 `using-shanforge` 流程总控判断下一步。

**目标：** 固化条件化需求分析和四类任务层级，并让任务层级进入现有项目知识投影。

**架构：** 正式事实仍由需求包、任务简报和关系声明持有。Markdown 提取器只把已声明的任务层级写入现有 `pk_entity.detail_json`，SQLite 不增加表、列或关系类型。

**技术栈：** Markdown Skill/模板、Python 标准库、pytest、ruff、skill quick validation

**工作项：** `REQUIREMENT-TASK-TRACEABILITY-001`

**状态：** `ready_for_review`

## 输入

- 用户已批准任务分层和需求分析条件化方案。
- 工作项简报：`.factory/workitems/REQUIREMENT-TASK-TRACEABILITY-001/brief.md`
- 项目会话卡：`.factory/memory/agent-session.md`
- 当前实现：`src/runtime/project_knowledge/extractors.py`

## 范围

### 目标

- 需求分析内容必做，输出模式按复杂度选择。
- 任务简报声明四类任务层级和对应关联规则。
- 提取器接受合法层级并拒绝非法层级。

### 非目标

- 不新增数据库 schema、关系类型或迁移。
- 不回填历史任务。
- 不修改 PM 页面和其他脏文件。

## 文件

| 类型 | 路径 | 职责 |
|---|---|---|
| 修改 | `skills/requirements-engineering/SKILL.md` | 定义分析模式和选择门槛 |
| 修改 | `skills/requirements-engineering/references/prd-template.md` | 提供嵌入式分析结构 |
| 修改 | `skills/document-templates/SKILL.md` | 文档创建时执行条件化选择 |
| 修改 | `skills/document-templates/references/repository-structure.md` | 标明独立分析文件为条件项 |
| 修改 | `skills/document-templates/references/document-catalog.md` | 修正文档默认性 |
| 修改 | `skills/document-templates/references/traceability-and-gates.md` | 修正需求到设计 Gate |
| 修改 | `skills/document-templates/assets/templates/02-requirements/requirements-analysis.md` | 声明 standalone 元数据 |
| 修改 | `skills/writing-plans/SKILL.md` | 定义任务层级与关联 Gate |
| 修改 | `skills/writing-plans/references/task-brief-template.md` | 增加任务层级和关联目标字段 |
| 修改 | `src/runtime/project_knowledge/extractors.py` | 提取并校验 task_scope |
| 新建 | `tests/test_requirements_analysis_mode_contract.py` | 锁定条件化需求分析合同 |
| 新建 | `tests/test_task_scope_contract.py` | 锁定四类任务层级和关联规则 |
| 修改 | `tests/test_project_knowledge_extractors.py` | 锁定合法和非法 task_scope |

## 边界

- 层级：Skill/模板定义正式输入；runtime 仅做无副作用提取；settings 投影保持不变。
- 领域：需求工程、计划编排、项目知识提取。
- 接口归属方：任务简报字段由 `writing-plans` 定义，提取器消费。
- 下游依赖：现有 `pk_entity.detail_json` 和关系图。
- 禁止耦合：不得让 SQLite 成为需求或任务正式事实源。

## 任务

### 任务 1：需求分析条件化

**任务切片：**

- 设计方案：分析内容必做，载体二选一。
- 接口设计：`analysis_mode` 和 `analysis_locator`。
- UI 或 `N/A`：`N/A`，本任务只修改 Skill 与正式文档模板。
- 测试设计：独立合同测试校验模式、选择条件和 Gate。
- 开发：修改需求工程与文档模板相关文件。
- 单测：运行跨 Skill 合同测试。
- review：独立检查是否仍存在无条件文件 Gate。
- 集成测试：运行需求工程与文档体系相邻测试。
- 失败断言：缺测试设计则失败；UI 已写明不适用原因；发现占位语则失败。

- [x] 红灯：在 `tests/test_requirements_analysis_mode_contract.py` 新增合同测试并确认当前文档仍把独立分析文件列为无条件必备。
- [x] 绿灯：写入模式、定位和复杂度选择规则。
- [x] 验证：运行目标测试、需求工程测试和相关文档模板测试；记录 evidence、report 和 ledger。
- [x] 评审门：实现者只推进到 `ready_for_review`。

### 任务 2：任务层级与提取

**任务切片：**

- 设计方案：独立 `task_scope`，关系继续复用现有图。
- 接口设计：`project | requirement | cross_cutting | system`。
- UI 或 `N/A`：`N/A`，本任务不改 PM 展示。
- 测试设计：合法值进入 details，非法值抛出明确错误；合同测试覆盖四类任务各自的强关联或零产品进度规则。
- 开发：修改任务模板、计划 Skill 和 Markdown 提取器。
- 单测：运行提取器测试。
- review：检查未复用 `task_kind`、未新增平行关系表。
- 集成测试：运行计划 Skill 和项目知识相邻测试。
- 失败断言：缺测试设计则失败；UI 已写明不适用原因；发现占位语则失败。

- [x] 红灯：在 `tests/test_task_scope_contract.py` 写四类关联规则测试，在 `tests/test_project_knowledge_extractors.py` 写提取器失败测试。
- [x] 绿灯：写入最小模板规则及提取校验。
- [x] 验证：运行目标及相邻测试，31 项通过；记录 evidence、report 和 ledger。
- [x] 评审门：实现者只推进到 `ready_for_review`。

## 测试策略

- 红灯：新合同测试和提取器测试必须因缺失行为失败。
- 绿灯：重跑同一测试。
- 定向回归：两个新增合同测试、`test_requirements_engineering_skill.py`、`test_writing_plans_skill.py`、`test_project_knowledge_extractors.py`。
- 邻近回归：`test_sf_sp_010_documentation_navigation.py` 和系统任务零产品进度契约测试。
- 全量回归：仅在定向或邻近测试显示影响扩大时执行。
- 未运行项：浏览器/E2E。
- 未运行原因：无 UI 和运行时交互变更。

## 文档同步

- 正式文档：本次修改的是可复用 Skill/模板，不改产品 PRD。
- `.factory/memory/`：终态同轮提交，不写共享脏 memory。
- 工作项流水账：`.factory/workitems/REQUIREMENT-TASK-TRACEABILITY-001/ledger.jsonl`

## 评审门

- 计划评审：`pending`
- 任务评审：`approved`
- 验证：`passed`
- 本地提交：`184a701`
- 记忆同步：`not_required_same_turn_terminal_workitem`

## 计划自审

- 规格覆盖：覆盖 `REQ-RTT-001`、`REQ-RTT-002`。
- 占位符扫描：无占位符。
- 发现占位语则失败：已检查。
- 缺测试设计则失败：两项任务均有测试设计。
- UI 写 `N/A` 但无原因则失败：均已写明原因。
- 类型一致性：枚举值统一使用小写 snake_case。
- 可构建性：文件路径、命令和期望失败已明确。
- Shanforge 门禁：计划与两项任务均已独立评审，关闭前验证已通过。
