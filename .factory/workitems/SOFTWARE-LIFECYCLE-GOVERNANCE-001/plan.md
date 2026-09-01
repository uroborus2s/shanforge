# 软件生命周期治理闭环实施计划

**目标：** 用最少的现行正式文档和一个跨文档治理测试，消除 Skill-first 与旧平台事实冲突，并固化完整生命周期的执行交接。

**架构：** `docs/` 保存稳定人类事实，机器附件只保留真实消费者使用的合同，`.factory/workitems/` 保存本次执行事实。Sol 负责范围和模型路由；测试、文档整改和一致性实现由 Terra worker 执行；批次末由未参与实现的 Terra/high reviewer 独立只读评审。

**技术栈：** Markdown、JSON、pytest、Python 标准库、Ruff、Git。

**工作项：** `SOFTWARE-LIFECYCLE-GOVERNANCE-001`

**状态：** `plan_ready`

## 输入与裁决

- 用户明确批准创建本 WorkItem，按“事实源统一 -> 生命周期矩阵 -> 一致性校验”实施并做到干净克隆全绿。
- 当前 WorkItem `MODEL-DISPATCH-RUNTIME-001` 已关闭，无人工 Gate，当前分支 `v2` 工作区干净。
- 任务涉及多个正式设计 owner、机器附件、追踪矩阵和测试，复杂度为 `complex`、风险为 `medium`。
- worker 固定为 `gpt-5.6-terra` / `medium`；独立 reviewer 固定为 `gpt-5.6-terra` / `high`。

## 任务与依赖

### T01：跨文档一致性 Red 测试

- 依赖：无。
- 交付：新增治理测试，并登记正式测试入口；旧候选必须因旧平台正文、版本漂移、需求状态或旧机器附件而失败。
- 写集：`tests/test_lifecycle_governance.py`、`docs/06-delivery/test-plan.md`、`docs/06-delivery/test-cases.md`。
- 验证：`uv run pytest tests/test_lifecycle_governance.py -q` 预期在整改前非零退出。

### T02：Skill-first 正式设计事实统一

- 依赖：T01 Red 已确认。
- 交付：把现行总体方案、技术选型、模块、数据、API、前端、UX/UI、记忆和接口矩阵压缩为真实 Skill-first 基线；删除没有当前消费者的旧平台机器附件并同步来源登记。
- 写集：任务简报列出的设计正文、旧机器附件和来源登记。
- 验证：治理测试中事实源与机器附件断言转绿，`git diff --check` 通过。

### T03：生命周期矩阵与追踪闭环

- 依赖：T01 Red 已确认；可与 T02 在无文件冲突时同层执行。
- 交付：重写流程执行设计，增加完整阶段矩阵和方法选择；同步文档索引、需求状态与设计导航。
- 写集：`docs/05-design/workflow-execution-design.md`、`docs/05-design/index.md`、`docs/document-index.md`、`docs/04-product/requirements-matrix.md`。
- 验证：生命周期、版本与需求状态断言转绿，`git diff --check` 通过。

### T04：集中质量、独立评审、提交与干净克隆

- 依赖：T01–T03 完成。
- 交付：一套实现摘要、验证 evidence、review input、独立 review、精确本地提交和提交后干净克隆验证。
- 首个候选运行完整质量门；Critical/Important 由原任务范围整改并复测。
- 不执行远端或生产动作。

## 测试策略

- Red：旧正式文档仍含已废止运行时、索引版本漂移、`REQ-SF-008` 状态过期、旧机器附件仍具资格。
- Green：`uv run pytest tests/test_lifecycle_governance.py -q` 通过。
- 定向回归：文档工厂、工作流、模型路由、测试治理测试通过。
- 批次验证：完整 pytest、Ruff、全部 Skill validator、TOML/JSON/JSONL、diff 卫生。
- UI/API E2E：不适用；本 WorkItem 移除不存在的运行面，不启动服务或浏览器。

## 集中质量门

- 计划自审：通过；三项实现交付物、精确写集、依赖、模型和验证命令完整。
- 独立评审：`pending`
- 批次验证：`pending`
- 本地提交：用户以“做到干净克隆全绿”授权当前 WorkItem 精确本地提交。
- 远端动作：`not_authorized`
