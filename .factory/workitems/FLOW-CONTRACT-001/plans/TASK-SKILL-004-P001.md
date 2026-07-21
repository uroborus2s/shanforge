# TASK-SKILL-004-P001 工作 Skill 状态信封去重计划

**目标：** 移除 32 个工作 Skill 重复携带的 `project_position`、`completion_level`、`stop_reason`、`scope_remaining`，让工作 Skill 只返回本职结果包，由 `using-shanforge` 结合 ledger 统一生成项目状态信封。

**架构：** `using-shanforge` 是项目状态信封唯一 owner；32 个工作 Skill 通过同一 reference 复用回写边界，不再复制字段和流程语义。正式统一任务包保持 `work_item/task/status/outputs/evidence/ledger_event/needs`，不修改产品 `src/` 或恢复 runtime Skill manager。

**技术栈：** Markdown Skill、pytest 文本契约测试、fresh-context 黑盒 eval、Skill validator、Ruff、mypy。

**工作项：** `FLOW-CONTRACT-001 / TASK-SKILL-004`

**状态：** `user_authorized_required_overlap_ready_for_local_commit`

## 输入

- 用户明确要求处理第二批“32 个工作 Skill 重复携带项目状态字段”。
- 上游：TASK-SKILL-002 曾为精确 32 个工作 Skill 增加四字段；TASK-SKILL-003 已把简单任务与项目化流程分流。
- 正式设计：`docs/05-design/workflow-execution-design.md` 的统一任务包不包含四个项目状态信封字段。
- 当前 owner：`skills/using-shanforge/SKILL.md`。

## 范围

### 目标

- 精确 32 个工作 Skill 删除重复四字段和重复项目化边界正文。
- 每个工作 Skill 只保留一条指向总控回写契约的链接，原专业输出契约不变。
- 对 32 个 Skill 在重复尾块之前的完整专业正文冻结 SHA-256；任何 status、needs、blocked、权限、人工决策或专业步骤漂移都使测试失败。
- 新建总控 reference，定义工作结果包、项目状态信封、真实阻塞与人工 Gate 的 owner。
- 修改 `using-shanforge`：工作 Skill 返回本职结果；总控再补项目位置、完成层级、停止原因、剩余范围和唯一下一动作。
- 同步正式设计、契约测试、黑盒 transcript、evidence、review、ledger 和最小 memory 索引。

### 非目标

- 不修改 6 个流程 owner Skill 的自身项目状态输出。
- 不改变 32 个 Skill 的 frontmatter、触发、专业步骤、status 枚举、outputs/evidence/needs 或真实人工决策边界。
- 不修改 `src/`、产品 API、正式需求数量、候选身份、发布、远端或部署。
- 不新增中心 dispatcher、registry、runtime Skill manager 或仓库级流程脚本。

## 文件与 owner

### 创建

- `skills/using-shanforge/references/work-skill-return-contract.md`：工作结果包与项目状态信封的唯一共享合同。
- `tests/test_work_skill_status_envelope_ownership.py`：精确 32 个 Skill 的去重、owner 契约与逐 Skill 专业正文 SHA-256 冻结。
- TASK-SKILL-004 plan、brief、evidence、reports、reviews。

### 修改

- `skills/using-shanforge/SKILL.md`：两段式回写与 reference 入口。
- `docs/05-design/workflow-execution-design.md`：统一任务包 owner 说明。
- `tests/test_remaining_skill_project_status_contract.py`：把“32 个 Skill 必须携带四字段”反转为“必须引用共享合同且不得携带四字段”。
- 计划中沿用 TASK-SKILL-002 的精确 32 个 `skills/*/SKILL.md`。
- `.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`、`.factory/memory/review-ledger.jsonl` 和三个最小 summary。
- review、verification 和 memory sync 闭环后，按 `gitcommitzh` 只提交可安全分离的当前任务改动。

## 含义保留清单

- 目标：只收敛项目状态信封 owner，不改变专业能力。
- 触发：32 个 frontmatter 和原触发条件不改。
- 输入：原 reference、工具、项目文件和用户输入不改。
- 步骤：专业流程、验证、错误处理和真实人工决策不改。
- 输出：保留原本职 `status/outputs/evidence/ledger_event/needs`；删除由总控生成的四字段。
- 标识：`task_id/task_type` 属于正式统一任务包，`skill` 是执行者身份；共享 reference 只解释关系，不强制 32 个 Skill 归一化原输出字段。
- 禁止项：原安全、版权、权限、发布、删除和技术栈限制不削弱。
- 例外：工作 Skill 仍可返回本地 `blocked`、`needs_user_input` 或 human-confirmation need；是否形成项目 Gate 和停止由总控结合 ledger 判断。
- 验收：精确 32/32 去重，owner/reference/正式设计一致，定向、相邻、黑盒和独立 review 通过。
- 风险：误删原专业 output 或真实人工 Gate；通过精确块替换、含义扫描和相邻测试防护。
- handoff：工作 Skill 返回结果包；总控生成用户可见项目状态信封和唯一下一动作。

