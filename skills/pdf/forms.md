**重要：你必须按顺序完成这些步骤。不要直接跳到编写代码。**

如果您需要填写 PDF 表单，首先检查 PDF 是否具有可填充的表单字段。在当前文件所在的目录下运行此脚本：
 `python scripts/check_fillable_fields <file.pdf>`，根据结果转到“可填充字段”或“不可填充字段”并遵循相应的说明。

# 可填充字段
如果 PDF 具有可填充的表单字段：
- 在当前文件所在的目录下运行此脚本：`python scripts/extract_form_field_info.py <input.pdf> <field_info.json>`。它将创建一个包含字段列表的 JSON 文件，格式如下：
```
[
  {
    "field_id": (字段的唯一 ID),
    "page": (页码，从 1 开始),
    "rect": ([left, bottom, right, top] PDF 坐标系下的边界框，y=0 是页面底部),
    "type": ("text", "checkbox", "radio_group", 或 "choice"),
  },
  // 复选框具有 "checked_value" 和 "unchecked_value" 属性：
  {
    "field_id": (字段的唯一 ID),
    "page": (页码，从 1 开始),
    "type": "checkbox",
    "checked_value": (将字段设置为此值以勾选复选框),
    "unchecked_value": (将字段设置为此值以取消勾选复选框),
  },
  // 单选按钮组具有包含可能选项的 "radio_options" 列表。
  {
    "field_id": (字段的唯一 ID),
    "page": (页码，从 1 开始),
    "type": "radio_group",
    "radio_options": [
      {
        "value": (将字段设置为此值以选择此单选选项),
        "rect": (此选项单选按钮的边界框)
      },
      // 其他单选选项
    ]
  },
  // 多选字段具有包含可能选项的 "choice_options" 列表：
  {
    "field_id": (字段的唯一 ID),
    "page": (页码，从 1 开始),
    "type": "choice",
    "choice_options": [
      {
        "value": (将字段设置为此值以选择此选项),
        "text": (选项的显示文本)
      },
      // 其他选项
    ],
  }
]
```
- 使用此脚本将 PDF 转换为 PNG（每页一张图像）：
`python scripts/convert_pdf_to_images.py <file.pdf> <output_directory>`
然后分析图像以确定每个表单字段的用途（确保将 PDF 坐标系的边界框转换为图像坐标）。
- 创建一个 `field_values.json` 文件，格式如下，包含要为每个字段输入的值：
```
[
  {
    "field_id": "last_name", // 必须与 `extract_form_field_info.py` 中的 field_id 匹配
    "description": "用户的姓氏",
    "page": 1, // 必须与 field_info.json 中的 "page" 值匹配
    "value": "Simpson"
  },
  {
    "field_id": "Checkbox12",
    "description": "如果用户年满 18 岁则勾选的复选框",
    "page": 1,
    "value": "/On" // 如果这是一个复选框，使用其 "checked_value" 值来勾选它。如果是单选按钮组，使用 "radio_options" 中的一个 "value" 值。
  },
  // 更多字段
]
```
- 运行 `fill_fillable_fields.py` 脚本以创建填写后的 PDF：
`python scripts/fill_fillable_fields.py <input pdf> <field_values.json> <output pdf>`
此脚本将验证您提供的字段 ID 和值是否有效；如果打印错误消息，请修正相应的字段并重试。

# 不可填充字段
如果 PDF 没有可填充的表单字段，您将添加文本注释。首先尝试从 PDF 结构中提取坐标（更准确），如果需要，再回退到视觉评估。

## 第 1 步：优先尝试结构提取

运行此脚本以提取文本标签、线条和复选框及其精确的 PDF 坐标：
`python scripts/extract_form_structure.py <input.pdf> form_structure.json`

这将创建一个包含以下内容的 JSON 文件：
- **labels**: 每个带有精确坐标的文本元素（PDF 点数单位下的 x0, top, x1, bottom）
- **lines**: 定义行边界的水平线
- **checkboxes**: 作为复选框的小正方形矩形（带有中心坐标）
- **row_boundaries**: 从水平线计算出的行顶部/底部位置

**检查结果**：如果 `form_structure.json` 具有有意义的标签（对应于表单字段的文本元素），请使用**方法 A：基于结构的坐标**。如果 PDF 是基于扫描/图像的且几乎没有标签，请使用**方法 B：视觉评估**。

