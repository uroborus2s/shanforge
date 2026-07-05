# SF-SP-009 黑盒流程 eval 实施计划

> 给执行者：本计划只为流程黑盒评估建立可执行契约和回归测试。执行完成后只能进入 `ready_for_review`，通过必须来自独立 review。

**目标：** 建立 Shanforge workflow 的黑盒评估契约，覆盖一句话需求、bug 修复、review 反馈、压缩恢复、完成声明和自评隔离场景，并用结构测试固定评分断言。

**架构：** 黑盒 eval 是 workflow contract，不是新的中心脚本。契约放在 `skills/using-shanforge/references/`，由流程总控引用；测试只校验 contract 完整性和无脚本主控回退。

**技术栈：** Markdown reference、pytest 结构测试、现有 skill validator。

**工作项：** `SF-SP-009`

**状态：** `ready_for_review`

---

## 输入

- 已批准的规格 / 需求 / 设计：`docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md` 中 `SF-SP-009` 和第 14 节黑盒评估场景。
- 当前工作项简报：用户要求 SF-SP-008 提交后直接进入 SF-SP-009 开发。
- 相关 `.factory/memory/` 摘要：`.factory/memory/tasks.summary.md`、`.factory/memory/current-state.md`。
- 已读取的正式文档：仅 Superpowers workflow integration plan 的 SF-SP-009 相关段落。

## 范围

### 目标

- 新增黑盒流程 eval reference，定义 fast smoke、full regression、证据格式和评分门。
- 覆盖六类场景：一句话需求、bug 修复、review 反馈、压缩恢复、完成声明、自评隔离。
- 更新 `using-shanforge`，让 SF-SP-009 或黑盒 eval 请求有唯一参考入口。
- 新增结构测试，防止 eval contract 缺场景、缺评分断言或退回中心脚本。

### 非目标

- 不新增 `scripts/factory-*`、`factory-dispatch` 或全局命令 gate。
- 不实现真实 LLM 对话评分器，不调用外部模型。
- 不关闭 SF-SP-009；本轮实现者只产出 `ready_for_review`。

## 文件

| 类型 | 路径 | 职责 |
|---|---|---|
| 新建 | `skills/using-shanforge/references/black-box-flow-eval.md` | 定义黑盒 eval 场景、评分断言、证据格式和失败门 |
| 修改 | `skills/using-shanforge/SKILL.md` | 为 SF-SP-009 / 黑盒 eval 请求增加 reference 入口 |
| 测试 | `tests/test_black_box_workflow_eval.py` | 固定场景覆盖、评分门和无脚本主控回退 |
| 文档 | `docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md` | 同步 SF-SP-009 当前开发状态 |
| 记忆 | `.factory/memory/current-state.md`、`.factory/memory/tasks.summary.md`、`.factory/memory/tests.summary.md`、`.factory/memory/skill-updates.summary.md` | 同步当前工作项状态和验证结果 |

## 边界

- 层级：workflow skill / process reference，不触碰 `src/` 六层架构代码。
- 领域：Shanforge 软件工厂流程治理。
- 接口归属方：`using-shanforge` 作为流程总控 owns 黑盒 eval reference 入口。
- 下游依赖：`project-memory`、`writing-plans`、`systematic-debugging`、`receiving-code-review`、`verification-before-completion`、`requesting-code-review` 的既有规则。
- 禁止耦合：禁止引入全局脚本主控、中心 dispatch gate、外部 LLM 服务依赖或实现者自批通过。

## 任务

### 任务 1：黑盒 eval 契约与结构测试

**文件：**

- 新建：`skills/using-shanforge/references/black-box-flow-eval.md`
- 修改：`skills/using-shanforge/SKILL.md`
- 测试：`tests/test_black_box_workflow_eval.py`
- 文档：`docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md`
- 记忆：`.factory/memory/*.summary.md`

- [x] **步骤 1：红灯，编写失败测试**

新增 `tests/test_black_box_workflow_eval.py`，断言黑盒 eval reference、六个场景、评分门、证据格式和无脚本主控回退。

- [x] **步骤 2：运行测试并确认失败**

运行命令：

```bash
.venv/bin/pytest tests/test_black_box_workflow_eval.py
```

期望输出：

```text
失败：缺少 black-box-flow-eval reference 或 using-shanforge 入口。
```

- [x] **步骤 3：绿灯，编写最小实现**

新增 reference，并在 `using-shanforge` 中加入 SF-SP-009 / 黑盒 eval 入口。

- [x] **步骤 4：运行测试并确认通过**

运行命令：

```bash
.venv/bin/pytest tests/test_black_box_workflow_eval.py
.venv/bin/ruff check tests/test_black_box_workflow_eval.py
python3 skills/skill-creator/scripts/quick_validate.py skills/using-shanforge
```

期望输出：

```text
通过。
```

- [x] **步骤 5：证据和记忆同步**

- 写入验证证据：`.factory/workitems/SF-SP-009/evidence/iteration-1-verification.md`。
- 写入实现报告：`.factory/workitems/SF-SP-009/reports/iteration-1-implementer-report.md`。
- 更新任务流水账：`.factory/workitems/SF-SP-009/ledger.jsonl`。
- 更新相关 `.factory/memory/` 摘要。

- [x] **步骤 6：评审门**

- 生成任务评审输入包：`.factory/workitems/SF-SP-009/reviews/review-brief.md`。
- 实现者状态只能进入 `ready_for_review`。
- 评审状态只能由独立评审者写成 `approved` 或 `changes_requested`。

## 测试策略

- 红灯：`tests/test_black_box_workflow_eval.py` 在 reference 未创建前失败。
- 绿灯：黑盒 eval reference 和 `using-shanforge` 入口补齐后通过。
- 定向回归：`pytest` + `ruff` + `using-shanforge` skill validator。
- 邻近回归：若时间允许，运行 `tests/test_execution_workflow_skills.py`、`tests/test_review_workflow_skills.py`、`tests/test_verification_debugging_workflow_skills.py`。
- 全量回归：不在本轮执行；仓库存在大量无关脏改动，定向验证更可控。
- 未运行项：真实 LLM 对话评分器、外部模型 eval。
- 未运行原因：本 work item 目标是本地黑盒 eval 契约与评分断言，不接入外部模型服务。

## 文档同步

- 正式文档：更新 Superpowers workflow integration plan 中 SF-SP-009 状态。
- `.factory/memory/`：更新 current-state、tasks、tests、skill-updates。
- 工作项流水账：记录进入、红灯、绿灯和 ready_for_review 事件。

## 评审门

- 计划评审：由本轮已批准的 SF-SP-009 高层计划约束，实施后进入 task review。
- 任务评审：`ready_for_review`
- 验证：`passed`
- 拉取请求 / 提交：`pending`
- 记忆同步：`done`

## 计划自审

- 规格覆盖：覆盖第 14 节所有列出的关键场景，并包含 SF-SP-009 明确的四类核心场景。
- 占位符扫描：无占位符；每个文件和命令均为具体路径。
- 类型一致性：只使用 Markdown 和 pytest 结构测试，无新增运行时类型。
- 可构建性：测试、reference 和 skill 更新可独立完成。
- Shanforge 门禁：包含 evidence、review brief、memory sync 和 ledger 更新，完成后只到 `ready_for_review`。
