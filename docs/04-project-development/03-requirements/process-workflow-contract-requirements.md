# 流程契约需求文档

## 版本信息

| 项目 | 内容 |
|---|---|
| 文档编号 | `FLOW-REQ-001` |
| 文档类型 | 需求文档 |
| 当前版本 | `0.1.0` |
| 当前状态 | 草稿 |
| 最近更新 | 2026-07-06 |

## 版本历史

| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `0.1.0` | 根据用户关于四类场景、三层文档、记忆结构、项目管理、领域模块、前后端设计、版本管理和防跳步门禁的讨论形成首版需求 | 2026-07-06 | Codex | 待审核 | 待批准 |
| `0.1.1` | 补充整体黑盒测试、UI 测试、接口测试、测试环境启动、端口管理、启动记忆读取和非活跃任务记忆降级规则 | 2026-07-06 | Codex | 待审核 | 待批准 |
| `0.1.2` | 将启动记忆读取从固定顺序修正为条件读取链，明确够用即停，避免恢复流程重新扩张上下文 | 2026-07-06 | Codex | 待审核 | 待批准 |

## 1. 背景

当前 Shanforge 已有 `using-shanforge`、`project-memory`、`requirements-engineering`、`writing-plans`、`executing-plans`、`requesting-code-review`、`verification-before-completion` 和 `gitcommitzh` 等 workflow skill。已有流程可以支持会话恢复、计划、执行、评审、验证和提交门，但用户反馈整体过程仍不够清晰，尤其是：

- 新项目、增加需求、变更需求、修复 bug 的入口差异没有统一表达。
- 单个需求和单个任务内部应该严格瀑布式推进，但多个需求之间应能并列敏捷推进。
- 项目级技术架构、领域划分、数据库基线、API 基线、整体 UI 设计这类自上而下任务没有清晰归属。
- 正式文档、临时文档、`.factory/memory/` 摘要、PM 看板和归档报告之间边界需要固定。
- AI 执行流程时必须有硬门禁，不能靠提示词自觉，不能跳过需求、设计、测试、评审或验证。

本需求要求把上述讨论固化为一套可执行、可评审、可回归测试的流程契约。

## 2. 目标

1. 建立四类场景入口：新项目、增加需求、变更需求、修复 bug。
2. 建立三层正式文档模型：项目总体设计、需求文档、任务执行卡。
3. 保留 `04-project-development` 内部项目开发文档层，并与 `02-user-guide`、`03-developer-guide` 分层。
4. 建立正式文档、临时文档、记忆摘要、work item ledger、PM 视图之间的事实源规则。
5. 建立项目级 baseline work item，用于领域划分、总体技术架构、数据库基线、API 基线和整体 UI 设计。
6. 建立后端领域模块设计规则，按微服务边界定义模块，即使当前实现是单体多模块应用。
7. 建立前端整体 UI 设计规则，并明确前端接口使用、复用后端接口和新增前端业务接口的处理方式。
8. 为每个 workflow skill 定义输入、输出、内部流程和状态回写契约。
9. 为完整流程建立 gate、evidence、review 和黑盒 eval，防止 AI 跳步、省略细节或自批完成。
10. 建立项目级整体测试和测试环境基线，覆盖接口测试、UI 测试、整体黑盒测试和发布回归。
11. 建立启动记忆读取顺序和非活跃任务记忆降级规则，避免 `current-state.md` 膨胀。

## 3. 非目标

- 本需求不直接实现所有 skill 改造。
- 本需求不迁移现有 `docs/04-project-development/*` 编号目录。
- 本需求不删除既有 Superpowers 流程集成文档。
- 本需求不要求马上把所有历史文档补齐中文版本信息和版本历史。
- 本需求不引入新的中心 CLI、动作注册表或全局流程脚本。
- 本需求不要求每次状态查看都生成归档级项目实施管理文档。

## 4. 业务对象

