# 项目设计与测试资产标准化实施计划

> **给执行者：** 计划评审通过后，把状态交还 `using-shanforge` 流程总控判断下一步。步骤使用复选框语法 (`- [ ]`) 便于追踪。

**目标：** 交付可校验、可索引、可追踪、可组合展示的 Penpot、OpenAPI 与测试资产主链。

**架构：** `access` 只解析固定命令，`application` 编排资产校验用例，
`domain` 定义纯合同与失败语义，`settings` 从仓库读取 YAML/JSON 并在 composition 装配。
项目知识提取器把已校验机器资产投影为稳定实体和关系，HTML 渲染器只消费 SQLite
投影，不把缓存当作事实源。

**技术栈：** Python 3.14、PyYAML、SQLite3、OpenAPI 3.1、静态 HTML、pytest、Ruff、Mypy。

**工作项：** `PROJECT-ARTIFACTS-001`

**状态：** `implemented_and_independently_approved`

---

## 输入

- 已批准的规格 / 需求 / 设计：本会话已确认的 Penpot、统一文档、OpenAPI、测试案例/结果/报告方案。
- 当前工作项简报：`.factory/workitems/PROJECT-ARTIFACTS-001/brief.md`
- 相关 `.factory/memory/` 摘要：`.factory/memory/agent-session.md`、`.factory/memory/doc-map.md`
- 已读取的正式文档：`docs/05-design/ux-ui-design.md`、`docs/05-design/api-design.md`、
  `docs/06-delivery/test-plan.md`

## 范围

### 目标

- 固化三类机器资产合同和固定 CLI 校验。
- 把 YAML 资产确定性投影到现有 SQLite 实体、locator、关系和测试表。
- 合并设计/文档入口，并在文档详情组合展示关联机器附件。
- 保持静态 HTML 增量构建、缓存命中和只读安全边界。

### 非目标

- 不创建伪 `.penpot` 文件，不连接用户 Penpot 账户，不生成线上服务。
- 不修改项目业务 API 实现，只描述当前四个 HTTP route 的正式合同。
- 不创建一测试一文件；同一能力的测试案例保存在一个目录级 catalog。
- 不提交运行结果、SQLite、HTML 或本机 MCP 配置。

## 文件

| 类型 | 路径 | 职责 |
|---|---|---|
| 新建 | `src/domain/project_artifacts/{__init__,models,validation}.py` | 资产合同、问题模型和纯校验规则 |
| 新建 | `src/application/project_artifacts/{__init__,service}.py` | 校验用例与仓库读取端口 |
| 新建 | `src/settings/project_artifacts/{__init__,local_repository,source_registry}.py` | YAML/JSON 读取和组合 source registry |
| 新建 | `src/runtime/project_artifacts/{__init__,yaml_extractor,site_renderer}.py` | YAML 实体投影和单入口 HTML 包装 |
| 修改 | `src/access/project_cli.py` | 增加三条固定校验命令 |
| 修改 | `src/application/project_knowledge/query_service.py` | 接入校验回调 |
| 修改 | `src/settings/composition/project_knowledge.py` | 唯一组合入口 |
| 修改 | `src/settings/project_knowledge/sqlite_index.py` | 测试案例投影到 `pk_test` |
| 新建 | `.factory/project-knowledge/artifact-source-registry.json` | 独立登记稳定机器资产源 |
| 修改 | `pyproject.toml`、`uv.lock` | PyYAML 运行时依赖 |
| 新建 | `design/ux-ui/design-manifest.yaml`、`design/ux-ui/tokens.json` | Penpot 设计状态与实现 Token |
| 新建 | `contracts/openapi/openapi.yaml` | OpenAPI 3.1 正式机器合同 |
| 新建 | `contracts/schemas/{design-artifact-manifest,openapi-shanforge-rules,test-case-catalog,test-run-result,test-report}.schema.json` | 机器合同规范 |
| 新建 | `tests/specifications/project-artifacts.testcases.yaml` | 本工作项稳定测试案例 |
| 修改 | `docs/05-design/ux-ui-design.md`、`docs/05-design/api-design.md` | 增补机器附件与阅读规则 |
| 修改 | `docs/04-product/prd.md` | 仅为 OpenAPI 已引用的既有需求补稳定 section ID，不改需求正文 |
| 修改 | `docs/06-delivery/test-plan.md` | 增补案例、结果和报告标准 |
| 新建 | `tests/test_project_artifact_contracts.py` | 合同与 CLI 单元/集成测试 |
| 新建 | `tests/test_project_artifact_extractor.py` | YAML 提取与追踪测试 |
| 新建 | `tests/test_project_artifact_index.py` | SQLite 原子测试投影 |
| 新建 | `tests/test_project_artifact_site_renderer.py` | 单入口和附件组合展示回归 |
| 记忆 | `.factory/memory/agent-session.md`、相关 summary | 只同步压缩事实和恢复点 |

