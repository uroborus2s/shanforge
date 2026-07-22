# TASK-DESIGN-002 R001 独立设计与计划评审

- reviewer_type: `independent_subagent`
- reviewer_id: `/root/design_plan_review`
- reviewer_independence_evidence: 未参与 R009、DESIGN R001 或 P001 的编制/实现；仅读取文件化评审包并运行只读 `rg/jq/shasum/sed` 检查，未修改文件、ledger、memory、Git 或外部系统。
- review_status: `changes_requested`
- next_gate_status: `changes_requested`
- review_score: `66 / 100`
- human_confirmation_required: `false`
- gate_reason: `none`

## 评分

- 需求符合度：20 / 30
- 架构一致性：12 / 20
- 测试充分性：11 / 20
- 代码质量：15 / 20
- 文档与记忆同步：8 / 10

只读检查确认：16 REQ、64 AC、11 NFR、39 表（29+10、2 FTS）、137/137 唯一字段、13 row models、50 transitions；PM map Hash 与 R009 pin 一致。T01/T02 的 UI N/A 接受。

## Findings

### Critical

- 无。

### Important

1. 一个 registry source 覆盖多文件，但 `pk_source_state` 只有 source 主键；实体/专用表/搜索条目缺来源贡献 owner，不能同时满足未变来源不重解析、删除一源无幽灵、同实体其他来源保留。
2. `pk_document_section.section_id PK` 与规范 `doc_id+section_id` 冲突；`pm_project_summary.project_id PK` 与已批准 field map 的 `summary_id` 冲突；137 map 校验缺 PK/父键/碰撞/基数/type/nullable/history/R014 pin。
3. 冻结 system-task enum 只允许 `PROJECT_PROGRESS_PROJECTION`，当前计划无法在不修改 `TASK-IMPLEMENT-002-R001` 的前提下复用 durable store。
4. 文档、质量、版本与 PM record 缺稳定详情 URL 和详情测试。
5. staging rename 到非空 current 目录不可用，两次 rename 又有空窗；缺可证明的原子站点指针协议。
6. Memory P95、10k 单来源、普通后台同步、固定时钟双构建 Hash、axe 与人工视觉等 NFR 证据未成为硬门。
7. 迁移 task allowlist 没有精确覆盖旧 Catalog JSON、`.factory/pm`、矩阵、导航、manifest 与 rollback 路径。

### Minor

1. SHA-256 应表述为 64 个十六进制字符/256 bit，而不是 64 位。
2. 作者 evidence 应附完整命令、exit code 和关键输出。

## Gate

全部 Finding 都可在既有批准范围内整改，无需人工产品决策。修复后交回同一 reviewer 复审。