| 对象 | 定义 | 事实源 |
|---|---|---|
| Project | 项目级目标、边界、治理和 baseline 集合 | `docs/04-project-development/project-baseline.md` 或当前阶段等价设计文档 |
| Baseline Work Item | 项目级整体设计任务，如领域划分、数据库基线、API 基线、整体 UI 设计 | `.factory/workitems/BASE-*`、正式设计文档 |
| Requirement | 一个业务需求、需求变更或 bug 修复需求 | `docs/04-project-development/03-requirements/*.md` |
| Task | 需求或 baseline 拆出的可执行任务 | `.factory/workitems/<ID>/plan.md`、`docs/04-project-development/05-development-process/*.md` |
| Gate | 状态流转门禁，定义进入下一阶段所需证据 | work item ledger、review、verification evidence |
| Evidence | 命令输出、测试报告、评审报告、设计产物、截图、commit 等证据 | `.factory/workitems/<ID>/evidence/`、`reviews/`、`reports/` |
| Memory Summary | 给 AI 恢复上下文的压缩摘要 | `.factory/memory/*.summary.md` |
| PM View | 从正式文档、ledger 和 summary 生成的管理视图 | `.factory/pm/generated/status-dashboard.html` |
| Test Baseline | 项目级测试环境、接口测试、UI 测试、黑盒测试和发布回归基线 | `docs/04-project-development/06-testing-verification/`、`.factory/workitems/TEST-*` |

## 5. 四类场景入口

### 5.1 新项目

新项目从 Project 进入，必须先建立项目级 baseline，再拆第一批需求。

流程：

```text
理解意图
-> 项目目标与非目标
-> 领域划分与模块边界
-> 总体技术架构
-> 数据库基线
-> API 基线
-> 整体 UI 设计
-> 第一批需求
-> 任务拆解
-> 执行任务
-> 关闭任务
-> 关闭需求
```

必需 baseline work item：

| ID 模式 | 名称 | 产物 |
|---|---|---|
| `BASE-001` | 项目目标与范围 | 项目目标、非目标、成功标准 |
| `BASE-002` | 领域划分与模块边界 | 领域模块清单、交互规则 |
| `BASE-003` | 总体技术架构 | 分层、依赖方向、运行链 |
| `BASE-004` | 数据库基线 | 数据库设计、ERD 总图 |
| `BASE-005` | API 基线 | API 设计、`openapi.yaml` |
| `BASE-006` | 整体 UI 设计 | UI 信息架构、页面、组件、状态 |

### 5.2 增加需求

增加需求从 Requirement 进入。它必须先判断是否影响 baseline。

流程：

```text
理解意图
-> 分析需求
-> 判断是否影响领域 / 架构 / 数据库 / API / UI baseline
-> 如影响，创建或更新 BASE-* baseline work item
-> 映射到领域模块
-> 拆任务
-> 执行任务
-> 关闭任务
-> 关闭需求
```

### 5.3 变更需求

变更需求必须保留原需求版本历史，不能直接覆盖旧事实。

流程：

```text
理解变更意图
-> 找到原 Requirement
-> 影响分析
-> 更新需求版本和版本历史
-> 判断是否触发 baseline 变更
-> 重拆或调整任务
-> 处理受影响任务
-> 回归测试
-> 关闭变更
```

### 5.4 修复 bug

bug 作为特殊 Requirement 管理。修 bug 不能跳过需求分析和根因定位。

流程：

```text
复现问题
-> 记录期望行为和实际行为
-> 定位根因
-> 判断是否是需求、领域、架构、数据库、API 或 UI baseline 缺陷
-> 如是，创建 baseline 变更
-> 设计修复方案
-> 写回归测试
-> 最小修复
-> 单元测试
-> code review
-> 集成 / 回归测试
-> 关闭 bug 需求
```

## 6. 需求内部瀑布流程

每个 Requirement 内部必须按以下顺序推进：

```text
理解意图
-> 分析需求
-> 影响分析
-> 映射领域模块
-> 分解任务
-> 任务执行
-> 需求级验证
-> 需求级 review
-> 人工确认
-> 关闭需求
```

需求 gate：

| Gate | 必需证据 | 失败处理 |
|---|---|---|
| 意图清晰 | 用户意图、非目标、成功标准 | 回到 `brainstorming` |
| 需求可验收 | REQ、AC、NFR、风险、未决问题 | 回到 `requirements-engineering` |
| 影响分析完成 | baseline 影响判断、领域模块映射 | 创建 baseline work item 或回到需求分析 |
| 任务可执行 | 任务清单、依赖、输入输出、测试策略 | 回到 `writing-plans` |
| 任务全部关闭 | 每个任务有 evidence、review、verification | 阻塞需求关闭 |
| 需求验证通过 | 验收标准逐项验证 | 回到相关任务 |
| 人工确认 | 用户明确 `human_approved` | 停在 `pending_human_confirmation` |

