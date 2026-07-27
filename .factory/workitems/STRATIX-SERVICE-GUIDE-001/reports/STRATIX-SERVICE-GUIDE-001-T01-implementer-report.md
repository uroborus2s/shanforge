# Implementer Report

- work_item：`STRATIX-SERVICE-GUIDE-001`
- task：`STRATIX-SERVICE-GUIDE-001-T01`
- 状态：`approved_ready_for_local_commit`

## 根因

旧 skill 以历史工具链发布冒烟和推测性 scaffold 为主，没有从当前应用生成模板、环境 API、模块生成器、`BaseRepository` 类型和完整开发指南串起业务实现，具体造成：

- 使用已移除的配置字段。
- 把 Forge 已拒绝的命令行 key 参数写成推荐用法。
- 保留 Core/Forge key 解析不一致的过期结论。
- Repository 示例没有遵守 `query()` 返回 `Either` 的契约。
- 没有说明 `module.yaml` 的治理边界和测试读取 API。

## 回源

- `/Users/uroborus/NodeProject/wps/obsync-root/AGENTS.md`
- create/forge 的配置与资源模板
- Core 环境、加密、bootstrap、配置类型
- Database `BaseRepository`
- Testing `createModuleFixture`
- 应用后端开发指南中的架构、数据库 CRUD、模块化和测试章节

## 实现

- 重写主 skill，使应用代码任务强制加载 source-backed application reference。
- 新增 `references/application-development.md`，包含当前配置模板、环境读取边界、模块 manifest 和 API → Kysely 完整代码链。
- 修正环境和 CLI：key 只从环境读取，支持 raw/hex/base64，拒绝命令行 key 参数。
- 压缩旧 scaffold/CLI 历史叙事，移除相互冲突的模板。
- 更新 runtime、source navigation、OpenAI metadata 和回归测试。

## 未修改

- 未修改 Stratix 框架仓库。
- 未修改 `ecosystem-map.md` 和历史报告；当前入口明确禁止继承历史报告结论。
- 未触碰工作区其他任务改动。

## 评审与验证

- 前向测试发现的 `isTest()`、MySQL 模板、模块命名、Repository 占位和 fixture/doctor 边界偏差已全部修正。
- 独立评审：`approved / 98 / C0-I0-M0`。
- 回归：`19 passed`；Ruff、skill validator、TypeScript syntax/type contract 和 diff check 全部通过。
