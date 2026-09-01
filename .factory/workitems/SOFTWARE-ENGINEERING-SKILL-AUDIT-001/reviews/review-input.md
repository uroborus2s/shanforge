# 五专家统一审计输入

- Work item：`SOFTWARE-ENGINEERING-SKILL-AUDIT-001`
- Baseline snapshot：完整工作树 `HEAD=96e29da`；这是现状审计，不是 commit-diff review，38 个 Skill 无需由该提交引入。
- Review type：五视角全面只读审计
- Population：运行 `find skills -mindepth 2 -maxdepth 2 -name SKILL.md -print | sort` 得到的全部 38 个 Skill
- Related evidence：每个 Skill 直接引用的 references、scripts 和相关 `tests/`
- Write policy：`state_or_gate_write`；专家本人只读，不得写文件

## 每位专家必须输出

1. `reviewer_type`、`reviewer_id`、独立性说明。
2. 覆盖数，必须为 `38/38`；缺读项必须明确列出，不能假装完整。
3. 逐 Skill 表：`skill | score(0-100) | C/I/M | one-line reason`。
4. Findings：按 Critical / Important / Minor 排列，每项含 `file:line`、问题、影响、最小改法。
5. 系统级问题：跨 Skill 重复、矛盾、缺口和过度设计。
6. 本视角总分、评分依据、前三项优先整改建议。

## 通用评分锚点

- 90–100：边界明确、可执行、证据充分，只有轻微优化。
- 80–89：可用，但有明确一致性、可读性或验证缺口。
- 70–79：主要流程可用，存在会导致误执行或难维护的重要缺陷。
- 60–69：多个关键合同不完整或相互冲突。
- <60：无法可靠执行或可能造成严重错误。

每位专家只按自己的专业视角评分。主代理按五专家等权合并，不得擅自把未被证据支持的意见升格为事实。
