# 当前状态

- 当前模式：cli_direct
- 当前阶段：MAINTENANCE
- 活跃任务：0
- 活跃变更：0
- 活跃缺陷：0
- 活跃 PR：0

- 角色目录总数：9
- 当前阶段主要角色：项目协调者、发布经理、文档与记忆管理员

- 当前技术画像：历史项目纳管基线画像
- 技术画像预设：custom
- 关键工程规则数：3
- 设计交付物数：0

## 最近条目

- 任务：无
- 变更：已完成 `factory-intent-resolver` 的 skill 生命周期解析重构；自然语言已可按候选状态路由到 `skill-eval`、`skill-approval`、`skill-promote`、`skill-delete-approval`、`skill-rollback`，并在缺少候选 skill 时显式保留阻塞边界；同时已将仓库级工程基线切到 `Python 3.14+` / `uv`，并将 docs 流程重构为 `document-templates` skill + `docs-stratego` CLI
- 缺陷：已修复 `evaluation-summary-and-approval-reporting.md` 中指向 `config/`、`scripts/` 的 Markdown 相对链接告警；当前聚合站点构建未再发现 `shanforge` 文档的无效链接告警

## 当前能力基线

- intent 固定样本回放：`13/13` 通过，命中率 `100.00%`
- 审批治理：`intent` 已支持审批票据申请、批准/拒绝执行，以及 workflow 型 profile 的风险提升
- 回复治理：`intent-resolver`、`intent-eval`、`intent-approval` 已输出固定 `reply_summary`，`intent-resolver` 已输出 `approval_guidance`，并可回报 `selected_skill_candidate` / `selected_skill_operation`
- 多代理治理：角色分派已支持 `--write-targets`，并默认阻断与现有分派的显式写集冲突
- skill 治理：已固定正式 `SKILL.md` 变更必须先走候选、正式评估和批准；`factory-skill-draft` 已可生成包含 `eval-report.json` 与 `change-summary.md` 的候选草案，`factory-skill-eval` 已可输出正式 `passed/failed` 报告，`factory-skill-approval` 已收紧为只有正式评估 `passed` 的候选 skill 才能申请审批票据，`factory-skill-delete-approval` 已可为首次发布的新 skill 申请删除回退审批票据，`factory-skill-promote` 已可执行正式晋升，`factory-skill-rollback` 已可在存在旧版本备份时恢复旧版，或在删除审批通过后执行首次发布新 skill 的受控删除回退；`intent` 层已可直接选择这条 skill 生命周期治理链上的下一条正式动作
- 工程基线：仓库已声明 `Python 3.14+`、`.python-version`、`pyproject.toml` 与 `uv.lock`；正式脚本入口以 `uv` 工作流为准，但当前环境中的 Homebrew `uv` 运行 `lock` / `docs-stratego` 时会触发系统配置 panic
- docs 入口治理：文档内容维护统一改走 `document-templates` skill，PyPI 已发布的 `docs-stratego` CLI 负责源仓校验、聚合接入、同步、构建与预览
- 当前剩余缺口：尚未覆盖真实子代理提交阶段的隐式写集探测、自动串行化与恢复协议

## 下一步建议

- 检查任务人天估算是否真实合理，仅在必要时再细化到 0.5 人天精度
- 若进入设计或实施阶段，先确认 `docs/04-project-development/04-design/technical-selection.md` 已明确框架、模块、后台范围和编码规则
- 若 UX/UI 需要可视化评审，优先登记真实设计交付物而不是只写文字
- 若工作项进入收尾，确认关联 PR 已完成评审并合并
- 阶段切换前先更新正式文档，再刷新 `/.factory/memory/` 压缩记忆
