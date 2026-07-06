# 项目组成员与 RACI

| 成员 / 角色 | 项目角色 | 责任 | RACI |
|---|---|---|---|
| 用户 / 项目负责人 | 赞助人与最终确认人 | 明确目标、确认阶段结果、批准关键变更 | A |
| `using-shanforge` | 流程总控 / CTO | 判断当前阶段、读取最小状态、选择下一步、处理人工确认门 | R |
| `project-memory` | 记忆管理员 | 恢复上下文、压缩状态、同步 memory | R |
| 工作 skill | 实现者 | 完成本职任务并回写状态、产物、证据和 needs | R |
| reviewer / review skill | 独立评审者 | 判断 `approved` 或 `changes_requested` | A |
| verification skill | 质量验证者 | 生成完成声明前的新鲜验证证据 | R |
| `gitcommitzh` | 提交执行者 | 在用户明确授权后按任务范围提交 | R |

R = 负责；A = 审批；C = 咨询；I = 知会。
