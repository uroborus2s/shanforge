# 技术选型与工程规则

**项目名称：** 山海工枢 / shanforge
**文档状态：** `v2` 技术基线
**负责人：** 仓库维护者
**主要读者：** 架构 | 平台开发 | 测试 | 维护者
**上游输入：** PRD | 需求分析
**下游输出：** 系统架构 | 模块边界 | 实施计划 | 测试计划
**最后更新：** 2026-04-15

## 1. 选型原则

- 先保证平台抽象正确，再扩展适配器数量。
- 先收口契约和边界，再做能力堆叠。
- 业务开发优先面对声明式协议，而不是基础设置实现细节。
- 所有关键能力都必须可 mock、可测试、可回放。

## 2. `v2` 实现基线

| 方向 | 选择 | 原因 |
|---|---|---|
| 主语言 | Python 3.14+ | 当前工程栈一致，类型表达和脚本化能力足够 |
| 包与工具链 | `uv` | 统一 Python、依赖、锁文件和工具执行 |
| 契约建模 | Typed schema + JSON/YAML manifest | 便于 workflow、model policy、capability 定义和校验 |
| 数据校验 | Pydantic v2 风格校验模型 | 适合运行时 contract validation |
| 事件记录 | JSONL / structured event records | 便于会话回放、调试和 evidence 对齐 |
| 文档 | Markdown + docs-stratego | 延续当前文档校验链路 |
| 测试 | `pytest` + mock providers + contract fixtures | 覆盖 workflow、provider、response 和 policy |

## 3. 平台层选型

| 层 | 选择 | 不选择 | 原因 |
|---|---|---|---|
| 架构风格 | DDD / Hexagonal | 直接在脚本外包一层薄 runtime | 平台需要清晰的业务隔离与适配器边界 |
| 层边界 | 六层架构 + consumer-owned ports | 统一 ports 层 / 跨层 owner | 保证接口 owner、业务 owner 和实现 owner 清晰分离 |
| 业务开发面 | Agent App Manifest + Workflow DSL | 业务代码直接耦合平台内核 | 降低业务流开发成本 |
| 模型交互 | `LLM Runtime + LLMProviderPort + ModelPolicy` | 业务 step 直接调 SDK | 保证供应商可替换和 step 级策略 |
| 工具治理 | `Capability Registry` | 任意脚本或 shell 暴露给业务 | 保证输入输出、风险和证据可控 |
| 上下文治理 | `Session + Memory + Context Engine` | 随机拼 prompt 或默认散读全局文档 | 保证最小上下文和可恢复性 |
| 响应处理 | `Response Normalizer + Output Parser + Schema Validator` | 原始模型文本直返业务层 | 保证返回格式稳定 |

## 4. 适配器策略

遗留代码、脚本、文件合同、CLI 入口仍可被复用，但只放在基础设置层实现区中。它们的定位是：

- 作为现有能力来源
- 作为迁移期间的桥接层
- 作为平台验证阶段的快速执行器

它们不再定义产品方向，也不再进入主需求判断。

## 5. 工程规则

- `pyproject.toml` 是版本和 Python 基线事实源。
- 平台代码必须优先围绕业务模型、业务调度、基础能力和基础设置实现区组织。
- 业务 App 不允许直接 import 基础设置适配器或 storage/provider 实现。
- workflow、model policy、capability 和 response schema 必须有显式契约。
- 接口 owner 必须跟随消费者所在层定义，不允许重新引入统一 ports 层。
- 文档、测试和 `.factory/memory` 必须与平台设计同步。

## 6. 同步要求

- 需求变更时同步更新：`system-architecture.md`、`module-boundaries.md`、`api-design.md`
- 契约变更时同步更新：`implementation-plan.md`、`test-plan.md`、追踪矩阵
- 新增业务 App 示例时同步更新：PRD 与测试计划中的验证范围

## 7. 版本记录

| 版本 | 日期 | 变更内容 |
|---|---|---|
| `v2.0` | 2026-04-13 | 重写技术选型，确立抽象 Agent 平台的实现基线和适配器策略 |
| `v2.1` | 2026-04-15 | 补齐六层架构、consumer-owned ports 和基础设置层约束 |
