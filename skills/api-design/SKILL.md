---
name: api-design
description: REST/HTTP API 契约设计与评审。用于新增端点、变更契约、分页过滤、错误响应、版本策略和公共 API 风险评估。
---

# API 设计

用于设计或评审 API 契约。主入口只保留决策清单；状态码、分页、鉴权和 OpenAPI 示例按任务需要输出，不在入口展开教程。

## 何时启用

- 设计新的 API 端点或资源模型。
- 评审已有 API 的命名、状态码、请求/响应、错误格式或兼容性。
- 添加分页、过滤、排序、搜索、幂等、速率限制或版本策略。
- 处理 API Bug、破坏性变更或消费者兼容风险。

## 边界

- 先沿用项目已有 API 风格、schema、错误格式、认证方式和文档位置。
- 本 skill 产出契约和评审结论，不替代后端实现、TDD 或完成前验证。
- API Bug 必须先定位根因：是路由、校验、权限、数据映射、状态码还是客户端契约漂移。
- 涉及安全、数据丢失或公共兼容性时，必须提高验证等级。

## 契约决策表

| 决策点 | 默认规则 | 升级条件 |
|---|---|---|
| 资源命名 | 名词、复数、稳定路径 | 动作无法映射 CRUD 时才用动词动作 |
| HTTP 方法 | GET 读，POST 建，PATCH 改，DELETE 删 | 幂等和重试语义必须写清 |
| 状态码 | 用 HTTP 语义表达成功和失败 | 不用 200 包所有错误 |
| 请求校验 | 边界入口校验并返回字段级错误 | 外部 API 需稳定错误 code |
| 分页 | 小型后台可偏移，大列表或 feed 用游标 | 公共 API 要写 cursor 兼容策略 |
| 过滤排序 | 查询参数稳定、可组合、可文档化 | 高成本查询需限制和索引说明 |
| 认证授权 | 认证和资源级授权分开描述 | 公共端点必须显式标记 |
| 版本兼容 | 非破坏性变更不升版本 | 删除/改名/改类型必须迁移策略 |

## 默认流程

1. 明确消费者、资源、用例、权限边界和错误场景。
2. 对照现有 API 找命名、响应封装、错误格式和分页惯例。
3. 输出最小契约：endpoint、method、request、response、error、auth、pagination、rate limit。
4. 标注兼容性：新增字段、弃用字段、破坏性变更、迁移窗口。
5. 给验证建议：schema/contract test、集成测试、目标 E2E 或人工验收。

## 输出类型

- 新 API：API contract、端点表、请求/响应 schema、错误 code、OpenAPI 片段。
- API 评审：按 Critical/Important/Minor 给问题、影响和最小修复。
- Bug/变更：根因、契约差异、迁移方案、防回归测试建议。
- 决策记录：取舍、兼容风险、不做项和后续触发条件。

## 风险分级验证

- 低风险：内部只读端点、文档补充、非破坏性字段新增。做契约自查和相关测试。
- 中风险：写接口、权限判断、分页过滤、错误格式变化。做集成测试和 schema/contract 断言。
- 高风险：公共 API、认证授权、计费、删除、迁移、破坏性变更。做兼容性检查、消费者影响评估、相关集成测试和目标 E2E。

## 自查清单

- URL、method、状态码和错误 code 符合现有约定。
- 输入校验在信任边界完成，错误不会泄露内部细节。
- 响应字段、空状态、分页、排序和过滤有稳定契约。
- 权限失败、资源不存在、冲突和限流有明确语义。
- 破坏性变更有迁移、弃用和回滚策略。
- 验证范围与风险匹配，没有把全量测试当作默认要求。

## 输出契约

```text
工作结果：
- work_item: <ID>
- skill: api-design
- status: passed | partial | failed | blocked
- outputs:
  - <API contract, review findings, or decision record>
- evidence:
  - <schema checks, tests, or review notes>
- ledger_event: <event id>
- needs:
  - none | product_decision | compatibility_review | tests | human_confirmation
```

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
