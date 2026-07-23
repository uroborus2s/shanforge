# T01 Review Feedback Triage

## 结论

首轮 7 项反馈均已对照当前代码和只读负例核实。Iteration 2 又发现 3 个同一合同
边缘问题，技术上成立，不涉及新的产品取舍，均在 T01 原文件边界内修复。

| ID | 严重度 | 技术要求 | 核实结果 | 决定 |
|---|---|---|---|---|
| T01-C1 | Critical | domain 与 Schema 对必填字段、稳定 ID 保持一致 | 缺字段负例确实返回 `valid=true` | Fixed |
| T01-I1 | Important | 在解析符号链接前拒绝路径链中的 symlink | `resolve()` 后检查会丢失链接身份 | Fixed |
| T01-I2 | Important | Token 独立解析、限长和领域校验 | 原实现只检查路径存在 | Fixed |
| T01-I3 | Important | Schema 表达等待连接和已连接状态条件 | 原 Schema 缺少 `if/then` | Fixed |
| T01-I4 | Important | 补齐安全负例与既有 CLI 回归 | 原测试覆盖不足 | Fixed |
| T01-I5 | Important | 未过 Gate 前不能登记正式批准事实 | 文档版本历史与任务状态冲突 | Fixed |
| T01-M1 | Minor | 证据保存完整可复现命令 | 原证据使用 `...` | Fixed |
| T01-R2-C1 | Critical | states 必须逐项为 enum 字符串且唯一 | 重复和数字状态确实误判为有效 | Fixed |
| T01-R2-I1 | Important | 完整回归必须包含 repository/service 集成测试 | 旧 fixture 的空 Token 与新合同冲突 | Fixed |
| T01-R2-I2 | Important | Schema 路径自身也必须拒绝点段 | 原字符类允许 `..` | Fixed |

## 风险判断

- 不改变用户已经确认的“一份 UX/UI 人类文档 + 机器附件”方案。
- 不创建伪 `.penpot`。
- 不引入新的运行时依赖。
- Token 读取继续限制为 4 MiB，损坏 JSON、路径逃逸和符号链接失败关闭。
