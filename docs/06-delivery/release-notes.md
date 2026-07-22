# 发布说明

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `RELEASE-NOTES-001` |
| 正式版本 | `v3.1.0` |
| 来源候选 | `TASK-DELIVERY-001-R001` |
| 发布事务 | `DELIVERY-RELEASE-TX-R001-G001` |
| 负责人 | `HUMAN_RELEASE_OPERATIONS_LEAD` |
| 修改 / 审核 / 批准 | `AI_EXECUTOR` / 独立 Reviewer / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | R002 released event、发布后验证、需求追踪 |
| 下游 | 用户、维护者、部署和运维交接 |

## 1. 发布结论

`TASK-IMPLEMENT-001-R002` 已通过本地事务 `IMPLEMENTATION-RELEASE-TX-R002-G001` 正式激活。该增量交付项目控制、执行位置、真实停止原因、严格十五行回复、evidence/Gate CAS、快速验证与 durable regression、写入 provenance 和五层集成。

本轮是本地产品实现发布，不是远端版本、制品库或生产部署。正式需求总数为 123；本轮有产品代码与测试追踪的需求为 15，剩余 108 项仍需后续实施。

## 2. 已发布能力

- 唯一 `LifecyclePlanBinding/v1` 和同一 fixed-H 项目位置。
- `ProjectProgressSnapshot/v2` → `ProjectExecutionPosition/v1` 的唯一 reducer/adapter 链。
- 七种互斥 `execution_disposition`、六类人工 Gate 和准确责任人。
- `ProjectStatusResponse/v4` 严格十五行 renderer，供主动查询、会话恢复和节点完成三个入口共同使用。
- exact-context permission、未登记 evidence observation 和五字段 Gate CAS。
- 60 秒 quick verification 预算与 durable regression transfer/readback/qualification。
- `ArtifactWriteAttestation/v1`、phase manifest、receipt 和 replay/drift 防护。
- 10,000 task / 100,000 event 性能夹具和无额外全库扫描证明。

## 3. 需求覆盖

| 范围 | 数量 | 状态 |
|---|---:|---|
| `REQ-ASYNC-015..016` | 2 | R002 已实现 |
| `REQ-VIS-001..009` | 9 | R002 已实现 |
| `NFR-VIS-001..004` | 4 | R002 已实现 |
| 其他正式需求 | 108 | 本轮未新增产品代码实现 |

`REQ-CHANGE-AI-EXEC-VISIBILITY-001` 是变更容器，不重复计入 15 项。

## 4. 质量结果

发布后证据记录：pytest 832/832；failed/skipped/not_run 为 0/0/0；Ruff 0；format 299/299；mypy 0/236；顶层 Skill 38/38；候选攻击 17/17；正式发布事务攻击 8/8；lock、diff 和 runtime Skill 目录边界通过。

权威证据：`.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-IMPLEMENT-001-R002-post-release-verification.md`。这是一份发布时点证据，不替代后续变更的新鲜验证。

## 5. 兼容、迁移和限制

- 保持五层依赖 `access -> application -> domain -> runtime -> settings`，未增加第六层或仓内 DI 内核。
- 项目状态入口是 framework-agnostic route 声明；仓库不包含可直接对外运行的完整 Web 服务。
- composition 默认仍使用本地/内存项目事实；生产持久化、认证、部署拓扑和线上监控不在 R002 范围。
- 顶层 `skills/*/SKILL.md` 是唯一 Skill 资产；`src/runtime/skills` 与 `src/settings/skills` 已撤销并保持不存在。
- 使用方需要从旧九行状态解析迁移到 `ProjectStatusResponse/v4` 十五行合同，不提供第二 renderer 兼容层。

## 6. 回滚入口

R002 采用冻结候选原地激活，正式事务没有重写 665 个候选文件字节。若后续发现阻断缺陷，应先停止扩大使用范围，保留 manifest、released event 和证据，再通过新的受控修复/发布事务恢复；不得用未审计的文件覆盖或破坏性 Git 命令冒充回滚。

本仓当前没有已执行的远端发布或生产部署，因此不存在可宣称已演练的远端/生产回滚。

## 7. 当前交付状态

- 本地正式实现：已激活并通过发布后验证。
- 正式交付文档：由本版本记录。
- Git commit / push / PR / merge：未执行。
- 远端 release / 制品上传：未执行。
- staging / production 部署：未执行。
- 产品整体需求：仍有 108 项未实现，不进入项目整体完成状态。

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v3.0.0` | 2026-07-18 | 基于 R019 正式落档设计期发布说明 | `uroborus` | `uroborus` | `uroborus` |
| `v3.1.0` | 2026-07-20 | 发布 R002 项目控制实现增量、15/123 覆盖和交付边界 | `AI_EXECUTOR` | 独立 Reviewer | `uroborus` |
