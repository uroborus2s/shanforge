# SKILL-CLEANUP-001-T01 独立评审输入

- Task brief：`../task-briefs/SKILL-CLEANUP-001-T01.md`
- 实施报告：`../reports/SKILL-CLEANUP-001-T01-implementer-report.md`
- 退役验证：`../evidence/completion-verification.md`
- 改名验证：`../evidence/go-developer-rename-and-global-link-sync-verification.md`
- 本轮新鲜验证：`../evidence/SKILL-CLEANUP-001-T01-fresh-verification.md`
- Ledger：`../ledger.jsonl`

## 必查

- 删除范围是否只包含被退役的仓内实现和专属测试。
- 是否仍有非历史文件依赖仓内 `skill-creator`。
- Go Skill 是否是完整改名而非丢文件或双目录并存。
- 测试是否真实覆盖名称、状态包、资源和剩余 Skill 契约。
- 全局软链接只做只读核对，不由 Reviewer 修改。
- 实际 diff 是否混入其他工作项。

Reviewer 只读，不修改文件、Git index 或外部系统。
