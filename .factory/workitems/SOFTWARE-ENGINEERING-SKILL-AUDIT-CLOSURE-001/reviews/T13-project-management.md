# 项目管理维度复评

首轮结论：`changes_requested`。38/38 Skill 已覆盖；PM-I04、PM-I05 部分关闭，并新增 PM-N01 Important、PM-N02 Minor。

| Skill | before | after | delta | reason/evidence |
|---|---:|---:|---:|---|
| agent-harness-construction | 83 | 92 | +9 | status/evidence/ledger 及 next action owner 清楚。 |
| ai-first-engineering | 82 | 92 | +10 | 工程规则、Gate、验证和共享回写合同齐全。 |
| ai-regression-testing | 86 | 93 | +7 | 根因、回归证据、多路径与风险分级可追踪。 |
| algorithmic-art | 82 | 93 | +11 | 输出、验证、blocked 与联网/离线边界明确。 |
| api-design | 88 | 93 | +5 | 契约、风险与验证建议可落到任务证据。 |
| art-asset-pipeline | 84 | 94 | +10 | 确认、manifest、清理 owner 与 validator 可核对。 |
| article-writing | 79 | 91 | +12 | 项目化输出引用共享合同。 |
| brainstorming | 85 | 94 | +9 | brief、批准点、ledger 与跨会话边界清楚。 |
| browser-control | 84 | 93 | +9 | 外部动作、证据、阻塞与候选路由清楚。 |
| crawler4j-model-project | 88 | 94 | +6 | 版本/发布 Gate 与兼容检查脚本可复核。 |
| doc-coauthoring | 83 | 92 | +9 | 事实来源、验证、待决项和共享回写明确。 |
| document-templates | 90 | 94 | +4 | 正式事实源、版本与文档治理完整。 |
| docx | 83 | 93 | +10 | capability fallback、验证与 round-trip 齐备。 |
| executing-plans | 80 | 87 | +7 | 有 TaskCard/Gate/验证；依赖 DAG 未闭环。 |
| frontend-patterns | 82 | 91 | +9 | 设计决策、状态边界和共享回写明确。 |
| gitcommitzh | 87 | 94 | +7 | 提交前 Gate、范围和证据重读明确。 |
| go-developer | 84 | 93 | +9 | 阶段、验证与质量 Gate 明确。 |
| humanizer | 79 | 91 | +12 | 项目状态事实保护与共享回写明确。 |
| java-developer | 82 | 92 | +10 | 阶段、最小变更、验证与状态输出完整。 |
| pdf | 83 | 93 | +10 | 不可逆动作、验证和 blocked 语义明确。 |
| project-memory | 75 | 89 | +14 | 模板补齐身份、Gate、停止原因；当前任务同步另列。 |
| python-uv-project | 83 | 92 | +9 | 工具链质量门、失败语义与共享回写明确。 |
| receiving-code-review | 85 | 93 | +8 | triage/response owner 与授权边界明确。 |
| release-deployment | 90 | 94 | +4 | 候选、授权、健康检查、回执完整。 |
| requesting-code-review | 89 | 94 | +5 | 独立性、严重度、人工 Gate 与 review 生命周期清楚。 |
| requirements-engineering | 86 | 93 | +7 | REQ/NFR、验收、版本与追踪明确。 |
| shadcn | 82 | 92 | +10 | 组件流程、验证与项目状态边界清楚。 |
| stratix-admin-web | 84 | 93 | +9 | 页面/权限/验证/状态回写清楚。 |
| stratix-service | 85 | 94 | +9 | 框架事实、验证矩阵、兼容性与发布门充分。 |
| subagent-driven-development | 79 | 87 | +8 | receipt、状态与并发 Gate 完整；依赖图未闭环。 |
| systematic-debugging | 88 | 94 | +6 | 根因、fault owner、Bug TaskCard 决策充分。 |
| tdd-workflow | 87 | 93 | +6 | Red/Green、根因、风险 Gate 与代码形状可复核。 |
| ui-ux-pro-max | 85 | 93 | +8 | 设计证据、状态矩阵与验收明确。 |
| using-shanforge | 76 | 87 | +11 | PM 快照验证 WBS 树和状态投影；未验证 TaskCard DAG。 |
| verification-before-completion | 89 | 94 | +5 | 七态统计、偏离记录与关闭 Gate 完整。 |
| webapp-testing | 87 | 93 | +6 | TEST-UI、环境、证据与路由边界明确。 |
| writing-plans | 74 | 82 | +8 | WBS、Gate、状态已补；依赖/owner/正式模板贯通仍缺。 |
| xlsx | 83 | 93 | +10 | capability fallback、重读验证与 round-trip 齐备。 |

