---
name: xlsx
description: 处理 Excel 电子表格 (.xlsx, .xls, .csv)。用于读取、写入、分析、修改、格式化和创建 Excel 文件。当用户提到“电子表格”、“Excel”、“数据表”、“xlsx”或想要分析结构化数据时使用。
---

# Excel 处理 (XLSX)

此技能用于处理 Excel 文件。主要使用 Python (`pandas`, `openpyxl`) 来执行操作。

## 核心原则

1. **优先使用 Python**: 处理 Excel 文件时，始终编写并执行 Python 脚本，使用 `pandas` 或 `openpyxl` 库。不要尝试直接作为文本读取二进制文件。
2. **先检查结构**: 在对文件进行复杂操作之前，先读取 Sheet 名称和前几行数据 (`head()`) 以了解结构。
3. **保留格式**: 如果用户要求修改现有文件，尽量保留原有的格式（如单元格颜色、字体），除非用户另有说明。使用 `openpyxl` 而不是 `pandas` 进行纯格式修改通常更安全。
4. **中文支持**: 在读取或写入包含中文的 CSV 文件时，注意编码问题（通常尝试 `utf-8` 或 `gbk`/`gb18030`）。

## 常用操作指南

### 1. 读取数据 (Reading)

使用 `pandas` 读取数据是最快的方法。

```python
import pandas as pd

# 读取所有 Sheet 名称
try:
    xl = pd.ExcelFile('data.xlsx')
    print(f"Sheet names: {xl.sheet_names}")
    
    # 读取第一个 Sheet 或指定 Sheet
    df = pd.read_excel('data.xlsx', sheet_name=0)
    # 打印前几行，使用 markdown 格式以便在对话中清晰显示
    print(df.head().to_markdown(index=False, numalign="left", stralign="left"))
except Exception as e:
    print(f"Error reading excel: {e}")
```

### 2. 分析数据 (Analysis)

获取数据后，提供数据的摘要统计，帮助用户理解数据概况。

- 检查列名 (`df.columns`)
- 检查缺失值 (`df.isnull().sum()`)
- 检查数据类型 (`df.dtypes`)
- 基本统计 (`df.describe()`)

### 3. 修改和写入 (Writing)

写入文件时，确保不会意外覆盖用户的重要文件，除非那是明确的意图。建议先保存为新文件名（如 `_modified.xlsx`）。

```python
# 写入到新文件
df.to_excel('output.xlsx', index=False)
```

### 4. 格式化 (Formatting)

如果用户需要调整列宽、颜色或样式，或者需要操作复杂的 Excel 特性（如公式、合并单元格），请使用 `openpyxl`。

```python
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

wb = load_workbook('output.xlsx')
ws = wb.active

# 示例：自动调整列宽
for column in ws.columns:
    max_length = 0
    column_letter = get_column_letter(column[0].column)
    for cell in column:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        except:
            pass
    adjusted_width = (max_length + 2)
    ws.column_dimensions[column_letter].width = adjusted_width

wb.save('output_formatted.xlsx')
```

## 示例

**输入**: "帮我把这个 sales.xlsx 里的 'Amount' 这一列总和算一下，然后把超过 1000 的行存到一个新文件 high_value.xlsx 里。"

**执行步骤**:
1. 编写 Python 脚本读取 `sales.xlsx`。
2. 计算 `Amount` 列的总和并打印结果。
3. 筛选 `df[df['Amount'] > 1000]`。
4. 将筛选后的 DataFrame 保存为 `high_value.xlsx`。

## 故障排除

- **依赖缺失**: 如果环境缺少 `pandas` 或 `openpyxl`，请尝试使用 `pip install` 安装它们。
- **大文件**: 对于非常大的 Excel 文件，考虑使用 `chunksize` 参数分块读取，或仅读取需要的列 (`usecols`)。
