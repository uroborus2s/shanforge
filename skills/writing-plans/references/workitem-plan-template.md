# <功能名称> 实施计划

> **给执行者：** 计划评审通过后，把状态交还 `using-shanforge` 流程总控判断下一步。步骤使用复选框语法 (`- [ ]`) 便于追踪。

**目标：** <用一句话说明本计划要交付什么>

**架构：** <用 2-3 句说明实现方案、分层边界和接口归属方>

**技术栈：** <列出关键技术、框架、库和项目命令>

**工作项：** `<WORKITEM-ID>`

**状态：** `ready_for_review`

---

## 输入

- 已批准的规格 / 需求 / 设计：
- 当前工作项简报：
- 相关 `.factory/memory/` 摘要：
- 已读取的正式文档：

## 范围

### 目标

- <目标 1>

### 非目标

- <明确排除的工作>

## 文件

| 类型 | 路径 | 职责 |
|---|---|---|
| 新建 | `exact/path` | <为什么需要这个文件> |
| 修改 | `exact/path` | <这里改什么> |
| 测试 | `tests/exact/path` | <覆盖什么行为> |
| 文档 | `docs/exact/path` | <同步什么事实> |
| 记忆 | `.factory/memory/exact.summary.md` | <同步什么压缩事实> |

## 边界

- 层级：
- 领域：
- 接口归属方：
- 下游依赖：
- 禁止耦合：

## 任务

### 任务 N：<组件名称>

**文件：**

- 新建：`exact/path/to/file.py`
- 修改：`exact/path/to/existing.py`
- 测试：`tests/exact/path/to/test.py`
- 文档：`docs/exact/path.md`
- 记忆：`.factory/memory/exact.summary.md`

- [ ] **步骤 1：红灯，编写失败测试**

```python
def test_specific_behavior():
    result = function(input_value)
    assert result == expected_value
```

- [ ] **步骤 2：运行测试并确认失败**

运行命令：

```bash
pytest tests/exact/path/to/test.py::test_specific_behavior -v
```

期望输出：

```text
失败：缺失目标行为或契约错误
```

- [ ] **步骤 3：绿灯，编写最小实现**

```python
def function(input_value):
    return expected_value
```

- [ ] **步骤 4：运行测试并确认通过**

运行命令：

```bash
pytest tests/exact/path/to/test.py::test_specific_behavior -v
```

期望输出：

```text
通过
```

- [ ] **步骤 5：证据和记忆同步**

- 写入验证证据：`.factory/workitems/<WORKITEM-ID>/evidence/task-N.md`。
- 写入实现报告：`.factory/workitems/<WORKITEM-ID>/reports/task-N.md`。
- 更新任务流水账：`.factory/workitems/<WORKITEM-ID>/ledger.jsonl`。
- 更新相关 `.factory/memory/` 摘要。

- [ ] **步骤 6：评审门**

- 生成任务评审输入包。
- 实现者状态只能进入 `ready_for_review`。
- 评审状态只能由独立评审者写成 `approved` 或 `changes_requested`。

## 测试策略

- 红灯：
- 绿灯：
- 定向回归：
- 邻近回归：
- 全量回归：
- 未运行项：
- 未运行原因：

## 文档同步

- 正式文档：
- `.factory/memory/`：
- 工作项流水账：

## 评审门

用以下门禁判断计划是否可进入执行候选。

- 计划评审：`pending`
- 任务评审：`pending`
- 验证：`pending`
- 拉取请求 / 提交：`pending`
- 记忆同步：`pending`

## 计划自审

- 规格覆盖：
- 占位符扫描：
- 类型一致性：
- 可构建性：
- Shanforge 门禁：
