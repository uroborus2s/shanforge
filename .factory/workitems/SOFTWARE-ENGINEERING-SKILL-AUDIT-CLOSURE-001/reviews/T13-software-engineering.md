# 软件工程维度复评

首轮结论：`changes_requested`。集中验证通过，但 `SE-I04`、`SE-I05` 仅部分关闭，并新增 `SE-NEW-M01`。

| Skill | before | after | delta | reason/evidence |
|---|---:|---:|---:|---|
| agent-harness-construction | 78 | 90 | +12 | 共享回写合同已接入；仍无 harness schema/eval 行为 fixture。 |
| ai-first-engineering | 83 | 89 | +6 | 根因与回归纪律明确；规则本身仍主要文本验证。 |
| ai-regression-testing | 86 | 91 | +5 | 多路径根因回归流程完整；无专属可执行样例。 |
| algorithmic-art | 82 | 90 | +8 | viewer 固定 p5 1.7.0，并明确联网/离线边界。 |
| api-design | 87 | 90 | +3 | 契约、风险与验证路径明确；缺机器可执行契约模板。 |
| art-asset-pipeline | 76 | 94 | +18 | manifest validator 与合法/非法 fixture 实测。 |
| article-writing | 85 | 90 | +5 | 授权样本边界已覆盖。 |
| brainstorming | 76 | 86 | +10 | 路由边界清晰；无端到端行为测试。 |
| browser-control | 83 | 91 | +8 | 能力探测、失败关闭、snapshot 选择明确并有回归断言。 |
| crawler4j-model-project | 74 | 82 | +8 | 有 fail-closed 检查器；未验证 manifest lock/真实结构 smoke。 |
| doc-coauthoring | 88 | 90 | +2 | 输入事实、输出边界稳定；无代表性交付行为验证。 |
| document-templates | 79 | 85 | +6 | 本地校验路径可用；外部 CLI 失败路径偏文本合同。 |
| docx | 84 | 92 | +8 | 实测 Office package 往返；未证明视觉/语义保真。 |
| executing-plans | 71 | 86 | +15 | 身份和验收标准合同已对齐；主要为流程结构验证。 |
| frontend-patterns | 87 | 91 | +4 | 状态共享语义已修正并覆盖。 |
| gitcommitzh | 86 | 91 | +5 | Gate、范围和回读规则明确。 |
| go-developer | 85 | 88 | +3 | 根因和风险分级清晰。 |
| humanizer | 90 | 92 | +2 | 状态事实保护边界明确并有合同测试。 |
| java-developer | 78 | 84 | +6 | 工程约束清晰；关键安全规则依赖未执行 reference。 |
| pdf | 86 | 89 | +3 | 写入保护与结构/视觉检查完整；无本轮 round-trip。 |
| project-memory | 80 | 90 | +10 | 无活动状态分支、receipt 和恢复字段已测试。 |
| python-uv-project | 82 | 87 | +5 | 工具链/根因路径明确；缺跨项目行为样本。 |
| receiving-code-review | 78 | 91 | +13 | 双授权及失败交还已测试。 |
| release-deployment | 84 | 89 | +5 | 发布回执与示例已覆盖；无真实发布 smoke。 |
| requesting-code-review | 82 | 90 | +8 | review/triage owner 已消歧。 |
| requirements-engineering | 79 | 88 | +9 | 身份路由冲突已消除。 |
| shadcn | 82 | 88 | +6 | 命令和状态边界清楚；全流程 eval 不足。 |
| stratix-admin-web | 84 | 90 | +6 | 相似组件比较动作、产物和验证要求明确。 |
| stratix-service | 72 | 82 | +10 | 有版本矩阵检查器；未读取 lockfile 或实跑 doctor smoke。 |
| subagent-driven-development | 68 | 91 | +23 | receipt 映射及 DONE 禁止直达 review 已测试。 |
| systematic-debugging | 88 | 91 | +3 | 根因、归因和高风险 Gate 完整。 |
| tdd-workflow | 79 | 93 | +14 | AST 检查命名局部函数与单调用候选；嵌套 lambda 缺口另列。 |
| ui-ux-pro-max | 80 | 87 | +7 | 检索术语已消歧；交付质量主要人工验证。 |
| using-shanforge | 70 | 83 | +13 | 路由、失败关闭和 mutation 已增强；历史 dispatch 回执证据不完整。 |
| verification-before-completion | 75 | 92 | +17 | 普通回执与批次证据合同统一。 |
| webapp-testing | 85 | 90 | +5 | 浏览器候选交还总控，失败边界清晰。 |
| writing-plans | 68 | 91 | +23 | 缺身份 blocked、WBS/TaskCard 映射和 review 模板已测试。 |
| xlsx | 84 | 92 | +8 | 实测 package 往返；未证明复杂公式/格式语义保真。 |

