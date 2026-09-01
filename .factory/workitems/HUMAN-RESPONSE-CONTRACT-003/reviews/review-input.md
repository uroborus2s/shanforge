# HUMAN-RESPONSE-CONTRACT-003 独立评审输入

## 目标

评审修复定位字段和代码形状禁令是否清楚、可执行、不会伪造或误伤正常代码结构。

## 输入

- `brief.md`
- `plan.md`
- T01 allowlist 的当前 diff
- `evidence/verification.md`

## 必查边界

- 修复说明能定位到实际文件和函数/方法/符号；无函数边界时使用真实模块/配置/章节。
- 调试尚未实施修复时不得输出虚假修改位置。
- 禁止函数/方法体内定义局部函数，不禁止正常函数调用组合。
- 单调用点且无独立职责的公共 helper 必须内联；真实框架入口、接口、回调或资源边界不误删。
- `code_shape_check` 的 `not_applicable` 仅用于未修改代码。
- 用户指南保持候选，不冒充正式发布。

## 输出

- `approved | changes_requested`
- Critical / Important / Minor；只有 Critical=0 且 Important=0 才通过。
