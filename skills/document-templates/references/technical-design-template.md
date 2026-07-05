# 技术方案模板

用于已批准需求进入实现前的轻量技术设计。小任务可以用本模板生成 work item 级设计，不必创建长文档。

## 背景

- Work item：
- 需求来源：
- 当前阶段：
- 相关 memory：
- 相关正式文档：

## 目标

说明本次改动要达成什么。

## 非目标

说明本次明确不做什么。

## 分层和接口边界

- 所属层：
- 所属领域：
- 接口 owner：
- 下游依赖：
- 禁止耦合：

必须遵守：

- `access -> application -> domain -> runtime -> settings`
- 不得引入新的中心脚本主控。
- 不得新增顶层 `src/adapters`、`src/storage`、`src/bootstrap`。
- 不得让业务层直接依赖 `settings` 具体实现。

## 影响文件

```text
代码：
测试：
文档：
.factory/memory/：
```

## 数据流

说明请求、领域对象、provider/store、证据和输出如何流动。

## 错误处理

- 输入错误：
- 依赖错误：
- 权限或审批错误：
- 可恢复失败：

## 测试策略

- Red 测试：
- Green 验证：
- 回归范围：
- 不运行项及原因：

## Review Gate

- Spec review：
- Quality review：
- verification：
- memory sync：
- PR / commit 状态：

## 状态

`draft | ready_for_review | approved`

实现者只能把设计或实现推进到 `ready_for_review`。`approved` 必须来自独立 review。
