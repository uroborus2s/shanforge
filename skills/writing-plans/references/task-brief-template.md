# 任务简报

## 工作项

- 工作项：
- 任务：
- 状态：`draft | active | ready_for_review | approved | changes_requested`
- 优先级：`P0 | P1 | P2`
- 任务层级：`project | requirement | cross_cutting | system`
- 关联目标：
  - `<稳定 ID；按任务层级声明一个或多个目标>`
- 强关系：`IMPLEMENTS | DEPENDS_ON | N/A`
- 上游计划：
- 流水账：

## 目标

用 1-3 句说明本任务必须完成的可观察结果。

## 输入

- 已批准计划：
- 相关规格 / 需求 / 设计：
- 必读文件：
- 可选参考：

## 允许修改

- `exact/path`

## 禁止修改

- 与本任务无关的文件。
- 用户已有未归属本任务的脏改动。
- 分层边界外的实现。

## 实施步骤

1. 读取必要文件并确认依赖。
2. 新增行为或 Bug 先写最小失败检查；已有测试足以覆盖时直接复用。
3. 写最小实现。
4. 运行必要的定向单元测试或静态检查。
5. 返回实现内容、真实测试结果、文件和 concerns。
6. 继续授权批次；只在跨会话恢复需要时写紧凑 checkpoint。

## 失败断言

- 发现占位语则失败。
- 未运行必要定向检查却声称完成则失败。

## 验证命令

```bash
<命令>
```

期望输出：

```text
<期望输出>
```

## 输出

- 实现内容：
- 测试结果：
- 修改文件：
- concerns：
- 可选 checkpoint：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`

## 完成口径

低、中风险任务完成后继续批次，不单独进入 review。只有高风险专项或批次质量候选可以写
`ready_for_review`；`approved` 必须来自适用的独立评审。
