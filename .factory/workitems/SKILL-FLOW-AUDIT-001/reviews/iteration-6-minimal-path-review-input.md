# Iteration 6 最小路径独立复评输入

- work_item: `SKILL-FLOW-AUDIT-001`
- author_status: `ready_for_review`
- requested_review: 8 Skill 中文语言 + Prompt 工程独立复评

## 必读

- `task-briefs/iteration-6-minimal-acceptance-amendment.md`
- `reports/iteration-6-review-root-cause-20260727.md`
- `reports/iteration-6-minimal-path-plan-20260727.md`
- `evidence/iteration-6-minimal-path-verification-20260727.md`
- `reviews/iteration-6-fix-language-prompt-97-independent-review.md`

## 复评范围

只复评验收修订冻结的 8 个 Skill 及共享工作 Skill 回写契约。先核对 SHA-256，
再按合同中的两个 100 分公式逐项评分，计算等权平均。

必须输出：

- reviewer 独立性证据；
- 8 行中文语言分、Prompt 分及一句理由；
- 两个平均分；
- Required Fixes 1-8 关闭情况；
- Critical / Important / Minor；
- `approved` 或 `changes_requested`；
- 是否可进入人工确认。

## 禁止

- 不恢复全仓 37 Skill 平均分 Gate。
- 不把其他 WorkItem 的旧测试失败算成本整改缺陷。
- 不修改 Skill、测试、ledger、memory 或 Git index。
- 不把本复评冒充人工确认。
