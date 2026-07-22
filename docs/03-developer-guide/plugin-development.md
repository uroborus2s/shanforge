# 插件开发

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DOC-PLUGIN-DEVELOPMENT-001` |
| 正式版本 | `v1.0.0` |
| 来源候选 | `TASK-DESIGN-001-R019` |
| 发布事务 | `DESIGN-RELEASE-TX-R019-G001` |
| 负责人 | `HUMAN_DEVELOPMENT_EXECUTOR` |
| 修改 / 审核 / 批准 | `uroborus` / `uroborus` / `uroborus` |
| 状态 | 已批准并生效 |
| 上游 | `application-development`、`interface-reference` |
| 下游 | `plugin implementation` |

## 文档职责

- 允许保存：插件入口；生命周期；打包验证；兼容边界。
- 禁止保存：业务项目私有方案；临时安装结果。
- 主要读者：插件作者、扩展开发者。

## 正式内容

## 1. 适用范围

本页面向需要扩展软件工厂能力的开发者，重点关注插件、扩展点和新增协作能力的接入。

## 2. 插件开发关注点

- 插件解决什么问题
- 暴露什么扩展点
- 与现有 `skills/`、`scripts/`、`docs/` 如何配合
- 对使用者和维护者分别新增哪些文档义务

## 3. 文档要求

插件一旦成为稳定能力，至少补齐：

- 使用场景
- 接入步骤
- 配置项
- 兼容策略
- Hook、函数或接口说明

## 正式版本历史（仅已发布）

| 版本 | 日期 | 变更 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `v1.0.0` | 2026-07-18 | 基于 `TASK-DESIGN-001-R019` 正式落档 | `uroborus` | `uroborus` | `uroborus` |
