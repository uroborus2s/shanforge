---
name: art-asset-pipeline
description: 美术方向 + 资源管线。用于需要先生成风格样张、UI 美术图或游戏概念图供用户确认，再生成资源清单，并在清单确认后生产应用开发资源包或游戏开发资源包的任务。
---

# Art Asset Pipeline

用于把美术探索变成可交付的开发资源。核心原则是先确认方向，再确认清单，最后生产资源包。

## 何时使用

- 用户需要风格样张、UI 美术图、游戏概念图、角色 / 场景 / 道具概念图。
- 用户需要应用开发资源包，例如图标、插画、空状态图、启动图、背景图、UI 纹理和品牌视觉素材。
- 用户需要游戏开发资源包，例如精灵图、角色、敌人、道具、地块、背景、特效帧和 UI HUD 素材。
- 用户要求从美术方向推进到资源清单、命名、尺寸、导出格式、预览和交付包。

## 不使用

- 只做界面结构、信息架构、可用性或响应式评审；交给 `ui-ux-pro-max`。
- 只做代码生成艺术、p5.js、流场或参数化作品；交给 `algorithmic-art`。
- 只做普通图片编辑且不需要资源清单或开发资源包。
- 用户要求复刻受版权保护作品、冒充具体在世艺术家风格，或绕过授权素材来源。

## 硬规则

| 规则 | 要求 |
|---|---|
| 阶段推进 | 未经用户确认不得进入下一阶段；确认美术方向前只生成候选图和方向说明；确认资源清单前不生产最终资源包。 |
| 目录流转 | `imagegen` 产出的候选图放 `candidates/`；用户明确确认后才移动或复制到 `approved/`；`approved/` 只放确认图和确认图的可追溯派生源。 |
| 最终交付 | 最终资源包、`manifest.json` 和最终说明只包含确认图，或由确认图确定性裁切、缩放、去背景、打包得到的派生文件；不得包含 `candidates/`、`tmp/` 或未确认图。 |
| 收尾清理 | 候选图跨会话保留，等待用户选择时不得删除；用户完成选择后删除未被选中的候选图并清空 `tmp/`。 |
- 生成图必须使用 `imagegen`。本地检查必须用 `view_image` 或浏览器预览查看关键输出。
- 需要去色键或透明背景时，优先使用资源包内的 `remove_chroma_key.py`，并在 `manifest.json` 记录输入、输出和参数。
- 不自批 `approved`。作者完成后只能回写 `ready_for_review`、`needs_user_input` 或 `blocked`。

## 推荐目录

每个资源任务使用独立输出目录，至少包含：

```text
<asset-pack>/
  art-direction.md
  sprite-spec.md
  manifest.json
  candidates/
  approved/
  preview/
    preview.html
  tools/
    remove_chroma_key.py
  tmp/
```

`candidates/` 是人工确认区，不是最终交付物；在等待选择期间持续保留。`tmp/` 只放可确定性重建的裁切、缩放、预览或打包中间文件，本轮结束可安全清空。最终导出时不包含这两个目录。

## 工作流程

1. 明确目标类型：应用开发资源包、游戏开发资源包，或只做美术方向探索。
2. 收集约束：目标用户、平台、尺寸、主题、禁用元素、品牌色、分辨率、透明背景、动画帧和导出格式。
3. 使用 `imagegen` 生成 2-4 张风格样张、UI 美术图或游戏概念图，写入 `candidates/`。
4. 使用 `view_image` 检查候选图。必要时用 `preview/preview.html` 在浏览器中并排预览。
5. 向用户提交候选方向。没有明确确认时停止，保留 `candidates/`，清理可再生的 `tmp/`，返回 `needs_user_input`。
6. 用户确认美术方向后，把确认图移入 `approved/`，删除未被选中的候选图，写入 `art-direction.md`。
7. 基于已确认方向生成资源清单，包含文件名、用途、尺寸、格式、透明度、派生关系和验收标准。
8. 向用户确认资源清单。未确认时停止，不生成最终包。
9. 用户确认清单后，生产应用开发资源包或游戏开发资源包。
10. 生成 `manifest.json`、`sprite-spec.md`、`preview/preview.html`，并把所有资源与确认来源关联。
11. 验证预览、透明背景、尺寸、命名、缺失文件和未确认资源泄漏。
12. 确认 `candidates/` 已在选择后清空，删除 `tmp/` 中所有可再生中间文件，再回写状态。

