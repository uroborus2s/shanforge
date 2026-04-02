# 评估摘要与审批回报契约

**文档状态：** MVP 已实现  
**主要读者：** 项目负责人 | 平台维护者 | 技能维护者 | QA  
**负责人：** 仓库维护者  
**关联 ID：** `REQ-003`, `REQ-005`, `REQ-006`, `API-014`, `API-015`, `API-016`, `API-017`  
**最后更新：** 2026-04-02  

## 1. 设计目标

山海工枢在日常软件工程协作中，不应把完整评估报告或审批票据原文直接灌进对话回复。

当前目标是固定一套更稳定的回报方式：

- 对话里返回管理摘要
- 仓库里固化审计报告
- 高风险动作通过审批票据继续推进
- skill 正式变更走候选、评估、批准链，而不是直接覆盖正式 `SKILL.md`

## 2. 回报分层

| 层级 | 作用 | 存放位置 |
|---|---|---|
| 对话摘要 | 给项目负责人快速判断是否继续推进 | 当前 CLI / Agent 回复 |
| 审计报告 | 给维护者复核细节和回溯 | `.factory/process/*.md` |
| 压缩记忆 | 给后续会话低成本接手 | `.factory/memory/*.summary.md` |

## 3. 哪些动作必须给对话摘要

当前 MVP 固定了 3 类动作必须返回 `reply_summary`：

| 动作 | 触发时机 | 必要摘要字段 |
|---|---|---|
| `intent-resolver` | 自然语言解析、`--execute-safe`、`--request-approval` | 输入、主推荐动作、风险级别、审批策略、子目标、安全执行状态、票据状态 |
| `intent-eval` | 回放评估 `intent` 能力 | 状态、总样本、通过、失败、命中率、摘要 |
| `intent-approval` | 列表、查看、批准、拒绝票据 | 状态、摘要、票据、动作、风险级别、审批策略、ownership 角色、ownership 校验 |

这些字段的正式契约位于：

- [reply-policy.json](../../../../config/reply-policy.json)

## 4. 为什么默认不回整份长报告

原因不是“不能给”，而是“默认不该给”：

- 日常开发消息应先服务于决策，而不是堆积审计细节
- 审批链路需要稳定字段，而不是自由文本
- 长报告更适合固化在 `.factory/process/`，便于复核和追踪

因此当前默认规则是：

- 回复里给摘要
- 如你明确要求“展开报告”，再读 `.factory/process/*.md`

## 5. 审批票据规则

### 5.1 必须进入票据审批的场景

当前 `intent-resolver` 会根据风险和策略给出 `approval_guidance`。

以下情况属于“必须通过票据推进”：

- 风险等级为 `L2` 或 `L3`
- 审批模式为 `summary_confirm` 或 `explicit_confirm`
- 执行模式为 `blocked_until_approved`

这类动作当前不会被 `--execute-safe` 放行。

### 5.2 当前已覆盖的典型场景

- 历史项目接管
- 批量 docs 升级
- workflow 型 `command-profiles`
  - `pre-gate`
  - `daily-close`
  - `release-ready`
  - `handover-ready`

### 5.3 批准方式

1. 通过 `intent-resolver --request-approval` 生成票据
2. 通过 `intent-approval --list` 查看票据
3. 通过 `intent-approval <ticket> --approve` 或 `--reject` 处理

批准前，系统会再次校验：

- 冻结 ownership 角色
- 冻结写入集合
- 当前负责人与票据执行人是否一致
- 当前显式写集是否冲突

## 6. Skill 进化的批准边界

当前正式规则不是“触发优化就自动改正式 skill”，而是：

1. 发现信号
2. 生成候选 skill 变更
3. 补评估样本与评估结果
4. 显式批准
5. 才允许晋升到正式 `skills/*/SKILL.md`

当前在策略文件里已经固定：

- 候选目录：`skills-drafts`
- 正式 skill 路径：`skills/*/SKILL.md`
- 必须先有候选
- 必须先有评估
- 必须先有审批记录

也就是说，系统未来可以自动：

- 建议新 skill
- 生成候选 skill 草案
- 跑评估

但默认不应自动：

- 直接覆盖正式 `SKILL.md`

## 7. 当前已实现的运行时资产

- [reply-policy.json](../../../../config/reply-policy.json)
- [factory_core.py](../../../../scripts/factory_core.py)
- [factory-intent-resolver](../../../../scripts/factory-intent-resolver)
- [factory-intent-eval](../../../../scripts/factory-intent-eval)
- [factory-intent-approval](../../../../scripts/factory-intent-approval)

当前运行时已经支持：

- `reply_summary`
- `approval_guidance`
- 评估摘要与审批摘要固定字段输出
- skill 正式变更必须先走候选/评估/审批的配置治理

## 8. 当前未闭环部分

- 还没有独立的 skill 候选生成器
- 还没有 skill 晋升专用审批命令
- 还没有 UI / 远程审批入口
- 还没有把“摘要回报契约”接入所有 legacy 动作

## 9. 变更记录

| 日期 | 变更内容 | 变更人 |
|---|---|---|
| 2026-04-02 | 初始版本，固化评估摘要、审批回报和 skill 变更批准边界 | Codex |
