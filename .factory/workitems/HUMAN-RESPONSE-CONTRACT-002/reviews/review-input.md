# HUMAN-RESPONSE-CONTRACT-002 独立评审输入

## 目标

检查会话响应是否采用统一外壳、按开发/测试/Bug/交付工作类型输出不同正文，并能明确回答 WBS 进度、完整测试结果、失败原因和修复 TaskCard 决策。

## 需求与计划

- `.factory/workitems/HUMAN-RESPONSE-CONTRACT-002/brief.md`
- `.factory/workitems/HUMAN-RESPONSE-CONTRACT-002/plan.md`

## 评审范围

- `skills/using-shanforge/SKILL.md`
- `skills/using-shanforge/references/human-readable-status.md`
- `skills/using-shanforge/references/work-skill-return-contract.md`
- `skills/systematic-debugging/SKILL.md`
- `skills/tdd-workflow/SKILL.md`
- `skills/verification-before-completion/SKILL.md`
- 三个对应测试文件。

## 验证

见 `evidence/verification.md`：本工作项范围 `25 passed, 1 deselected`，Ruff、四个 Skill validator、ledger 与 diff check 均通过。并行生命周期治理正在改写一个正式文档，导致范围外旧锚点测试暂时失败；不得归因到本工作项，也不得把当前仓库表述为全部通过。

## 首轮评审整改

- 已要求所有 WBS/产品进度变化先对账已批准 WBS、TaskCard、ledger；无法匹配的 worker facts 只作观察或技术记录。
- 已在专业验证状态包和共享回写合同中结构化规定八列计数、覆盖/未覆盖范围、失败/错误用例明细。
- 已增加进度对账决策表、测试事实结构和修复 TaskCard 三分支断言。

## 评审要求

- 只读，不修改文件。
- 检查需求覆盖、事实 owner 边界、误报项目进度风险、失败归因诚实性和 TaskCard 分支完整性。
- 输出 Critical / Important / Minor；只有 Critical=0 且 Important=0 才可通过。