- coverage: `38/38`
- 平均 before: `83.7`
- 平均 after: `92.1`
- 平均 delta: `+8.4`

## T04 原始 Finding

| ID | 严重度 | decision | 证据/理由 |
|---|---|---|---|
| PM-I01 | Important | verified_fixed | WBS 四列表、快照树解析与循环/孤儿校验已存在。 |
| PM-I02 | Important | verified_fixed | task/ledger/session 稳定身份、Gate、下一动作字段已统一。 |
| PM-I03 | Important | verified_fixed | 生命周期与 review_status 已拆分，approved 不算完成。 |
| PM-I04 | Important | partially_fixed | plan review 只有“依赖 DAG”文字；正式 TaskCard 模板无结构化 `depends_on` 和 owner，也无依赖图机器校验。 |
| PM-I05 | Important | partially_fixed | PM 贯通测试实例化 plan，但 TaskCard/ledger 是手写简化文本，没有实例化正式 TaskCard 模板或失败路径。 |
| PM-M01 | Minor | verified_fixed | session card 有停止原因。 |
| PM-M02 | Minor | verified_fixed | Gate 表有 ID、owner、进入条件、evidence path、状态。 |

## 新 Finding

- `PM-N01` / Important：`workitem-plan-template.md`、`task-brief-template.md` 缺稳定 owner 与结构化 depends_on；无法机械拒绝缺 owner、未知依赖、自依赖、环。
- `PM-N02` / Minor：首轮复评时 T13 TaskCard 的 Gate/下一动作落后于 ledger，可能重复派发。

WBS `current` 是进度状态，不是 TaskCard 生命周期；整改应明确两套受控词表，而不是把二者混为一谈。

## 首轮 Gate

- 原始剩余：`C0/I2/M0`
- 新发现：`C0/I1/M1`
- 总剩余：`C0/I3/M1`
- gate_decision: `changes_requested`
- 下一步：补模板 owner/depends_on、可执行 DAG 校验、真实双模板贯通测试，并同步当前 TaskCard 恢复字段。

## 第一次定向复审补充

- `PM-I04`、`PM-I05`：`verified_fixed`。模板、可执行 DAG 校验、双正式模板贯通和状态词表分离均通过。
- `PM-N01`：`partially_fixed`。新模板正确，但当前工作项旧 TaskCard 尚未全部加入 owner 和完整 TaskCard ID depends_on，真实工作项不能通过新校验器。
- `PM-N02`：`partially_fixed`。T13 Card 的下一动作落后于最新 ledger。
- WBS `current` 合法且与 TaskCard 生命周期不同，首轮相关异议撤回。
- 临时分数更新：writing-plans `82→89`、executing-plans `87→89`、subagent-driven-development `87→89`、using-shanforge `87→89`、project-memory `89→90`；其余 33 项不变。
- 临时 after 平均 `92.4`；before `83.7`；delta `+8.7`。
- remaining C/I/M：`0/1/1`；`gate_decision: changes_requested`。

## 最终定向复审补充

- `PM-N01`：`verified_fixed`。R06 将当前工作项 11/11 张 TaskCard 迁移为稳定 owner 与完整存在的 TaskCard ID 依赖；独立实际运行图校验器退出码 0，无缺 owner、未知、自依赖或环。
- `PM-N02`：`verified_fixed`。最终复审时 T13 Card 与最新状态同步事件的 `current_gate`、唯一 `next_required_action` 一致。
- 最终分数：writing-plans `94`、executing-plans `91`、subagent-driven-development `92`、using-shanforge `93`、project-memory `91`；其余 33 项不变。
- after 平均 `92.8`；before `83.7`；delta `+9.1`。
- remaining/new C/I/M：`0/0/0`；最终 `gate_decision: approved`。
