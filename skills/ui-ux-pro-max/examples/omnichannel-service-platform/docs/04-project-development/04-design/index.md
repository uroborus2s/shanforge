# 设计

## 版本信息

| 文档编号 | 版本 | 状态 | 读者 | 更新日期 |
|---|---|---|---|---|
| `DOC-DESIGN-INDEX-001` | `0.1.0` | 样例 | 产品、设计、研发、测试 | 2026-07-24 |

## 版本历史

| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `0.1.0` | 建立设计导航 | 2026-07-24 | AI 示例作者 | 待审核 | 待批准 |

| 文档 | 主要作用 |
|---|---|
| [方案总览](solution-overview.md) | 从业务目标看整体方案和关键取舍 |
| [技术选型](technical-selection.md) | 固定四端、服务端和基础设施栈 |
| [系统架构](system-architecture.md) | 领域边界、调用关系、可靠性与安全 |
| [数据设计](data-design.md) | 实体 owner、状态机、约束和保留策略 |
| [API 设计](api-design.md) | 接口语义、错误、幂等和兼容策略 |
| [UX/UI 设计](ux-ui-design.md) | 用户流、页面清单、状态和可访问性 |
| [跨端矩阵](platform-matrix.md) | iOS、Android、小程序、后台差异 |
| [设计系统](design-system.md) | Token、组件、内容和动效规则 |
| [Penpot 交接](penpot-handoff.md) | 页面、画板、导出和开发映射 |

机器契约位于 [`contracts/`](contracts/design-artifact-manifest.yaml)。静态预览仅在 Penpot MCP 导出成功后生成，当前状态以清单为准。