## 边界

- 层级：`access -> application -> domain -> runtime -> settings`。
- 领域：项目资产合同与项目知识投影。
- 接口归属方：资产源 port 由 `application` 定义，`settings` 实现。
- 下游依赖：SQLite 索引、只读 HTML、前端/测试/集成方。
- 禁止耦合：domain 不读文件；renderer 不直接解析仓库 YAML；settings 不重定义业务规则。

## R2 基线隔离与提交策略

- 旧工作项 `PK-SOURCE-MIGRATION-001-T04` 仍停在人工确认门，本工作项不改变其状态，
  不提交其已有改动。
- 本任务开始前已有脏文件按 `git diff -- <path>` 记录前像；本任务只添加可单独解释的
  新 hunk。最终使用 `git diff --cached --check`、`git diff --cached --name-status`
  和逐文件 `git diff --cached` 审计暂存区。
- 对含旧 hunk 的文件只暂存本任务新增 hunk；若某个新 hunk无法脱离旧 hunk应用到
  `HEAD`，该 hunk不进入本次提交，并把相应验收标为 blocked，不借机发布旧候选。
- `pyproject.toml` / `uv.lock` 已有 `types-pyyaml` 候选改动。本任务只拥有运行时
  `PyYAML>=6.0.2` 及对应锁记录；暂存审计必须把两者区分。
- 可独立新增的模块优先落到 `project_artifacts` 命名空间，减少对旧工作项文件的重叠。
- T02 真实索引重建发现 `REQ-001/002/003/005/006/007/009` 只有人类标题、没有稳定
  section marker，导致强关系因 endpoint 不存在而原子失败。允许只在这些既有标题前
  增加同名 `sf:section-id`；禁止改需求正文、状态、版本或验收内容。
- 暂存完成后执行运行级隔离验证：用 `git worktree add --detach <临时目录> HEAD` 创建
  干净工作树；用 `git diff --cached --binary --output=<临时补丁>` 导出本任务候选；
  在临时工作树 `git apply` 后运行本计划全部定向测试、Ruff、Mypy、合同 CLI 和两次快照。
  该隔离验证不读取当前脏工作树；任一失败都阻塞提交。临时目录和补丁不进入仓库。

## R2 锁定机器合同

### `DesignArtifactManifest/v1`

- 根字段：`schema_id`、`id`、`title`、`status`、`document_id`、`source`、
  `pages`、`components`、`tokens_file`、`exports`。
- 状态：`awaiting_penpot_connection | draft | ready | deprecated`。
- `source.format=penpot`；`ready/deprecated` 必须有仓内 `design/ux-ui/*.penpot`，
  等待连接必须 `file=null` 且 `connection_required=true`。
- 所有路径是仓库相对 POSIX 路径，禁止绝对路径、`..` 和 symlink；真实文件以索引
  已有 content SHA-256 管理，manifest 不复制 hash。
- `source` 固定为
  `{format:"penpot", file:string|null, connection_required:boolean}`。