## 7. 任务内部瀑布流程

每个 Task 内部必须按以下顺序推进：

```text
任务目标
-> 设计方案
-> 接口设计
-> UI 设计或 N/A
-> 测试设计
-> 开发
-> 单元测试
-> code review
-> 评审
-> 集成测试
-> 关闭任务
```

任务 gate：

| Gate | 必需证据 | 允许 N/A 条件 |
|---|---|---|
| 设计方案 | 方案、边界、影响文件、禁止项 | 不允许 N/A |
| 接口设计 | 函数/API/类型/数据结构契约 | 确无接口变化，需写原因 |
| UI 设计 | 页面、状态、组件、交互、可访问性 | 非 UI 任务，需写原因 |
| 测试设计 | 单测、集成、回归测试用例 | 不允许 N/A |
| 开发 | 代码 diff 或文档 diff | 不允许 N/A |
| 单元测试 | 命令和输出 | 文档-only 任务可写 N/A，需 review 接受 |
| code review | 独立 review 文件 | 不允许 N/A |
| 集成测试 | 命令、输出、未运行原因 | 需明确无集成面且 review 接受 |
| 关闭任务 | ledger 无阻塞、evidence 齐全 | 不允许 N/A |

## 8. 领域模块与微服务边界

后端模块按微服务原则定义，即使当前代码部署为单体多模块应用。

规则：

- 模块是最小高内聚领域单元。
- 模块拥有自己的领域模型和数据写入边界。
- 模块之间禁止直接读写内部对象。
- 模块之间通过应用服务接口、领域事件、只读查询视图、集成表、API 契约或其他明确边界交互。
- 单体应用内部也按模块边界写代码，避免未来拆服务时重画领域边界。

禁止：

- A 模块直接 import B 模块 repository。
- A 模块直接改 B 模块业务表。
- A 模块绕过 B 模块服务写业务状态。
- 需求任务绕过领域模块直接修改数据库或 API。

## 9. 设计归属

### 9.1 项目级设计

以下设计属于 Project baseline，不挂普通业务需求：

| 设计任务 | Work item 类型 | 典型产物 |
|---|---|---|
| 领域划分 | `baseline` | 领域模块清单、职责、交互规则 |
| 总体技术架构 | `baseline` | 分层、依赖方向、运行链 |
| 数据库基线 | `baseline` | `database-design.md`、ERD |
| API 基线 | `baseline` | `api-design.md`、`openapi.yaml` |
| 整体 UI 设计 | `baseline` | UI 设计文档、页面清单、组件规则 |

### 9.2 需求级设计

需求级设计只处理增量：

- 需求映射到哪些领域模块。
- 需求是否修改数据库实体、字段、索引或迁移。
- 需求是否新增或修改 API。
- 需求是否新增页面、状态、组件或前端业务接口。
- 需求是否要求 baseline 变更。

### 9.3 任务级设计

任务级设计只回答当前任务怎么做：

- 修改哪些文件。
- 使用哪个已有模块、接口或模板。
- 最小实现是什么。
- 测试如何证明它满足需求。

## 10. 文档与记忆结构

正式文档保留四大模块结构：

```text
docs/
  01-getting-started/
  02-user-guide/
  03-developer-guide/
  04-project-development/
    03-requirements/
    04-design/
    05-development-process/
```

执行事实和记忆结构：

```text
.factory/
  memory/
    runtime-brief.md
    current-state.md
    doc-map.md
    *.summary.md
  workitems/
    <WORKITEM-ID>/
      brief.md
      plan.md
      task-briefs/
      evidence/
      reviews/
      reports/
      ledger.jsonl
  pm/
    generated/
      status-dashboard.html
```

边界：

| 层 | 作用 | 规则 |
|---|---|---|
| `docs/` | 人类可审计正式事实源 | 需要版本信息和版本历史 |
| `.factory/workitems/` | 执行证据和 ledger | 可以记录过程细节，不替代正式文档 |
| `.factory/memory/` | AI 快速恢复上下文摘要 | 不复制完整正文，不作为最终事实源 |
| `.factory/pm/generated/` | 展示视图 | 可覆盖生成，不作为事实源 |

### 10.1 启动读取规则

