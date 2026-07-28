# 系统架构设计

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DESIGN-ARCH-001` |
| 正式版本 | `v4.0.0` |
| 来源候选 | `SKILL-FIRST-PM-001` |
| 发布事务 | `N/A：用户直接批准 skill-first 边界收口` |
| 负责人 | `HUMAN_ARCHITECTURE_DOMAIN_LEAD` |
| 修改 / 审核 / 批准 | `uroborus` / `uroborus` / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | `project-overview`、`用户指南` |
| 下游 | `using-shanforge`、专项 skills、项目记忆 |

## 1. 架构结论

Shanforge 是运行在各类代理宿主中的 `skill-first` 软件工厂资产，
不是 Agent 平台运行时、Python SDK 或独立服务。

```text
用户自然语言
  → 代理宿主加载 using-shanforge
  → using-shanforge 选择一个专项 skill
  → 专项 skill 使用宿主工具修改目标项目
  → 目标项目保存 docs / code / tests / .factory facts
```

仓库不提供 `src/`。目标项目不得导入 Shanforge 模块、复用 Shanforge 虚拟环境，或
依赖本机上的 Shanforge 源码绝对路径。

## 2. 交付单元

| 目录 | 职责 |
|---|---|
| `skills/` | 流程规则、专项方法、按需 references 与自带确定性 scripts |
| `docs/` | Shanforge 自身的正式产品、使用和维护事实 |
| `.factory/` | Shanforge 自身的 work item、ledger、evidence 和压缩记忆 |
| `scripts/` | skill 同步等仓库级辅助动作，不承载流程主控 |
| `tests/` | skills、规则合同和自带脚本的回归检查 |

## 3. Skill 边界

- `SKILL.md` 负责触发条件、判断规则和工作流。
- `references/` 保存只在特定场景读取的详细合同。
- `scripts/` 保存需要确定性、可重复执行的最小代码。
- 脚本优先使用标准库，不在目标项目安装 Shanforge 依赖。
- 脚本从参数接收目标项目根目录，不猜测或硬编码仓库位置。
- skill 同步时整个目录作为一个单元安装，脚本随 skill 一起可用。

## 4. 项目事实边界

每个目标项目拥有自己的：

- `AGENTS.md` / `GEMINI.md` 等宿主规则。
- `docs/` 正式事实。
- `.factory/workitems/` 执行事实。
- `.factory/memory/` 恢复摘要。
- 源码、测试、构建与发布配置。

Shanforge skill 只能在用户授权范围内读取或修改这些文件。任何缓存、HTML 或索引都是
可重建投影，不能覆盖正式文档和 ledger。

项目会话固定先分类、再按需恢复：

```text
classifying → restoring_if_projectized → routing → scoping → executing → verifying
```

| 角色 | 职责 |
|---|---|
| 项目负责人 | 决定产品边界、风险接受和不可逆业务选择 |
| 代理宿主 | 加载 skill、提供工具、权限和执行环境 |
| Shanforge skill | 约束流程、读取范围、证据和 Gate |

## 5. PM 快照

PM 快照属于 `using-shanforge` 自带能力：

```text
skills/using-shanforge/scripts/project_snapshot.py
```

它读取目标项目的 `.factory` 登记事实，写入
`.factory/cache/site/current/index.html`，并返回
`SkillProjectSnapshotReceipt/v1`。输入未变化时复用缓存。

快照不提供编辑、审批、提交或发布入口；工作项数量不等于产品功能完成率。

## 6. 安全与失败

- 目标项目根目录不存在或没有 `.factory/` 时失败。
- 非法 JSON/JSONL 失败关闭，不静默猜测状态。
- `--relative-paths` 只改变 receipt 路径格式，不代表页面内容已脱敏。
- 不读取目标项目秘密、未登记外部系统或 Shanforge 源码。
- 破坏性、远端、部署或凭证动作继续服从宿主审批和项目 Gate。

## 7. 历史架构处置

`v3.x` 及更早版本描述的 `access -> application -> domain -> runtime -> settings`
Python 平台、DI 容器、SQLite 项目知识服务和公共 API 均已废止。对应源码和专属测试
已删除；旧设计只保留在 Git 历史，不得作为当前实现入口。

## 正式版本历史

| 版本 | 日期 | 变更 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v4.0.0` | 2026-07-28 | 收口为 skill-first 架构并废止 Python 平台 runtime | `uroborus` | `uroborus` | `uroborus` |
| `v3.1.0` | 2026-07-18 | 发布旧 Python 平台架构 | `uroborus` | `uroborus` | `uroborus` |
