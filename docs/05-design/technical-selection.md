# 技术选型与工程规则

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DESIGN-TECH-001` |
| 正式版本 | `v4.0.0` |
| 状态 | 已批准并生效 |
| 负责人 | `HUMAN_ARCHITECTURE_DOMAIN_LEAD` |
| 上游 | `PRD-SHANFORGE-001`、`DESIGN-ARCH-001` |
| 下游 | skills、自带脚本、测试 |

## 文档职责

- 记录当前技能资产和确定性辅助能力的技术选择。
- 不定义独立服务、SDK、数据库或公共 HTTP 契约。

## 当前设计

| 方向 | 当前选择 | 约束 |
|---|---|---|
| 流程能力 | `SKILL.md` + 按需 references | 宿主负责加载和工具权限。 |
| 确定性辅助 | 所属 skill 的 `scripts/` | 优先标准库；参数接收目标项目根目录。 |
| 正式事实 | Markdown、JSON、JSONL | 各事实只有一个 owner。 |
| 校验 | `uv`、pytest、Git 检查 | 不为目标项目引入 Shanforge 依赖。 |
| 快照 | `project_snapshot.py` 生成静态 HTML | 只读、可删除重建。 |

仓库不含可被目标项目导入的产品 runtime。若某能力可由宿主原生工具或现有 skill 完成，不新增平台层或依赖。

## 适用验证

- `uv run pytest tests/test_lifecycle_governance.py -q`
- `git diff --check`

## 正式版本历史

| 版本 | 日期 | 变更 |
|---|---|---|
| `v4.0.0` | 2026-09-01 | 收口为 skill、文档、脚本和测试的当前技术基线。 |
| `v3.1.0` | 2026-04-15 | 历史：旧平台技术选型。 |
