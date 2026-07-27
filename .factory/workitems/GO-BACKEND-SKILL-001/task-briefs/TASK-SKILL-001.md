# TASK-SKILL-001：创建 Go 后端开发 skill

## 目标

创建 `go-backend-developer`，为 Gin、GORM、Logrus、Consul 技术栈提供可执行的开发、评审和验证规则，并提供最小代码模板。

## 用户指定基线

- HTTP：Gin。
- ORM：GORM。
- 日志：Logrus。
- 配置中心：Consul。
- 调研 GitHub 上成熟可靠的 Go skill，核对后再本地化。

## 新增能力清单

- 精确触发和与其他技术栈的边界。
- 新建、实现、重构、Bug 修复和 Review 阶段约束。
- Gin/GORM/Logrus/Consul 组合契约。
- 物理数据库独立选型规则。
- Consul bootstrap、ACL、配置校验和 last-known-good 规则。
- Logrus maintenance mode 风险声明。
- 可渲染的最小服务模板。
- 定向结构测试和真实 Go 编译验证。

## 写集

- `skills/go-backend-developer/**`
- `tests/test_go_backend_developer_skill.py`
- `.factory/workitems/GO-BACKEND-SKILL-001/**`
- `.factory/memory/skill-updates.summary.md` 的当前任务单独 hunk（通过 review 后）

## 禁止

- 不修改 Shanforge 本体 Python 技术基线。
- 不改动当前 `FLOW-CONTRACT-001` 候选或正式设计。
- 不覆盖工作区已有未提交改动。
- 作者不得自批 `approved`。

## 验收

- skill quick validation 通过。
- 定向 pytest 和 Ruff 通过。
- 模板渲染后 `go test ./...`、`go vet ./...` 通过。
- 独立 reviewer 给出结论。
