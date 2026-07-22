# TASK-REQ-006 R003 Review Response R004

## Fixed `R003-I-001`

R004 将权威授权状态检查设为 cache-hit、read、path return 和 HTML serve 的共同前置条件。未知、inactive、revoked 或授权检查不可用时全部 fail-closed，不返回 HTML 内容或文件路径。

授权事实提交为 revoked 后，任何后续服务决策必须立即拒绝；SQLite 行标记和磁盘删除仍可异步执行，因此清理延迟不再构成读取窗口。R004 同时固定拒绝 reason code，便于实现和测试不靠 AI 临场判断。

## Verification

验证证据见 `evidence/TASK-REQ-006-R004-review-fix-verification.md`。
