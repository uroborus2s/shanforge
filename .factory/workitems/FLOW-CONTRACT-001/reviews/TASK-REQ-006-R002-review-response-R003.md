# TASK-REQ-006 R002 Review Response R003

## Fixed `R002-I-001`

R003 将 `RenderViewScope/v1` 与 `RenderInputFingerprint/v1` 分离。文件路径和唯一行只由稳定 scope 决定；fingerprint 只决定是否刷新同一个 `current.html`。R001 的每类 3 份默认值被显式覆盖为每 scope 1 份。

## Fixed `R002-M-001`

R003 无条件禁止不同 `authorization_digest` 复用 HTML，并要求权限摘要预登记、撤销后清理。

## Verification

验证证据见 `evidence/TASK-REQ-006-R003-review-fix-verification.md`。
