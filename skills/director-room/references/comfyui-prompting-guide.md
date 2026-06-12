# ComfyUI 提示词与控制图指南

本指南服务于导演分镜部的统一提示词阶段。它规定双语 ComfyUI 交付物的结构，同时说明场景母图、平面调度、低模导出、深度图、线稿、遮罩、首尾帧和参考图如何进入工作流计划。本指南不要求已经存在可运行的 ComfyUI 图，但必须使后续操作者知道每个输入应接到什么条件角色。

## 双语契约

所有面向人的分镜区块和所有 JSON 提示词记录必须包含中文与英文：

- 中文提示词字段使用 `_zh`。
- 英文提示词字段使用 `_en`。
- 不得只在主字段写一种语言，再把另一种语言放进备注。
- 中英文语义必须一致；英文提示词可为了模型友好而调整词序和短语，不必逐字翻译中文。

## 提示词分层

每条最终视频提示词记录有两个顶层表面：

- `production_metadata`：用于规划、工作流绑定、质检、剪辑和修复的流程字段。包括 `episode_id`、`shot_id`、`segment_id`、`generation_method`、`duration`、`fps`、`aspect_ratio`、`asset_refs`、`first_frame_ref`、`last_frame_ref`、`audio_refs`、`workflow_hint`、`source_refs` 和 `continuity_refs`。
- `model_visible_prompt`：真正送入图像或视频模型的文本。不得包含输出文件名、`shot_id`、`generation_method`、`asset_id`、`episode_id`、workflow ID 或仅供流程使用的 source refs。

`model_visible_prompt` 由六个稳定部分构成：

1. 可见目标；
2. 风格与画质；
3. 主体内容；
4. 构图与运动；
5. 可见连续性约束；
6. 负面提示词。

双语记录中，每个部分都应有语义对应的中文和英文。视频模型可以被告知角色处于说话、呼吸或轻微口型状态；准确对白文本属于字幕和音频文件，不属于视频提示词。

支持性提示词从以下层次生成：

1. 身份与主体：角色、服装、道具、可见状态；
2. 动作与情绪：可拍行为、手势、表情、互动；
3. 环境：地点、时间、天气、地理关系、前中后景；
4. 摄影与运动：景别、镜头感、机位、运镜、构图；
5. 光线与色彩：主光、反差、调色、实际光源；
6. 风格与连续性：视觉锁点、材质语言、重复母题、禁止矛盾；
7. 质量意图：适合当前模型族的画质、媒介和渲染质量词。

全局风格和全局负面词应放入可复用 preset。单镜头提示词只写该镜头真正变化的内容。

## 场景控制输入

AI 视频的一致性依靠“条件证据”而不是自然语言记忆。ComfyUI 工作流计划应把以下输入分别标注为条件角色：

- 场景母图：用于 IP-Adapter、参考图或图生图，锁定美术气质、材质、色彩和光线。
- `layout.yaml`：不直接送入模型，而是作为平面调度和低模导出的事实源。
- `top-view.png`：用于人工复核站位、道具、机位和轴线；可作为流程说明图，不应当作最终画面参考。
- `camera-map.png`：用于复核每个镜头的摄影机位置、朝向和焦段。
- `shot-guides/`：每个镜头的构图参考图，可进入 I2V、REFERENCE_IMAGE 或人工质检。
- `depth/`：深度图，通常绑定到 ControlNet Depth 或同类条件节点。
- `lineart/`：线稿、边缘或结构图，通常绑定到 ControlNet Lineart、Canny、HED 或同类条件节点。
- `masks/`：局部重绘、遮挡、角色/道具分区和合成控制。
- 首帧/尾帧：用于 I2V 或 FLF2V，以锁定动作起止、站位变化和镜头连续。
- OpenPose 或动作参考：用于角色姿势、打斗、复杂动作和表演调度。

若项目不能直接运行 Blender、Unreal 或 ComfyUI，仍应写出占位路径、生成条件、预期尺寸和用途，状态标为 `needs_config` 或 `missing_asset`。

## 面向操作者的可复制提示词

后资产 ComfyUI 包必须包含组装好的 Markdown：

```text
{episode-id}/prompts/comfyui-render-prompts.md
```

该文件是给 ComfyUI 操作者复制到节点中的生产交付面。不得要求操作者手工拼接 JSON 字段。每个镜头必须提供四个可复制块：

```text
positive_prompt_zh
negative_prompt_zh
positive_prompt_en
negative_prompt_en
```

`comfyui-render-prompts.md` 可以使用清晰标题，但不得把项目专属视觉规则、标签、光线规则或风格文本硬编码到技能里。标题可从项目交付约定或稳定的 `model_visible_prompt` 部分中选择，例如风格与画质、可见目标、主体内容、构图与运动、连续性约束、负面模块。

避免重复写入风格锚点。若 `global_positive_prefix` 已经包含格式与风格锚点，组装镜头提示词时应从镜头级风格段落中去除重复语句。作者说明和 QC 规则不得进入最终模型可见提示词。

正向提示词组装顺序：

```text
global_positive_prefix_{lang}
+ visible_goal_{lang}
+ style_quality_{lang}
+ subject_content_{lang}
+ composition_motion_{lang}
+ visible_continuity_{lang}
+ global_positive_suffix_{lang}
```