- coverage: `38/38`
- 平均 before: `80.6`
- 平均 after: `89.1`
- 平均 delta: `+8.5`

## T03 原始 Finding

| ID | 严重度 | decision | 证据/理由 |
|---|---|---|---|
| SE-I01 | Important | verified_fixed | 正式身份完整性与临时 ID 禁令已固化。 |
| SE-I02 | Important | verified_fixed | 四种 worker receipt 有唯一控制器动作，禁止 `DONE→ready_for_review`。 |
| SE-I03 | Important | verified_fixed | 普通回读回执与批次/关闭落盘 evidence 已分层。 |
| SE-I04 | Important | partially_fixed | FLOW-S11 已覆盖合同，但 T10–T12 ledger 派发记录缺完整 `requested_model/status/source/agent_id` 父工具回执。 |
| SE-I05 | Important | partially_fixed | checker 有版本正反 fixture，但 Crawler4j 未读 manifest lock/执行结构 smoke，Stratix 未读 lock/执行 help 与 doctor。 |
| SE-M01 | Minor | verified_fixed | manifest validator 真实执行正反样例。 |
| SE-M02 | Minor | verified_fixed | AST checker 与直接执行测试存在；首轮未覆盖 lambda。 |
| SE-M03 | Minor | verified_fixed | DOCX/XLSX 最小 package 往返实测。 |

## 新 Finding

`SE-NEW-M01` / Minor：`check_code_shape.py::ShapeVisitor` 未处理 `ast.Lambda`，函数体内 lambda 可绕过禁止函数套函数。修复位置为 `ShapeVisitor.visit_Lambda` 与 `tests/test_code_shape_check.py`。

## 首轮 Gate

- remaining: `C0/I2/M1`
- gate_decision: `changes_requested`
- 下一步：补完整父工具回执；兼容检查执行 lock + CLI smoke；补 lambda 回归，然后由本专家复审这些结论。

## 定向复审补充

- `SE-I04`：`verified_fixed`。ledger `E043`–`E045` 以原 dispatch ID 完整记录 requested model/effort、fork、canonical task、accepted 与 parent_tool_receipt；`E046` 验证 3/3、JSON 与唯一键。
- `SE-I05`：`verified_fixed`。Crawler4j 不猜 manifest schema，实际执行 version/structure；Stratix 读取 pnpm lock 后实际执行 help/doctor；正反 CLI fixture 证明失败关闭和不兼容跳过 smoke。
- `SE-NEW-M01`：`verified_fixed`。`ShapeVisitor.visit_Lambda` 拒绝函数体 lambda，模块级 lambda 不误判。
- 分数更新：crawler4j `82→94`、stratix-service `82→94`、tdd-workflow `93→96`、using-shanforge `83→94`；其余 34 项不变。
- after 平均 `90.1`；before `80.6`；delta `+9.5`。
- remaining/new C/I/M：`0/0/0`；最终 `gate_decision: approved`。