启动时不能只看 `current-state.md`，也不能固定读取所有 memory 文件。

启动恢复使用条件读取链。每一步如果已经足够判断当前阶段、工作项、禁止动作和下一步，就停止，不继续读取后续文件。

```text
当前对话已有新鲜会话卡
-> 够用则停止
-> 不够才读 .factory/memory/agent-session.md
-> 仍缺关键事实才读 runtime-brief.md / current-state.md 的最小片段
-> 有当前 work item 时才读该 work item ledger
-> summary 不足时才读当前任务相关 summary
-> 只有需要定位正式事实源时才读 doc-map.md
-> 只有 summary 与 ledger 仍不足时，才按 doc-map.md 单文件回源正式文档
```

规则：

- `current-state.md` 只回答当前阶段、活跃任务、阻塞项和最近事实。
- `current-state.md` 不承载完整任务历史。
- `runtime-brief.md` 承载稳定入口、禁止动作和流程边界。
- `*.summary.md` 承载主题索引。
- work item ledger 承载执行事实。
- 正式文档仍是最终事实源。
- `agent-session.md`、`runtime-brief.md`、`current-state.md` 不是每次必读集合；它们是逐级 fallback。
- 读取目标是形成小型会话卡，不是把 memory 文件重新塞回上下文。

### 10.2 非活跃任务记忆降级

非活跃任务不能长期留在 `current-state.md`。

| 任务状态 | 处理 |
|---|---|
| `ready_for_review` | 仍是活跃任务，保留在 `current-state.md` |
| `changes_requested` | 仍是活跃任务，保留在 `current-state.md` |
| `pending_human_confirmation` | 仍是活跃任务，保留在 `current-state.md` |
| `blocked` 且有下一动作 | 仍是活跃任务，保留在 `current-state.md` |
| `closed` / `committed` / `done` | 下一次 memory sync 后从 `current-state.md` 移除 |
| `superseded` | 下一次 memory sync 后从 `current-state.md` 移除，并在 summary 写替代项 |
| 暂停但未关闭 | 从 `current-state.md` 移到 backlog summary，除非用户恢复 |

保留规则：

- work item ledger 永不删除。
- evidence、review、report 永不因从当前记忆移除而删除。
- `tasks.summary.md` 保留已关闭任务的一行索引，直到阶段归档。
- 阶段归档后，已关闭任务压缩进历史摘要或 release report。
- PM 看板只展示活跃、阻塞、待确认和当前发布相关任务。

## 10.3 整体测试与测试环境

整体接口测试、UI 测试、黑盒测试和发布回归不挂在随机业务需求下。它们挂 Project、Baseline 或 Release。

项目级测试 work item：

| Work item | 作用 | 事实源 |
|---|---|---|
| `TEST-ENV-001` | 测试环境基线 | `test-environment.md` |
| `TEST-API-001` | 全量接口契约和接口回归 | `api-test-cases.md`、`openapi.yaml` |
| `TEST-UI-001` | UI smoke、交互和 E2E | `ui-test-cases.md` |
| `TEST-BB-001` | 整体黑盒测试 | `black-box-test-cases.md` |
| `TEST-REL-001` | 发布前回归 | `release-regression-report.md` |

挂载规则：

- 单个接口测试挂对应 `REQ` 或 `TASK`。
- 全量接口测试挂 `TEST-API-*`。
- 单个页面交互测试挂对应 `REQ` 或 `TASK`。
- 全站 UI / E2E 测试挂 `TEST-UI-*`。
- 整体黑盒测试挂 `TEST-BB-*` 或 `TEST-REL-*`。
- 每个测试用例必须反向关联 `REQ`、`AC`、API、页面、模块或 baseline。

测试环境规则：

- 谁执行测试，谁启动测试环境。
- `verification-before-completion` 或测试类 work item 执行者负责启动、健康检查、记录端口和停止环境。
- 默认端口写入 `test-environment.md`。
- 测试命令通过环境变量读取实际端口。
- 端口冲突时可以换端口，但测试报告必须记录实际 `BASE_URL`、`API_BASE_URL` 和原因。
- 测试报告必须写启动命令、健康检查、测试数据和关闭方式。

## 11. 文档版本管理

每个正式文档必须包含中文版本信息：

