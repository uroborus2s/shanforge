# 测试案例目录

## 目录信息

| 字段 | 内容 |
|---|---|
| 目录 ID / 版本 | `TEST-CATALOG-xxx` / `1.0.0` |
| 项目 / 模块 |  |
| 定义状态 | draft \| active \| deprecated \| retired |
| Owner / 评审人 |  |
| 上游测试计划 |  |
| 最后更新 | YYYY-MM-DD |

## 案例索引

| 案例 ID | 名称 | 需求 / 验收标准 | 层级 | 优先级 | 风险等级 | 自动化入口 |
|---|---|---|---|---|---|---|
| `TEST-xxx-001` |  | `REQ-xxx` / `AC-xxx` | 单元 / 契约 / 集成 / E2E / UI / API / 发布 | P0 / P1 / P2 | high / medium / low | `tests/test_x.py::test_y` |

## 案例：`TEST-xxx-001`

- 名称：
- 版本：`1.0.0`
- 定义状态：draft | active | deprecated | retired
- 测试目标：
- 需求 / 验收标准：
- 关联设计 / API / UI / 任务：
- 测试类型与层级：
- 优先级：P0 | P1 | P2
- 风险等级：high | medium | low
- Owner：
- 环境别名：
- 自动化状态：automated | manual | planned
- 自动化入口：

### 前置条件

1. `<前置条件>`

### 测试数据 / fixture

| 数据 / fixture | 用途 | 敏感 | 准备 / 复位方式 |
|---|---|---|---|
|  |  | true / false |  |

### 步骤与判定

| 序号 | 操作步骤 | 预期结果 | 证据要求 |
|---:|---|---|---|
| 1 |  |  | 日志 / 截图 / 响应 / 命令回执的安全引用 |

### 后置条件与清理

- `<后置或清理条件>`

### 标签

- `<标签>`

案例定义不填写 `passed` 或 `failed`。运行后在当前 WorkItem evidence 中记录案例 ID、run ID、环境别名、精确候选、七态结果、缺陷 ID 和证据引用。

## 自动有效性校验

`<skill-dir>` 表示 `document-templates` skill 的实际安装目录。

案例目录定稿前运行：

```bash
uv run python <skill-dir>/scripts/validate_test_documents.py \
  --repo-root . \
  --catalog <项目测试案例目录路径>
```

校验失败时不得把目录标为 `active`。校验器检查索引与详情 ID 一致、必填字段与枚举有效、`automated` 案例的 pytest 文件/节点存在，以及每个步骤都有操作、预期和证据要求。
