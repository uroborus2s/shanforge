# T06 独立评审整改报告

## 结果

- 首轮：38/38，整体 `89.1 / C0-I23-M0`，23 个 Skill 归属 Important 合并为 15 个 finding。
- 整改：15/15 已按 P0 顺序完成；未新增依赖、中心注册表或仓内平台运行时。
- 复评状态：`ready_for_same_reviewer_rereview`。

## P0-A：错误成功、配置污染与进程清理

| Finding | 结果 | 行为守卫 |
|---|---|---|
| I-05 docx | 超时、非法输出或残留修订标记均非零失败 | `test_accept_changes_fails_closed_on_timeout_or_remaining_revisions` |
| I-10 pdf | bbox FAILURE 非零；图片输出目录自动创建 | `test_pdf_bounding_box_failure_is_nonzero`、`test_pdf_conversion_creates_output_directory` |
| I-13 webapp-testing | 不使用未消费 PIPE；检测早退并终止进程组 | `test_with_server_handles_high_output_and_stops_process_tree` |
| I-14 xlsx | stdlib ZIP/XML 结构校验支持真实 XLSX 并拒绝破损文件 | `test_xlsx_validator_accepts_valid_workbook_and_rejects_broken_archive` |
| I-15 xlsx | LibreOffice 使用隔离临时 profile；超时非零失败，不覆盖用户宏 | `test_xlsx_recalc_uses_isolated_profile_and_fails_on_timeout` |

## P0-B：可移植性、模板与资源完整性

| Finding | 结果 |
|---|---|
| I-01 algorithmic-art | 移除固定品牌与 Google Fonts；明确 p5.js 联网 starter 和离线内联要求 |
| I-02 brainstorming | 可视化伴侣全部资源改用 `<skill-dir>` |
| I-03/I-04 document-templates | 通用目录与技术模板去项目特化；Shanforge 拆为条件 profile；质量命令改用 `<skill-dir>` |
| I-09 pdf | `forms.md` 全部命令改用 `<skill-dir>`，补齐 `.py` |
| I-11 shadcn | 补齐 `Updating Components` 锚点及最小 smart merge 流程 |
| I-12 using-shanforge | 工具映射更新为当前协作工具，移除失效动作和全局配置修改 |

## P0-C：状态信封与 review 路由

| Finding | 结果 |
|---|---|
| I-06 | 9 个 Skill 不再返回项目级下一动作；执行/子代理/验证 Skill 不再重复项目状态信封 |
| I-07 | receiving-code-review 明确 triage 与整改两种 write policy，只有整改 TaskCard 可改源码/测试 |
| I-08 | review approved 默认 `return_to_orchestrator`；仅真实人工 Gate 进入 `pending_human_confirmation` |

## 验证

- P0 行为测试：`6 passed`。
- 受影响 Skill 回归：`70 passed`。
- 旧契约迁移复测：`65 passed`。
- 完整 pytest：`262 passed, 4 subtests passed`。
- Ruff：`All checks passed!`。
- Skill validator：`38/38`。
- `git diff --check`：通过。
- reviewer 复验发现的 memory/ledger 投影漂移已同步；精确快照 `1 passed`，同步后完整 pytest 仍为 `262 passed / 4 subtests passed`。
