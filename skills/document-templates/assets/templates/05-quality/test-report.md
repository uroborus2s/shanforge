# 测试报告

## 1. 报告控制

| 字段 | 内容 |
|---|---|
| 报告 ID / 版本 | `TEST-REPORT-xxx` / `1.0.0` |
| 文档状态 | 草稿 \| 评审中 \| 已批准 \| 已废弃 |
| Owner / 主要读者 |  |
| 上游测试计划 |  |
| WorkItem / run ID |  |
| 精确候选 | commit SHA / digest / 不可变版本 |
| 环境别名 | 不写完整地址、IP、端口或凭证 |
| 执行时间 | 带时区起止时间 |
| 批次验证结论 | passed \| partial \| failed \| blocked |

## 2. 范围与追踪

- 测试范围：
- 明确未测范围与原因：
- 需求 / 验收标准：
- 关联任务 / 缺陷：

## 3. 准入与准出

### 准入条件

| 条件 | 结果 | 证据 |
|---|---|---|
| 候选、环境、数据和入口已冻结 | passed / failed / blocked |  |

### 准出条件

| 条件 | 结果 | 证据 |
|---|---|---|
| 必需测试完成且阻断问题关闭 | passed / failed / blocked |  |

## 4. 环境健康与清理

| 环境别名 | 启动 / 就绪 | 健康检查 | 关闭 / 产物清理 | 结果 |
|---|---|---|---|---|
|  |  |  |  | passed / failed / N/A（原因） |

## 5. 结果汇总

| 总数 | 通过 | 失败 | 错误 | 阻塞 | 跳过 | 未运行 | 取消 |
|---:|---:|---:|---:|---:|---:|---:|---:|
|  |  |  |  |  |  |  |  |

案例结果只使用 `passed / failed / error / blocked / skipped / not_run / cancelled`。批次验证结论单独使用 `passed / partial / failed / blocked`。

## 6. 需求覆盖

| 需求 / 验收标准 | 案例 ID | 结果 | 证据 | 缺口 |
|---|---|---|---|---|
|  |  |  |  |  |

## 7. 未通过与未执行项

| 案例 ID | 状态 | 未运行 / 跳过原因 | 缺陷 ID | Owner | 证据引用 |
|---|---|---|---|---|---|
|  | failed / error / blocked / skipped / not_run / cancelled |  |  |  |  |

## 8. 缺陷历史与残余风险

| 缺陷 / 风险 | 严重度 | 状态 | 处置或接受人 | 证据引用 |
|---|---|---|---|---|
|  | Critical / Important / Minor |  |  |  |

## 9. 发布建议

- 建议：GO | NO-GO
- 依据：
- GO 条件或 NO-GO 解除条件：

## 10. 评审与批准

| 角色 | 姓名 / ID | 结论 | 时间 | 备注 |
|---|---|---|---|---|
| 编写 |  |  |  |  |
| 独立评审 |  | approved / changes_requested |  |  |
| 批准 |  | approved / rejected / not_required |  |  |

## 11. 版本历史

| 版本 | 日期 | 变更内容 | 修改人 | 审核 | 批准 |
|---|---|---|---|---|---|
| `1.0.0` | YYYY-MM-DD | 初版 |  |  |  |

案例步骤、请求 body、预期断言和完整日志保留在测试脚本或 evidence 中，不复制到本报告。不得记录完整内部 URL、IP、端口、凭证、令牌、DSN、账号、密码、个人信息或原始敏感日志。

## 12. 自动聚合校验

`<skill-dir>` 表示 `document-templates` skill 的实际安装目录。

里程碑、发布候选或用户明确要求的 WorkItem 报告定稿前运行：

```bash
uv run python <skill-dir>/scripts/validate_test_documents.py \
  --report <当前 WorkItem 测试报告路径>
```

校验器检查精确候选、七态计数之和、批次四态和 GO/NO-GO 一致性。普通小任务仍只保留命令摘要，不强制生成本报告。
