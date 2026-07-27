# TASK-SKILL-001 Revision 4 验证证据

时间：2026-07-13T09:15:53+08:00

## 变更范围

- 增加 GitHub skill / 模板候选评估与明确取舍。
- 增加 Ponytail、单次调用拆分、嵌套深度、Go 式对象设计、设计模式门槛和回退/兼容扩张禁令。
- 模板从 9 个文件缩减为 6 个文件，移除一次性 logging/database 包装、`execute`、`serve` 和弱 request ID fallback。

## 新鲜验证

1. `uv run pytest tests/test_go_backend_developer_skill.py`
   - 结果：`5 passed`。
2. `uv run ruff check tests/test_go_backend_developer_skill.py`
   - 结果：`All checks passed!`。
3. `python3 skills/skill-creator/scripts/quick_validate.py skills/go-backend-developer`
   - 结果：`Skill is valid!`。
4. 渲染 `assets/service-template/` 到 `/tmp/go-backend-skill-template.H9WmQY`，固定 Go `1.26.1`、Gin `v1.12.0`、Consul API `v1.34.4`、Logrus `v1.9.4`、GORM `v1.31.2`、PostgreSQL driver `v1.6.0`。
5. 在渲染目录执行 `go mod tidy && go vet ./... && go test ./... && go test -race ./...`。
   - 结果：命令退出码 `0`。
6. `git diff --check -- skills/go-backend-developer tests/test_go_backend_developer_skill.py .factory/workitems/GO-BACKEND-SKILL-001/ledger.jsonl`
   - 结果：退出码 `0`。

## 边界

- 以上证据只覆盖 revision 4 当前候选，不复用 revision 3 的人工确认状态。
- 尚未取得本轮独立 reviewer 结论与新的人工确认，不得提交。
