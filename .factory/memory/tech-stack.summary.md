# 技术画像摘要

- 当前画像：Skill-first 软件工厂
- 预设：custom
- 技术栈：Markdown Skills / Python 3 / uv / pytest / Git
- 最近更新时间：2026-08-23

## 摘要

Shanforge 由代理宿主加载，不提供公共 API、SDK、自托管服务或仓内平台运行时。

## 项目范围

- Shanforge Skills
- 目标项目工程协作
- 宿主模型分层路由

## 模块

- `skills/`：流程和专项工程方法
- `docs/`：正式产品与技术事实
- `.factory/`：任务、ledger、evidence 与恢复摘要
- `tests/`：合同和确定性脚本回归
- `scripts/`：仓库级同步辅助

## 工程规则

- Skill、正式文档、测试与 `.factory/memory/` 必须同步。
- 目标项目不得依赖 Shanforge 源码、虚拟环境或本机绝对路径。
- 确定性能力放在所属 skill 的 `scripts/`，优先标准库。
- 远端、部署和生产动作需要单独授权。
