# Iteration 6 隔离关闭门修复

- 父工作项：`SKILL-FLOW-AUDIT-001`
- 任务：`iteration-6-hermetic-closeout-repair`
- 状态：`closed`
- 来源：已确认的关闭门非隔离根因

## 目标

让 8 个已冻结 Skill 的关闭验证只依赖这 8 个候选、共享回写合同和与其直接相关的
测试节点，不再被 `stratix-service` 等范围外 Skill 的并行改动改变结果。

## 用户角色

仓库维护者需要一个可重放、范围与评分对象一致的关闭门。

## 主流程

1. 保留现有 8 Skill 与共享合同的 9 个 SHA-256。
2. 把冻结 workflow 清单从“整文件”改为“节点级”，逐项排除读取候选范围外
   Skill、旧工作项或全仓动态集合的节点。
3. 不修改 `stratix-service`、其他 Skill 或测试实现。
4. 运行收紧后的全部节点、Ruff、候选哈希、JSONL 和限定 diff check。
5. 交独立 reviewer 复核清单确实只依赖冻结输入。

## 异常流程

- 若某个候选 Skill 缺少现有独立测试节点，停止并报告缺口，不用全仓测试替代。
- 若 8 Skill 或共享合同哈希变化，重新冻结并重新评审。

## 业务规则

- 评分对象与验证输入必须一致。
- 全仓工作 Skill 合同测试仍保留为项目诊断，不作为本 8 Skill 整改包的关闭 Gate。
- 原始失败与 E105/E106 历史事件保留，不覆盖。

## 安全与权限

- 允许修改：本任务简报、Iteration 6 验收修订、验证/评审材料、本 WorkItem ledger，
  以及 `tests/test_skill_flow_process_audit.py` 的现有聚合断言拆分。
- 禁止修改：`skills/**`、其他 `tests/**`、其他 WorkItem、远端 Git、发布和部署。

## 验收标准

1. 冻结清单中的每个测试节点仅读取 8 Skill、共享合同或本 WorkItem 固定输入。
2. `stratix-service` 当前工作区内容不变时，关闭门可以独立运行。
3. 9 个候选哈希一致，目标测试、Ruff、JSONL 与限定 diff check 全部通过。
4. 独立 reviewer 给出 `C0/I0`，并确认不存在范围外测试输入。

## Baseline 影响

无领域、架构、数据库、API 或 UI baseline 影响；只修正本整改包验收清单。

## 未决问题

需要用户批准本方案后才能修改验收修订并重新评审。

方案已批准，但执行时发现两个候选缺少现有隔离测试节点；详见
`evidence/iteration-6-hermetic-closeout-repair-blocker-20260727.md`。解阻需要扩大
允许范围到 `tests/test_skill_flow_process_audit.py`，仅拆分现有聚合断言。

用户已批准该最小测试拆分范围，不授权修改 Skill 或其他测试。
