---
name: docx
description: "每当用户想要创建、读取、编辑或操作 Word 文档（.docx 文件）时，请使用此技能。触发因素包括：任何提到“Word 文档”、“.docx”或要求生成带有目录、标题、页码或信头的专业文档的请求。此外，当需要从 .docx 文件中提取或重新组织内容、在文档中插入或替换图像、在 Word 文件中执行查找和替换、处理修订或批注，或将内容转换为精美的 Word 文档时，也要使用此技能。如果用户要求以 Word 或 .docx 文件形式提供“报告”、“备忘录”、“信函”、“模板”或类似的交付成果，请使用此技能。切勿用于 PDF、电子表格、Google 文档或与文档生成无关的通用编程任务。"
license: 版权所有。完整条款请参阅 LICENSE.txt
---

# DOCX 创建、编辑与分析

## 概述

.docx 文件是一个包含 XML 文件的 ZIP 归档。

## 快速参考

| 任务 | 方法 |
|------|----------|
| 读取/分析内容 | 使用 `pandoc` 或解包查看原始 XML |
| 创建新文档 | 使用 `docx-js` - 参见下文“创建新文档” |
| 编辑现有文档 | 解包 → 编辑 XML → 重新打包 - 参见下文“编辑现有文档” |

### 将 .doc 转换为 .docx

旧版 `.doc` 文件在编辑前必须进行转换：

```bash
python scripts/office/soffice.py --headless --convert-to docx document.doc
```

### 读取内容

```bash
# 提取带有修订内容的文本
pandoc --track-changes=all document.docx -o output.md

# 访问原始 XML
python scripts/office/unpack.py document.docx unpacked/
```

### 转换为图像

```bash
python scripts/office/soffice.py --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

### 接受修订

生成一份接受了所有修订的干净文档（需要 LibreOffice）：

```bash
python scripts/accept_changes.py input.docx output.docx
```

---

## 创建新文档

使用 JavaScript 生成 .docx 文件，然后进行验证。安装命令：`npm install -g docx`

### 设置
```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
        Header, Footer, AlignmentType, PageOrientation, LevelFormat, ExternalHyperlink,
        InternalHyperlink, Bookmark, FootnoteReferenceRun, PositionalTab,
        PositionalTabAlignment, PositionalTabRelativeTo, PositionalTabLeader,
        TabStopType, TabStopPosition, Column, SectionType,
        TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
        VerticalAlign, PageNumber, PageBreak } = require('docx');

const doc = new Document({ sections: [{ children: [/* 内容 */] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer));
```

### 验证
创建文件后，请对其进行验证。如果验证失败，请解包，修复 XML，然后重新打包。
```bash
python scripts/office/validate.py doc.docx
```

### 页面尺寸

```javascript
// 重要：docx-js 默认使用 A4，而非 US Letter
// 始终显式设置页面尺寸以确保结果一致
sections: [{
  properties: {
    page: {
      size: {
        width: 12240,   // 8.5 英寸（单位为 DXA）
        height: 15840   // 11 英寸（单位为 DXA）
      },
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1 英寸页边距
    }
  },
  children: [/* 内容 */]
}]
```

**常见页面尺寸（DXA 单位，1440 DXA = 1 英寸）：**

| 纸张 | 宽度 | 高度 | 内容宽度 (1" 边距) |
|-------|-------|--------|---------------------------|
| US Letter | 12,240 | 15,840 | 9,360 |
| A4 (默认) | 11,906 | 16,838 | 9,026 |

**横向打印 (Landscape)：** docx-js 在内部会交换宽/高，因此请传入纵向尺寸并让它处理交换：
```javascript
size: {
  width: 12240,   // 传入短边作为宽度
  height: 15840,  // 传入长边作为高度
  orientation: PageOrientation.LANDSCAPE  // docx-js 会在 XML 中交换它们
},
```

### 样式（覆盖内置标题）

使用 Arial 作为默认字体（通用支持）。保持标题为黑色以提高可读性。

```javascript
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } }, // 默认 12pt
    paragraphStyles: [
      // 重要：使用精确的 ID 来覆盖内置样式
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } }, // 目录需要 outlineLevel
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("标题")] }),
    ]
  }]
});
```

### 列表（切勿使用 Unicode 项目符号）

```javascript
// ❌ 错误 - 永远不要手动插入项目符号
new Paragraph({ children: [new TextRun("• 项目")] })  // 错误
new Paragraph({ children: [new TextRun("\u2022 项目")] })  // 错误