- `pages[]` 必填 `id/title/purpose`，ID 匹配 `UI-PAGE-[A-Z0-9-]+`；
  `components[]` 必填 `id/title/purpose/states`，ID 匹配
  `UI-COMPONENT-[A-Z0-9-]+`，states 非空且只允许
  `default/loading/empty/error/disabled/focus/hover/pressed/success/blocked`。
- `exports[]` 固定为 `id/kind/subject_id/file/format/purpose`；
  subject 必须引用同 manifest 的 page/component；file 位于
  `design/ux-ui/exports/` 且真实存在，format 只允许 `svg/png/webp/pdf`。
- 实体映射：根 `design_asset`；pages 为 `ui_page`；components 为 `ui_component`；
  locator 使用 YAML path；`doc:DESIGN-UX-UI-001 CONTAINS design_asset`，
  根资产 `CONTAINS` 页面与组件。

### OpenAPI 3.1

- 每个 operation 必须有 `operationId`、中文 `summary`、不少于 20 字且含中文的
  `description`、`x-shanforge-id`、`x-shanforge-requirements`、
  `x-shanforge-tests`、`x-shanforge-owner`。
- 参数、requestBody、response、schema 和 property 必须有中文 description；
  参数及每个媒体类型必须有 example(s)；每个操作至少一个 2xx/3xx 和一个 4xx/5xx。
- 与 `build_runtime_routes()` 比较 `(METHOD,path)` 集合，缺失和额外路由均失败。
- 实体映射：operation 为 `api_operation`，ID 取 `x-shanforge-id`，locator 为 YAML path；
  `doc:DESIGN-API-001 CONTAINS operation`，operation `SATISFIES` requirement。

### 测试合同

- `TestCaseCatalog/v1` 根字段：`id/title/version/status/cases`。案例字段：
  `id/version/title/definition_status/objective/type/level/priority/risk/owner/traceability/
  preconditions/test_data/steps/postconditions/environment/automation/tags`。
- 定义状态：`draft | active | deprecated | retired`。每步必须有 `action/expected`；
  requirement 追踪至少一个，并且 acceptance/design/UI/API/task 至少一种。
- `type` 是
  `unit|contract|integration|system|acceptance|usability|accessibility|security|performance|regression`；
  `level` 是 `unit|component|integration|system|acceptance`；
  `priority` 是 `P0|P1|P2|P3`；`risk` 是 `low|medium|high|critical`。
- `preconditions`、`postconditions`、`tags` 是字符串数组；
  `test_data[]` 固定 `{name,value,sensitive:boolean}`，value 可为 JSON 标量或对象；
  `environment` 是稳定环境 ID 字符串；`automation` 固定
  `{status,entrypoint}`，status 为 `manual|planned|automated|partial`，
  automated/partial 必须有 entrypoint，manual/planned 可为 null。
- `traceability` 是六个字符串数组：
  `requirements/acceptance_criteria/designs/ui_pages/api_operations/tasks`；引用分别使用
  `REQ-*|NFR-*`、`*-AC-*`、`DESIGN-*`、`UI-PAGE-*`、`API-*`、稳定 task/work item ID。
- `TestRunResult/v1` 只进入 `.factory/workitems/<ID>/evidence/test-results/*.json`，
  状态固定为 `passed | failed | error | blocked | skipped | not_run | cancelled`。
- result 必填：
  `id/run_id/test_case_id/test_case_version/status/started_at/finished_at/environment/
  step_results/evidence`。`environment={id,git_commit,runtime}`；
  `step_results[]={step,status,actual,evidence_refs}`，step 从 1 连续递增且 status 使用七态；
  `evidence[]={id,kind,path,sha256}`，path 必须在当前 work item evidence 下，
  sha256 为 64 位小写十六进制。
- `TestReport/v1` 只进入 `.factory/workitems/<ID>/evidence/test-reports/*.json`，
  `summary` 必须与引用 result 的七态逐项聚合一致；HTML 只消费当前 work item 明确传入
  的合格 evidence，不把历史运行结果登记成稳定 source。
