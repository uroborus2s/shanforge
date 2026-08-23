# 测试治理剩余闭环实施计划

**目标：** 发布测试策略、建立正式案例目录并用可执行校验器闭合案例和报告一致性。

**架构：** 人类事实只保存在 Markdown 测试计划、案例目录和 WorkItem 报告中。`document-templates` 自带标准库校验器读取这些文档，检查结构、自动化入口、七态计数和四态批次结论，不新增第二份案例注册表。

**技术栈：** Python 3.14 标准库、pytest、Ruff、Markdown 正式文档。

**工作项：** `TEST-GOVERNANCE-CLOSURE-001`

**状态：** `implementation_ready_for_commit`

## 输入

- 已批准输入：用户本轮“完成测试治理剩余闭环”。
- 前置工作项：`TEST-GOVERNANCE-001`。
- 正式事实：`docs/06-delivery/test-plan.md`。
- 审计输入：截图中的七项成熟度判断。

## 范围

### 目标

- 关闭案例定义、报告、自动有效性、状态聚合和正式发布缺口。

### 非目标

- 不新增不存在的产品暴露面或重复机器注册表。
- 不修改并行工作项。

## 文件

| 类型 | 路径 | 职责 |
|---|---|---|
| 新建 | `docs/06-delivery/test-cases.md` | 当前项目人类可读正式案例目录 |
| 新建 | `skills/document-templates/scripts/validate_test_documents.py` | 标准库案例/报告有效性校验 |
| 修改 | `docs/06-delivery/test-plan.md` | 发布 `v3.2.0` 并登记校验入口 |
| 修改 | `skills/document-templates/assets/templates/05-quality/test-*.md` | 模板补齐可执行校验合同 |
| 测试 | `tests/test_project_test_governance.py` | Red-Green 与当前资产闭环守卫 |
| 文档 | `docs/06-delivery/index.md`、`docs/document-index.md` | 正式导航和索引 |
| 记忆 | `.factory/memory/*`、本 WorkItem | 收口事实、证据、评审和报告 |

## 边界

- 层级：系统治理。
- 领域：测试设计、验证与文档资产。
- 接口归属方：`document-templates` 拥有模板和校验器，正式文档拥有项目测试事实。
- 禁止耦合：不依赖 Shanforge 源码运行时，不引入第三方 Markdown 解析器。

## 任务

### T01：案例目录与自动有效性校验

- 先在 `tests/test_project_test_governance.py` 增加失败断言，要求正式案例目录、入口解析、完整字段、状态和报告聚合校验。
- 实现 `validate_test_documents.py` 与 `docs/06-delivery/test-cases.md`。
- 定向命令：`uv run pytest -q tests/test_project_test_governance.py`，期望先按缺口失败，再全部通过。
- 风险：`medium`。

### T02：模板合同与正式发布

- 更新测试计划、案例和报告模板的校验入口与报告适用边界。
- 将正式计划发布为 `v3.2.0`，同步质量入口、文档索引和 `doc-map.md`。
- 运行校验器验证正式案例和当前 WorkItem 报告候选。
- 风险：`medium`。

### T03：集中质量门与收口

- 生成一套实现摘要、验证 evidence、审计判断对照和人类可读测试报告。
- 运行完整 pytest、Ruff、受影响 Skill validator、JSON/JSONL、Git hygiene。
- 完成独立评审与同范围整改，使用 `gitcommitzh` 本地提交并做干净克隆终验。
- 风险：`medium`。

## 测试策略

- 红灯：正式案例目录、校验脚本和 `v3.2.0` 发布事实缺失时失败。
- 绿灯：有效案例/报告通过；失效入口、错误计数和错误批次结论负例被拒绝。
- 定向回归：`tests/test_project_test_governance.py`。
- 批次回归：完整 pytest、Ruff、两个 Skill validator、JSON/JSONL、Git hygiene。
- 未运行项：不存在真实运行时的网络 API、性能、安全和动态 UI，不为补表运行。

## 集中质量门

- 计划独立评审：`N/A`（中风险，作者自审）。
- 批次代码评审：`approved / 98 / C0-I0-M0`。
- 批次验证：隔离候选 `246 passed / 4 subtests passed`，Ruff、文档校验和结构化数据门通过。
- 本地提交：`pending`。
- 记忆同步：已按共享文件 hunk 精确同步。

## 计划自审

- 规格覆盖：七项截图判断均映射到 T01/T02/T03。
- 占位符扫描：无实现占位语。
- 类型一致性：案例七态、批次四态沿用已发布合同。
- 可构建性：路径、命令和输出明确。
- 批次质量门：集中在 T03。
