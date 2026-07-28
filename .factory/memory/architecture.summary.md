# 架构摘要

- 更新时间：2026-07-28
- 当前架构：`skill-first`
- 正式 owner：`docs/05-design/system-architecture.md` `v4.0.0`

## 当前事实

- Shanforge 是面向代理宿主的 skills、文档模板、项目规则和记忆体系。
- 仓库不提供 `src/` Python 平台 runtime、SDK、公共 API 或独立 CLI。
- `SKILL.md` 定义触发和流程；`references/` 保存按需合同；确定性辅助能力随所属
  skill 放在 `scripts/`。
- 目标项目拥有自己的源码、文档和 `.factory` 事实，不依赖 Shanforge 源码路径、
  虚拟环境或本机绝对路径。
- PM 快照由 `skills/using-shanforge/scripts/project_snapshot.py` 生成，输入是目标项目
  `.factory`，输出是可删除重建的 `.factory/cache/site/current/`。
- 仓库根 `scripts/` 只承担 skill 同步，不承载软件工厂流程主控。
- `v3.x` 的 `access -> application -> domain -> runtime -> settings` 分层及其平台代码
  已废止，只可从 Git 历史追溯。

## 当前约束

- 可重复脚本优先使用标准库。
- skill 不硬编码 Shanforge 仓库、目标项目或用户主目录绝对路径。
- HTML、索引和缓存不是正式事实。
- 破坏性、远端、部署与凭证动作仍需明确授权。