负面提示词组装顺序：

```text
global_negative_{lang}
+ negative_prompt_{lang}
```

`comfyui-shot-prompts.json` 是审查、质检和自动修复的结构化事实源；`comfyui-render-prompts.md` 是派生的操作交付面。两者冲突时，修复结构化事实源并重新生成 Markdown。

## 分镜提示词结构

分镜计划使用以下双语结构：

```text
1. 基础设定 / Basic Setup
2. 氛围和画质 / Atmosphere and Image Quality
   2.1 风格核心 / Style Core
   2.2 视觉基调 / Visual Tone
   2.3 色彩和影调 / Color and Tonal Range
3. 画面内容 / Shot Panels
   分镜一 / Shot 1
     景别 / Shot Size:
     构图 / Composition:
     运镜手法 / Camera Movement:
     画面内容 / Visual Content:
     光线与色彩 / Lighting and Color:
     连续性锚点 / Continuity Anchors:
     控制图需求 / Control Inputs:
```

每个标签下都应有中文和英文。字段较长时，每种语言各写一个紧凑段落。

## 生成方法映射

- `T2V`：文字提示词加可选风格参考。只适用于身份、空间、动作连续性风险较低的镜头。
- `I2V`：使用图像参考或首帧加提示词。用于需要保持角色身份、服装、地点、构图或场景布局的镜头。
- `FLF2V`：使用首帧和尾帧加提示词。用于动作终点、姿势过渡、走位、打斗结果或屏幕方向必须被约束的镜头。
- `REFERENCE_IMAGE`：用于图像生成或静帧工作流。适合角色设定、插入镜头、地点板、场景母图和可复用视觉目标。
- `REDRAW`：使用 mask、局部重绘或 inpainting 条件。适合只改变既有图像或帧的一部分。

## 美术资产输出格式

存在图片资产输出时，导演分镜部必须保留每个资产的 `output_format` 契约：

- 中性母卡、转面图和细节裁切图用于身份、尺度、材质和连续性参考；
- 透明抠图用于 mask、叠加、合成或局部重绘控制；
- 只有 `video_reference_frame` 和 `shot_override_frame` 可作为 I2V/FLF2V 的场景首帧、尾帧或完整参考帧；
- 视频参考帧和镜头覆盖帧必须保留前景、中景、背景、机位、屏幕方向、光线和动作状态。

不得把透明抠图、中性卡、转面图或细节裁切图称为镜头的首帧、尾帧或完整场景参考。

## 负面提示词策略

负面词应模块化：

- 全局画质负面；
- 角色身份负面；
- 解剖、面部和手部瑕疵负面；
- 道具和地点矛盾负面；
- 视频运动和时序瑕疵负面；
- mask、局部重绘、首尾帧漂移等方法专属负面。

不同生成方法风险不同，不得每个镜头都套同一个通用负面词。必须同时提供 `negative_prompt_zh` 和 `negative_prompt_en`。

## 参数计划

生产设置应写入计划，而不是藏在散文里：

- `workflow_family`：稳定的工作流族名，例如 `t2v_text_only`、`i2v_reference`、`flf2v_transition`、`reference_image_still`、`redraw_masked_region`、`i2v_depth_lineart_locked`。
- `node_binding_hints`：说明正向提示词、负面提示词、图像输入、首尾帧、mask、LoRA stack、ControlNet 深度图/线稿/OpenPose、IPAdapter 参考、输出路径应接到哪里。
- `parameter_profile`：分辨率、采样器、调度器、步数、CFG、seed 策略、denoise、帧数、FPS、motion bucket、参考权重和批处理说明。

模型、LoRA、ControlNet、IPAdapter 或 workflow template 未知时，写占位符并把镜头或工作流族标为 `needs_config`。

## JSON 上下文传递

JSON artifact 是持久交接文件，不表示每次模型调用都要粘贴整个项目。

- 只有短小且直接相关的 JSON 才完整发送。
- 长 JSON 只发送相关场景或镜头记录，加全局元数据、schema 和 source refs。
- 主协调代理合并员工输出后，返回完整目标 artifact。
- 跨切片保持 `shot_id`、`generation_method`、`continuity_refs` 和 `source_refs` 完全一致。

## 反馈调优

存在 ComfyUI 渲染反馈时，按失败类型诊断：

- 身份漂移：强化角色 token、参考图绑定、LoRA 或 IPAdapter 权重，或降低 denoise。
- 构图不符：调整主体、动作、机位词顺序，增加画框约束；若需要参考控制，改用 I2V 或 FLF2V。
- 空间漂移：检查 `layout.yaml`、top view、camera map、depth、lineart 是否来自同一低模场景；必要时重导控制图，而不是继续抽卡。
- 动作失败：简化动作、拆分镜头、降低运动强度，或加入首尾帧/动作参考/OpenPose。
- 风格不符：先改 style preset，不要逐镜头大修。
- 画面瑕疵：先改负面模块，再考虑采样器、CFG 和步数。
- 道具或地点缺失：强化资产引用和连续性锁点，再加入局部镜头 token。

每次只改最小有效面，并把变更记录到 `{episode-id}/prompts/comfyui-tuning-log.json`。