- report 必填 `id/run_id/title/generated_at/result_refs/summary`；
  `result_refs[]={result_id,test_case_id,status,evidence_path,sha256}`，result_id 唯一；
  `summary={total,passed,failed,error,blocked,skipped,not_run,cancelled}`。
  一致性算法按唯一 result_ref 计数：total 等于引用数，七态各字段等于对应 status 计数，
  引用的 status、path、sha256 必须与已校验 result 精确一致，否则失败。
- JSON Schema 固定在 `contracts/schemas/`；稳定 catalog 位于
  `tests/specifications/*.testcases.yaml`。CLI 为 `test-cases validate`；
  单次 result/report 由 domain 公共 validator 和自动测试验证，首版不增加接受任意路径
  的 CLI，避免扩大读取范围。
- 实体映射：case 为 `test`，YAML locator；case 对 requirement、AC、design、UI、
  API、task 均使用 `VERIFIES`。`pk_test.framework=catalog`、
  `test_kind=case.type`、`test_status=definition:<definition_status>`；
  UI 把它显示为“测试定义已登记 / 尚未执行”，绝不映射为运行通过。
- JSON Schema 和 domain validator 共享 `tests/test_project_artifact_contracts.py`
  中的同一组正负样本；测试还必须逐项断言 schema 的 required/enum 与上述字段一致，
  防止两份规则漂移。

## R3 SQLite 原子扩展点

- `src/runtime/project_artifacts/yaml_extractor.py` 把 catalog test 元数据写入
  `SourceContribution/v1.tests`，每项固定：
  `{test_id,entity_id,framework:"catalog",test_kind,test_status:"definition:<status>",
  code_symbol_id:null,last_evidence_entity_id:null}`。
- 现有 `SQLiteProjectKnowledgeIndex._replace_current_projection()` 在发布 generation 的
  同一 SQLite transaction 内，除现有 pytest test_rows 外，再收集所有 contribution.tests，
  与 Python 测试合并后一次 `executemany` 写入 `pk_test`。
- 不使用“publish 后二次写入”的 wrapper，不新增独立 transaction。最小 hunk 位于当前
  `test_rows` 组装处，并由临时干净 worktree 的原子失败测试验证：非法 catalog test 使
  整个 publish rollback，旧 current generation 和旧 `pk_test` 保持不变。

## R2 固定 Python 接口

- `domain.project_artifacts.models.ArtifactValidationIssue` 与
  `ArtifactValidationReport.to_dict()`。
- `domain.project_artifacts.validation` 暴露以下纯函数，domain 不读取文件：
  - `validate_design_manifest(payload, *, available_paths: Set[str])`；application 从
    repository 的 `available_design_paths()` 取得已经做过 root、symlink 和 regular-file
    检查的相对路径集合。
  - `validate_openapi(payload, *, expected_routes: Set[tuple[str,str]])`；application 从
    composition 注入的 `build_runtime_routes()` 取得 upper-case method/path 集合。
  - `validate_test_case_catalog(payload)`。
  - `validate_test_run_result(payload, *, evidence_root: str)`；evidence_root 由 application
    根据当前 work item scope 注入，domain 只做 POSIX containment 与字段校验。
  - `validate_test_report(payload, *, validated_results_by_id: Mapping[str, ValidatedTestResult])`；
    application 先逐份调用 result validator，再只把已通过 result 的
    `test_case_id/status/evidence_path/sha256` 不可变映射传入，domain 不相信 report 自报值。
- `application.project_artifacts.service.ProjectArtifactRepositoryPort` 由 application 拥有；
  `ProjectArtifactValidationService` 暴露 `validate_design/api/test_cases/all`。
- `settings.project_artifacts.local_repository.LocalProjectArtifactRepository` 只实现严格
  YAML/JSON 读取和仓内路径检查。