```markdown
## 版本信息

| 项目 | 内容 |
|---|---|
| 文档编号 |  |
| 文档类型 |  |
| 当前版本 |  |
| 当前状态 |  |
| 最近更新 |  |
```

每个正式文档必须包含版本历史：

```markdown
## 版本历史

| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
```

版本规则：

| 版本 | 含义 |
|---|---|
| `0.x` | 草稿 |
| `1.0` | 首次批准 |
| `1.x` | 兼容性修改 |
| `2.0` | 重大重写或破坏性变更 |

## 12. PM 与归档报告

日常状态使用 `.factory/pm/generated/status-dashboard.html`，可覆盖生成。

阶段归档或对外汇报时，才生成项目实施管理文档。该文档只能汇总事实，不能创造事实。缺证据必须写 `blocked` 或 `缺证据`。

## 13. 功能需求

### `FLOW-REQ-001` 四类场景入口

- 优先级：P0
- 状态：draft
- 说明：流程必须识别新项目、增加需求、变更需求、修复 bug，并为每类场景生成不同的输入包、gate 和工作项类型。
- AC-1: 给定用户提出新项目，当进入流程，则创建 Project baseline 输入包。
- AC-2: 给定用户提出新增功能，当进入流程，则创建 Requirement 输入包并检查 baseline 影响。
- AC-3: 给定用户要求变更已有需求，当进入流程，则定位原需求并写版本历史。
- AC-4: 给定用户报告 bug，当进入流程，则必须先复现和定位根因。

### `FLOW-REQ-002` 需求瀑布流程

- 优先级：P0
- 状态：draft
- 说明：每个需求必须按意图、分析、影响分析、任务拆解、任务执行、验证、review、人工确认、关闭推进。
- AC-1: 给定需求缺少验收标准，当请求进入任务拆解，则流程阻塞。
- AC-2: 给定需求的任务未全部关闭，当请求关闭需求，则流程阻塞。

### `FLOW-REQ-003` 任务瀑布流程

- 优先级：P0
- 状态：draft
- 说明：每个任务必须包含方案设计、接口设计、UI 设计或 N/A、测试设计、开发、单测、code review、评审、集成测试和关闭。
- AC-1: 给定任务没有测试设计，当请求开发，则流程阻塞。
- AC-2: 给定任务没有独立 code review，当请求关闭任务，则流程阻塞。

### `FLOW-REQ-004` Baseline work item

- 优先级：P0
- 状态：draft
- 说明：领域划分、总体架构、数据库基线、API 基线和整体 UI 设计必须挂在 Project 下的 baseline work item，不挂普通需求。
- AC-1: 给定整体 UI 设计任务，当登记 work item，则类型为 `baseline`。
- AC-2: 给定普通需求需要调整领域边界，当分析需求，则创建 baseline 变更并反向关联该需求。

### `FLOW-REQ-005` 文档治理

- 优先级：P0
- 状态：draft
- 说明：正式文档只能在登记路径下维护，临时文档只能在临时目录或 work item evidence 中维护。
- AC-1: 给定新增正式文档，当保存文件，则必须同步根导航或 doc-map。
- AC-2: 给定修改正式文档，当保存文件，则必须更新版本历史。

### `FLOW-REQ-006` 记忆同步

- 优先级：P0
- 状态：draft
- 说明：`.factory/memory/` 只存摘要、索引、当前状态和读取映射，不能复制完整正式文档。
- AC-1: 给定正式需求更新，当同步 memory，则只写 ID、状态、优先级、当前 gate 和关键约束。
- AC-2: 给定 summary 与正式文档冲突，当恢复上下文，则以正式文档和 ledger 为准。

### `FLOW-REQ-007` 后端领域模块设计

- 优先级：P0
- 状态：draft
- 说明：后端按领域模块设计，模块边界遵守微服务原则，模块交互必须通过明确接口或解耦数据结构。
- AC-1: 给定需求修改数据库，当设计任务，则必须先映射到领域模块。
- AC-2: 给定跨模块交互，当评审设计，则必须能指出接口、事件、只读视图或集成表边界。

### `FLOW-REQ-008` 数据库设计

- 优先级：P0
- 状态：draft
- 说明：数据库设计必须独立维护，并包含 ERD；顺序为先统一领域边界，再按领域 / 模块设计数据，最后按需求增量修改。
- AC-1: 给定新项目数据库设计，当进入设计，则必须生成数据库基线和 ERD 总图。
- AC-2: 给定需求新增字段或表，当设计任务，则必须写迁移、兼容和回滚策略。

