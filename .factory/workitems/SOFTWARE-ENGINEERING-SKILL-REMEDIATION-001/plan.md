# 软件工程 Skill 审计整改实施计划

**目标：** 修复审计发现的跨 Skill 矛盾，让 AI 能基于真实 WBS、TaskCard、状态、测试和 Bug 事实输出用户看得懂的进度与修复说明。

**工作项：** `SOFTWARE-ENGINEERING-SKILL-REMEDIATION-001`

**状态：** `completed`

**风险：** `medium`。不涉及产品运行时、生产系统、数据迁移或外部发布，但会修改多个软件工程 Skill 的公共协作合同。

## 先解释问题究竟是什么

当前不是“少写了一段说明”，而是五类事实之间没有完全对齐：

1. 计划模板没有稳定生成进度页面需要的 WBS 和任务身份。
2. `approved`、`done`、`ready_for_review` 在评审、开发任务和产品进度里含义不同，却被混在一起使用。
3. 有的 Skill 说普通任务不用保存 evidence，有的检查清单又要求任何完成都必须保存 evidence。
4. 总控要求回复必须说明进度、验证、Bug 和下一动作，但部分工作 Skill 只返回状态码和路径。
5. 部分工具型 Skill 假设脚本、CLI 或版本一定存在，实际不存在时仍给出不可执行步骤。

因此修复必须先改事实合同，再改会话措辞；否则会话写得再漂亮，也可能是在清楚地描述错误状态。

## Work Breakdown

| id | parent_id | title | status |
|---|---|---|---|
| WBS-REM-01 |  | 让计划稳定产生 WBS 和任务身份 | completed |
| WBS-REM-02 | WBS-REM-01 | 分离评审状态、任务状态和产品完成状态 | completed |
| WBS-REM-03 | WBS-REM-02 | 统一子代理回执和验证证据规则 | completed |
| WBS-REM-04 | WBS-REM-03 | 保证会话一定拿到进度、测试和 Bug 事实 | completed |
| WBS-REM-05 | WBS-REM-04 | 统一 Go/Python 的定向与全量验证边界 | completed |
| WBS-REM-06 | WBS-REM-05 | 修复工具不存在时仍继续执行的问题 | completed |
| WBS-REM-07 | WBS-REM-06 | 为固定版本生态增加版本探测和失败关闭 | completed |
| WBS-REM-08 | WBS-REM-07 | 运行跨 Skill 行为回归和独立评审 | completed |

## 执行顺序和用户能看到的变化

| 顺序 | 修复后用户能看到什么 | 对应任务 |
|---:|---|---|
| 1 | 任何项目回复都能说清 WBS 第几步、当前 TaskCard、真实下一动作 | T01 |
| 2 | “评审通过”不会再被误报成“功能完成” | T02 |
| 3 | AI 能区分开发者回执、可评审状态和真实测试证据 | T03 |
| 4 | 开发、测试、Bug、修复回复都有必需事实，humanizer 不会删除状态结构 | T04 |
| 5 | 小修改只报定向测试，批次/高风险才报全量测试；未运行范围写清楚 | T05 |
| 6 | 脚本或 CLI 不存在时明确阻塞，不再输出无法执行的命令 | T06 |
| 7 | Crawler4j/Stratix 等版本不匹配时停止并说明差异 | T07 |
| 8 | 用完整场景证明以上行为能连起来工作 | T08 |

## T01：让计划、TaskCard 和进度页面使用同一套身份

**问题：** `writing-plans` 要求已有 WorkItem/TaskCard，却又允许创建临时 ID；计划模板没有稳定输出快照脚本要求的四列 WBS，session/ledger 模板也没有把任务身份放在固定位置。

**修改文件：**

- `skills/writing-plans/SKILL.md`：删除临时 ID 分支；缺身份时返回登记需求。
- `skills/writing-plans/references/workitem-plan-template.md`：固定生成 `id | parent_id | title | status` 的 `Work Breakdown`。
- `skills/writing-plans/references/task-brief-template.md`：把 `task_card_id`、`wbs_id`、`current_gate`、`next_required_action` 放到头部必填区。
- `skills/writing-plans/references/plan-review-template.md`：缺 WBS、TaskCard 映射或恢复字段时评审失败。
- `skills/project-memory/references/session-card-template.md`、`memory-ledger-event-template.md`：同步相同身份字段。
- `tests/test_writing_plans_skill.py`、`tests/test_project_memory_skill.py`、`tests/test_using_shanforge_snapshot.py`：增加模板到快照的贯通测试。

