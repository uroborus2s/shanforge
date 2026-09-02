---
name: tdd-workflow
description: 在编写新功能、修复 Bug 或重构代码时使用此技能。执行测试先行、根因先行和风险分级验证；覆盖率与 E2E 范围按项目门禁和变更风险决定。
---

# 测试驱动开发工作流

用于把需求、Bug 或重构落到可验证代码。目标是先证明行为，再写最小实现；不是给所有任务套固定覆盖率或无关端到端套件。

## 何时激活

- 编写新功能、API、组件或脚本。
- 修复 Bug 或回归。
- 重构会影响行为、接口、数据流或用户路径。
- 需要决定测试层级和验证范围。

## 核心原则

### 测试先于代码

- 先写能失败的最小检查，再写实现。
- 如果已有测试能准确覆盖行为，先运行并记录失败证据。
- 无法自动化时，先写清人工验收步骤和原因。

### Bug 根因先于修复

修 Bug 时必须先完成根因说明，再修改实现：

- 先复现失败，并记录可观察症状、触发条件和受影响路径。
- 明确直接原因与根源原因：直接原因说明哪一行、哪一个分支或哪一个契约破坏导致失败；根源原因说明为什么系统允许它发生。
- 只在根因、事实 owner、影响范围和风险已确认后执行修复。
- 低、中风险不新增人工 Gate；高风险必须先通过根因确认和修复方案确认 Gate。
- 新增或修改测试必须锁定根因路径，而不是只断言兜底结果。
- 禁止把 `try/except`、默认值、空结果、重试、忽略异常、宽松解析或“兼容一下”当作主要修复，除非已经证明该降级行为是产品契约，并且原始根因已经被修复或被明确登记为接受风险。
- 如果暂时无法定位根因，只允许增加诊断、日志、复现测试或最小探针；不得提交行为修复。

## 决策表

| 任务 | 先写的检查 | 实现后验证 |
|---|---|---|
| 纯函数或规则 | 单元测试 | 相关单元测试 |
| API/服务契约 | 契约或集成测试 | 相关集成测试，必要时 schema 校验 |
| UI 交互 | 组件测试或目标页面 smoke | 组件测试，必要时目标 E2E |
| Bug 修复 | 复现测试和根因记录 | 复现测试由红转绿，相关回归测试 |
| 重构 | 先跑现有行为测试 | 同一测试集通过，必要时补缺口 |

## 默认流程

1. 写行为说明；Bug 修复先读取根因、事实 owner、影响范围和风险结论。
2. 高风险 Bug 确认根因和修复方案 Gate 均已通过；低、中风险直接进入最小修复。
3. 选择最小测试层级，优先使用项目现有测试工具。
4. `RED`：运行测试，确认失败原因符合预期。
5. 写最小实现，只改根因路径；在 `GREEN` 前执行两条代码形状禁令：不得定义局部函数；单调用点且无独立职责的 helper 必须内联。
6. `GREEN`：重新运行原失败测试、根因测试和受影响调用方 / 契约；单次缺陷修复不默认运行全仓测试。修改源码或测试后运行 `python <skill-dir>/scripts/check_code_shape.py <changed-python-files>`；它拒绝函数/方法内的命名函数，并报告只有一个调用点的 helper 候选供内联判断。
7. 如需重构，保持测试通过后再整理。
8. 完成前记录新鲜验证证据、失败数量、跳过项和未运行项，以及 RED 测试范围、GREEN 回归范围、覆盖与未覆盖范围；完整七态汇总由完成前验证流程按正式基线报告。

根因定位清单见 [root-cause-checklist.md](references/root-cause-checklist.md)。
完成证据格式见 [evidence-report-template.md](references/evidence-report-template.md)。
TDD、调试和完成前验证的合并质量门见 [tdd-debugging-verification-gate.md](references/tdd-debugging-verification-gate.md)。

## 风险分级验证

- 低风险：小型纯函数、文案、局部样式。运行相关单元测试或静态检查。
- 中风险：API、状态、持久化、权限判断。运行相关单元和集成测试。
- 高风险：认证、支付、删除、迁移、跨服务契约、核心用户流程。运行相关集成测试和目标 E2E。

覆盖率阈值按项目已有门禁执行。没有门禁时，优先补能防止本次回归的测试，不用固定百分比替代判断。

## 与相邻 workflow 的边界

- 根因不明、复现困难或多次修复失败时，先做系统化调试。
- 高风险根因未获人工确认，或修复方案确认 Gate 未通过时，禁止进入 `GREEN` 实现。
- 本 skill 负责测试先行和最小实现，不负责宣布完成。
- 完成声明前必须运行本轮新鲜验证命令并读取 exit code。
- 已有项目模式优先；不要为测试新增框架或全局脚手架。

## 输出契约

```text
工作结果：
- work_item: <ID>
- skill: tdd-workflow
- status: passed | partial | failed | blocked
- outputs:
  - <changed files>
  - <tests added or updated>
- evidence:
  - <red command/result>
  - <green command/result>
- code_shape_check: passed | failed | not_applicable（执行两条代码形状禁令：不定义局部函数；不抽取单调用点公共 helper）
- `not_applicable` 只有本轮没有修改代码时才可使用；凡修改源码或测试代码不得用 N/A。
- change_locations:
  - file: <实际修改文件>
    symbol: <实际函数、方法或符号；没有函数边界时写模块、配置项或文档章节>
    change: <具体改动>
    reason: <改动原因>
    verification: <green command/result>
- ledger_event: <event id>
- needs:
  - none | root_cause | tests | verification | human_confirmation
```

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
