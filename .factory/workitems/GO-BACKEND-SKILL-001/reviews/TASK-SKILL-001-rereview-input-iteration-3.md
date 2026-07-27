# TASK-SKILL-001 独立复审输入（Revision 4）

## 评审目标

只读评审用户变更请求后的 `go-backend-developer` skill，重点判断规则是否可执行、是否自相矛盾、模板是否真正体现 Ponytail，以及是否仍存在未获批准的 fallback/兼容扩张。

## 用户硬要求

- 借鉴成熟可靠的 GitHub Go skill 和模板，但不能盲目复制。
- 写 Go 代码时采用 Ponytail / YAGNI。
- 禁止仅为排版拆分只调用一次的方法或私有 helper。
- 控制方法嵌套深度。
- 采用符合 Go 的面向对象思维，设计模式只解决真实问题。
- 禁止多余回退、扩大兼容面和不必要的兼容代码。

## 评审范围

- `skills/go-backend-developer/**`
- `tests/test_go_backend_developer_skill.py`
- `.factory/workitems/GO-BACKEND-SKILL-001/evidence/TASK-SKILL-001-revision-4-verification.md`
- `.factory/workitems/GO-BACKEND-SKILL-001/reports/TASK-SKILL-001-revision-4-report.md`

## 明确边界

- 只读，不修改任何文件。
- 不复用 revision 3 的 97 分结论；按 revision 4 全量重评。
- 检查模板中的每个 package/function 是否有稳定边界，尤其是 `main -> run`、配置解析和 Gin middleware。
- 区分安全机制与推测性 fallback：校验、超时、关闭、事务回滚不得因简化被删除。

## 已有证据

见 `TASK-SKILL-001-revision-4-verification.md`：Python 定向测试 5 passed、Ruff、skill validator、渲染模板 tidy/vet/test/race 和 diff check 均通过。

## 输出要求

- 状态：`approved` 或 `changes_requested`。
- 评分：0-100。
- Findings 按 critical / important / minor 排序，包含文件和可执行修正。
- 明确指出是否满足本次六项用户要求，以及是否可以进入新的人工确认门。
