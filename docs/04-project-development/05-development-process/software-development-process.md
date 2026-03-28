# 软件开发流程

## 1. 流程总览

当前项目内部软件开发流程按以下主线推进：

1. 调研与问题澄清
2. 需求确认与验收标准固化
3. 设计拆分与接口约束确认
4. 任务拆解与开发实施
5. 测试与验证
6. 发布与交付
7. 运维与维护
8. 复盘与演进

## 2. 当前项目的阶段落点

- 调研与问题澄清：`02-discovery/`
- 需求确认与验收标准：`03-requirements/`
- 设计与接口约束：`04-design/`
- 过程控制与执行记录：`05-development-process/`
- 测试与验证：`06-testing-verification/`
- 发布与交付：`07-release-delivery/`
- 运维与维护：`08-operations-maintenance/`
- 演进与复盘：`09-evolution/`
- 关系闭环：`10-traceability/`

## 3. 过程规则

- 需求未确认，不进入实现。
- 设计未成文，不扩边界。
- 接口未确认，不对外承诺。
- 代码、测试、文档、AI 记忆必须同步更新。
- 变更、缺陷、发布、交接都必须留下正式记录。

## 4. 变更驱动

当需求、接口、函数、部署方式发生变化时，必须回写对应正式文档，并在追踪矩阵中保留关联关系。

## 5. 当前仓库的最小闭环

1. 修改脚本或文档
2. 更新受影响的正式文档
3. 执行 `python3 -m unittest discover -s tests -p 'test_*.py'`
4. 执行 `python3 scripts/factory-docs-index-refresh --project . --name shanforge --check`
5. 如涉及历史项目迁移，再到目标项目执行迁移和校验
