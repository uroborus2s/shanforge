# SKILL-FIRST-PM-001-T01 独立审查输入

## 审查目标

确认本次修改真正建立 skill-first 边界：

1. 外部项目只调用已加载 `using-shanforge` skill 自带脚本。
2. 脚本不依赖 Shanforge 源码、虚拟环境、CLI、SQLite 或第三方包。
3. 快照只读取登记事实，只写可删除缓存，重复运行可命中缓存。
4. `src/` 和只服务于旧 runtime 的测试/依赖已删除。
5. ITA Club 的 `WI-STATUS-002` 不再提出跨仓修改 Shanforge `src/`。

## 主要材料

- `.factory/workitems/SKILL-FIRST-PM-001/brief.md`
- `.factory/workitems/SKILL-FIRST-PM-001/task-briefs/SKILL-FIRST-PM-001-T01.md`
- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/pm-dashboard-rendering.md`
- `skills/using-shanforge/scripts/project_snapshot.py`
- `tests/test_using_shanforge_snapshot.py`
- `.factory/workitems/SKILL-FIRST-PM-001/evidence/SKILL-FIRST-PM-001-T01-verification.md`
- `.factory/workitems/SKILL-FIRST-PM-001/reports/SKILL-FIRST-PM-001-T01-implementer-report.md`

## 只读验证

```bash
UV_CACHE_DIR=/tmp/shanforge-uv-cache uv run pytest -q tests/test_using_shanforge_snapshot.py
test ! -d src
rg -n 'PYTHONPATH=src|settings\.composition\.project_knowledge' AGENTS.md README.md skills docs .factory/memory
```

请按 critical / important / minor 报告问题，并给出 `approved` 或 `changes_requested`。