---

## 方法 A：基于结构的坐标（首选）

当 `extract_form_structure.py` 在 PDF 中找到文本标签时使用此方法。

### A.1：分析结构

读取 `form_structure.json` 并识别：
1. **标签组**：构成单个标签的相邻文本元素（例如，“姓”+“氏”）。
2. **行结构**：具有相似 `top` 值的标签属于同一行。
3. **字段列**：输入区域在标签结束后开始（x0 = label.x1 + 间隔）。
4. **复选框**：直接使用结构中的复选框坐标。

**坐标系**：PDF 坐标，y=0 位于页面顶部，y 向下增加。

### A.2：检查缺失元素
结构提取可能无法检测到所有表单元素。常见情况：
- **圆形复选框**：仅正方形矩形被检测为复选框。
- **复杂图形**：装饰元素或非标准表单控件。

如果您在 PDF 图像中看到 `form_structure.json` 中没有的表单字段，您需要对这些特定字段进行**视觉分析**（参见下文的“混合方法”）。

### A.3：创建带有 PDF 坐标的 fields.json

对于每个字段，从提取的结构中计算输入坐标：
- **文本字段**：x0 = 标签 x1 + 5；top = 标签 top。
- **复选框**：直接使用 `form_structure.json` 中的矩形坐标。

使用 `pdf_width` 和 `pdf_height` 创建 `fields.json`（表示 PDF 坐标）：
```json
{
  "pages": [
    {"page_number": 1, "pdf_width": 612, "pdf_height": 792}
  ],
  "form_fields": [
    {
      "page_number": 1,
      "description": "姓氏输入字段",
      "field_label": "姓氏",
      "label_bounding_box": [43, 63, 87, 73],
      "entry_bounding_box": [92, 63, 260, 79],
      "entry_text": {"text": "张", "font_size": 10}
    }
  ]
}
```

### A.4：验证边界框
在填写之前，检查边界框是否有误：
`python scripts/check_bounding_boxes.py fields.json`

---

## 方法 B：视觉评估（回退方案）

当 PDF 是基于扫描/图像的且结构提取未发现可用的文本标签时使用此方法。

### B.1：将 PDF 转换为图像
`python scripts/convert_pdf_to_images.py <input.pdf> <images_dir/>`

### B.2：初步字段识别
检查每页图像以识别表单部分并获取字段位置的**粗略估计**。

### B.3：缩放细化（准确性的关键）
对于每个字段，在其估计位置周围裁剪一个区域以精确细化坐标。

**使用 ImageMagick 创建缩放裁剪：**
```bash
magick <page_image> -crop <width>x<height>+<x>+<y> +repage <crop_output.png>
```
**检查裁剪后的图像**以确定精确坐标：
1. 识别输入区域开始的精确像素。
2. 识别输入区域结束的位置。

**将裁剪坐标转换回完整图像坐标：**
- full_x = crop_x + crop_offset_x
- full_y = crop_y + crop_offset_y

### B.4：创建带有细化坐标的 fields.json
使用 `image_width` 和 `image_height` 创建 `fields.json`（表示图像坐标）：
```json
{
  "pages": [
    {"page_number": 1, "image_width": 1700, "image_height": 2200}
  ],
  "form_fields": [
    {
      "page_number": 1,
      "description": "姓氏输入字段",
      "field_label": "姓氏",
      "entry_bounding_box": [255, 175, 720, 218],
      "entry_text": {"text": "张", "font_size": 10}
    }
  ]
}
```

---

## 混合方法：结构 + 视觉
当结构提取适用于大多数字段但遗漏了某些元素（如圆形复选框）时使用此方法。

1. 对于检测到的字段使用**方法 A**。
2. 对于缺失的字段使用**方法 B**。
3. **统一坐标系**：将图像坐标转换为 PDF 坐标，并在 `fields.json` 中统一使用 `pdf_width`/`pdf_height`。

---

## 第 2 步：填写前验证
**务必在填写前验证边界框：**
`python scripts/check_bounding_boxes.py fields.json`

## 第 3 步：填写表单
填写脚本会自动检测坐标系并处理转换：
`python scripts/fill_pdf_form_with_annotations.py <input.pdf> fields.json <output.pdf>`

## 第 4 步：验证输出
将填写后的 PDF 转换为图像并验证文本位置。