**完成标准：** 用正式模板生成一个最小计划和 ledger 后，快照能读出 WBS、当前 TaskCard 和唯一下一动作；缺任何身份字段时测试失败。

## T02：分离“评审通过”和“任务完成”

**问题：** `approved` 同时被当作 review 结论、TaskCard 状态和 WBS 完成状态，可能把“代码审查通过”误显示为“产品功能已完成”。

**修改文件：**

- `skills/writing-plans/references/task-brief-template.md`：生命周期只用 `planned/active/ready_for_review/completed/closed/blocked`。
- `skills/requesting-code-review/references/task-review-template.md`：`approved` 只写入 `review_status`。
- `skills/using-shanforge/scripts/project_snapshot.py`：修改 `_category()`、`_effective_event()` 和 `_plan_stages()`；产品完成只认 `completed/closed/superseded`，不认 review approved。
- `skills/using-shanforge/references/pm-dashboard-rendering.md`：记录上述状态映射。
- `tests/test_using_shanforge_snapshot.py`、`tests/test_review_workflow_skills.py`：加入“review approved 但 TaskCard 未完成”的反例。

**完成标准：** review approved 时页面仍显示任务待完成；只有 TaskCard 进入 completed/closed 后才增加产品完成度。

## T03：统一子代理状态和测试证据

**问题：** worker 可以返回 `DONE`，控制器却只接受 `ready_for_review/blocked/needs_user_input`，中间没有映射；普通任务 evidence 是否必须落盘也存在冲突。

**修改文件：**

- `skills/subagent-driven-development/SKILL.md`：增加 worker receipt → 控制器状态映射表；`DONE` 只能表示任务实现结束，不能表示项目完成。
- `skills/verification-before-completion/SKILL.md`：普通低中风险任务允许命令回执；批次、里程碑、高风险和关闭声明必须落盘 evidence。
- `skills/verification-before-completion/references/completion-claim-checklist.md`：与主文使用同一规则。
- `skills/using-shanforge/references/work-skill-return-contract.md`：明确 receipt、verification 和 completion 的边界。
- `tests/test_execution_workflow_skills.py`、`tests/test_verification_debugging_workflow_skills.py`、`tests/test_work_skill_status_envelope_ownership.py`：锁定映射和 evidence 分级。

**完成标准：** 每种 worker 状态有唯一控制器结果；普通任务、批次和项目关闭三种场景分别得到正确 evidence 要求。

## T04：保证会话一定拿到可读事实

**问题：** 总控要求三段式进度回复，但 `humanizer` 可能把三段式当成 AI 痕迹删除；`brainstorming` 又可能要求每个章节都停下来确认；工作 Skill 的局部状态模板没有强调必须补齐进度、验证和 Bug 字段。

**修改文件：**

- `skills/humanizer/SKILL.md`：保护 Shanforge 的三段式语义，只润色段内文字。
- `skills/brainstorming/SKILL.md`：只有改变目标、范围、验收或不可逆取舍时才合并成一次确认。
- `skills/using-shanforge/references/work-skill-return-contract.md`：明确局部状态模板只是专业增量，必须合并 `human_summary/progress_delta/verification_summary/defect_summary/change_locations`。
- `skills/using-shanforge/references/human-readable-status.md`：为开发、测试、Bug、修复各给一个最小必填示例。
- 新建 `tests/test_human_response_contract_integration.py`：输入开发 partial、测试 failed、Bug root cause 和修复完成四类状态，断言最终回复字段齐全且只有一个下一动作。

**完成标准：** 四类代表性会话都能直接回答“做到哪、什么没做、测试怎样、Bug 原因、改哪里、下一步是什么”。

## T05：统一 Go/Python 的测试范围

