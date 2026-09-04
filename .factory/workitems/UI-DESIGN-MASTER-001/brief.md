# UI-DESIGN-MASTER-001：统一 UI 设计与素材交付流程

## 目标

让 `ui-ux-pro-max` 成为 UI 从需求、设计到开发交付的唯一入口，并把 `art-asset-pipeline` 收缩为独立美术和游戏资源生产。

## 范围

- 将 UI 美术方向、资源清单、确认、生产和交付并入 `ui-ux-pro-max`。
- 明确可编辑设计源、评审预览、设计 token、正式 UI 素材及 manifest 的交付边界。
- 删除 UI 流程对 `art-asset-pipeline` 的依赖和重复路由。
- 保留 `art-asset-pipeline` 的独立美术与游戏资源生产能力。
- 更新最小语义测试，并由独立中文语言专家评审精简。

## 非目标

- 不重命名 skill 目录或破坏既有调用名。
- 不新增图像生成工具、依赖、模板或资源文件。
- 不改变 `art-asset-pipeline` 的 manifest 校验脚本合同。
- 不执行远端 push、PR、发布或历史改写。

## 验收标准

1. UI 任务只需进入 `ui-ux-pro-max`，即可完成结构、视觉、关键页确认、全页面扩展、UI 素材生产和开发交接。
2. UI 主交付包含可编辑设计源及版本；PNG/PDF 页面图只作评审或归档预览。
3. 普通控件、文字、状态和通用图标不烘焙进图片；只生产必须的品牌或内容型素材。
4. UI 素材经过方向确认和清单确认后进入正式 `assets/`，并由 manifest 记录用途、格式、尺寸和来源。
5. `art-asset-pipeline` 不再承接 UI 项目中的素材流程，只承接独立美术或游戏资源任务。
6. 相关定向测试、Skill validator 和独立中文语言评审通过。
