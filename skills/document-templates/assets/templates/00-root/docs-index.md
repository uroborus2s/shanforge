---
title: <项目名称>
mkdocs:
  home_access: public
  nav:
    - title: 入门说明
      children:
        - title: 概览
          path: 01-getting-started/index.md
          access: public
        - title: 项目概览
          path: 01-getting-started/project-overview.md
          access: public
        - title: 快速开始
          path: 01-getting-started/quick-start.md
          access: public
        - title: 文档地图
          path: 01-getting-started/document-map.md
          access: public
    - title: 用户指南
      children:
        - title: 概览
          path: 02-user-guide/index.md
          access: public
        - title: 使用指南
          path: 02-user-guide/user-guide.md
          access: public
    - title: 开发者指南
      children:
        - title: 概览
          path: 03-developer-guide/index.md
          access: public
    - title: 项目开发文档（内）
      children:
        - title: 概览
          path: 04-project-development/index.md
          access: private
---
# <项目名称>

这是项目文档首页，也是全站导航与页面权限的唯一事实源。

## 维护要求

- 根据项目真实模块裁剪 `mkdocs.nav`，不需要的节点直接删除
- 所有页面顺序、标题和 `public/private` 只在这里维护
- 子目录 `index.md` 只写正文概览，不重复声明导航
- 新增、删除或移动页面后，同步刷新根导航
