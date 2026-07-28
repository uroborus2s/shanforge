# SKILL-FIRST-PM-001：Skill-first PM 快照与 runtime 清理

- 阶段：`IMPLEMENTATION`
- 状态：`closed`
- 用户目标：让 `using-shanforge` 自带 PM 快照能力，先完成 ITA Club 进度查询，再删除 Shanforge `src/` 平台代码，避免外部项目依赖源码仓。

## 范围

- 在 `skills/using-shanforge/scripts/` 提供标准库实现的确定性 PM 快照脚本。
- 更新 `using-shanforge` 的 PM 状态页调用合同。
- 在 ITA Club 真实运行进度查询并回写 `WI-STATUS-002` 事实。
- 删除 Shanforge `src/` 及只服务于该运行时的测试、依赖和说明。
- 同步受影响的正式架构事实、项目记忆并执行本地中文提交。

## 边界

- `work_item_id`: `SKILL-FIRST-PM-001`
- `task_card_id`: `SKILL-FIRST-PM-001-T01`
- `current_gate`: `user_authorized_direct_execution`
- `write_policy`: `source_or_test_write`
- `allowed_paths`:
  - `skills/using-shanforge/**`
  - `skills/project-memory/**`
  - `src/**`
  - `tests/**`
  - `pyproject.toml`
  - `uv.lock`
  - `README.md`
  - `AGENTS.md`
  - `docs/**`
  - `.factory/workitems/SKILL-FIRST-PM-001/**`
  - `.factory/workitems/PM-DASHBOARD-004/**`
  - `.factory/memory/**`
  - `/Users/uroborus/NodeProject/ita-club/.factory/workitems/WI-STATUS-002/**`
  - `/Users/uroborus/NodeProject/ita-club/.factory/memory/**`
- `forbidden_actions`:
  - 修改 ITA Club 业务代码
  - 提交其他工作项的未提交改动
  - Push、PR、Merge 或部署
  - 把本机绝对路径写入可复用 skill

## 验收

1. 快照脚本从已安装 skill 目录运行，只接收目标项目根目录。
2. ITA Club 能生成并重复读取 `.factory/cache/site/current/index.html`。
3. Shanforge 不再包含 `src/`，仓内无 `PYTHONPATH=src` 或 `settings.composition.project_knowledge` 有效入口。
4. 保留的测试通过，skill 校验通过。

## 当前结论

- ITA Club 已由 `using-shanforge/scripts/project_snapshot.py` 生成并命中缓存。
- Shanforge `src/` 已删除，旧 `PM-DASHBOARD-004` runtime 实现已终止。
- 首轮、两次复审及 project-memory 增量复审 finding 已全部关闭；最终验证完成。
- 主实现提交 `ac67036`，看板验收收口提交 `4f5ed56`；未执行远端动作。