// ✅ 正确 - 使用带有 LevelFormat.BULLET 的编号配置
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("项目符号项")] }),
      new Paragraph({ numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("数字编号项")] }),
    ]
  }]
});
```

### 表格

**重要：表格需要双重宽度设置** - 既要在表格上设置 `columnWidths`，又要在每个单元格上设置 `width`。如果不同时设置，表格在某些平台上渲染会出错。

```javascript
// 重要：始终设置表格宽度以确保渲染一致
// 重要：使用 ShadingType.CLEAR（而非 SOLID）以防止背景变黑
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

new Table({
  width: { size: 9360, type: WidthType.DXA }, // 始终使用 DXA (百分比在 Google Docs 中会失效)
  columnWidths: [4680, 4680], // 必须等于表格总宽度 (DXA: 1440 = 1 英寸)
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 4680, type: WidthType.DXA }, // 也要在每个单元格上设置
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR }, // 使用 CLEAR 而非 SOLID
          margins: { top: 80, bottom: 80, left: 120, right: 120 }, // 单元格内边距
          children: [new Paragraph({ children: [new TextRun("单元格内容")] })]
        })
      ]
    })
  ]
})
```

**表格宽度计算：**
始终使用 `WidthType.DXA`。对于带有 1 英寸页边距的 US Letter 纸张，内容宽度为 9360 DXA。

### 图像

```javascript
// 重要：type 参数是必需的
new Paragraph({
  children: [new ImageRun({
    type: "png", // 必需：png, jpg, jpeg, gif, bmp, svg
    data: fs.readFileSync("image.png"),
    transformation: { width: 200, height: 150 },
    altText: { title: "标题", description: "描述", name: "名称" } // 三者均为必需
  })]
})
```

### 分页符

```javascript
// 重要：PageBreak 必须位于 Paragraph 内部
new Paragraph({ children: [new PageBreak()] })
```

---

## 编辑现有文档

**请按顺序执行以下 3 个步骤。**

### 第 1 步：解包
```bash
python scripts/office/unpack.py document.docx unpacked/
```
提取 XML，进行美化排版，合并相邻的运行块 (runs)，并将智能引号转换为 XML 实体。

### 第 2 步：编辑 XML

编辑 `unpacked/word/` 中的文件。

除非用户明确要求使用其他名称，否则**请使用 "Claude" 作为修订和批注的作者**。

**直接使用文本替换工具。不要编写 Python 脚本。**

**重要：为新内容使用智能引号。** 在添加带有省略号或引号的文本时，请使用 XML 实体：
`&#x2018;` (‘), `&#x2019;` (’), `&#x201C;` (“), `&#x201D;` (”)。

### 第 3 步：打包
```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```
该步骤会自动验证并生成 DOCX 文件。

---

## XML 参考

### 修订 (Tracked Changes)

**插入：**
```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>插入的文本</w:t></w:r>
</w:ins>
```

**删除：**
```xml
<w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>删除的文本</w:delText></w:r>
</w:del>
```

### 批注 (Comments)

**重要：`<w:commentRangeStart>` 和 `<w:commentRangeEnd>` 是 `<w:r>` 的同级元素，切勿位于 `<w:r>` 内部。**

```xml
<w:commentRangeStart w:id="0"/>
<w:r><w:t>被批注的文本</w:t></w:r>
<w:commentRangeEnd w:id="0"/>
<w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr><w:commentReference w:id="0"/></w:r>
```

---

## docx-js 的关键规则

- **显式设置页面尺寸** - 默认是 A4；对于国内通用文档建议检查尺寸要求。
- **切勿使用 `\n`** - 使用独立的 Paragraph 元素。
- **切勿使用 Unicode 项目符号** - 使用编号配置。
- **PageBreak 必须位于 Paragraph 中** - 独立存在会导致 XML 无效。
- **表格需要双重宽度设置** - 必须同时匹配 `columnWidths` 数组和单元格 `width`。
- **使用 `ShadingType.CLEAR`** - 单元格底色切勿使用 SOLID。
- **切勿使用表格作为分隔线** - 单元格有最小高度；请改用段落边框。