## T01：工作 Skill 状态信封 owner 收敛

- 设计方案：共享 reference 单一 owner；32 个消费者只保留链接。
- 接口设计：工作结果包为 `work_item/skill/status/outputs/evidence/ledger_event/needs`；总控信封为 `project_position/completion_level/stop_reason/scope_remaining/next_required_action`。
- UI：`N/A`，只修改 Skill/流程合同和测试，没有产品界面。
- 测试设计：先反转旧测试并新增 owner 测试，确认当前 32 个重复块导致 RED；为每个 Skill 固化重复尾块之前的完整专业正文 SHA-256，保证实现只能替换尾块；再最小替换和同步总控/设计至 GREEN。
- 开发：精确修改 32 个工作 Skill、总控 Skill、共享 reference 和正式设计一处。
- 单测：运行两个状态契约测试、using-shanforge/任务语义/独立 review Gate 相邻测试。
- review：作者只到 `ready_for_review`；由未参与实现的 reviewer 独立判定。
- 集成：Skill validator、Ruff、format、mypy、全仓 pytest、JSONL 和 diff check。

### RED

```bash
uv run pytest tests/test_remaining_skill_project_status_contract.py tests/test_work_skill_status_envelope_ownership.py -q
```

期望：当前 32 个 Skill 仍携带四字段、缺共享 reference，且总控工作结果包仍混入项目状态信封。

### GREEN

1. 创建共享 reference，并修改总控两段式回写协议。
2. 精确替换 32 个相同项目化状态边界块为一行共享合同引用。
3. 同步正式统一任务包 owner 说明。
4. 重跑 RED 命令、相邻回归和 fresh-context 黑盒 eval。
5. 写 evidence/report/ledger/memory，交独立 reviewer；同范围 finding 自动整改复审。

## 验证

- 定向：两个状态 owner 测试，其中新测试逐项校验 32 个专业正文 SHA-256、共享链接、四字段缺失和总控 owner。
- 相邻：`test_skill_progress_visibility_and_continuation.py`、`test_task_workflow_semantics.py`、`test_black_box_workflow_eval.py`、`test_independent_review_gate.py` 及全部 `test_*skill*.py`；继续覆盖 systematic-debugging、browser-control、gitcommitzh 等高风险专项语义。
- Skill：验证 `using-shanforge` 及 32 个 Skill。
- 静态：Ruff、format、mypy、`git diff --check`。
- 全量：`uv run pytest -q`；范围外失败如实记录，不在本任务篡改冻结候选。
- 未运行：产品 UI/E2E、远端、发布、部署；不在目标范围。本地 Git 提交在全部 Gate 闭合后按 `gitcommitzh` 执行。

## 评审门

- 计划评审：`approved_100_C0_I0_M0`；同一 reviewer 已确认 `P001-I-001`、`P001-M-001` 闭环
- 实现评审：首轮 `changes_requested_92_C0_I1_M0`；同一 reviewer 复审 `approved_100_C0_I0_M0`，`I-001` closed
- 验证：最终定向 `9`、Skill 相邻 `141`、流程相邻 `30`、黑盒 `10/10`、Skill validator、目标 Ruff/format、mypy、JSONL 与 diff check 通过；全仓 `1143 passed / 3 failed`，仅范围外 R002 冻结计数漂移
- 本地 Git：用户已明确授权纳入形成完整提交所必需的同文件上游内容；只提交 TASK-SKILL-004 候选文件集，不扩大到整个工作区
- 远端 / 发布 / 部署：`not_authorized`

## 计划自审

- 规格覆盖：32 个消费者、总控 owner、共享 reference、正式设计、测试和黑盒均有落点。
- 占位符：无 TODO/TBD 或未定义交付。
- 类型一致：工作结果包与项目状态信封分开，字段 owner 唯一。
- 可构建：文件、替换块、RED/GREEN 和验证命令明确。
- Shanforge Gate：evidence、独立 review、整改、ledger、memory 齐全。
- 作者结论：独立计划评审已批准，进入测试先行实现；作者未自批 approved。
