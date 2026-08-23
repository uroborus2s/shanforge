# T05/T06 批次验证证据

## 验证对象

- 候选：当前工作区中 `SKILL-FULL-OPTIMIZATION-001` 的 13 个 Skill 修改、3 个既有合同测试修改、1 个新增动态合同测试及 WorkItem 文件。
- 并发排除：`TEST-GOVERNANCE-CLOSURE-001` 及其 document-templates、verification、正式测试文档和测试改动不属于本工作项。

## 首个完整候选

| 检查 | 结果 |
|---|---|
| 38 个 `quick_validate.py` | passed，38/38 |
| `uv run ruff check .` | passed |
| JSON / JSONL 解析 | passed，179 JSON / 44 JSONL |
| Skill Python 脚本语法 | passed，45 个 `.py` |
| 38 个 `SKILL.md` 本地链接 | passed，98/98 可达 |
| `uv run pytest -q -p no:cacheprovider` | failed，`247 passed / 1 failed / 4 subtests passed` |
| 排除并发测试治理文件的回归 | passed，`233 passed / 4 subtests passed` |

唯一失败是并发工作项 `tests/test_project_test_governance.py::test_test_governance_revision_is_formally_published`：测试要求正式版本 `v3.2.0`，当时 `docs/06-delivery/test-plan.md` 仍为 `v3.1.0` 候选。未修改该工作项文件。

## 最终候选

为隔离并发未完成改动，从 `HEAD` 创建临时 Git 候选，只应用本工作项 13 个 Skill、3 个既有测试和 1 个新增测试的精确 diff：

| 检查 | 结果 |
|---|---|
| 隔离候选完整 pytest | passed，`245 passed / 4 subtests passed` |
| 隔离候选 Ruff | passed |
| 隔离候选 38 个 validator | passed，38/38 |
| 当前工作区排除并发治理测试文件的回归 | passed，`233 passed / 4 subtests passed` |
| 当前工作区 JSON / JSONL | passed，179 / 44 |
| 当前工作区 Skill Python 脚本语法 | passed，45 个 `.py` |
| 当前工作区 38 个 `SKILL.md` 本地链接 | passed，98/98 |
| `git diff --check` | passed |

隔离候选第一次运行有 1 个环境型失败：`test_ui_ux_pro_max_skill.py` 调用 `git ls-files`，而 `git archive` 目录没有 `.git`；在临时目录初始化 Git 并只登记 `skills/ui-ux-pro-max` 后，同一完整命令通过。该处理只补测试所需观察环境，不修改候选内容。

## 结论

- 本工作项精确候选：完整验证通过。
- 并发 `TEST-GOVERNANCE-CLOSURE-001` 完成正式版本收口后，当前合并工作区重新运行完整 pytest 为 `249 passed / 4 subtests passed`；Ruff、38/38 validator 和 `git diff --check` 同轮通过。
- 首轮并发失败和隔离候选证据保留为诊断历史；最终当前工作区为全绿。

## T06 独立评审整改候选

首轮 reviewer 的 15 个 Important finding 按错误成功、资源可移植性、状态 owner 三批完成整改。新增行为守卫先得到预期 Red，再在最小修复后转 Green。

| 检查 | 新鲜结果 |
|---|---|
| P0 脚本失败合同 | passed，`6 passed` |
| 受影响 Skill 定向回归 | passed，`70 passed` |
| 旧契约迁移复测 | passed，`65 passed` |
| 完整 pytest | passed，`262 passed / 4 subtests passed` |
| `uv run ruff check .` | passed，`All checks passed!` |
| 38 个 `quick_validate.py` | passed，`38/38` |
| `git diff --check` | passed |

第一次 T06 完整 pytest 为 `255 passed / 7 failed / 4 subtests passed`；7 项均是现有测试仍强制工作 Skill 返回项目状态信封、通用模板硬编码 Shanforge 路径/分层等旧契约，与独立 reviewer 的 P0 finding 直接冲突。迁移这些断言后，失败文件定向复测 `65 passed`，随后完整回归全绿。

T06 候选已达到 `ready_for_same_reviewer_rereview`；实现者不自评最终分数或 C/I/M。

同 reviewer 首次复验捕获 1 个状态投影失败：WorkItem ledger 已进入 `same_reviewer_rereview_all_38_scorecards`，但 `.factory/memory/agent-session.md` 仍保留旧整改动作。同步五份当前态投影并追加 memory sync 事件后，精确快照 `1 passed`，完整 pytest 再次为 `262 passed / 4 subtests passed`。该失败作为复评前像保留，不计作成功结果。
