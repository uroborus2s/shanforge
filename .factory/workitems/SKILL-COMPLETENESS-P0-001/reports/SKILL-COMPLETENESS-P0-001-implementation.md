# P0 实现摘要

- `P0-1`：`sync-codex-skills` 只发现含 `SKILL.md` 的一级目录；未新增注册表。
- `P0-2`：`brainstorming`、`requirements-engineering`、`document-templates` 优先解析目标项目登记路径，四模块只作新项目回退。
- `P0-3`：美术候选图跨会话保存在 `candidates/`，`tmp/` 只放可再生中间物，批准后清理未选候选。
- `P0-4`：能力清单以 `skills/*/SKILL.md` 为唯一事实；正式设计、默认配置和项目角色文档路由完成收口。
- `P0-5`：移除 32 个工作 Skill 的整文件 SHA 快照，新增发现、路径、生命周期和正式事实不变量测试。

实现遵守 skill-first 边界：没有新增平台运行时、依赖、目录注册表或中心校验服务。
