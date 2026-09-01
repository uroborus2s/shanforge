# 接口与事件设计

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DESIGN-API-001` |
| 正式版本 | `v4.0.0` |
| 状态 | 已批准并生效 |
| 负责人 | `HUMAN_API_INTEGRATION_LEAD` |
| 上游 | `DESIGN-ARCH-001`、`PRD-SHANFORGE-001` |
| 下游 | 接口参考、接口矩阵、测试 |

## 文档职责

- 描述当前宿主与 skill 之间的文件和状态包契约。
- 不声明 HTTP runtime、端点、OpenAPI 或 SDK。

## 当前设计

共享会话契约顺序为 `classifying → restoring_if_projectized → routing → scoping → executing → verifying`：先只依据当前消息分类；只有项目化请求才恢复项目事实，再路由和界定范围。`direct_answer` 与 `lightweight_analysis` 不读取 `.factory/memory/`。

| 契约 | owner | 最小内容 | 验证 |
|---|---|---|---|
| Skill 输入输出 | 对应 `SKILL.md` | 触发、输入、动作、状态、outputs、evidence、needs | 定向 skill 测试。 |
| Route/status 包 | `using-shanforge` | 身份、范围、Gate、模型路由与人类可读状态 | 控制面测试。 |
| WorkItem / TaskCard / ledger | `.factory/workitems/` | 任务身份、允许范围、证据、Gate、追加事件 | 结构和生命周期测试。 |
| Subagent receipt | 代理宿主 | 派发模型、强度、任务和工具回执 | 路由与派发测试。 |
| Snapshot receipt | `project_snapshot.py` | 输入指纹、输出路径和缓存复用信息 | 快照脚本测试。 |

契约由文件内容和宿主工具实现；没有网络监听、请求状态码或服务兼容层。契约变更须同步所属 `SKILL.md`、相关正式设计和定向测试。

## 适用验证

- `uv run pytest tests/test_lifecycle_governance.py -q`
- 受影响 skill 或快照脚本的定向 pytest。

## 正式版本历史

| 版本 | 日期 | 变更 |
|---|---|---|
| `v4.0.0` | 2026-09-01 | 以当前文件与宿主契约取代旧服务接口设计。 |
| `v3.1.0` | 2026-07-23 | 历史：旧平台接口与事件设计。 |
