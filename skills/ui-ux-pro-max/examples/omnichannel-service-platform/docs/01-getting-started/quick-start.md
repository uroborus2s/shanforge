# 快速开始

## 版本信息

| 文档编号 | 版本 | 状态 | 读者 | 更新日期 |
|---|---|---|---|---|
| `DOC-QUICKSTART-001` | `0.1.0` | 样例 | 设计师、开发者、评审者 | 2026-07-24 |

## 版本历史

| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `0.1.0` | 初版 | 2026-07-24 | AI 示例作者 | 待审核 | 待批准 |

## 五分钟阅读

1. 在 [PRD](../04-project-development/03-requirements/prd.md) 找到需求与验收标准。
2. 在 [UX/UI 设计](../04-project-development/04-design/ux-ui-design.md) 找到用户流和页面 ID。
3. 在 [跨端矩阵](../04-project-development/04-design/platform-matrix.md) 查看平台差异。
4. 在 [OpenAPI](../03-developer-guide/openapi/public-v1.openapi.yaml) 查看接口契约。
5. 在 [需求追踪矩阵](../04-project-development/10-traceability/requirements-matrix.md) 验证需求是否落到设计和测试。

## 重新生成 Penpot 样例

前提：Penpot 当前文件已加载 MCP 插件并显示 Connected。

```text
通过 Penpot MCP 的 execute_code 运行：
../../tools/build-penpot-example.js
```

脚本按页面幂等创建同名画板。Penpot 一次只能修改当前活动页面，因此实际执行器应按 `00-说明` 至 `05-管理后台` 逐页切换后运行。
