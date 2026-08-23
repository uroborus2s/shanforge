# Skill 完整性 P0 实施计划

**目标：** 用最小根因修复按顺序关闭五类已确认的 Skill 完整性缺口。

**架构：** 继续以 `skills/*/SKILL.md`、目标项目 `doc-map.md` 和现有 Markdown/JSON 事实为源；只复用 Python 标准库、pytest 和现有脚本，不增加目录注册表或平台层。

**工作项：** `SKILL-COMPLETENESS-P0-001`

**状态：** `completed`

## 顺序任务

1. 修正 `sync-codex-skills` 的发现条件，并以临时目录回归空目录误发现。
2. 修正正式文档解析语义：已有登记先回源 `doc-map.md`，四模块布局只作新项目回退。
3. 修正美术候选资源跨会话生命周期，区分 `candidates/` 与可再生 `tmp/`。
4. 收口正式设计、默认配置与当前 Skill 文件系统事实，保留历史快照不变。
5. 补齐最小不变量守卫，运行完整验证、评审并精确提交本工作项。

## 允许修改

- `scripts/sync-codex-skills`
- `skills/brainstorming/SKILL.md`
- `skills/requirements-engineering/SKILL.md`
- `skills/document-templates/**`（仅在并发工作项完成且重新读取后）
- `skills/art-asset-pipeline/SKILL.md`
- `config/software-factory.defaults.json`
- `.factory/project.json`
- `docs/05-design/workflow-execution-design.md`
- 与上述合同直接对应的 `tests/**`
- `.factory/workitems/SKILL-COMPLETENESS-P0-001/**`
- 批次结束时必要的 `.factory/memory/**`

## 质量门

- 每项先有能复现缺口的失败断言，再实施最小修复。
- 定向测试通过后才进入下一项。
- 完整 pytest、Ruff、Skill validator、JSON/JSONL 和 `git diff --check` 通过。
- 只提交本工作项文件；并发工作项改动留在工作区且不纳入提交。
