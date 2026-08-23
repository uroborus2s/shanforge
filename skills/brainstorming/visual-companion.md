# 可视化伴侣指南

可视化伴侣用于在头脑风暴中展示界面稿、图表和视觉选项。它是辅助工具，不是流程主控。

## 何时使用

逐个问题判断，不按整场会话判断。

判断标准：**用户看到画面是否比阅读文字更容易理解？**

适合用浏览器：

- UI 草图、线框图、页面布局、导航结构、组件设计。
- 架构图、数据流、关系图、状态机、流程图。
- 两到四个视觉方向的并排比较。
- 视觉层级、间距、版式、风格和设计 polish。
- 空间关系强的问题，例如实体关系、步骤走向、页面区域。

适合继续在终端：

- 需求和范围问题。
- 概念型 A/B/C 选择。
- 优缺点列表和文本表格。
- API、数据模型、技术选型等文字决策。
- 任何答案主要是文字而不是视觉偏好的澄清问题。

涉及 UI 不等于必须用浏览器。“你想要什么样的向导？”是概念问题，用终端。“这两个向导布局哪个更合适？”是视觉问题，用浏览器。

## 工作方式

服务器监听一个内容目录，自动展示最新的 HTML 文件。

- 你把 HTML 写入 `screen_dir`。
- 用户在浏览器里看到画面。
- 用户点击的选项写入 `state_dir/events`。
- 下一轮你读取事件，再结合用户在终端输入的文字判断反馈。

默认写 **HTML 片段**。如果文件以 `<!DOCTYPE` 或 `<html` 开头，服务器按完整文档展示，并只注入 helper script。否则服务器会自动包上 frame 模板，加入标题栏、主题样式、连接状态和交互脚本。

下文的 `<skill-dir>` 表示本 skill 所在目录；不要假设当前工作目录是 Shanforge 仓库根目录。

## 启动会话

用户同意使用可视化伴侣后启动。

```bash
<skill-dir>/scripts/start-server.sh \
  --project-dir /path/to/project \
  --workitem-id WORKITEM-ID \
  --open
```

返回示例：

```json
{
  "type": "server-started",
  "port": 52341,
  "url": "http://localhost:52341/?key=ab12...",
  "screen_dir": "/path/to/project/.factory/workitems/WORKITEM-ID/design-assets/brainstorm/12345-1706000000/content",
  "state_dir": "/path/to/project/.factory/workitems/WORKITEM-ID/design-assets/brainstorm/12345-1706000000/state"
}
```

保存返回的 `screen_dir` 和 `state_dir`。使用 `--open` 后，首屏推送时浏览器会自动打开；仍要把完整 URL 发给用户作为 fallback。

URL 中的 `?key=...` 是会话密钥。必须给用户完整 URL，不要去掉 query string。服务器会拒绝没有密钥的 HTTP 和 WebSocket 请求。首次加载后浏览器会把密钥保存到 cookie，刷新和 `/files/*` 资源仍能使用。

### shanforge 路径规则

使用 `--project-dir` 时必须同时传 `--workitem-id`。

持久化文件固定写入：

```text
.factory/workitems/<WORKITEM-ID>/design-assets/brainstorm/<SESSION-ID>/
  content/
  state/
```

可视化伴侣的持久化文件统一保存到当前 work item 的 `design-assets/brainstorm/` 目录。不要把临时 HTML 直接当成正式设计文档。被采纳的设计交付物需要同步登记到 `docs/04-project-development/04-design/assets/` 或对应设计文档，并刷新 `.factory/memory/design-assets.summary.md`。

如果只是一次性临时查看，且尚未登记 work item，可以不传 `--project-dir`，让文件落到 `/tmp`。一旦用户采纳视觉结果，必须回写到 work item brief、ledger 和正式设计资产。

### 查找连接信息

服务器会把启动 JSON 写入 `$STATE_DIR/server-info`。如果后台启动时没有捕获 stdout，读取该文件即可得到 URL 和端口。

使用 shanforge 持久化目录时，可在以下位置查找最近会话：

```text
.factory/workitems/<WORKITEM-ID>/design-assets/brainstorm/
```

### 平台启动方式

Codex 环境会回收脱离的后台进程。脚本检测到 `CODEX_CI` 时会自动使用 foreground 模式。正常运行即可。

如果浏览器无法访问返回 URL，通常是远程或容器网络问题。可以绑定非 loopback host：

```bash
<skill-dir>/scripts/start-server.sh \
  --project-dir /path/to/project \
  --workitem-id WORKITEM-ID \
  --host 0.0.0.0 \
  --url-host localhost
```

`--url-host` 只控制返回 URL 里展示的 host。

## 循环步骤

1. **确认服务器还活着。**
   - 检查 `$STATE_DIR/server-info` 存在。
   - 检查 `$STATE_DIR/server-stopped` 不存在。
   - 如果服务器停了，用同一个 `--project-dir` 和 `--workitem-id` 重启。脚本会复用端口和密钥，用户已打开的 tab 会自动重连。

