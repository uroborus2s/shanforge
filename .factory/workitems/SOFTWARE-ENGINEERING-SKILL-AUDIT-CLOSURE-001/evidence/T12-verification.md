# T12 术语、单一 owner 与派发黑盒闭环

## 结论

- status: `completed`
- finding closure: `10/10`
- independent pytest: `57 passed`
- failed: `0`
- skipped: `0`
- Ruff: `passed`
- `git diff --check`: `passed`
- code shape: `passed`；仅报告本轮前既有 `transcript_bodies`、`_replayed_exit_code` 候选

## 问题与修复位置

| Finding | 修复文件与章节/符号 | 修复结果 |
|---|---|---|
| ZH-I01 | `using-shanforge`、`writing-plans`、`executing-plans`、`subagent-driven-development` 的简单任务/任务 Gate | 尚未执行的输入统一写“验收标准”，不再误写“验收结果”。 |
| ZH-I02 | `skills/subagent-driven-development/SKILL.md`“授权执行包” | 删除重复派发公式，只引用 `using-shanforge` 的唯一严格派发定义。 |
| ZH-I03 | `skills/using-shanforge/SKILL.md`“普通项目化路由包” | 路由字段按任务身份、控制/复杂度、风险/范围、派发、Gate/升级分组，字段不跨组重复。 |
| ZH-I04 | `skills/ui-ux-pro-max/SKILL.md` 引言与检索 | 改为“设计知识检索命中/未命中”，不再像业务数据库。 |
| ZH-I05 | `skills/frontend-patterns/SKILL.md` 状态选择表 | 改为“多个兄弟或下游组件共享”。 |
| ZH-I07 | `skills/stratix-admin-web/SKILL.md`“总原则”“开发顺序” | 明确查既有文件、记录复用模式与差异、产出页面/组件清单后再实现。 |
| ZH-M02 | `skills/browser-control/SKILL.md` snapshot 选择 | 中文说明 DOM 验结构/属性、state 验控件状态、accessibility 验可访问树/名称/角色。 |
| ZH-M03 | `skills/article-writing/SKILL.md` 场景与语气流程 | 只使用用户提供或明确授权样本，禁止自行抓取、推断或模仿未授权个人。 |
| SE-I04 | `tests/test_black_box_workflow_eval.py::evaluate_observation` 的 `FLOW-S11`；`black-box-flow-eval.md` | 1 个 worker 派发场景、7 条断言、16 个 mutation；检查 WBS/写策略/授权、Luna-low 或 Terra-medium、fork none、父工具回执一致、合法 worker 回执、禁止 Sol 代写、未授权/派发失败关闭。worker DONE 后仍 `close_allowed=false`，下一步为父级复验。 |
| SD-M04 | `skills/using-shanforge/SKILL.md`“工作 skill 状态回写协议” | 删除重复字段枚举；`work-skill-return-contract.md` 单一拥有本职结果包和 release_summary。 |

## 失败与根因记录

1. 第一轮新增 FLOW-S11 前，RED 为 unknown scenario；实现后现有 6 文件 `54 passed`，但完整命令因计划中的 residual 测试未创建而无法启动。
2. 独立检查发现路由分组把 control_model 误当身份、授权断言不完整、残余合同没有测试；新增 residual 测试后先 `1 failed`，修复后 `57 passed`。
3. 第二次独立检查发现 worker DONE 被允许直接关闭；改为父级复验后先 `1 failed`，修复后 `57 passed`。
4. 第三次独立检查发现 route 与 receipt 若同时使用非法推理/fork 仍可通过；加入合法模型矩阵与三个共同错误 mutation 后先 `1 failed`，最终 `57 passed`。

## 黑盒边界

- pytest 验证 transcript/observation 与 fail-closed 规则，不声称调用真实 `spawn_agent`。
- T13 必须用本工作项已有父工具派发回执和 worker 回执复核真实派发链。