- CLI 回执继续使用 `ProjectCommandReceipt/v1`；合法合同 exit code 0，
  格式不合格返回成功执行但 `data.valid=false`，解析/路径错误返回 exit code 2。

## R2 HTML 附件口径

- 首版只在同一文档详情展示机器附件的中文标题、状态、用途、稳定 ID、字段摘要和追踪，
  不复制/嵌入 PNG、SVG 或 `.penpot` 二进制文件。
- 只有 manifest 已登记且文件真实存在时才显示仓库相对文件名；不存在时显示
  “等待在 Penpot 打开文件并连接插件”，不显示假链接。
- 二进制资源发布需要独立的 hash、MIME、路径和增量复制设计，不属于本工作项首版。

## 任务

### 任务 1：UX/UI 与 Penpot 资产合同

**任务切片：**

- 设计方案：单一 UX/UI 文档绑定一个机器 manifest、Token 和导出资源集合。
- 接口设计：`DesignArtifactManifest/v1`；真实 `.penpot` 可缺省但状态必须说明原因。
- UI：展示文档正文、设计源状态、页面/组件/导出资产和 Token 摘要。
- 测试设计：拒绝伪源路径、越界资源、缺稳定 ID、声称 ready 但无 `.penpot` 的 manifest。
- 开发：上述固定接口、CLI `design validate`、正式 manifest 与 Token；先执行
  `uv lock`、`uv sync`，只拥有 PyYAML 运行时依赖 hunk。
- 单测：合同正负例和 CLI 回执。
- review：独立检查无伪 `.penpot` 与路径边界。
- 集成测试：repository 读取真实 manifest/Token，CLI 输出合法结构化回执。
- 失败断言：缺测试设计则失败；发现占位语则失败。

- [x] 红灯：编写设计 manifest 正负例与 CLI 测试。
- [x] 绿灯：实现最小合同、读取器、命令与正式资产。
- [x] 集成：从仓库文件完成严格读取和固定命令校验。
- [x] 证据：写 `evidence/task-1.md`、`reports/task-1.md` 和 ledger。
- [x] 评审：独立复审 `approved / 97`。

### 任务 2：OpenAPI 详细合同

**任务切片：**

- 设计方案：人类 API 设计文档解释决策，OpenAPI 描述可执行 HTTP 合同。
- 接口设计：OpenAPI 3.1；每个 operation 必须有稳定中文摘要/描述、operationId、
  参数/请求/响应/字段描述、错误响应、示例及 `x-shanforge-*` 追踪。
- UI：同一 API 设计文档详情中展示操作卡、请求响应和追踪。
- 测试设计：缺中文、描述、错误响应、示例、需求或测试追踪均失败。
- 开发：CLI `api validate`、四个当前 route 的正式 OpenAPI。
- 单测：逐条规则正负例。
- review：API route 与代码 route 集合一致。
- 集成测试：设计资产与 API operation 进入 source contribution，具备稳定实体、
  YAML locator 与设计/需求关系；HTML 展示留给 T04。
- 依赖：T01 先交付共享 validation report、repository port 和 CLI 扩展点。

- [x] 红灯：编写 OpenAPI 规则和 route 对齐失败测试。
- [x] 绿灯：实现 validator 和 OpenAPI 文件。
- [x] 集成：提取操作与追踪关系，不承担 HTML 展示。
- [x] 证据：写 `evidence/task-2.md`、`reports/task-2.md` 和 ledger。
- [x] 评审：独立复审 `approved / 99`。

### 任务 3：测试案例、结果与报告合同

**任务切片：**

- 设计方案：稳定 TestCaseCatalog 与单次 TestRunResult、聚合 TestReport 分离。
- 接口设计：案例包含目标、类型、层级、优先级、风险、追踪、前置、数据、步骤、
  后置、环境和自动化；结果使用七态枚举；报告只聚合有来源的运行结果。