2. **写一个新的 HTML 文件到 `screen_dir`。**
   - 使用语义化文件名，例如 `layout.html`、`visual-style.html`、`architecture-flow.html`。
   - 每一屏都用新文件名。
   - 迭代版本用 `layout-v2.html`、`layout-v3.html`。
   - 使用文件编辑工具创建文件，不要用 `cat` 或 heredoc 往终端灌大段 HTML。

3. **告诉用户看到什么，并结束本轮。**
   - 每次都提醒完整 URL。
   - 简短说明屏幕内容，例如“正在展示 3 个首页布局方向”。
   - 请用户在终端回复反馈；如果愿意，也可以点击浏览器里的选项。

4. **下一轮读取反馈。**
   - 如果 `$STATE_DIR/events` 存在，读取其中的 JSONL。
   - 终端文字反馈优先。
   - 浏览器事件用于补充用户点击、犹豫和最终选择。

5. **迭代或推进。**
   - 如果反馈改变当前屏幕，写新版本。
   - 当前问题确认后，再进入下一个问题。

6. **回到终端时清空旧画面。**
   - 下一个步骤不需要浏览器时，推送等待页，避免用户继续看旧决策。

```html
<div style="display:flex;align-items:center;justify-content:center;min-height:60vh">
  <p class="subtitle">继续在终端沟通...</p>
</div>
```

## HTML 片段写法

默认只写页面内容。不要写 `<html>`、CSS 或 `<script>`，除非确实需要完整控制页面。

```html
<h2>哪个布局更合适？</h2>
<p class="subtitle">请重点比较可读性和视觉层级</p>

<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>单列布局</h3>
      <p>聚焦阅读，适合线性内容。</p>
    </div>
  </div>
  <div class="option" data-choice="b" onclick="toggleSelect(this)">
    <div class="letter">B</div>
    <div class="content">
      <h3>双栏布局</h3>
      <p>侧边导航加主内容，适合频繁跳转。</p>
    </div>
  </div>
</div>
```

## 可用 CSS 类

### 选项

```html
<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>标题</h3>
      <p>说明</p>
    </div>
  </div>
</div>
```

多选：

```html
<div class="options" data-multiselect>
  <!-- 同样的 option 结构 -->
</div>
```

### 卡片

```html
<div class="cards">
  <div class="card" data-choice="design1" onclick="toggleSelect(this)">
    <div class="card-image"><!-- mockup 内容 --></div>
    <div class="card-body">
      <h3>名称</h3>
      <p>说明</p>
    </div>
  </div>
</div>
```

### Mockup 容器

```html
<div class="mockup">
  <div class="mockup-header">预览：Dashboard Layout</div>
  <div class="mockup-body"><!-- mockup HTML --></div>
</div>
```

### 并排对比

```html
<div class="split">
  <div class="mockup"><!-- 左侧 --></div>
  <div class="mockup"><!-- 右侧 --></div>
</div>
```

### 优缺点

```html
<div class="pros-cons">
  <div class="pros"><h4>优点</h4><ul><li>收益</li></ul></div>
  <div class="cons"><h4>缺点</h4><ul><li>代价</li></ul></div>
</div>
```

### 线框元素

```html
<div class="mock-nav">Logo | Home | About | Contact</div>
<div style="display:flex">
  <div class="mock-sidebar">Navigation</div>
  <div class="mock-content">Main content area</div>
</div>
<button class="mock-button">Action Button</button>
<input class="mock-input" placeholder="Input field">
<div class="placeholder">Placeholder area</div>
```

### 排版

- `h2`：页面标题。
- `h3`：小节标题。
- `.subtitle`：标题下的说明。
- `.section`：内容区块。
- `.label`：小号标签文字。

## 浏览器事件格式

用户点击会记录到 `$STATE_DIR/events`，每行一个 JSON 对象。推送新屏幕后，事件文件会被清空。

```jsonl
{"type":"click","choice":"a","text":"Option A - Simple Layout","timestamp":1706000101}
{"type":"click","choice":"c","text":"Option C - Complex Grid","timestamp":1706000108}
{"type":"click","choice":"b","text":"Option B - Hybrid","timestamp":1706000115}
```

最后一次 `choice` 通常是最终选择，但点击顺序也能显示用户犹豫点。没有 `$STATE_DIR/events` 时，说明用户没有在浏览器交互，只使用终端反馈。

## 设计建议

- 精度匹配问题：布局问题用线框，视觉风格问题再做更精细 mockup。
- 每屏只问一个视觉问题。
- 每屏最多 2-4 个选项。
- 能用真实内容就不用占位内容。
- 先让结构清楚，再追求细节。
- 反馈改变当前屏幕时先迭代，不要急着进入下一个问题。

## 文件命名

- 使用语义名：`platform.html`、`visual-style.html`、`layout.html`。
- 不复用文件名。
- 迭代加版本后缀：`layout-v2.html`、`layout-v3.html`。

## 清理

```bash
<skill-dir>/scripts/stop-server.sh "$SESSION_DIR"
```

`/tmp` 会话会被删除。`.factory/workitems/<WORKITEM-ID>/design-assets/brainstorm/` 下的会话会保留，用于后续审阅和 evidence 回看。

## 参考

- Frame 模板：`<skill-dir>/scripts/frame-template.html`
- 浏览器 helper：`<skill-dir>/scripts/helper.js`
