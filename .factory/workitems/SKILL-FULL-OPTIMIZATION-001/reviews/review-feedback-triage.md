# Review Feedback Triage

- work_item: `SKILL-FULL-OPTIMIZATION-001`
- task: `SKILL-FULL-OPTIMIZATION-001-T06`
- source: `.factory/workitems/SKILL-FULL-OPTIMIZATION-001/reviews/independent-scorecards.md`
- route: `source_or_test_write`

| ID | Severity | 技术核实 | 处理决定 | 证据 |
|---|---|---|---|---|
| I-02 | Important | 主入口仍绑定仓库 cwd | Fixed | 安装副本跨 cwd 测试 |
| I-04 | Important | 两个入口仍使用目标项目相对脚本 | Fixed | 两入口统一 `<skill-dir>` |
| I-07 | Important | `implementation` 不在输出枚举 | Fixed | 状态合同测试 |
| I-11 | Important | 主入口命令与 CLI 参考冲突 | Fixed | 跨文件命令断言 |
| I-13 | Important | Windows 只终止父 shell | Fixed | 原生 `taskkill /T /F` 测试 |
| I-15 | Important | XLSX CLI 错误返回 0 | Fixed | 三条 subprocess 失败测试 |
| I-16 | Important | 必填 next action 会自阻塞提交 | Fixed | 三份提交合同一致性测试 |
| I-17 | Important | `TC-*` / `TEST-*` 分裂 | Fixed | 跨资源 ID 断言 |
| M-01 | Minor | 源包链接确有断链 | Fixed in source package | 源树链接可达；物化后语义由 reviewer 保留为 Minor |

所有反馈均清楚、技术正确，不与用户授权冲突，也不需要新增依赖或抽象。
