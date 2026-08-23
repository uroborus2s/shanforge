# Completion Evidence

## 基本信息

- Work item：`SKILL-COMPLETENESS-P0-001`
- Actor：`AI_EXECUTOR`
- 时间：`2026-08-23T21:32:26+08:00`
- 验证声明：五项 P0 根因修复和回归守卫已实现，当前混合工作树通过完整测试与静态门。
- 结论：`passed`

## Red-Green

| P0 | Red | Green |
|---|---|---|
| Skill 发现 | 空 `references/` 被计划同步，断言失败且显示 `linked=2` | 只同步含 `SKILL.md` 的目录，真实仓 dry-run 为 `linked=38` |
| 正式文档解析 | 工作 Skill 仍含 `docs/04-project-development/`，模板缺少已有登记优先语义 | 三个入口统一 `doc-map.md` 回源，新项目才回退四模块 |
| 美术候选生命周期 | 等待选择时删除 `tmp/` 中非确定性候选，跨会话无法继续 | 候选进入 `candidates/`，选择后清理未选图，最终包排除工作目录 |
| 能力与正式事实 | 设计冻结 `37` 个 Skill，工作流仍引用已撤销运行时，项目文档路由不存在 | 文件系统动态发现；运行时旧落点删除；配置和角色文档路由均存在 |
| 行为守卫 | 修改专业 Skill 会触发整文件 SHA 失败 | 删除 SHA 快照，改查唯一 frontmatter、专业正文和共享合同不变量 |

## 新鲜验证

- `UV_CACHE_DIR=/private/tmp/shanforge-audit-uv-cache uv run pytest -q -p no:cacheprovider`
  - exit code：`0`
  - 结果：`242 passed, 4 subtests passed in 1.09s`
  - failed / error / skipped / not_run：`0 / 0 / 0 / 0`
- `UV_CACHE_DIR=/private/tmp/shanforge-audit-uv-cache uv run ruff check .`
  - exit code：`0`
  - 结果：`All checks passed!`
- `uv run python .../skill-creator/scripts/quick_validate.py <skill>`
  - exit code：`0`
  - 结果：`art-asset-pipeline`、`brainstorming`、`document-templates`、`requirements-engineering` 均为 `Skill is valid!`
- `PYTHONPYCACHEPREFIX=/private/tmp/shanforge-p0-pycache python3 -m py_compile scripts/sync-codex-skills`
  - exit code：`0`
- Python 标准库读取 `config/software-factory.defaults.json`、`.factory/project.json`
  - exit code：`0`
  - 结果：`json ok`
- `git diff --check`
  - exit code：`0`

## 偏离与边界

- 裸 Python 执行系统 `quick_validate.py` 因环境缺少 `yaml` 失败；改用项目锁定的 `uv run python` 后同一校验器四项全部通过。
- `TEST-GOVERNANCE-001` 已先行提交为 `c4534ba`、`087bb64`；本工作项最终验证时 index 为空，仅保留 P0 范围工作树。
- 未执行远端、PR、merge、发布或部署。

## 提交前最终验证

- 时间：`2026-08-23T22:00:40+08:00`
- 状态投影根因：收尾同步一度让 `current-state.md` 超过“最近事实最多 5 条”并把阶段后缀误写为 phase；事实 owner 是现有 project-memory 契约。压缩重复历史并恢复 `工作项 / 活跃任务 ID` 格式后，定向测试 `1 passed`。
- 完整 pytest：`242 passed, 4 subtests passed in 1.00s`，exit code `0`。
- Ruff、四个 Skill validator、脚本编译、全量 JSON/JSONL 和 `git diff --check`：exit code `0`。
- failed / error / skipped / not_run：`0 / 0 / 0 / 0`。
