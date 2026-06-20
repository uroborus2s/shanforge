# 部署与 CI/CD 设计

**项目名称：** 山海工枢 / shanforge  
**文档状态：** `v2` 运行模式与部署基线  
**负责人：** 仓库维护者  
**主要读者：** 架构 | 平台开发 | 测试 | 运维  
**上游输入：** 系统架构 | 基础设置层设计 | 技术选型  
**下游输出：** 部署手册 | 运维手册 | 发布说明  
**最后更新：** 2026-04-18

## 1. 文档目标

说明平台当前如何装配、运行、验证和回滚。

当前项目不是“必须先上云才能运行”的在线服务，而是一个以本地可开发、可测试、可审计为第一优先级的抽象 Agent 平台主仓。

## 2. 部署视图

平台部署时需要区分 3 类单位：

| 单位 | 责任 | 当前形态 |
|---|---|---|
| UI 宿主 | 人机交互或上游系统接入 | 仓外 Web、外部 CLI 前台、自动化宿主 |
| 平台运行时 | access/application/domain/runtime 五层逻辑 | 本仓 `src/` + 默认容器 |
| 设置资源 | provider、store、Hermes bridge、配置 | `src/settings/` |

正式原则：

- UI 宿主可以更换，但必须消费统一网关契约。
- 平台运行时负责稳定业务语义和执行主链。
- 设置资源决定“用什么实现”，不决定“平台怎么思考”。

## 3. 当前支持的运行模式

### 3.1 本地开发模式

默认模式面向开发和单测：

- `build_default_container()` 使用 `InMemory*Store`
- LLM 默认可使用 mock provider
- session、memory、evidence 生命周期跟随进程

适合：

- 用例开发
- 契约测试
- 分层边界验证

### 3.2 本地持久化模式

当 `memory_store_root` 被配置后，默认容器切换到 `JSONL-backed` evidence/memory/dataset store：

- 保留 local-first
- 支持跨进程回放
- 支持记忆和蒸馏回归验证

这是当前最重要的可持续运行模式。

### 3.3 Hermes 增强模式

当设置中开启 Hermes bridge 且指定 adapter 集合时，可切换部分基础设置实现：

- `capability_registry`
- `approval`
- `delegation`

正式约束：

- Hermes 只允许在基础设置层实现区被复用。
- Hermes 不能反向主导 `application / domain / runtime` 的边界。

### 3.4 未来托管模式

后续可演进到：

- 外部数据库或索引服务
- hosted API gateway
- 外部 approval/delegation backend
- 更完整的 Web console

但这些都必须建立在当前六层架构和 provider port 基线之上。

## 4. 装配入口

当前默认装配入口是：

- `src/settings/composition/settings.py`
- `src/settings/composition/container.py`
- `src/settings/composition/component_bindings.py`
- sibling `shanforge-di`

装配时至少要完成：

1. 读取 settings
2. 通过本地业务绑定 + `shanforge-di` 选择 store/provider/backend 实现
3. 绑定 `runtime ports`
4. 组装 application/domain/runtime 服务图
5. 暴露 API/CLI 等 access 入口

## 5. 部署门禁

任何影响平台运行模式的变更，至少需要覆盖：

- 分层契约检查：接口 owner 和依赖方向是否仍正确
- 单元测试：domain/runtime/storage 的核心行为
- 集成测试：默认容器是否还能跑通主执行链
- 文档同步：`04-design`、`06-testing-verification`、`.factory/memory` 是否已同步

当前最关键的验证对象包括：

- `tests/test_application_execution.py`
- `tests/test_context_engine.py`
- `tests/test_domain_services.py`
- `tests/test_runtime_memory_summarizer.py`
- `tests/test_settings_memory_stores.py`
- `tests/test_platform_scaffold.py`
- `tests/test_infrastructure_scaffold.py`

## 6. 发布与回滚

当前发布以 Git 版本为主，回滚路径也以 Git 为主：

1. 回退对应代码与配置变更
2. 重新装配默认容器
3. 重跑关键测试
4. 验证 access 入口、session、memory、provider 绑定恢复正常

若问题来自基础设置层：

- 优先切回 `in-memory` 或 `JSONL-backed` 保守实现
- 再定位具体 adapter / provider / backend

## 7. 环境矩阵

| 模式 | UI 宿主 | 持久化 | Provider | 适用阶段 |
|---|---|---|---|---|
| `dev-local` | CLI / API 调试 | `in-memory` | mock / local | 开发、单测 |
| `local-persistent` | CLI / API / automation | `JSONL-backed` | mock / real provider | 联调、回归 |
| `hybrid-hermes` | CLI / API / automation | local store + Hermes-backed adapter | Hermes bridge + real provider | 能力增强验证 |
| `future-hosted` | Web + API | external DB / index | hosted providers | 后续演进 |

## 8. 关联文档

- [基础设置层与外部资源设计](./infrastructure-layer-design.md)
- [后端设计文档](./backend-design.md)
- [测试计划](../06-testing-verification/test-plan.md)
- [部署手册](../08-operations-maintenance/deployment-guide.md)
