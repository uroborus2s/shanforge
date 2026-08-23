# Review Feedback Triage

## P0-REVIEW-I001

- 来源：独立 task review
- severity：Important
- 要求：正式文档解析测试必须锁定“已有登记优先，四模块只作新项目回退”的顺序和分支语义。
- 技术核实：`yes`；现有测试仅检查三个词汇存在，反向规则也可能通过。
- YAGNI：不新增解析器；只截取 `默认工作流` 段并检查登记分支、回退分支及顺序。
- 决定：`Fixed`

## P0-REVIEW-I002

- 来源：独立 task review
- severity：Important
- 要求：删除整文件 SHA 后，仍应证明工作 Skill 保留非占位的专业正文。
- 技术核实：`yes`；单个 `##` 标题不足以排除占位正文。
- YAGNI：不建立 32 项内容注册表；使用通用结构不变量，并为本批修改的四个 Skill 检查其专业流程/产物锚点。
- 决定：`Fixed`

## Minor

- Red/Green：在修复证据中补定向命令、exit code 和时间顺序摘要。
- Memory：正式 owner 为 `architecture.summary.md`、`tasks.summary.md`、`tests.summary.md`；已在并发工作项释放 memory/index 后同步本任务事实。

## P0-REVIEW-I003

- 来源：同 reviewer 的 memory 增量复核
- severity：Important
- 要求：追加保存已经发生的 `97 / C0-I0-M1` 首次复审及后续 `98 / C0-I1-M0` memory 复核，不得让当前态停在首轮 `87`。
- 技术核实：`yes`；两份 ledger 和六份当前态投影均落后一轮。
- YAGNI：只追加两条历史事件并推进现有投影，不新增状态系统。
- 决定：`Fixed`；同 reviewer 终审 `approved / 100 / C0-I0-M0`。
