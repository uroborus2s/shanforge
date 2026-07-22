# 运维手册

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `OPS-RUNBOOK-001` |
| 正式版本 | `v3.1.0` |
| 来源候选 | `TASK-DELIVERY-001-R001` |
| 发布事务 | `DELIVERY-RELEASE-TX-R001-G001` |
| 负责人 | `HUMAN_RELEASE_OPERATIONS_LEAD` |
| 修改 / 审核 / 批准 | `AI_EXECUTOR` / 独立 Reviewer / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | 部署手册、系统架构、R002 发布说明 |
| 下游 | 巡检 evidence、故障流程、后续环境运维计划 |

## 1. 运行边界

当前没有持续运行的生产服务、线上监控或值班告警系统。运维对象是本地 Python 平台工作区、composition 能力、测试/验证链和正式发布证据。任何 staging/production 运维结论都必须等待独立部署事务和真实环境回执。

## 2. 例行巡检

每次重要变更后执行：

```bash
UV_CACHE_DIR=/tmp/shanforge-uv-cache uv run pytest -q
UV_CACHE_DIR=/tmp/shanforge-uv-cache uv run ruff check src tests
UV_CACHE_DIR=/tmp/shanforge-uv-cache uv run ruff format --check src tests
UV_CACHE_DIR=/tmp/shanforge-uv-cache uv run mypy src
uv lock --check
git diff --check
test ! -d src/runtime/skills
test ! -d src/settings/skills
```

同时核对：

- `ProjectStatusService`、`ProjectProgressReducer/v2` 和 `ProjectStatusResponse/v4` 各只有一份装配。
- 主动查询、会话恢复、节点完成三个入口使用同一 fixed-H service。
- exact-context permission 不改变全局路线分母，不泄漏未授权 task、路径、风险或审批。
- durable regression 只有在 transfer/readback/qualification 全部成立时显示“已派发”。
- `skills/*/SKILL.md` 仍是唯一 Skill 资产，38 个顶层 Skill 结构验证通过。

## 3. 状态能力故障分流

| 现象 | 先查 | 处理 |
|---|---|---|
| N/M、任务或节点不一致 | lifecycle binding、snapshot H、position adapter | 停止推进 Gate，重放目标测试并核对唯一 reducer |
| 十五行缺失/重复 | renderer registry、consumer、authorization view | 保留输出和权限摘要，运行 response/integration 回归 |
| 错误显示“已派发” | regression request、outbox、parent Gate、qualification receipt | 阻止后台状态传播，运行 durable dispatch 攻击夹具 |
| 权限字段泄漏 | project/H/authorization digest、permission store | 视为高优先级安全缺陷，冻结发布范围并执行 exact-context 攻击 |
| evidence 推进错误 Gate | parent/gate/artifact/test plan/generation CAS | 停止 Gate，保留 observation，运行 evidence 回归 |
| 大项目查询变慢 | rows/bytes/elapsed/direct-read 指标 | 运行 10k/100k fixture，禁止引入 event-log 全扫 |
| import 或装配失败 | 五层依赖、consumer-owned port、composition root | 运行 boundary/container tests，不新增第二 DI 内核 |

## 4. 数据与持久化

R002 的默认本地装配使用内存项目事实；durable regression 测试使用受控 SQLite fixture。生产数据库、备份、灾备、数据保留和迁移策略尚未资格化。不得把测试 SQLite 文件当成生产存储，也不得把 memory summary 当成权威 event log。

## 5. 安全和权限

- permission source 必须绑定 project、H 和 authorization digest；重复或冲突 exact key 失败关闭。
- access 层不得直接读取 settings store。
- 未授权字段在结构化响应和十五行文本中都不得出现。
- 正式 docs、Git、远端、部署、凭证和生产动作分别授权；一个动作的批准不能迁移到另一个动作。
- 故障记录不得包含密钥、生产数据原文或未脱敏身份信息。

## 6. 恢复与升级

1. 先确认当前 formal manifest、released event、work item ledger 和目标文件 hash。
2. 复现并定位根因；验证失败、环境失败和权限拒绝分别处理。
3. 用新 TaskCard/候选修订完成 TDD、作者验证和独立 Review。
4. 需要正式变更时绑定精确候选 hash 请求人类批准；正式发布事务单独授权。
5. 发布后重新运行全量门并同步 ledger/memory。
6. 旧候选、旧 Review 和旧人工决定不迁移到新 hash。

## 7. 升级条件

进入 staging 或 production 前至少补齐：可运行 server adapter、认证/授权集成、生产持久化、配置/密钥管理、健康检查、可观察性、容量和 SLO、备份恢复、制品/commit 身份、回滚演练、环境专用验证与人工授权。

## 8. 升级联系人与责任

| 范围 | 责任 |
|---|---|
| 产品范围和剩余 108 项优先级 | 人类项目负责人 |
| 五层实现和测试 | 开发执行者 |
| 独立质量结论 | 未参与实现的 Reviewer |
| 正式发布、Git、远端和部署 | 对应人工授权人和发布/运维负责人 |
| 事故证据与恢复 | 运维负责人；涉及产品取舍时升级给项目负责人 |

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v3.0.0` | 2026-07-18 | 基于 R019 正式落档旧共享脚本运维说明 | `uroborus` | `uroborus` | `uroborus` |
| `v3.1.0` | 2026-07-20 | 校准为 R002 项目控制、本地巡检、故障分流和生产资格边界 | `AI_EXECUTOR` | 独立 Reviewer | `uroborus` |
