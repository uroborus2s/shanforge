# T04 评审整改验证

- 时间：2026-07-23 14:48（Asia/Shanghai）
- 红灯：新增英文/编号格式、138 份注册简报实体覆盖和非推测空态测试后 `3 failed`。
- 绿灯：上述三项测试修复后 `3 passed`；局部任务身份测试 `2 passed`。
- 真实语料：
  `138 total / 138 unique work_item / 138 with_any_semantics`。
- 字段覆盖：
  `goal=129 / work_items=64 / deliverables=71 / completion_conditions=93 / verification=88`。
- 项目知识目标回归：`67 passed in 0.97s`。
- Mypy：`Success: no issues found in 279 source files`。
- Ruff 首次发现 1 个整改产生的未使用局部变量，删除后限定 Ruff 通过。
- 固定 CLI：
  `generation:4da7096c748193759905048d8e98bc3b7c972248f12145d66338f83b51c029d6`，
  `parsed=146`、`rendered=361`、`reused=1731`。
- 真实 Chrome：
  需求树 17 个业务域、27 项需求、64 条验收链接；任务详情四区块及 `REQ-PKI-008`
  深链通过；390px 视口无横向溢出；控制台错误为 0。
- HTML、SQLite 和 cache 均为本地派生物，不进入 Git。

## Iteration 2 身份合并整改

- 新增 source registry 驱动的真实注册语料测试，同时断言 138 个实体 ID 全局唯一。
- 新增 brief + Ledger SQLite 索引级合并测试：同一个局部任务只生成一个实体，
  `lifecycle_status=in_progress` 且 `detail_json.goal` 来自任务简报。
- 项目知识目标回归：`69 passed in 1.12s`。
- Ruff：`All checks passed`。
- Mypy：`Success: no issues found in 279 source files`。
- 固定 CLI：
  `generation:a25a7c3633d4ed0b3a04027c0c8759295d0cfa28b41c37b4135391f1728de8e6`，
  `parsed=36`、`rendered=23`、`reused=2062`，退出码 `0`。
