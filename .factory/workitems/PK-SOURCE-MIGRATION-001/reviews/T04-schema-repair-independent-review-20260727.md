# PK T04 Schema 修复独立评审

- verdict：`changes_requested`
- score：`86 / 100`
- C/I/M：`0 / 1 / 0`
- reviewer_type：`independent_subagent`
- reviewer_id：`/root/enterprise_delivery_review`
- independence：未参与实现；仅审阅指定输入、限定 diff，并运行只读复现与验证；未写
  文件、Git index 或外部系统。

## I1：`Task:` 身份字段被误判为目标

`_TASK_BRIEF_SECTION_KEYS` 将 `task` 映射为 `goal`，同行字段解析也复用该映射。因此
只含 `Task:` 和 `Status:` 元数据的任务简报会得到伪造的 `goal`，绕过 Registry
任务语义完整性门。

要求在保持单一语义别名表的前提下，让同行解析排除任务身份字段，并补
`Task + Status` 专门负例；修复前不能达到 `C0/I0`。

## 已通过

- 同行别名、空值缩进列表、普通未知字段负例和唯一真实缺失目标。
- `markdown-v4` 首次全量失效。
- 五文件 `65 passed`，Ruff format/lint、Mypy 290、JSON/JSONL、diff-check。
- 最终快照 `generation:2cd90dcc...9a044`。
- Chrome 5 页 × 2 视口 `10/10`，无横向溢出或控制台错误。
- API 与发布 `N/A` 合理。
