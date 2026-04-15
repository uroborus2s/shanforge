# 测试计划

**项目名称：** 山海工枢 / shanforge
**文档状态：** `v2` 测试基线
**负责人：** 仓库维护者
**主要读者：** QA | 架构 | 平台开发 | 业务 Agent 开发
**上游输入：** PRD | API 设计 | 实施计划
**下游输出：** 测试报告 | 发布说明
**最后更新：** 2026-04-14

## 1. 测试目标

- 验证平台契约是否稳定
- 验证 workflow、模型和 capability 运行时是否闭环
- 验证业务 App 是否真的只依赖平台契约
- 验证高风险执行和证据记录是否可控

## 2. 测试层次

| 层次 | 范围 | 重点 |
|---|---|---|
| Schema / Contract 测试 | Manifest、Workflow DSL、ModelPolicy、Capability、AgentResponse | 字段完整性、约束、一致性 |
| Domain / Use Case 测试 | Session、workflow step、state transition | 运行逻辑和状态迁移 |
| Provider / Capability Mock 测试 | mock LLM、mock capability | 可替换性和离线验证 |
| Memory Distillation 测试 | candidate extraction、promotion gate、recall bundle | 二级资产保真与治理正确性 |
| Integration 测试 | Kernel + workflow + response pipeline | 主闭环可运行 |
| Policy / Sandbox 测试 | approval、writeset、execution gates | 风险控制是否生效 |
| Demo App 验收测试 | 编码流、写作流 | 业务装配是否可用 |

## 3. 关键测试项

| 用例 | 目标 |
|---|---|
| `TC-001` Manifest 校验 | Agent App schema 可校验 |
| `TC-002` Workflow DSL 校验 | step、条件、输出契约有效 |
| `TC-003` ModelPolicy fallback | 模型不可用时执行 fallback |
| `TC-004` Capability 风险控制 | 高风险能力触发审批 |
| `TC-005` Context Package 生成 | 上下文最小集可复现 |
| `TC-006` AgentResponse 标准化 | 模型与工具输出均可归一化 |
| `TC-007` 写集冲突 | 委派合并前可识别冲突 |
| `TC-008` Demo 编码流 | 编码工作流可跑通 |
| `TC-009` Demo 写作流 | 写作工作流可跑通 |
| `TC-010` Session Ledger 保真 | 原始 event/evidence 不被蒸馏层覆盖 |
| `TC-011` Promotion Gate | 无 evidence 或冲突 candidate 不能晋升长期记忆 |
| `TC-012` Recall Bundle | recall 只返回 accepted memory，并带 diagnostics 与 source refs |

## 4. 质量门

- `docs-stratego source validate --repo-path .`
- `.factory/project.json` 与 `traceability.json` JSON 校验
- schema / contract 测试通过
- `uv run pytest`
- `git diff --check`

## 5. 发布前检查

- 所有 P0 需求有对应测试覆盖
- demo Agent Apps 可在 mock provider 下稳定运行
- 关键 API 契约未出现未登记变更
- 响应结构、审批事件和 evidence 可回放
- memory candidate、promotion decision 与 recall bundle 可追溯

## 6. 版本记录

| 版本 | 日期 | 变更内容 |
|---|---|---|
| `v2.0` | 2026-04-13 | 重写测试计划，围绕平台契约、运行时闭环和 demo Agent App 校验 |
| `v2.1` | 2026-04-14 | 新增记忆蒸馏、promotion gate 和 recall bundle 的测试方向 |
