# SKILL-FIRST-PM-001-T01：迁移 PM 快照并删除平台 runtime

- 类型：实现
- 层级：system
- 优先级：P0
- 状态：verified_ready_for_commit
- 目标：以最小 skill-local 脚本替代 Shanforge 源码运行时，并在 ITA Club 完成真实进度查询。
- 验证：先写脚本行为测试并观察失败，再实现、运行 ITA Club 快照、删除 runtime、执行保留测试和引用扫描。
- 禁止：修改 ITA Club 业务代码；提交范围外脏改动；远端 Git 动作。

## 看板验收

1. 首屏先说明当前重点、工作项目标、当前任务和下一步，不以内部状态码代替业务说明。
2. 工作项按“需要关注、正在推进、后续待办、已完成”分组；
   `needs_user_input` 不得归入普通待办，`superseded` 必须归档。
3. 当前 task brief 已登记的信息必须显示任务层级、优先级、需求关系、任务目标和完成标准。
4. 没有 brief 和 ledger 的分组目录不显示为工作项；原始 ID 和状态放入折叠技术区。
5. 390×844 与 1440×900 下无页面级横向溢出，键盘可访问跳转链接和折叠区，
   浏览器控制台无错误。
- 实现证据：`../evidence/SKILL-FIRST-PM-001-T01-verification.md`
- 实现报告：`../reports/SKILL-FIRST-PM-001-T01-implementer-report.md`
- 审查输入：`../reviews/SKILL-FIRST-PM-001-T01-review-input.md`
