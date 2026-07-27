# TASK-SKILL-001 最终新鲜验证

- 时间：`2026-07-27`
- 当前名称：`go-developer`
- 结论：`passed`

## Skill 契约

```bash
uv run pytest -q tests/test_go_developer_skill.py tests/test_remaining_skill_project_status_contract.py tests/test_deprecated_skill_cleanup.py
```

- exit code：`0`
- 结果：`14 passed in 0.05s`

```bash
uv run ruff check tests/test_go_developer_skill.py tests/test_crawler4j_model_skill_integration.py tests/test_remaining_skill_project_status_contract.py tests/test_work_skill_status_envelope_ownership.py
```

- exit code：`0`
- 结果：`All checks passed!`

## 模板行为

将 `skills/go-developer/assets/service-template/` 渲染到
`/tmp/shanforge-go-skill-0eJVC3`，固定使用原批准版本：

- Go `1.26.1`
- Gin `v1.12.0`
- Consul API `v1.34.4`
- Logrus `v1.9.4`
- GORM `v1.31.2`
- PostgreSQL driver `v1.6.0`

执行：

```bash
GOWORK=off go mod tidy
gofmt -d .
GOWORK=off go vet ./...
GOWORK=off go test ./...
GOWORK=off go test -race ./...
```

- exit code：全部为 `0`
- `gofmt -d`：无差异
- 结果：通过

第一次运行因沙箱禁止访问用户级 Go build cache 而失败；随后沙箱内
`-race` 仍因 `runtime/race` 不可用失败。保持模板和命令不变，在获批的
沙箱外环境重跑 `vet / test / race` 后通过。

## 改名完整性

- `skills/go-backend-developer` 已不存在。
- `skills/go-developer` 包含 `SKILL.md`、5 份 reference 和 6 个模板文件。
- `tests/test_go_developer_skill.py` 覆盖触发边界、工程规则、Ponytail 约束、模板资源和关键行为。
- 当前名称下的验证未发现内容回归。