### `FLOW-REQ-009` API 设计

- 优先级：P0
- 状态：draft
- 说明：接口设计必须独立维护，并输出 `openapi.yaml`；管理后台接口也必须受同一契约治理。
- AC-1: 给定新增 API，当评审设计，则必须能在 `openapi.yaml` 中找到契约。
- AC-2: 给定前端需要新业务接口，当设计前端任务，则必须判断复用后端接口、扩展后端接口或新增 BFF。

### `FLOW-REQ-010` 前端整体 UI 设计

- 优先级：P0
- 状态：draft
- 说明：前端必须有整体 UI 设计，包括信息架构、页面清单、用户路径、组件规则、状态设计和接口使用。
- AC-1: 给定新项目包含前端，当项目 baseline 未完成 UI 设计，则普通前端任务不得进入开发。
- AC-2: 给定需求影响全局 UI 规则，当需求分析完成，则必须创建 baseline 变更。

### `FLOW-REQ-011` Skill 输入输出契约

- 优先级：P0
- 状态：draft
- 说明：每个 workflow skill 必须定义输入、输出、内部流程、状态回写和禁止动作。
- AC-1: 给定 skill 完成工作，当输出状态包，则必须包含 work item、status、outputs、evidence、ledger_event 和 needs。
- AC-2: 给定工作 skill 输出“下一步调用哪个 skill”，当评审 skill，则判定为不合格。

### `FLOW-REQ-012` 防跳步门禁

- 优先级：P0
- 状态：draft
- 说明：流程必须通过 gate、evidence、review 和黑盒 eval 防止 AI 跳步、省步骤或自批完成。
- AC-1: 给定缺少 evidence，当请求关闭任务，则流程阻塞。
- AC-2: 给定作者自检通过，当请求写 `approved`，则流程阻塞。
- AC-3: 给定用户要求“直接提交”，当 review 或 verification 缺失，则流程阻塞并说明缺口。

### `FLOW-REQ-013` PM 视图

- 优先级：P1
- 状态：draft
- 说明：项目管理状态从 docs、work item ledger 和 memory summary 生成，日常输出 HTML 看板，阶段需要时生成归档管理文档。
- AC-1: 给定任务状态变化，当刷新 PM 看板，则看板从 ledger 汇总状态。
- AC-2: 给定需要阶段汇报，当生成实施管理文档，则必须列出证据路径和缺证据项。

### `FLOW-REQ-014` 追踪矩阵

- 优先级：P1
- 状态：draft
- 说明：Requirement、Baseline、Task、Design、Evidence、Review、Verification 必须可追踪。
- AC-1: 给定任一任务，当检查追踪，则能找到父需求或父 baseline。
- AC-2: 给定任一需求，当检查关闭条件，则能列出所有任务和 evidence。

### `FLOW-REQ-015` 兼容现有 Shanforge 流程

- 优先级：P0
- 状态：draft
- 说明：新流程契约必须复用现有 skill-first 架构，不恢复旧中心脚本、动作注册表或旧全局流程脚本。
- AC-1: 给定实施方案，当评审架构，则不得出现新的中心 CLI 主控。
- AC-2: 给定确定性 helper，当设计使用方式，则必须归属到具体 skill 的 `scripts/` 或 references。

### `FLOW-REQ-016` 项目级测试与测试环境

- 优先级：P0
- 状态：draft
- 说明：整体黑盒测试、UI 测试、接口测试和发布回归必须作为 Project、Baseline 或 Release 级测试工作项管理，并反向关联具体需求和任务。
- AC-1: 给定全量接口测试，当登记测试任务，则挂到 `TEST-API-*`，不能挂到随机业务需求。
- AC-2: 给定整体 UI / E2E 测试，当登记测试任务，则挂到 `TEST-UI-*` 或 `TEST-REL-*`。
- AC-3: 给定测试需要本地服务，当执行测试，则测试执行者必须启动环境、记录端口、健康检查和关闭方式。
- AC-4: 给定端口冲突，当换端口执行测试，则测试报告必须记录实际 URL 和原因。

### `FLOW-REQ-017` 启动记忆和非活跃任务降级

