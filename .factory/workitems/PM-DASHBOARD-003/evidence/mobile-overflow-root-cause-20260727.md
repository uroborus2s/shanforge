# PM Dashboard 移动端横向溢出根因

- 时间：`2026-07-27T19:08:07+08:00`
- skill：`systematic-debugging`
- status：`root_cause_found`
- 本轮未修改原型实现。

## 复现

临时只读 HTTP server + Chromium：

```text
desktop: ten=10 overflow=false drawer=项目成员 tabs=5 errors=0
mobile:  ten=10 overflow=true  drawer=项目成员 tabs=5 errors=0
```

移动端五个 lane 和详情抽屉交互均可用，但根节点 `scrollWidth=462`，
viewport 为 390。

## 根因

- 直接原因：`sidebar` 计算宽度为 462px，带动 `.app-shell`、`.workspace`、
  `.topbar` 和 `main` 全部扩到 462px。
- 根源原因：`@media(max-width:900px)` 把单列 Grid 写成
  `grid-template-columns:1fr`。Grid item 默认最小宽度为 `auto`，横向
  `.side-nav` 的 intrinsic min-content 宽度把唯一 track 撑大。

越界证据：

```text
HTML/BODY/app-shell scrollWidth=462
sidebar width=462
side-nav width=438 scrollWidth=676
workspace/topbar/main width=462
```

## 修复方向（尚未实施）

最小根因修复是在移动断点把单列 track 改为
`grid-template-columns:minmax(0,1fr)`，让导航只在自己的 `overflow-x:auto`
容器内滚动。根因获人工确认后再形成并确认正式修复方案。

## 证据

- `review-fix-browser-desktop.png`
  SHA-256 `407dd99e961b5a6e9613d576d78d6c312056bb2ad80ce56ef39918f03e2f5017`
- `review-fix-browser-mobile.png`
  SHA-256 `bec3ca6d927684ee14b1a7e647a94f5bd71d7125d4b2e2f248b44c84eb2f851c`
