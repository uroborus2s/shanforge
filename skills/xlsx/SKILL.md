---
name: xlsx
description: 读取、分析、修改、格式化、生成或验证 Excel / `.xlsx` / `.xls` / `.csv` 文件时使用。只在用户明确要求电子表格交付物、Excel 文件处理、工作簿格式或表格数据文件时触发；普通数据解释不自动接管。
---

# Excel / XLSX 处理

## 任务分支

| 分支 | 动作 |
|---|---|
| 读取 / 结构检查 | 用 `pandas.ExcelFile` 或 `openpyxl.load_workbook` 读取 sheet 名、列名、行数和前几行；不要把二进制 Excel 当文本读。 |
| 数据分析 | 用 `pandas` 计算汇总、筛选、透视或导出；保留脚本或命令摘要。 |
| 修改现有工作簿 | 用 `openpyxl`，尽量保留格式、公式、合并单元格和多 sheet 结构。 |
| 创建新工作簿 | 用 `pandas` 或 `openpyxl` 写新文件；需要样式、列宽、冻结窗格或公式时用 `openpyxl`。 |
| CSV 编码 | 中文 CSV 先识别或尝试 `utf-8`、`gbk`、`gb18030`；不要静默丢字符。 |
| 验证 / 重算 | 读取输出文件，核对 sheet、列、行数、关键公式和值；需要时运行 `python scripts/recalc.py` 或 `python scripts/office/validate.py output.xlsx`。 |

## 安全写入

- 默认写新文件，例如 `input_modified.xlsx`、`input_filtered.xlsx`、`output.xlsx`。
- 除非用户明确要求，不覆盖原始工作簿或 CSV。
- 修改前先读取 workbook 结构；多 sheet 文件不能只看第一个 sheet 就改。
- 涉及公式、隐藏 sheet、合并单元格、筛选器、样式或图表时优先 `openpyxl`，不要用 `pandas` 重写整个工作簿。
- 大文件只读取必要列或分块处理；无法完整验证时报告 partial。

## 最小示例

```python
import pandas as pd

xl = pd.ExcelFile("data.xlsx")
print(xl.sheet_names)
df = pd.read_excel("data.xlsx", sheet_name=0)
print(df.head().to_markdown(index=False))
```

```python
from openpyxl import load_workbook

wb = load_workbook("input.xlsx")
ws = wb.active
ws["A1"] = "updated"
wb.save("input_modified.xlsx")
```

## 输出清单

交付时列出：

- 输入文件路径、sheet 数和处理的 sheet。
- 输出文件路径。
- 行数、列数、筛选条件、公式或格式修改摘要。
- 编码判断和转换结果（CSV 时）。
- 验证命令和结果。

## 验证

- 重新打开输出文件。
- 核对 sheet 名、行数、列名、关键单元格、公式和值。
- 格式修改要抽查列宽、样式、冻结窗格、合并单元格或条件格式。
- CSV 要检查编码和特殊字符。

## 失败处理

- 文件缺失、损坏、密码保护或依赖缺失：`status: blocked`，写清失败命令。
- sheet、列名、输出路径或覆盖意图不明确：`status: needs_user_input`。
- 写入成功但重读验证失败：`status: blocked`。
- 只完成部分 sheet 或部分行：报告 partial，并列出未处理范围。

## Shanforge 状态包

```text
工作结果：
- work_item: <WORKITEM-ID>
- skill: xlsx
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <output.xlsx/csv>
- evidence:
  - <structure/readback/recalc/validate summary>
- ledger_event: <event id or none>
- needs:
  - review | verification | user_input | none
```
