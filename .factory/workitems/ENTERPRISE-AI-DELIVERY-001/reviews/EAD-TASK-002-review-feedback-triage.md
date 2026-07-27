# EAD-TASK-002 Review Feedback Triage

## 结论

5 项反馈均已对照任务卡和主契约核实，技术上成立，且可在已批准 T02 范围内修复。

| ID | Severity | 技术要求 | 核实 | 决定 |
|---|---|---|---|---|
| `I1` | Important | 增加稳定人员身份、决策身份、版本链和审计字段 | 当前只有 role，不能定位人或版本 | Fixed |
| `I2` | Important | 用封闭转移表定义 from/event/guard/to、退回和重开 | 箭头表达不足以验证 `INVALID_STATE` | Fixed |
| `I3` | Important | 为验收建立独立记录类型和追踪关系 | 当前只有无类型的验收证据 | Fixed |
| `I4` | Important | 明确 memory 写入授权并隔离共享文件 hunk | task brief 未列 memory | Fixed |
| `M1` | Minor | 以真实可执行命令和负例替换占位验证 | evidence 命令不可复跑 | Fixed |
| `I5` | Important | 固定 digest 前像、JCS 序列化、排除字段和 mismatch 拒绝 | Iteration 2 发现摘要会被追加审计影响 | Fixed |
| `M2` | Minor | 补 actor、AI reviewer、revision、digest、redaction 负例 | Iteration 1 只覆盖状态负例 | Fixed |
| `I6` | Important | 统一业务字段 JSON 结构、正式 schema_version 和 golden digest | Iteration 3 发现契约顶层字段与 validator 嵌套字段不一致 | Fixed |

## 边界核对

- 不需要产品取舍或新增外部系统。
- 不改变 Web、数据库、API 或 UI baseline。
- memory 同步是既有流程动作；只增加精确文件授权和 hunk 暂存约束。
- 不引入 schema 框架或运行时实现，仅增加一个 stdlib 验证脚本。
