# Agent 会话卡

- 生成时间：2026-08-23 22:04 +0800
- 项目：`shanforge`
- 当前工作项：`SKILL-COMPLETENESS-P0-001`
- 当前任务：`SKILL-COMPLETENESS-P0-001-T01`
- 当前状态：`implementation_committed_pending_clean_clone`
- 当前焦点：按顺序关闭 Skill 完整性五项 P0 缺口
- 下一动作：`verify_clean_clone`

## 当前事实

- Shanforge 是 skill-first 工程协作资产，旧 `src/` 平台和对应测试不属于当前产品。
- Skill 同步以含 `SKILL.md` 的一级目录为发现源，当前真实仓为 38 个。
- 正式文档优先按目标项目 `doc-map.md` 的 owner 映射回源；四模块只作新项目回退。
- 美术候选图跨会话保存在 `candidates/`，最终包排除候选和可再生临时目录。
- 能力目录由文件系统动态派生，不增加运行时、注册表或依赖。
- 首轮独立 review 的两项 Important 已修复；同 reviewer 首次复审为 `97 / C0-I0`。
- memory 已补录首次复审和随后 `98 / changes_requested / C0-I1` 的状态历史；提交前完整回归为 `242 passed / 4 subtests passed`。
- 同 reviewer 独立终审为 `approved / 100 / C0-I0-M0`。
- 实现提交为 `fd908b4`；首次干净克隆捕获会话卡与最新 ledger 下一动作不一致，已按同一状态合同同步。

## 当前 Gate

- `postcommit_clean_clone_verification`
- 独立终审：`approved / 100 / C0-I0-M0`；实现已提交，下一步重跑干净克隆验证。

## 后续授权范围

- 允许同范围脚本、Skill、正式文档、配置、测试、WorkItem、memory、独立只读复审和本地提交。
- 不执行 push、PR、merge 或部署。

## 恢复入口

- `.factory/workitems/SKILL-COMPLETENESS-P0-001/brief.md`
- `.factory/workitems/SKILL-COMPLETENESS-P0-001/plan.md`
- `.factory/workitems/SKILL-COMPLETENESS-P0-001/ledger.jsonl`
