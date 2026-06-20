# 数据库设计文档

**项目名称：** 山海工枢 / shanforge  
**文档状态：** `v2` 数据与持久化基线  
**负责人：** 仓库维护者  
**主要读者：** 架构 | 平台开发 | 测试 | 运维  
**上游输入：** 系统架构 | 模块边界 | 记忆系统详细设计  
**下游输出：** 存储实现 | 契约测试 | 运维说明  
**最后更新：** 2026-04-15

## 1. 文档目标

说明平台当前如何组织持久化对象、存储端口和本地实现。

文件名沿用“数据库设计”是为了兼容旧索引，但当前正式语义是：

```text
平台数据与持久化设计
```

它既包含未来可接外部数据库的设计，也包含当前已经落地的 `in-memory` / `JSONL-backed` local-first 实现。

## 2. 设计结论

当前平台不以单一数据库为中心，而是按业务资产类型拆分持久化职责：

- `session ledger`：保存会话、事件、artifact 等第一事实源。
- `evidence store`：保存从事实源投影出来的审计证据。
- `memory store`：保存长期记忆资产。
- `memory dataset store`：保存 `candidate -> decision -> record` 样本链。
- `runtime resource store`：为通用 JSONL 资源和后续扩展提供公共基础。

这些对象的 owner 分层如下：

| 层 | 责任 |
|---|---|
| `domain` | 定义会话、证据、记忆、样本等业务模型 |
| `runtime` | 定义 store/provider ports，约束查询与写入语义 |
| `settings` | 实现本地 `in-memory` / `JSONL-backed` 持久化 |
| `settings/composition` + `shanforge-di` | 通过本地业务绑定选择并装配具体实现 |

## 3. 当前持久化对象

| 对象 | 业务含义 | 当前实现 |
|---|---|---|
| `AgentSession` / `SessionEvent` | 会话和事件第一事实源 | `src/settings/session/store.py` |
| `SessionArtifact` | 会话附件和产物 | `src/settings/session/artifact_store.py` |
| `EvidenceRecord` | 事实投影，供审计与记忆蒸馏使用 | `src/settings/memory/evidence_store.py` |
| `MemoryRecord` | 长期记忆资产 | `src/settings/memory/store.py` |
| `MemoryDistillationSample` | 蒸馏样本链 | `src/settings/memory/dataset_store.py` |
| 通用 JSONL 资源 | 共享本地资源序列化基础 | `src/settings/shared/jsonl.py` |

## 4. 设计原则

### 4.1 第一事实源与派生资产分离

- `session / event / artifact` 是第一事实源。
- `evidence` 是对第一事实源的可审计投影。
- `memory` 是二级蒸馏资产，不能覆盖第一事实源。
- `dataset sample` 只服务蒸馏治理与后续学习，不替代正式记忆。

### 4.2 store 不承载业务策略

存储层只负责：

- 保存和读取结构化对象
- 维持幂等更新
- 支持按 session、scope、profile 等键查询

存储层不负责：

- 决定候选是否晋升
- 决定 recall 排序和预算
- 决定 profile、skill、rule 的装配策略

### 4.3 local-first，外部存储通过设置层扩展

当前正式基线优先保证：

- 本地可开发
- 本地可测试
- 本地可回放
- 本地可审计

因此默认实现优先选择 `in-memory` 和 `JSONL-backed`，未来外部数据库或索引系统必须通过基础设置层接入，而不是反向改写领域语义。

## 5. 当前实现模式

| 模式 | 适用场景 | 说明 |
|---|---|---|
| `in-memory` | 单测、快速开发、无持久化调试 | 容器启动快，进程退出即丢失 |
| `JSONL-backed` | 本地持久化、跨进程验证、记忆回归 | 通过 `memory_store_root` 装配 evidence/memory/dataset 文件 |
| `future-external` | 外部数据库、向量库、归档索引 | 规划中，必须经 runtime ports + settings adapters 接入 |

## 6. 一致性规则

当前持久化一致性主要依赖三类规则，而不是单机数据库事务：

- 稳定主键：evidence、candidate、memory、dataset sample 都使用稳定 ID。
- 幂等写入：同一 session repeated distill 不应重复脏写。
- 分层约束：application/domain/runtime/storage 只在各自边界内读写。

对记忆系统而言，至少必须满足：

- `EvidenceRecord` 可以从 session facts 重建。
- `MemoryRecord` 必须能追溯到 supporting refs。
- `MemoryDatasetStore` 必须保存 decision 结果，而不是只保存候选草案。

## 7. 推荐的本地目录布局

当前详细设计建议继续向下面的本地布局收敛：

```text
<memory_root>/
  profiles/
    <profile_id>/
      memory-records.jsonl
      memory-dataset.jsonl
      profile-config.json
  sessions/
    <session_id>/
      session-events.jsonl
      evidence-records.jsonl
      assembly-manifest.json
      sub-agent-digests.jsonl
  indexes/
    session-archive.sqlite
```

其中：

- `profiles/` 保存长期资产。
- `sessions/` 保存一次运行的事实和装配快照。
- `indexes/` 只负责查询优化，不替代正式事实源。

## 8. 下一步缺口

当前仍需补齐：

- `assembly store`、`digest store`、`session archive index`
- 外部数据库或更稳定本地索引实现
- profile 级分区和 explainability 查询读模型
- storage contract 的更系统化测试矩阵

## 9. 关联文档

- [系统架构设计](./system-architecture.md)
- [基础设置层与外部资源设计](./infrastructure-layer-design.md)
- [记忆系统详细设计方案](./memory-system-detailed-design.md)
- [记忆领域接口视图](./memory-runtime-interfaces.md)