- UI：质量页展示测试定义及其需求/设计/API 追踪，运行结果缺失时明确为“尚未执行”。
- 测试设计：拒绝无步骤、无预期、无追踪、非法状态及把定义状态冒充运行结果。
- 开发：CLI `test-cases validate`、稳定测试 catalog、SQLite `pk_test` 投影。
- 单测：合同、提取器、数据库和 HTML 正负例。
- review：定义、结果、报告职责不混淆。
- 集成测试：测试案例在同一索引事务进入 `pk_test` 并生成 VERIFIES 边；
  质量页和双向 HTML 访问留给 T04。
- 依赖：T02 先冻结 API operation ID，测试追踪才能引用稳定 API ID。

- [x] 红灯：编写三类合同及 SQLite 投影失败测试。
- [x] 绿灯：实现 validator、catalog 和投影。
- [x] 集成：验证 SQLite 实体、测试表和关系原子投影。
- [x] 证据：写 `evidence/task-3.md`、`reports/task-3.md` 和 ledger。
- [x] 评审：独立复审 `approved / 98`。

### 任务 4：单一项目文档入口与增量快照

**任务切片：**

- 设计方案：导航只有“项目文档”；设计是文档分类，不再是第二事实入口。
- 接口设计：renderer 仅消费 SQLite model；机器附件通过实体关系绑定到文档。
- UI：文档列表按分类分组，详情含返回按钮、Markdown 正文、章节导航和关联附件。
- 测试设计：无重复导航、正文可见、附件可见、链接安全、缓存命中和最小重绘。
- 开发：删除独立设计入口、扩展文档组合渲染并升级 renderer 版本。
- 单测：renderer 与 publisher 回归。
- review：信息架构、可读性、移动端和只读边界。
- 集成测试：统一承担 design manifest、API operation、测试案例/关系在文档详情、
  质量页和关联页面的全部 HTML 验收；完整 snapshot 两次，第二次必须 cache hit。
- 依赖：T01-T03 的实体、关系和状态映射先完成。

- [x] 红灯：更新商业只读站点断言并确认失败。
- [x] 绿灯：实现单入口与附件组合展示。
- [x] 集成：完整索引/快照、链接和缓存验证。
- [x] 证据：写 `evidence/task-4.md`、`reports/task-4.md` 和 ledger。
- [x] 评审：独立评审 `approved / 96`。

## 测试策略

- 红灯：每个合同先用最小非法样本证明校验规则会拒绝。
- 绿灯：定向运行新测试与受影响现有测试。
- 定向回归：artifact contracts、extractors、index、site renderer、CLI。
- 邻近回归：project knowledge security/performance/state sync。
- 全量回归：`uv run pytest -q`、Ruff、format、Mypy、`uv lock --check`。
- 未运行项：真实 Penpot 文件编辑与导出。
- 未运行原因：需要用户在 Penpot 中打开具体文件并加载本地插件后，MCP 才有设计画布目标。

## 文档同步

- 正式文档：只增补现有 UX/UI、API、测试计划，不另建重复说明文档。
- `.factory/memory/`：完成后更新 session、API、architecture、tests、traceability 摘要。
- 工作项流水账：`.factory/workitems/PROJECT-ARTIFACTS-001/ledger.jsonl`。

## 评审门

- 计划评审：`R5 approved`
- 任务评审：`pending`
- 验证：`pending`
- 拉取请求 / 提交：`pending`
- 记忆同步：`pending`

## 计划自审

- 规格覆盖：覆盖 Penpot、统一文档、OpenAPI、测试定义/结果/报告和 HTML 增量构建。
- 占位符扫描：正式产物不得含 `TBD`、`TODO`、`unknown` 冒充内容。
- 发现占位语则失败：是。
- 缺测试设计则失败：是。
- UI 写 `N/A` 但无原因则失败：没有任务把 UI 写成 `N/A`。
- 类型一致性：三类 schema ID 和七态结果枚举在代码、文件、测试、文档一致。
- 可构建性：每个任务有路径、命令、红绿验证和证据位置。
- Shanforge 门禁：包含 evidence、独立 review、memory sync、ledger 和本地提交门。
