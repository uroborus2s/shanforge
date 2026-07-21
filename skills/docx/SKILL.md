---
name: docx
description: "创建、读取、编辑或验证 Word `.docx` 文件时使用。只在交付物本身必须是 Word/DOCX，或任务明确要求处理 `.docx`、修订、批注、目录、页眉页脚、版式和 Word 模板时触发；普通文本写作、PDF、电子表格和 Google Docs 不由本 skill 接管。"
license: 版权所有。完整条款请参阅 LICENSE.txt
---

# DOCX 处理

## 任务分支

先判断用户要的是哪一种结果，不要从工具清单开始。

| 分支 | 动作 |
|---|---|
| 读取 / 提取 | 先用 `pandoc --track-changes=all document.docx -o output.md` 或 `python scripts/office/unpack.py document.docx unpacked/` 读取内容；需要版式证据时再转 PDF/图片。 |
| 创建新文档 | 使用仓内已有 `docx` 依赖或现有生成脚本；没有依赖时先报告缺口，不建议临时安装新依赖。 |
| 编辑现有文档 | 先解包，编辑 `unpacked/word/` 的 XML，再用 `python scripts/office/pack.py unpacked/ output.docx --original document.docx` 打包。 |
| 修订 / 批注 | 保留 Word 修订结构；作者字段使用用户指定名称，未指定时用中性项目名或当前执行者名称，不写特定助手品牌。 |
| 验证 / 视觉检查 | 运行 `python scripts/office/validate.py output.docx`；版式敏感时用 `python scripts/office/soffice.py --headless --convert-to pdf output.docx` 再渲染抽查页面。 |

旧版 `.doc` 先转换：

```bash
python scripts/office/soffice.py --headless --convert-to docx document.doc
```

接受全部修订生成干净副本：

```bash
python scripts/accept_changes.py input.docx output.docx
```

## 安全写入

- 默认写新文件，例如 `name_edited.docx`、`name_clean.docx` 或用户指定路径；只有用户明确要求覆盖时才覆盖原文件。
- 修改现有文档前先确认输入文件可读，并保留原始 `.docx` 不动。
- XML 编辑只改与任务相关的 `word/document.xml`、`word/comments.xml`、关系文件或样式文件；不要顺手重排无关 XML。
- 批量替换必须先确认匹配数量；匹配为 0、过多或上下文歧义时先停止。
- 图像、页眉页脚、目录、脚注、批注和修订属于高风险区域，改完必须验证。

## DOCX 关键规则

- 显式设置页面尺寸和页边距；不要依赖 `docx-js` 默认 A4。
- 不要用 `\n` 表示换段，使用独立 Paragraph。
- 列表用编号配置，不手写 Unicode 项目符号。
- `PageBreak` 必须放在 Paragraph 内。
- 表格宽度同时设置 `columnWidths` 和每个单元格 `width`；单元格底色优先 `ShadingType.CLEAR`。
- 图片必须写入 `altText`，并用稳定尺寸避免版式漂移。
- `<w:commentRangeStart>` 和 `<w:commentRangeEnd>` 与 `<w:r>` 同级，不要放进 `<w:r>`。

## 输出清单

交付时列出：

- 输入文件路径。
- 输出 `.docx` 路径。
- 若生成了中间文件，列出 PDF、页面图片或解包目录。
- 修改摘要：新增、删除、替换、修订、批注或格式调整。
- 验证命令和结果。

## 验证

最小验证：

```bash
python scripts/office/validate.py output.docx
```

版式敏感文档还要执行：

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.docx
pdftoppm -jpeg -r 150 output.pdf page
```

验证失败时先修 XML 或生成逻辑，再重新打包和验证。不能打开、转换或验证时，不得宣称文件可用。

## 失败处理

- 输入文件缺失、加密、损坏或无法转换：`status: blocked`，写清失败命令和 stderr。
- 用户要求覆盖但风险不清：`status: needs_user_input`。
- 验证失败：`status: blocked`，列出失败原因、已生成文件和未完成项。
- 只完成文本提取但未做版式验证：报告 partial，不说“完成文档生成”。

## Shanforge 状态包

```text
工作结果：
- work_item: <WORKITEM-ID>
- skill: docx
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <output.docx>
- evidence:
  - <validate/convert/render command summary>
- ledger_event: <event id or none>
- needs:
  - review | verification | user_input | none
```

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
