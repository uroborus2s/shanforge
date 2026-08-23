---
name: pdf
description: 读取、提取、合并、拆分、生成、填写、加密、解密、OCR、渲染或验证 PDF 文件时使用。只因任务目标包含 `.pdf` 或 PDF 交付物而触发；普通文档写作、DOCX 和电子表格不由本 skill 接管。
license: 版权所有。完整条款请参阅 LICENSE.txt
---

# PDF 处理

## 任务分支

先按用户目标选分支，再选择工具。

以下 `<skill-dir>` 表示当前 `SKILL.md` 所在目录；执行前替换为该目录的实际绝对路径，不假设目标项目包含本 Skill 的 `scripts/`。

| 分支 | 动作 |
|---|---|
| 读取文本 | 先试 `pdftotext` 或 `pdfplumber`；需要保留版面时用 `pdftotext -layout`。 |
| 提取表格 | 用 `pdfplumber` 读取页和表格；导出表格时写 `.xlsx` 或 `.csv` 新文件。 |
| 合并 / 拆分 / 旋转 | 用 `pypdf` 或 `qpdf`，保持原 PDF 不动，输出新文件。 |
| 创建 PDF | 用 `reportlab` 生成；版式敏感时渲染页面图片检查。 |
| 表单填写 | 先读 `forms.md`，优先使用 `<skill-dir>/scripts/check_fillable_fields.py`、`<skill-dir>/scripts/extract_form_field_info.py` 和对应填表脚本。 |
| OCR / 扫描件 | 先确认普通文本不可提取，再使用 OCR；记录 OCR 置信风险，不把 OCR 当原文。 |
| 加密 / 解密 | 只在用户授权且拥有密码时执行；失败时不绕过权限。 |
| 验证 / 渲染 | 用 `qpdf --check`、页面渲染或 `<skill-dir>/scripts/create_validation_image.py` 做结构和视觉检查。 |

常用工具名保留：`pypdf`、`pdfplumber`、`reportlab`、`pdftotext`、`pdftoppm`、`pdfimages`、`qpdf`、`pytesseract`、`pdf2image`。

## 安全写入

- 默认写新文件，例如 `input_extracted.txt`、`input_merged.pdf`、`input_pages_1-5.pdf`、`input_filled.pdf`。
- 不覆盖源 PDF，除非用户明确要求且已说明不可逆风险。
- 合并、拆分和旋转前先读取页数；页码范围越界时停止。
- 解密、去水印、移除限制或修改签名相关内容必须有明确授权。
- OCR、表格识别和坐标填表都可能误读；输出必须标注方法和残余风险。

## 常用命令

```bash
pdftotext input.pdf output.txt
pdftotext -layout input.pdf output.txt
qpdf --check input.pdf
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
pdfimages -j input.pdf output_prefix
```

表单任务先从这里开始：

```bash
python <skill-dir>/scripts/check_fillable_fields.py input.pdf
python <skill-dir>/scripts/extract_form_field_info.py input.pdf field_info.json
python <skill-dir>/scripts/fill_fillable_fields.py input.pdf field_values.json output.pdf
python <skill-dir>/scripts/convert_pdf_to_images.py input.pdf images/
python <skill-dir>/scripts/fill_pdf_form_with_annotations.py input.pdf fields.json output.pdf
```

## 输出清单

交付时列出：

- 输入 PDF 和页数。
- 输出文件路径。
- 处理分支：文本、表格、合并、拆分、生成、OCR、表单或加密。
- 使用的命令或库。
- 验证结果：结构检查、页数检查、渲染检查、抽样页或 OCR 风险。

## 验证

- 结构：`qpdf --check output.pdf`。
- 页数：读取输入和输出页数，确认合并、拆分、旋转结果符合预期。
- 视觉：对生成、填写、水印、旋转和版式敏感结果渲染抽样页面。
- 提取：文本或表格结果抽样对照原页；扫描件注明 OCR 不是精确转录。

不能提取文本时先判断是否扫描件、加密或损坏。若需要 OCR、密码或人工确认，报告阻塞或待输入，不假装已完成。

## 失败处理

- 文件缺失、损坏、加密且无密码：`status: blocked`。
- 页码范围、字段坐标或输出格式不明确：`status: needs_user_input`。
- 验证失败或渲染不一致：`status: blocked`，保留失败输出用于排查。
- OCR 结果低可信：交付 partial，并列出需要人工复核的页。

## Shanforge 状态包

```text
工作结果：
- work_item: <WORKITEM-ID>
- skill: pdf
- status: ready_for_review | partial | blocked | needs_user_input
- outputs:
  - <output.pdf/txt/xlsx/csv/images>
- evidence:
  - <qpdf/page-count/render/OCR check summary>
- ledger_event: <event id or none>
- needs:
  - review | verification | user_input | none
```

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