## 输出文件

`art-direction.md` 必须包含：

- 用户确认的美术方向。
- 选中的确认图路径，只能引用 `approved/`。
- 色彩、材质、线条、光照、构图、UI 气质或游戏世界观约束。
- 明确排除的风格和元素。
- 后续生成 prompt 的稳定关键词。

`sprite-spec.md` 必须包含：

- 应用资源或游戏资源的尺寸表。
- 游戏资源的帧数、行列、锚点、碰撞盒、动画名和播放建议。
- 应用资源的用途、状态、密度倍图、暗色模式和裁切安全区。
- 命名规则、导出格式和透明背景要求。

`manifest.json` 必须包含：

- 资源包类型：`app` 或 `game`。
- 每个文件的路径、用途、尺寸、格式、状态和确认来源。
- `approved_source` 字段，指向 `approved/` 中的确认图或其派生链。
- `derived_from` 字段，记录裁切、缩放、去背景或 sprite packing 来源。
- `tooling` 字段，记录 `imagegen`、`remove_chroma_key.py`、预览和验证命令。
- 不得包含 `tmp/` 路径，不得列入未确认图。

`preview/preview.html` 必须包含：

- 所有最终资源的缩略图预览。
- 文件名、尺寸、用途和透明背景检查底纹。
- 应用资源按页面 / 状态分组；游戏资源按角色、地块、道具、特效和 UI 分组。
- 本地打开即可查看，不依赖远端服务。

`remove_chroma_key.py` 必须满足：

- 输入图、输出图、色键颜色和容差可配置。
- 默认不覆盖源文件。
- 失败时返回非零退出码，并说明输入缺失、格式错误或输出不可写。
- 只作为确定性后处理工具，不替代用户确认。

## 验证要求

- 运行资源清单一致性检查：`manifest.json` 中的每个文件都存在。
- 检查 `manifest.json` 没有 `tmp/` 路径。
- 检查最终资源包没有 `candidates/`、`tmp/` 或未确认中间图。
- 使用 `view_image` 抽查关键图，确认构图、裁切、透明背景和可读性。
- 使用浏览器打开 `preview/preview.html`，检查缩略图加载、尺寸标签、透明背景底纹和分组。
- 需要透明背景时，运行 `remove_chroma_key.py` 的最小 smoke check。
- 游戏资源必须检查 sprite sheet 尺寸、帧格一致、锚点说明和动画命名。
- 应用资源必须检查目标平台尺寸、暗色 / 亮色适配和空状态 / 图标可读性。

## 失败语义

返回 `needs_user_input`：

- 等待用户确认美术方向。
- 等待用户确认资源清单。
- 用户需要在多个候选图之间选择。

返回 `blocked`：

- `imagegen` 不可用，且任务必须生成新图。
- 无法查看关键图，无法判断输出是否可交付。
- 用户要求侵权复刻、冒充在世艺术家或使用未授权素材。
- 用户选择后无法删除未选候选图或临时文件，或无法证明最终包只包含确认图。

返回 `ready_for_review`：

- 美术方向已确认。
- 资源清单已确认。
- 最终资源包只包含用户确认过的图。
- `candidates/` 已在用户选择后清理。
- `tmp/` 已清理。
- `manifest.json`、`art-direction.md`、`sprite-spec.md` 和 `preview/preview.html` 已生成并验证。

## 状态回写

非 Shanforge work item 的轻量交付至少回写：

- `status`: `ready_for_review`、`needs_user_input` 或 `blocked`
- `outputs`: 等待选择时的 `candidates/`，或完成后的资源包目录、`approved/`、`manifest.json`、`art-direction.md`、`sprite-spec.md`、`preview/preview.html`
- `evidence`: 用户确认记录、`imagegen` 记录、`view_image` 检查、浏览器预览、清单一致性检查和 `tmp/` 清理证据
- `verification`: 实际运行的检查命令；未运行必须说明原因
- `needs`: 仍需用户确认的美术方向、资源清单或授权素材

若在 Shanforge work item 中使用，只回写状态包，不替 `using-shanforge` 决定 review、人工确认、提交或下一步 skill：

```text
工作结果：
- work_item: <WORKITEM-ID or none>
- skill: art-asset-pipeline
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <asset-pack paths>
- evidence:
  - <confirmation records, preview checks, manifest checks, cleanup evidence>
- ledger_event: <event id or none>
- needs:
  - review | user_input | none
```

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
