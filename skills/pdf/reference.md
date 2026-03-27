# PDF 处理高级参考指南

本文档包含高级 PDF 处理功能、详细示例以及主技能说明中未涵盖的额外库。

## pypdfium2 库 (Apache/BSD 许可证)

### 概述
pypdfium2 是 PDFium（Chromium 的 PDF 库）的 Python 绑定。它非常适用于快速 PDF 渲染、图像生成，可作为 PyMuPDF 的替代品。

### 将 PDF 渲染为图像
```python
import pypdfium2 as pdfium
from PIL import Image

# 加载 PDF
pdf = pdfium.PdfDocument("document.pdf")

# 将页面渲染为图像
page = pdf[0]  # 第一页
bitmap = page.render(
    scale=2.0,  # 更高分辨率
    rotation=0  # 不旋转
)

# 转换为 PIL 图像
img = bitmap.to_pil()
img.save("page_1.png", "PNG")

# 处理多页
for i, page in enumerate(pdf):
    bitmap = page.render(scale=1.5)
    img = bitmap.to_pil()
    img.save(f"page_{i+1}.jpg", "JPEG", quality=90)
```

### 使用 pypdfium2 提取文本
```python
import pypdfium2 as pdfium

pdf = pdfium.PdfDocument("document.pdf")
for i, page in enumerate(pdf):
    text = page.get_text()
    print(f"第 {i+1} 页文本长度: {len(text)} 字符")
```

## JavaScript 库

### pdf-lib (MIT 许可证)

pdf-lib 是一个强大的 JavaScript 库，用于在任何 JavaScript 环境中创建和修改 PDF 文档。

#### 加载并操作现有 PDF
```javascript
import { PDFDocument } from 'pdf-lib';
import fs from 'fs';

async function manipulatePDF() {
    // 加载现有 PDF
    const existingPdfBytes = fs.readFileSync('input.pdf');
    const pdfDoc = await PDFDocument.load(existingPdfBytes);

    // 获取页数
    const pageCount = pdfDoc.getPageCount();
    console.log(`文档共有 ${pageCount} 页`);

    // 添加新页面
    const newPage = pdfDoc.addPage([600, 400]);
    newPage.drawText('由 pdf-lib 添加', {
        x: 100,
        y: 300,
        size: 16
    });

    // 保存修改后的 PDF
    const pdfBytes = await pdfDoc.save();
    fs.writeFileSync('modified.pdf', pdfBytes);
}
```

## 高级命令行操作

### poppler-utils 高级功能

#### 提取带有边界框坐标的文本
```bash
# 提取带有边界框坐标的文本（对于结构化数据至关重要）
pdftotext -bbox-layout document.pdf output.xml
# XML 输出包含每个文本元素的精确坐标
```

#### 高级图像转换
```bash
# 以特定分辨率转换为 PNG 图像
pdftoppm -png -r 300 document.pdf output_prefix

# 高分辨率转换特定页面范围
pdftoppm -png -r 600 -f 1 -l 3 document.pdf high_res_pages
```

### qpdf 高级功能

#### 复杂的页面操作
```bash
# 将 PDF 拆分为页面组
qpdf --split-pages=3 input.pdf output_group_%02d.pdf

# 合并来自多个 PDF 的特定页面
qpdf --empty --pages doc1.pdf 1-3 doc2.pdf 5-7 doc3.pdf 2,4 -- combined.pdf
```

#### PDF 优化与修复
```bash
# 为 Web 优化 PDF（线性化以支持流式传输）
qpdf --linearize input.pdf optimized.pdf

# 尝试修复损坏的 PDF 结构
qpdf --check input.pdf
qpdf --fix-qdf damaged.pdf repaired.pdf
```

## 高级 Python 技术

### pdfplumber 高级功能

#### 提取带有精确坐标的文本
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    page = pdf.pages[0]
    
    # 提取前 10 个字符及其坐标
    chars = page.chars
    for char in chars[:10]:
        print(f"字符: '{char['text']}' 位于 x:{char['x0']:.1f} y:{char['y0']:.1f}")
```

### reportlab 高级功能

#### 使用表格创建专业报告
```python
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

data = [
    ['产品', '第一季度', '第二季度'],
    ['小部件', '120', '135'],
    ['小工具', '85', '92']
]

doc = SimpleDocTemplate("report.pdf")
elements = []
styles = getSampleStyleSheet()
elements.append(Paragraph("季度销售报告", styles['Title']))

# 添加带有高级样式的表格
table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
elements.append(table)
doc.build(elements)
```

## 性能优化技巧

1. **针对大型 PDF**：使用流式处理方法，而非将整个 PDF 加载到内存。使用 `qpdf --split-pages` 进行拆分。
2. **针对文本提取**：`pdftotext -bbox-layout` 是纯文本提取最快的方法。使用 pdfplumber 处理结构化数据。
3. **针对图像提取**：`pdfimages` 比渲染页面快得多。
4. **内存管理**：分块处理 PDF 页面。

## 常见问题排查

### 加密 PDF
```python
from pypdf import PdfReader
reader = PdfReader("encrypted.pdf")
if reader.is_encrypted:
    reader.decrypt("密码")
```

### 文本提取失败
对于扫描件，应回退到 OCR：
```python
from pdf2image import convert_from_path
import pytesseract
images = convert_from_path("scanned.pdf")
text = "".join([pytesseract.image_to_string(img) for img in images])
```
