# TASK-DESIGN-002 R001 iteration 4 Review 整改验证

## Finding closure

| Finding | 整改 | 验证点 |
|---|---|---|
| I-001 来源贡献 | 一 concrete file 一 source；`pk_generation_source.contribution_json` 复用未变贡献；affected entity 重算 | 同实体多来源删除一源测试已进入 T02 硬门 |
| I-002 主键/field map | section 改 `section_key` + `(document_id,section_id)`；PM summary 改 `summary_id`；补全 map 结构验证 | PM map 137/137，summary PK 精确匹配 |
| I-003 frozen queue | 独立 `ProjectStateSyncQueuePort` 与 `.factory/runtime/project-state-sync.sqlite3` | 冻结 system-task 文件不在 allowlist，T05 要求 Hash 不变 |
| I-004 页面详情 | 补文档、质量、版本、报告和 PM record 详情稳定 URL | T04 全详情深链/返回测试 |
| I-005 原子站点 | immutable builds + `os.replace` current symlink | 崩溃点、并发 reader、越界 symlink 测试 |
| I-006 NFR | 补 Memory、10k、ordinary sync、双构建、axe、人工视觉硬门 | 浏览器/NFR 未运行时整体保持阻塞 |
| I-007 迁移 allowlist | 精确列出两 Catalog JSON、旧 PM 文件、evidence 目标、before Hash/rollback | 强关系 0 丢失，否则阻断 |
| M-001 Hash 文案 | 改为 64 个十六进制字符 / 256 bit | 设计正文检查 |
| M-002 Evidence | 写入完整命令、关键输出和 exit code | 作者 evidence iteration 2 |
| I3-001 section key | 39 表数据字典统一为 JCS Hash，检查脚本显式拒绝旧拼接公式 | 设计 marker + negative assertion |
| I3-002 PM 四态 | 计划和 T04 brief 均增加四态逐项断言 | `known|unknown|not_registered|not_applicable` |
| I3-003 迁移发布边界 | T05 只写 migration staging after-image，T06 验证后激活最终目标 | T05 allowlist 不再含最终 Catalog/manifest |
| I3-M-001 queue 依赖 | T05 brief 改为 R009 独立 queue，明确不依赖冻结候选 | brief 上游合同 |

## 结构验证结果

```text
requirements=16 acceptance=64 nfr=11
schema=29+10 fts=2
pm_fields=137 unique row_models=13 summary_pk=summary_id
review_fix_markers=all_present placeholders=0 jsonl=valid sqlite_fts=ok
exit code: 0
```

当前候选 Hash：

- Design: `ca83613f06a29dc546c7cb6174a405b77001c04aa44c6aa4832272a355e9aacb`
- Plan: `8bec0cb0a958e67fb82867a4b2929684d8113abc71b30b57222bc94b92ffbfea`
- Executable structure check: `1018a31cd5ac27b664155e21fa4333190ccf57fb8676cc7450c31ee3283a6ec0`

下一步：交回 `/root/design_plan_review` 同一独立 reviewer iteration 4，复审剩余 Finding closure 与无回退。