- 优先级：P0
- 状态：draft
- 说明：启动恢复不能只依赖 `current-state.md`；非活跃任务必须从当前记忆降级，避免 current-state 长期堆积历史。
- AC-1: 给定新会话启动，当已有会话卡足够判断当前阶段、工作项和禁止动作，则不得继续读取 `agent-session.md`、`runtime-brief.md` 或 `current-state.md`。
- AC-2: 给定会话卡缺失、过期或不匹配，当恢复上下文，则先读取 `agent-session.md`；仍缺关键事实时才读取 `runtime-brief.md` 和 `current-state.md` 的最小片段。
- AC-3: 给定 summary 足够回答当前任务，当恢复上下文，则不得默认散读正式 `docs/`。
- AC-4: 给定任务已 `closed`、`committed` 或 `done`，当下一次 memory sync 执行，则从 `current-state.md` 移除该任务。
- AC-5: 给定任务从 `current-state.md` 移除，则 ledger、evidence、review 和 summary 索引不得删除。

## 14. 非功能需求

| ID | 类型 | 要求 | 验证 |
|---|---|---|---|
| `FLOW-NFR-001` | 可审计性 | 每个状态变更必须有 ledger 或 evidence | ledger 解析、review |
| `FLOW-NFR-002` | 可恢复性 | 上下文压缩后可从 memory、work item 和正式文档恢复 | 恢复场景 eval |
| `FLOW-NFR-003` | 可维护性 | 主 skill 保持短流程，长模板进入 references | skill 结构测试 |
| `FLOW-NFR-004` | 一致性 | docs、memory、PM 视图冲突时按事实源优先级裁决 | 黑盒 eval |
| `FLOW-NFR-005` | 防绕过 | 缺 gate 时不能关闭、提交或宣称完成 | 负向测试 |

## 15. 影响范围

| 范围 | 影响 |
|---|---|
| `skills/using-shanforge/` | 增加四类场景路由、baseline work item、关闭 gate |
| `skills/project-memory/` | 增加三层文档和 memory 映射恢复规则 |
| `skills/brainstorming/` | 强化意图理解和场景识别 |
| `skills/requirements-engineering/` | 增加需求版本、影响分析、领域模块映射 |
| `skills/document-templates/` | 增加三层正式文档、版本历史、临时文档规则 |
| `skills/writing-plans/` | 增加任务瀑布流和测试设计前置 |
| `skills/executing-plans/` | 强化按任务 gate 执行，不跳步 |
| `skills/requesting-code-review/` | 强化独立 review 和 N/A 接受规则 |
| `skills/verification-before-completion/` | 强化关闭前新鲜验证 |
| `.factory/memory/` | 增加流程契约摘要和 doc-map 映射 |
| `.factory/pm/` | 以 ledger 生成日常 PM 看板，阶段性生成归档报告 |
| `docs/04-project-development/` | 新增流程契约需求与实施方案 |

## 16. 风险与未决问题

| 风险 | 影响 | 处理 |
|---|---|---|
| 文档过多 | AI 和人类都难维护 | 坚持三层正式文档，按需拆附件 |
| baseline 和需求边界混淆 | 整体设计被塞进普通需求 | baseline work item 独立建模 |
| memory 复制正式文档 | 事实冲突 | memory 只写索引和摘要 |
| skill 互相决定下一步 | 流程失控 | `using-shanforge` 统一路由 |
| AI 跳过 N/A 说明 | 质量 gate 失效 | N/A 必须写原因并被 reviewer 接受 |

## 17. 关闭条件

本需求关闭前必须满足：

1. 正式需求文档已通过 review。
2. 正式实施方案已通过 review。
3. 每个受影响 skill 的修改任务已拆分并登记。
4. 每个 skill 的输入、输出、内部流程和状态回写已在实施方案中定义。
5. 文档版本信息、版本历史和临时文档规则已进入模板。
6. 黑盒 eval 覆盖四类场景、baseline 任务、缺 evidence、作者自批、跳过测试、跳过 review、直接提交等负向场景。
7. 项目级测试 work item、测试环境启动规则和端口记录规则已进入实施方案。
8. 启动记忆读取顺序和非活跃任务降级规则已进入 `project-memory` 改造任务。
9. PM 看板能从 work item ledger 展示需求和任务状态。
10. 相关 `.factory/memory/` 摘要和 `doc-map.md` 已同步。