**问题：** Go/Python Skill 默认要求每次都跑全量检查，与总控“普通修改定向验证、批次集中全量验证”的规则冲突。

**修改文件：**

- `skills/go-developer/SKILL.md`：普通低中风险修改默认 gofmt、受影响包测试和必要 vet；批次/高风险/发布才跑 `go test ./...`。
- `skills/python-uv-project/SKILL.md`：普通修改默认受影响 pytest、Ruff 和必要 mypy；批次/高风险/发布才跑完整集合。
- `tests/test_go_developer_skill.py`：锁定 Go 风险分级命令。
- 新建 `tests/test_runtime_skill_verification_scope.py`：锁定 Python 定向/全量边界和未运行项报告。

**完成标准：** 小修改不会被无关全仓检查阻塞；回复仍明确写出哪些全量检查未运行及原因。

## T06：工具不存在时必须停止，而不是继续给命令

**问题：** `art-asset-pipeline` 引用不存在的脚本，browser/Office 类 Skill 也常假设 CLI 或库已经可用。

**修改文件：**

- `skills/art-asset-pipeline/SKILL.md`：删除对不存在 `remove_chroma_key.py` 的硬承诺；透明背景工具不可用时返回明确 blocked，不伪造完成。
- `skills/browser-control/SKILL.md`：先探测 browser-use/插件/Computer Use，再选择真实可用入口。
- `skills/docx/SKILL.md`、`skills/pdf/SKILL.md`、`skills/xlsx/SKILL.md`：增加依赖探测、选择顺序和全部不可用时的 blocked 回执。
- `tests/test_browser_control_skill.py`：覆盖 browser-use 不存在和插件可用的分支。
- 新建 `tests/test_external_tool_skill_fallbacks.py`：覆盖资源、DOCX、PDF、XLSX 的失败关闭合同。

**完成标准：** 工具不存在时回复准确列出缺失能力和唯一解决动作，不再输出假定可运行的命令。

## T07：固定版本 Skill 必须先核对真实版本

**问题：** Crawler4j 和 Stratix 把精确版本写死在说明里；上游版本变化后可能继续指导用户运行旧命令。

**修改文件：**

- `skills/crawler4j-model-project/SKILL.md`：执行前核对 CLI/manifest 协议版本，不匹配即 blocked。
- `skills/stratix-service/SKILL.md`：以 package.json/lockfile/已安装包回读版本，不匹配时输出差异，不沿用旧命令。
- `skills/stratix-admin-web/SKILL.md`：同步生成器版本探测合同。
- `tests/test_crawler4j_model_skill_integration.py`、`tests/test_stratix_service_skill.py`、`tests/test_stratix_service_framework_guide.py`、`tests/test_stratix_admin_web_skill.py`：加入版本不匹配反例。

**完成标准：** 支持版本通过，未知或不兼容版本明确 blocked，并显示检测到的版本与要求版本。

## T08：集中质量门

**目标：** 证明 T01–T07 不是文字各自正确，而是能连成一个完整开发会话。

**验证：**

1. 运行 T01–T07 所有定向测试。
2. 运行 `uv run pytest -q`。
3. 运行 `uv run ruff check skills tests`。
4. 运行全部 38 个 Skill validator。
5. 执行最小黑盒场景：创建计划 → 生成 TaskCard/ledger → worker partial → 测试失败 → Bug 根因 → 修复位置 → review approved → TaskCard completed → 最终回复。
6. 独立 reviewer 核对 Critical/Important；存在任一未关闭 Important 时不得完成或提交。

**完成标准：** 全部命令 exit code 0；黑盒回复能让用户不读内部状态码就看懂进度、未完成项、测试、Bug 根因、修复文件/符号和唯一下一动作。

## 计划自审

- 审计 Finding 均映射到 T01–T07；T08 负责集中质量收口。
- 每个任务有精确文件、行为、测试和完成标准。
- 执行顺序有依赖：T01 → T02 → T03 → T04 → T05 → T06 → T07 → T08。
- 没有把整改计划写成已经完成。
- 用户已于 2026-09-01 明确授权按顺序执行 T01–T08；T01–T08 均已完成验证和独立评审。
