# 文档索引

## 版本信息

| 文档编号 | 版本 | 状态 | 负责人 | 更新日期 |
|---|---|---|---|---|
| `DOC-CATALOG-001` | `0.1.0` | 样例 | 文档负责人 | 2026-07-24 |

## 版本历史

| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `0.1.0` | 建立唯一事实源索引 | 2026-07-24 | AI 示例作者 | 待审核 | 待批准 |

## 面向人的正式文档

| 文档 ID | 中文名称 | 主要回答 | 唯一入口 |
|---|---|---|---|
| `DOC-OVERVIEW-001` | 项目概览 | 系统是什么、给谁用、边界是什么 | [项目概览](../../01-getting-started/project-overview.md) |
| `DOC-USER-001` | 用户指南 | 消费者如何完成预约和售后 | [用户指南](../../02-user-guide/user-guide.md) |
| `DOC-ADMIN-GUIDE-001` | 管理员指南 | 运营如何处理订单、服务和权限 | [管理员指南](../../02-user-guide/admin-guide.md) |
| `DOC-CHARTER-001` | 项目章程 | 目标、范围、角色和成功标准 | [项目章程](../01-governance/project-charter.md) |
| `DOC-PRD-001` | 产品需求文档 | 用户故事、功能需求、AC 和 NFR | [PRD](../03-requirements/prd.md) |
| `DOC-SOLUTION-001` | 方案总览 | 需求如何变成系统和四端体验 | [方案总览](../04-design/solution-overview.md) |
| `DOC-TECH-001` | 技术选型 | 为什么选择这些技术与替代边界 | [技术选型](../04-design/technical-selection.md) |
| `DOC-ARCH-001` | 系统架构 | 模块、依赖、状态和安全边界 | [系统架构](../04-design/system-architecture.md) |
| `DOC-DATA-001` | 数据设计 | 实体、约束、生命周期和隐私 | [数据设计](../04-design/data-design.md) |
| `DOC-API-DESIGN-001` | API 设计 | 资源、错误、幂等、认证和版本 | [API 设计](../04-design/api-design.md) |
| `DOC-UXUI-001` | UX/UI 设计 | 流程、页面、状态、动效和可访问性 | [UX/UI 设计](../04-design/ux-ui-design.md) |
| `DOC-PLATFORM-001` | 跨端平台矩阵 | 共同语义如何映射到四个平台 | [跨端平台矩阵](../04-design/platform-matrix.md) |
| `DOC-DESIGN-SYSTEM-001` | 设计系统 | Token、组件、状态和实现规则 | [设计系统](../04-design/design-system.md) |
| `DOC-PENPOT-001` | Penpot 设计交接 | 设计源、画板 ID、生成和交接 | [Penpot 交接](../04-design/penpot-handoff.md) |
| `DOC-PLAN-001` | 实施计划 | 按什么顺序实现、每项做到什么程度 | [实施计划](../05-development-process/implementation-plan.md) |
| `DOC-TEST-PLAN-001` | 测试计划 | 如何验证、环境和门禁是什么 | [测试计划](../06-testing-verification/test-plan.md) |
| `DOC-TEST-REPORT-001` | 测试报告 | 本次执行结果和发布建议 | [测试报告](../06-testing-verification/test-report.md) |
| `DOC-RELEASE-NOTES-001` | 发布说明 | 本版本变化、兼容性和限制 | [发布说明](../07-release-delivery/release-notes.md) |
| `DOC-ROLLBACK-001` | 回滚计划 | 何时、如何安全止损 | [回滚计划](../07-release-delivery/rollback-plan.md) |
| `DOC-DEPLOY-001` | 部署指南 | 如何发布和验证 | [部署指南](../08-operations-maintenance/deployment-guide.md) |
| `DOC-RUNBOOK-001` | 运维手册 | 如何观测、排障和恢复 | [运维手册](../08-operations-maintenance/operations-runbook.md) |
| `DOC-TRACE-MATRIX-001` | 需求追踪矩阵 | 需求对应哪些设计、接口、UI 和测试 | [需求追踪矩阵](requirements-matrix.md) |

## 机器契约

| 契约 | 用途 | 入口 |
|---|---|---|
| OpenAPI 3.1 | API 请求、响应、认证和错误契约 | [public-v1.openapi.yaml](../../03-developer-guide/openapi/public-v1.openapi.yaml) |
| 设计 Token | 各端语义样式映射 | [design-tokens.json](../04-design/contracts/design-tokens.json) |
| 设计资产清单 | Penpot 页面、画板和导出状态 | [design-artifact-manifest.yaml](../04-design/contracts/design-artifact-manifest.yaml) |
| 测试用例 | 机器可读的测试定义和需求关联 | [test-cases.yaml](../06-testing-verification/test-cases.yaml) |
| 测试结果 | 单次执行事实 | [test-results.json](../06-testing-verification/test-results.json) |

## 维护规则

同一事实只有一个正文 owner。导航、矩阵和 SQLite 索引只引用它；内容变化修改原文档并增加版本历史，不创建 `final-v2-new` 等平行文件。
