# AI 剧制作三 Skill 协作方案

## 1. 总体建议

当前保持三间房协作，不新增第四个 `post-room`。

- `writer-room` 负责故事事实、剧本、角色文字圣经、世界观和连续性 canon。
- `director-room` 负责导演分镜、镜头表、视频生产计划、ComfyUI 镜头提示词、渲染 QC、剪辑、AI 配音计划和后期计划。
- `art-room` 负责全剧可复用视觉资产、单集前置资产、角色卡、物品卡、场景卡、参考帧和资产 QC。

后期第一阶段归入 `director-room`，因为剪辑、字幕、配音、声音、调色和镜头 QC 都要服务镜头意图。只有当音频和交付工作复杂到需要独立管理多轮配音、混音、调色和平台交付规范时，再讨论是否拆出 `post-room`。

全剧统一角色资产不在写剧本时生成，也不等到镜头失败后临时补。正确时机是：全剧角色 bible 稳定后，`art-room` 创建全剧母资产；每集导演分镜稳定后，再创建该集状态资产、场景状态资产、物品状态资产和参考帧。

## 2. 术语

本文使用以下术语区分资产生成前后的导演工作：

- `资产前导演分镜包`：`director-room` 在资产尚未生成时，基于最终剧本创建分镜、镜头表、视觉连续性、生成计划和视频生产初步方案。它的目的不是直接开渲染，而是给 `art-room` 明确资产需求。
- `资产后视频生产包`：`art-room` 完成资产和资产 QC 后，`director-room` 读取真实 asset ID、canonical 图片路径和资产状态，刷新 ComfyUI 提示词、视频生产计划和渲染顺序。
- `角色卡`：锁定角色视觉身份的生产资产，不只是单张好看的角色图。它由角色设计规格、角色卡图片和角色图像提示词组成。
- `物品卡`：锁定物品、旗帜、徽章、符号、器具、服装配件等视觉形态的生产资产。
- `场景卡`：锁定地点空间结构、光线、材质、地理关系和可拍摄区域的生产资产。
- `canonical path`：下游固定读取的正式文件路径。正式文件不通过 `new`、`final-final`、`v2` 文件名表达当前版本。
- `handoff lock`：某个正式文件已经被下游读取后进入交接锁定。后续若必须修改，只能由 owner skill 原地修复，并触发下游刷新。
- `render lock`：提示词或生产计划已经进入渲染后进入渲染锁定。后续若必须修改，必须写入 tuning/QC 记录。

## 3. 统一项目根

所有 skill 必须读写同一个生产项目根：

```text
project/{project-name}/
```

项目级目录保存跨集事实、规则、共享资产和长期记忆；单集目录保存本集剧本、分镜、资产、渲染、QC、剪辑、AI 配音和后期产物。

```text
project/{project-name}/
  project.json
  bible/
  outline/
  synopsis/
  production/
  art/
  assets/
  memory/
  01/
  02/
  ...
```

## 4. 方案修订规范

本方案后续修订时必须保持完整清稿形态。

- 不用补丁式段落堆叠新旧说法。
- 不保留“上次说法”“新增补充”“临时说明”这类痕迹。
- 一旦确认新的术语、目录或文件规则，应把相关章节重编成完整、连贯、可直接执行的正文。
- 每次方案修订后必须审核：术语是否统一、上下游读取链是否闭合、同一文件是否只有一个 owner、是否存在互相矛盾的修改方式。
- 修改方案文档不等于修改 skill。只有当方案确认后，才进入 `writer-room`、`director-room`、`art-room` 的 skill 实现修改。

## 5. 文件短名规则

所有自动创建的文件名必须满足：

```text
不含扩展名，不超过 20 个字符。
```

目录名不计入长度限制。语义不靠文件名承载，文件名只做稳定短码；真实名称、用途和来源写入 JSON 索引。

推荐短码：

```text
c001m.png      # character 001 master card
c001e01.png    # character 001 episode 01 state card
p001m.png      # prop/item 001 master card
p001e01.png    # prop/item 001 episode 01 state card
l001m.png      # location 001 master scene card
l001e01.png    # location 001 episode 01 scene state card
f001m.png      # flag/emblem 001 master card
r001s02.png    # reference frame 001 for scene/shot group 02
d001.wav       # dialogue line 001
sfx001.wav     # sound effect 001
mx001.wav      # music cue 001
```

索引示例：

```json
{
  "file": "c001e01.png",
  "file_path": "01/assets/characters/c001e01.png",
  "asset_id": "character_shen_weisang_ep01_hunter",
  "display_name": "沈微桑 猎户状态卡",
  "asset_type": "character",
  "asset_subtype": "character_episode_state_card"
}
```

## 6. 层次推进

### 6.1 全剧基础层

`writer-room` 主导创建全剧故事基础。此阶段只创建文字事实源，不生成图像资产。

```text
bible/world.md
bible/geography.md
bible/factions.md
bible/timeline.md
bible/characters.md
bible/scenes.md
bible/continuity.md
bible/visual-style.md
outline/series-outline.md
outline/episode-outline-index.md
synopsis/story-synopsis.md
```

### 6.2 全剧生产规则与母资产层

`director-room` 创建全剧视频规则，`art-room` 创建全剧资产策略和母资产。

```text
production/series-video-rules.md
art/series-asset-plan.md
assets/asset-index.json
assets/characters/
assets/locations/
assets/props/
assets/costumes/
assets/style/
```

`production/series-video-rules.md` 固定画幅、帧率、镜头风格、动作约束、画质底线、禁止项、渲染反馈格式和 AI 音频后期规则。

`art/series-asset-plan.md` 固定哪些角色需要母卡，哪些势力需要视觉规则，哪些地点和物品跨集复用，哪些未来状态不能提前生成。

项目级 `assets/` 只放全剧复用母资产，例如 `c001m.png`、`p001m.png`、`l001m.png`。带 episode 语义的状态卡不是全剧母资产，不得放进项目级 `assets/`。

### 6.3 单集循环层

每集按固定顺序推进：

```text
writer-room：单集剧本
  -> director-room：资产前导演分镜包
  -> art-room：单集前置资产
  -> director-room：资产后视频生产包
  -> ComfyUI：渲染输出
  -> director-room：QC / 剪辑 / AI 配音 / 后期
  -> writer-room + director-room + art-room：经验写回
```

单集目录固定为：

```text
project/{project-name}/{episode-id}/
  brief/
  script/
  reports/
  director/
  shots/
  storyboard/
  continuity/
  production/
  prompts/
  art/
  assets/
    characters/
    locations/
    props/
    costumes/
    reference-frames/
    shot-overrides/
    temp/
  renders/
  qc/
  edit/
  audio/
  post/
  logs/
  memory/
```

## 7. 正式文件修改规则

正式交付物使用稳定路径作为当前事实源。文件不合格时，由 owner skill 原地修复 canonical 文件，同时用对应 report、log 或 QC 文件记录原因、影响范围和修复结论。

| 文件类型 | 修改方式 | 记录位置 | 说明 |
|---|---|---|---|
| 草稿类文本 | 可保留多稿文件 | 同目录 critique/report | 下游不读取草稿 |
| 正式 Markdown 文档 | 原地修改 canonical 文件 | 文件内 `Revision Log` 或 owner report | 例如 `production/video.md`、`art/assets.md` |
| 正式 JSON 文件 | 原地修复 canonical 文件 | 对应 QC/log/report；schema 允许时可加 `revision_log` | 保持 `shot_id`、`asset_id`、`prompt_id` 稳定 |
| 图片资产 | canonical final path + `history/` | `thread-results.json`、`asset-index.json`、`asset-qc-report.md` | 最终图只放 canonical path；旧稿或废稿进 `history/*.v001.png` |
| 视频渲染 | 原始渲染保留，状态分流 | `render-manifest.json`、`shot-qc-report.json` | raw 不静默覆盖；accepted/rejected/redraw 分别登记 |
| 音频资产 | canonical final path + takes/history | `audio-manifest.json`、`audio-qc.md` | AI 配音可保留多条 take，最终文件走短名 |
| 已交付下游文件 | owner skill 原地修复，并触发下游刷新 | owner report 和下游 tuning/QC | 下游 skill 不能偷改上游事实 |

修改流程：

```text
发现文件不符合要求
  -> 判断文件 owner skill
  -> 判断是否已被下游读取
  -> 未交付下游：owner skill 原地修复 canonical 文件
  -> 已交付下游：记录问题、影响范围和所需刷新链
  -> owner skill 修复 canonical 文件
  -> 下游 skill 刷新依赖文件
  -> QC/report/log 记录修复原因、修复内容和残留风险
```

交付锁定规则：

- `script/final-script.md` 被 `director-room` 读取后进入 handoff lock。若再改，必须重新刷新分镜、镜头表、视觉连续性和提示词。
- `shots/shot-list.json` 被 `art-room` 读取后进入 handoff lock。若再改，必须重新刷新资产清单、资产提示词和视频生产计划。
- `art/asset-index.json` 和 canonical 图片资产被 `director-room` 读取后进入 handoff lock。若再改，必须刷新 ComfyUI 镜头提示词和视频生产计划。
- `prompts/comfyui-shot-prompts.json` 进入 ComfyUI 渲染后进入 render lock。若再改，必须写入 `prompts/comfyui-tuning-log.json`。
- `audio/dialogue/*` 被剪辑使用后进入 audio lock。若再改，必须更新 `audio/audio-manifest.json` 和 `edit/edit-decision-list.json`。

## 8. 资产卡片格式

资产卡片是可复用视觉生产资产，由三部分组成：

```text
设计规格 JSON
  -> 图片生成提示词记录
  -> canonical 图片文件
```

### 8.1 角色卡

角色卡用于锁定人物身份，避免脸、年龄、体态、服装和动作习惯漂移。

角色卡分两类：

- `character_master_card`：全剧母卡，锁脸、骨相、体态、气质和身份锚点。
- `character_episode_state_card`：单集状态卡，锁本集服装、伤痕、道具、污渍、情绪和动作状态。

设计规格必须包含：

```text
asset_id
file
asset_type
asset_subtype
display_name
identity_lock
episode_state
card_layout
continuity_refs
source_refs
usage
```

`identity_lock` 必须包含：

```text
年龄/年龄感
脸型和五官
眼神
发型
皮肤质感
身高体态
动作习惯
禁止提前暴露的信息
```

### 8.2 物品卡

物品卡用于锁定道具、旗帜、徽章、器具、文书、饰物、武器、服装配件等视觉形态。

物品卡分两类：

- `prop_master_card`：跨集复用母卡，锁轮廓、材质、比例、标识和用途。
- `prop_episode_state_card`：单集状态卡，锁本集磨损、污渍、损坏、摆放和使用状态。

设计规格必须包含：

```text
asset_id
file
asset_type
asset_subtype
display_name
prop_lock
episode_state
card_layout
continuity_refs
source_refs
usage
```

`prop_lock` 必须包含：

```text
剧情用途
归属角色/势力
轮廓和比例
尺度和重量感
材质
磨损和标记
旗帜/徽章/符号规则
禁止提前暴露的信息
```

### 8.3 场景卡

场景卡用于锁定地点空间结构、地理关系、光线、材质、可拍摄区域和连续性锚点。

场景卡分两类：

- `location_master_scene_card`：跨集复用地点母卡。
- `location_episode_scene_card`：单集场景状态卡。

设计规格必须包含：

```text
asset_id
file
asset_type
asset_subtype
display_name
location_lock
episode_state
card_layout
continuity_refs
source_refs
usage
```

`location_lock` 必须包含：

```text
剧情功能
地理关系
入口和出口
空间结构
行动区
镜头可拍摄区
关键连续性锚点
禁止出现的现代/错误元素
```

## 9. 结构化提示词格式

提示词分为两层：`生产元数据` 和 `模型可见提示词`。

生产元数据给流程系统、ComfyUI 工作流、QC、剪辑和返修使用；模型可见提示词才会进入图像或视频生成模型。不要把生产元数据混进模型正文。

生产元数据包括：

```text
episode_id
shot_id
asset_id
prompt_id
output_file
asset_refs
generation_method
duration
fps
aspect_ratio
workflow_hint
source_refs
continuity_refs
```

这些字段决定“读取哪个文件、走哪个工作流、如何追踪返修”，但不会直接改善模型画面。模型真正需要的是可见内容、构图、材质、动作、光线和禁止项。

例如，不写进模型正文：

```text
episode_id: 01
shot_id: SC002-SH001
generation_method: I2V
output_file: l001e01
asset_id: location_canyangao_gate_ep01_blood_check
```

应转换成模型能生成的可见描述：

```text
残阳坳山口的狭窄木栅关门，临时验血桌，村民排队，冷白清冥标识，阴冷白日，山风、尘土和冷雾。
```

模型可见提示词固定为六段：

```text
1. 可见目标
2. 风格和画质
3. 主体内容
4. 构图与运动
5. 可见连续性约束
6. 负面提示
```

`质量控制` 不能写成生产检查清单，而应改写为会影响生成结果的视觉约束，例如“真实重心”“自然接触反作用”“真实材质”“无文字水印”。

### 9.1 角色卡提示词

角色卡提示词用于生成角色参考图或角色参考板。模型正文不包含文件名、asset ID、集数 ID 或用途说明。

生产元数据必须包含：

```text
asset_id
asset_subtype
output_file
prompt_id
source_refs
continuity_refs
usage
```

模型可见提示词必须包含：

```text
1. 可见目标
- 生成真实电影角色参考板
- 角色姓名或可见身份
- 当前可见状态

2. 风格和画质
- 超写实
- 电影级质感
- 真实皮肤
- 真实布料
- 非海报、非游戏 CG、非动漫

3. 主体内容
- 年龄感
- 脸型和五官
- 眼神
- 发型
- 身高体态
- 服装
- 随身物品
- 污渍、伤痕、风雪、尘土等可见状态

4. 构图与运动
- 正面全身
- 45 度全身
- 背面全身
- 脸部近景
- 手部和随身物品细节
- 服装材质细节
- 三种表情
- 两到三种自然动作姿态

5. 可见连续性约束
- 保持同一张脸、同一骨相、同一体态
- 保持同一服装层次和材质
- 排除会剧透的可见元素；例如不出现白色官袍、异变痕迹、未来身份标识

6. 负面提示
- 不要动漫风
- 不要游戏 CG
- 不要塑料皮肤
- 不要蜡像感
- 不要僵硬摆拍
- 不要过度美颜
- 不要文字
- 不要水印
```


角色卡完整示例。生产元数据用于流程追踪，不进入模型正文：

```text
asset_id: character_shen_weisang_master
asset_subtype: character_master_card
output_file: c001m.png
prompt_id: art-char-c001m-001
source_refs: bible/characters.md#沈微桑
continuity_refs: bible/visual-style.md
usage: face reference, costume reference, character identity lock
```

模型可见提示词示例：

```text
1. 可见目标
生成一张真实电影角色参考板。角色是沈微桑，十八岁左右的边境猎户少女，长期在山林和寒风中生活，当前状态是第一集出场前的日常猎户状态。

2. 风格和画质
超写实，电影级质感，真实皮肤纹理，真实布料纤维，低饱和冷色调，自然环境光，轻微风雪和尘土，非海报，非游戏 CG，非动漫。

3. 主体内容
她脸型偏瘦，颧骨清晰，眼神警觉克制，眉眼有长期缺觉的疲惫感。黑发束起，少量碎发被风吹乱。体态结实但不夸张，肩背有猎户习惯形成的紧绷感。穿深灰粗布短袄、旧皮护腕、磨损皮靴，腰间有短刀、绳索和小兽皮袋。衣角有泥点、干草屑和旧血痕，手指有冻裂和弓弦磨痕。

4. 构图与运动
同一画面内呈现角色参考板：正面全身、45 度全身、背面全身、脸部近景、手部和腰间随身物品细节。姿态自然，有站立警戒、半蹲查看地面、回头听声三种动作。动作要有真实重心和关节受力，不要僵硬摆拍。

5. 可见连续性约束
保持同一张脸、同一骨相、同一身高体态、同一发型和同一服装层次。短刀、皮护腕、旧皮靴和兽皮袋必须保持一致。不出现白色官袍、异变痕迹、贵族饰品、现代装备或未来身份标识。

6. 负面提示
不要动漫风，不要游戏 CG，不要塑料皮肤，不要蜡像感，不要过度美颜，不要僵硬摆拍，不要悬浮肢体，不要错误手指，不要文字，不要水印。
```

### 9.2 物品卡提示词

物品卡提示词用于生成道具、旗帜、徽章、符号、器具、文书、武器和服装配件参考图。模型正文不包含文件名、asset ID 或用途说明。

生产元数据必须包含：

```text
asset_id
asset_subtype
output_file
prompt_id
source_refs
continuity_refs
usage
```

模型可见提示词必须包含：

```text
1. 可见目标
- 生成真实电影物品参考板
- 物品名称或可见类型
- 当前可见状态

2. 风格和画质
- 超写实
- 电影级道具摄影
- 真实材质反光
- 真实磨损和重量感

3. 主体内容
- 轮廓
- 比例
- 尺度
- 材质
- 磨损
- 污渍
- 刻痕
- 旗帜/徽章/符号的形状、颜色、方向和位置

4. 构图与运动
- 主视图
- 手持比例图
- 材质近景
- 标识近景
- 使用状态或损坏状态

5. 可见连续性约束
- 标识形状不变
- 主色不变
- 比例不变
- 符号方向不变
- 不出现隐藏标记或未来状态

6. 负面提示
- 不要现代产品感
- 不要商业目录图
- 不要塑料质感
- 不要错误文字
- 不要错误徽章
- 不要发光魔法物品，除非剧情明确要求
```


物品卡完整示例。生产元数据用于资产索引和 ComfyUI 条件引用，不进入模型正文：

```text
asset_id: prop_qingming_blood_flag_master
asset_subtype: prop_master_card
output_file: f001m.png
prompt_id: art-prop-f001m-001
source_refs: bible/factions.md#清冥会
continuity_refs: assets/asset-index.json#prop_qingming_blood_flag_master
usage: flag reference, emblem lock, line reference source
```

模型可见提示词示例：

```text
1. 可见目标
生成一张真实电影物品参考板。物品是清冥会验血关卡使用的竖向布旗，当前状态是第一集山口关门外悬挂的旧旗。

2. 风格和画质
超写实，电影级道具摄影，真实布料织纹，真实磨损，冷白日光，布面有风吹褶皱和尘土，不是商业产品图，不是概念设定图。

3. 主体内容
竖向窄旗，灰白粗布材质，上端穿过黑木横杆，边缘有不规则磨损和线头。旗面中央是黑青色断环徽记：一个不完整圆环，下方有三条短竖痕，符号居中，方向固定。旗面下半部有干涸暗褐色血点和雨水冲刷痕迹。木杆有裂纹、铁钉和旧绳结，整体尺寸约成人半身高。

4. 构图与运动
同一画面内呈现主视图、背面视图、手持比例图、布料近景、徽记近景、木杆和绳结近景。旗布可以轻微摆动，但徽记形状、方向和相对位置不能变化。

5. 可见连续性约束
断环徽记形状不变，黑青主色不变，灰白布底不变，徽记永远居中且竖直，不出现额外文字，不出现其他组织符号，不出现金属发光或魔法光效。

6. 负面提示
不要现代广告旗，不要商业 logo 感，不要塑料布，不要错误文字，不要错误徽章，不要华丽新旗，不要发光魔法物品，不要水印。
```

### 9.3 场景卡提示词

场景卡提示词用于生成地点参考图。模型正文不包含输出文件短名、asset ID 或集数 ID。

生产元数据必须包含：

```text
asset_id
asset_subtype
output_file
prompt_id
source_refs
continuity_refs
usage
```

模型可见提示词必须包含：

```text
1. 可见目标
- 生成真实电影场景参考图
- 地点名称或可见地点类型
- 当前可见状态

2. 风格和画质
- 超写实
- 电影级环境摄影
- 时间
- 天气
- 主光源
- 空气质感

3. 主体内容
- 地理关系
- 入口
- 出口
- 道路、院落、房间、井、墙、平台等空间结构
- 人物行动区
- 关键连续性锚点

4. 构图与运动
- 9:16 竖屏构图
- 建立镜头视角
- 关键入口出口视角
- 人物行动区视角
- 材质和陈设细节视角

5. 可见连续性约束
- 地理结构不变
- 入口出口位置不变
- 关键锚点不变
- 时间、天气和破坏状态保持一致

6. 负面提示
- 不要现代建筑
- 不要景区感
- 不要舞台布景
- 不要空泛概念图
- 不要错误文字
- 不要水印
```


场景卡完整示例。生产元数据用于地点索引和下游镜头引用，不进入模型正文：

```text
asset_id: location_canyangao_gate_ep01
asset_subtype: location_episode_scene_card
output_file: l001e01.png
prompt_id: art-loc-l001e01-001
source_refs: bible/scenes.md#残阳坳山口
continuity_refs: 01/continuity/visual-continuity-bible.json
usage: location reference, spatial continuity, establishing shot source
```

模型可见提示词示例：

```text
1. 可见目标
生成一张真实电影场景参考图。地点是残阳坳山口的临时验血关门，当前状态是第一集白日阴冷、村民被迫排队检查的入口。

2. 风格和画质
超写实，电影级环境摄影，冷白阴天，山风，低雾，尘土，湿冷空气，低饱和灰青色影调，真实木材、泥地、布旗和旧铁器质感。

3. 主体内容
狭窄山路从画面前景通向木栅关门，左右是陡峭黄灰山壁和枯草。关门由粗木桩、横梁和临时绳索搭成，右侧有验血桌、陶碗、铁针、名单木牌，左侧有清冥会灰白竖旗。村民排队区域在路中央，守卫站位在关门两侧，后方可见通往谷内的弯路。关键锚点是木栅门、验血桌、灰白旗、山壁裂缝和地面车辙。

4. 构图与运动
9:16 竖屏建立镜头视角，略高机位俯看山口纵深，用山路作为引导线。画面要清楚显示入口、出口、排队区、守卫区和验血桌位置。空气中有轻微尘雾，旗布被风吹动，但空间结构稳定。

5. 可见连续性约束
木栅门位于画面中后部，验血桌始终在右侧，灰白竖旗始终在左侧，山路从前景通向关门再转入谷内。不要改变入口出口方向，不要增加现代建筑、石板景区路、车辆、电线或现代标牌。

6. 负面提示
不要现代建筑，不要景区感，不要舞台布景，不要空泛概念图，不要宏大奇幻城门，不要错误文字，不要干净崭新材质，不要水印。
```

### 9.4 视频制作提示词

视频制作提示词用于生成视频画面和动作。模型正文不包含 `shot_id`、`generation_method`、`asset_id`、输出文件名或工作流名称。

生产元数据必须包含：

```text
shot_id
segment_id
generation_method
duration
fps
aspect_ratio
asset_refs
first_frame_ref
last_frame_ref
audio_refs
workflow_hint
source_refs
continuity_refs
```

模型可见提示词必须包含：

```text
1. 可见目标
- 本镜头画面要发生的事情
- 画面中的角色、地点和关键物品

2. 风格和画质
- 超写实
- 电影级质感
- 真实光影
- 真实材质
- 色彩和影调

3. 主体内容
- 景别
- 角色位置
- 场景环境
- 动作内容
- 表演细节
- 关键物品

4. 构图与运动
- 画幅构图
- 摄影机位置
- 运镜方式
- 动作路径
- 速度和节奏
- 角色接触、停顿、转身、奔跑等运动细节

5. 可见连续性约束
- 角色服装、伤痕、随身物品不变
- 场景空间结构不变
- 旗帜、徽章、物品标识不变
- 屏幕方向不乱
- 不新增剧情信息
- 对白只表现为说话状态，不要求模型生成准确台词

6. 负面提示
- 不要动漫风
- 不要游戏 CG
- 不要漂浮慢动作
- 不要僵硬摆拍
- 不要滑步
- 不要肢体畸形
- 不要脸部漂移
- 不要错误服装
- 不要错误物品
- 不要错误文字
- 不要水印
```


视频制作完整示例。生产元数据用于渲染任务、资产条件和剪辑追踪，不进入模型正文：

```text
shot_id: e01-sc02-sh004
segment_id: e01-sc02-sh004-s01
generation_method: I2V
duration: 6s
fps: 24
aspect_ratio: 9:16
asset_refs: c001m.png, l001e01.png, f001m.png
first_frame_ref: r004a.png
last_frame_ref: r004b.png
audio_refs: d003.wav
workflow_hint: image-to-video with character, location, and flag references
source_refs: 01/script/final-script.md#scene-02
continuity_refs: 01/continuity/visual-continuity-bible.json
```

模型可见提示词示例：

```text
1. 可见目标
在残阳坳山口验血关门前，沈微桑站在排队村民边缘，听见守卫喊她上前，她压低呼吸，抬眼看向验血桌和灰白旗。

2. 风格和画质
超写实，电影级质感，真实冷白阴天光线，低饱和灰青色影调，真实皮肤、粗布、泥地、木栅和旗布质感，空气中有冷雾和尘土。

3. 主体内容
中近景到近景。沈微桑穿深灰粗布短袄和旧皮护腕，腰间有短刀和兽皮袋，脸上有疲惫和警觉。她原本站在人群边缘，听到声音后肩膀微微收紧，右手短暂碰到兽皮袋，随后抬眼看向右侧验血桌。背景能看到木栅关门、排队村民、左侧灰白竖旗和右侧验血桌。

4. 构图与运动
9:16 竖屏构图，摄影机在人物前方略低位置缓慢推进，先带到她的上半身，再停在脸部近景。动作速度克制真实，肩部、呼吸、眼神和手部反应要自然。人群在背景轻微移动，旗布被山风轻轻吹动。

5. 可见连续性约束
沈微桑的脸、发型、灰布短袄、皮护腕、腰间短刀和兽皮袋保持一致。验血桌在画面右侧，灰白竖旗在左侧，木栅关门在后方。只表现角色正在低声回应或准备回应，不要求视频模型生成准确台词，不新增剧情信息。

6. 负面提示
不要动漫风，不要游戏 CG，不要漂浮慢动作，不要僵硬摆拍，不要滑步，不要肢体畸形，不要脸部漂移，不要错误服装，不要错误物品，不要错误文字，不要水印。
```

## 10. ComfyUI 资产使用原则

一致性不能只靠文字提示词，必须靠资产图、参考控制和 QC。

角色卡、物品卡、场景卡在 ComfyUI 中的用途是：

```text
角色母卡 -> 锁脸、骨相、体态
角色状态卡 -> 锁服装、伤痕、道具、表演状态
物品卡 -> 锁物品形状、材质、徽章、旗帜、封印
场景卡 -> 锁空间结构、光线、地理关系
参考帧 -> 锁首帧、末帧、镜头衔接
```

工作流配置未确认前，方案不写死具体节点名称。只固定控制目标：

```text
reference image：用于角色、服装、物品和场景一致性
face reference：用于脸部身份一致性
pose/depth/line reference：用于姿态、空间和旗帜轮廓一致性
inpaint/redraw：用于修复徽章、文字、手、脸、物品局部错误
```

## 11. 旗帜、徽章和精细物品一致性

旗帜、徽章、符号、名册、封印和文字类物品属于高精度资产，不能只靠扩散模型自由生成。

推荐流程：

```text
先做旗帜/徽章/符号母卡
  -> 做线稿或轮廓参考
  -> 镜头生成时使用 reference + line/depth/canny 类控制
  -> 失败时局部重绘
  -> 仍要求精确时，后期合成透明 PNG/SVG
```

高精度标识必须在 `asset-index.json` 里有唯一 `asset_id`、短文件名、颜色、形状、方向、位置规则和禁止变体。

如果徽章必须完全一致，优先使用透明 PNG/SVG 后期合成。视频模型只负责生成干净承载区域和自然布料运动，不负责创造精确徽章。

## 12. 长镜头处理

不建议一次生成超过 30 秒的完整长镜头。生产上应拆成多个短片段，视觉上再剪成连续长镜头感。

推荐规则：

```text
一个叙事长镜头
  -> 多个 4-8 秒生产片段
  -> 上一段末帧作为下一段首帧参考
  -> 使用同一角色/场景/物品资产
  -> 保持光线、屏幕方向、动作状态
  -> 剪辑中隐藏断点
```

字段建议：

```text
long_take_id
segment_id
first_frame_ref
last_frame_ref
continuity_bridge
```

## 13. AI 配音和后期方案

AI 可以完成配音和大量后期辅助，但不建议让视频模型直接一次性生成带精准对白的视频。

原因：

- 视频模型很难稳定生成准确台词。
- 声音、口型、字幕和角色身份容易失控。
- 一旦对白错了，整段视频往往要重做。
- 后期单独处理音频更容易返修。

推荐简单方案：

```text
视频模型生成无对白或弱口型表演画面
  -> AI TTS 生成每句对白音频
  -> 字幕文件对齐对白
  -> 必要时用口型同步工具处理近景说话镜头
  -> 剪辑中用反应镜头、背影、过肩镜头降低口型压力
  -> 最后合成对白、音效、环境声、音乐和字幕
```

对白不按每个分镜逐条创建，而按对白句、旁白句和声音事件管理。一个镜头可以没有对白，也可以引用同一条对白音频；一条对白也可以跨多个反应镜头播放。

对白生产单位：

```text
dialogue line：一句角色对白
voiceover line：一句旁白
sfx cue：一个音效事件
music cue：一段音乐情绪
```

3 分钟视频的简单工作量估算：

```text
总时长：约 180 秒
镜头数量：约 25-45 个
对白/旁白：约 20-45 句
AI TTS 生成：约 10-30 分钟
挑选与重配：约 30-90 分钟
字幕和剪辑对齐：约 30-90 分钟
近景口型同步：只处理少量关键镜头，可能额外 1-3 小时
```

为了降低工作量，第一版采用“配音先行但口型弱绑定”的制作方式：

```text
先整理对白和字幕
  -> 批量生成 AI TTS
  -> 粗剪时按音频长度调整镜头
  -> 说话近景减少长台词
  -> 多用背影、侧脸、过肩、反应镜头承接对白
  -> 只对关键近景做口型同步或重绘
```

视频提示词只控制表演状态，不承载完整对白。可以写：

```text
角色低声说话，嘴唇轻微开合，呼吸压低，眼神警觉。
```

不要写：

```text
让角色准确说出整句台词。
```

对白文本固定来自：

```text
script/final-script.md
post/subtitle-script.md
audio/dialogue-plan.json
```

AI 配音文件建议：

```text
audio/dialogue/d001.wav
audio/dialogue/d002.wav
audio/dialogue/d003.wav
audio/sfx/sfx001.wav
audio/music/mx001.wav
```

后期文件建议：

```text
audio/voice-bible.md
audio/dialogue-plan.json
audio/audio-manifest.json
audio/audio-qc.md
post/subtitle-script.md
post/sound-plan.md
post/color-plan.md
post/delivery-qc-report.md
```

`audio/voice-bible.md` 固定角色声音：年龄感、音色、语速、气息、情绪、禁区。没有真人配音能力时，使用 AI TTS 或 AI voice generation 生成对白；如果没有口型同步能力，镜头设计优先使用短台词、侧脸、背影、反应镜头和字幕。

## 14. 项目级文件

| 路径 | 用处 | Owner | 创建时机 | 修复方式 |
|---|---|---|---|---|
| `project.json` | 项目元数据、状态、全剧输入、当前阶段 | `writer-room` 初始化，三方可读 | 项目启动 | 协调者更新状态，不写剧情细节 |
| `bible/world.md` | 世界观规则 | `writer-room` | 全剧基础层 | 剧情事实变更时由 `writer-room` 修订 |
| `bible/geography.md` | 地理、路线、区域关系 | `writer-room` | 全剧基础层 | 与场景/分镜冲突时先修 bible，再刷新下游 |
| `bible/factions.md` | 种族、势力、阶层、制度 | `writer-room` | 全剧基础层 | 只记录故事 canon，不写资产 prompt |
| `bible/timeline.md` | 历史事件和纪年 | `writer-room` | 全剧基础层 | 重大剧情变更后由 `writer-room` 修订 |
| `bible/characters.md` | 全剧角色文字圣经 | `writer-room` | 全剧基础层 | 角色事实变更后修订，下游资产需重新 QC |
| `bible/scenes.md` | 跨集地点和场景文字圣经 | `writer-room` | 全剧基础层 | 地点事实变更后修订，下游场景卡需重新 QC |
| `bible/continuity.md` | 已确认播出事实和连续性状态 | `writer-room` 主导 | 每集完成后写回 | 只写最终确认事实，不写失败生成结果 |
| `bible/visual-style.md` | 故事侧视觉基调和禁区 | `writer-room` 草拟，`art-room` 读取 | 全剧基础层 | 不替代资产风格 bible |
| `outline/series-outline.md` | 全剧大纲 | `writer-room` | 全剧基础层 | 剧本重构时修订 |
| `outline/episode-outline-index.md` | 分集大纲索引 | `writer-room` | 全剧基础层 | 每集调整时更新 |
| `synopsis/story-synopsis.md` | 全剧梗概 | `writer-room` | 全剧基础层 | 对外梗概变化时更新 |
| `production/series-video-rules.md` | 全剧视频制作规则 | `director-room` | 全剧基础层后 | 根据渲染和后期经验最小修订 |
| `art/series-asset-plan.md` | 全剧资产规划 | `art-room` | 全剧 bible 稳定后 | 新增母资产或禁区时修订 |
| `assets/asset-index.json` | 全剧共享资产索引 | `art-room` | 首批母资产生成后 | 资产 QC 后更新状态 |
| `legacy/` | 旧项目原始材料只读归档 | 协调者创建，三方可读 | 旧项目迁移开始 | 不在此处修正文档，只保留原样证据 |
| `migration/migration-map.json` | 旧路径到新 canonical 路径的映射 | 三方共同维护，协调者收口 | 旧项目迁移开始 | owner skill 更新映射状态和缺口 |
| `migration/backfill-plan.md` | 旧项目缺失文件和需重建资产清单 | 三方共同维护，协调者收口 | 迁移盘点后 | 按 owner skill 分派补齐任务 |
| `migration/migration-report.md` | 迁移结论、风险、通过项和阻塞项 | 三方共同审核，协调者收口 | 迁移 QC 后 | 修复后原地更新并重审 |
| `memory/current-state.md` | 当前制作状态 | 三方写回，协调者收口 | 项目启动 | 每集完成后摘要更新 |
| `memory/failure-patterns.json` | 失败模式和修复策略 | `director-room` 主导 | 首次失败反馈后 | 只记录可复用生产经验 |
| `memory/evolution-notes.md` | skill 或流程演进建议 | 三方写回 | 每轮复盘后 | 需要人工批准后才改 skill |

## 15. 单集文件

| 路径 | 用处 | Owner | 创建时机 | 修复方式 |
|---|---|---|---|---|
| `brief/episode-brief.md` | 单集创作目标 | `writer-room` | 单集启动 | 剧本重做前修订 |
| `script/episode-outline.md` | 单集故事大纲 | `writer-room` | 单集剧本前 | 由 `writer-room` 修订 |
| `script/script-v01.md` | 初稿剧本 | `writer-room` | 单集剧本阶段 | 按 critique 重写，可保留多稿 |
| `script/final-script.md` | 导演交接剧本 | `writer-room` | 剧本通过评分后 | 分镜开始后原则上不改；必须改则全链刷新 |
| `reports/critique-v01.md` | 剧本诊断 | `writer-room` | 初稿后 | 仅记录诊断，不改剧本 |
| `reports/continuity-report.md` | 剧本连续性报告 | `writer-room` | 最终剧本后 | 剧本变更后重跑 |
| `reports/script-score.md` | 剧本评分 | `writer-room` | 最终剧本后 | 剧本重写后重跑 |
| `director/director-brief.md` | 导演阐释和镜头原则 | `director-room` | 读取最终剧本后 | 不改剧情，只改拍法 |
| `director/camera-plan.md` | 摄影、机位、运动计划 | `director-room` | shot list 后 | 根据镜头 QC 修订 |
| `shots/scene-breakdown.json` | 场景拆分 | `director-room` | 导演阶段 | 剧本变更后重建 |
| `shots/shot-list.json` | 稳定镜头表 | `director-room` | 场景拆分后 | 保持 `shot_id` 稳定 |
| `storyboard/storyboard-plan.md` | 双语分镜说明 | `director-room` | 摄影计划后 | 只修拍法和可视信息 |
| `continuity/visual-continuity-bible.json` | 本集视觉连续性锁 | `director-room` | 分镜后 | 资产/镜头冲突时最小修订 |
| `production/generation-plan.json` | 每镜头生成方式和依赖资产 | `director-room` | 分镜后 | 根据资产和模型反馈修订 |
| `production/video-production-plan.md` | 本集视频生产方案 | `director-room` | 资产前创建，资产后刷新 | 原地更新，并写 Revision Log |
| `production/render-manifest.json` | 渲染任务和输出登记 | `director-room` | ComfyUI 生产开始 | 每次渲染追加或更新状态 |
| `prompts/shot-prompts-draft.json` | 镜头提示词草稿 | `director-room` | generation plan 后 | 资产完成后刷新 |
| `prompts/comfyui-prompt-brief.md` | ComfyUI 提示词总说明 | `director-room` | 资产后提示词刷新 | 根据 QC 最小修订 |
| `prompts/comfyui-style-preset.json` | ComfyUI 风格预设 | `director-room` | 资产后提示词刷新 | 根据生产规则最小修订 |
| `prompts/comfyui-asset-prompt-pack.json` | 资产条件包 | `director-room` | 资产后提示词刷新 | 根据 asset index 刷新 |
| `prompts/comfyui-shot-prompts.json` | 可生产双语镜头提示词 | `director-room` | 资产后提示词刷新 | 根据 QC 和 tuning log 修订 |
| `prompts/comfyui-workflow-plan.json` | 工作流参数计划 | `director-room` | 资产后提示词刷新 | 不发明未知 checkpoint/node ID |
| `prompts/comfyui-tuning-log.json` | 渲染反馈和调参记录 | `director-room` | 首轮渲染后 | 每次修复写入原因和结果 |
| `reports/comfyui-prompt-qc.md` | 提示词 QC 报告 | `director-room` | 提示词完成后 | 渲染反馈后可更新 |
| `art/asset-prep-plan.md` | 本集前置资产准备计划 | `art-room` | 读取 shot list 和 generation plan 后 | 资产范围变更时修订 |
| `art/asset-manifest.json` | 本集资产清单 | `art-room` | asset-prep-plan 后 | 保持 `asset_id` 稳定 |
| `art/character-designs.json` | 角色母卡/状态卡设计 | `art-room` | asset manifest 后 | 只修资产设计，不改角色 canon |
| `art/location-designs.json` | 场景卡设计 | `art-room` | asset manifest 后 | 只修视觉设计，不改地点 canon |
| `art/prop-costume-designs.json` | 物品和服装设计 | `art-room` | asset manifest 后 | 只修视觉设计，不改剧情用途 |
| `art/style-continuity-bible.json` | 资产侧风格连续性 | `art-room` | 设计 JSON 后 | 解决资产之间的风格漂移 |
| `prompts/art-image-prompts.json` | 角色/场景/物品/参考帧图像提示词 | `art-room` | 资产设计完成后 | 根据资产 QC 修订 |
| `art/thread-plan.json` | 后台图片生成线程计划 | `art-room` | 图像提示词后 | 只在输出路径稳定后创建 |
| `art/thread-results.json` | 图片生成线程结果 | `art-room` | 图片生成后 | 记录最终文件和 history 文件 |
| `art/asset-index.json` | 本集资产索引 | `art-room` | 资产 QC 后 | 标记 ready/missing/retry |
| `assets/characters/` | 本集角色状态卡 | `art-room` | 资产生产阶段 | 例如 `c001e01.png`；不得放入项目级 `assets/characters/` |
| `assets/locations/` | 本集场景状态卡 | `art-room` | 资产生产阶段 | 例如 `l001e01.png`；不得放入项目级 `assets/locations/` |
| `assets/props/` | 本集道具状态卡 | `art-room` | 资产生产阶段 | 例如 `p001e01.png`；不得放入项目级 `assets/props/` |
| `assets/costumes/` | 本集服装状态卡 | `art-room` | 资产生产阶段 | 服装跟随 `prop_episode_state_card` 路由；不得放入项目级 `assets/costumes/` |
| `art/asset-qc-report.md` | 资产质量报告 | `art-room` | 资产生成后 | 说明可用性和重做建议 |
| `assets/reference-frames/` | 本集首帧、末帧、关键参考帧 | `art-room` | 资产生产阶段 | 草稿进 `history/`，最终留 canonical path |
| `assets/shot-overrides/` | 单镜头局部覆盖参考 | `art-room` | 失败镜头修复时 | 只为目标镜头服务 |
| `assets/temp/` | 临时资产暂存 | `art-room` | 图片生产中 | 交接前必须清空或归档 |
| `renders/raw/` | 原始渲染结果 | `director-room` 登记 | ComfyUI 输出后 | 不直接删除，供 QC 追溯 |
| `renders/accepted/` | 通过 QC 的镜头 | `director-room` | QC 通过后 | 若后续否决，移出 accepted |
| `renders/rejected/` | 不采用镜头 | `director-room` | QC 拒绝后 | 记录拒绝原因 |
| `renders/redraw/` | 局部重绘结果 | `director-room` | REDRAW 修复后 | 关联原始镜头 |
| `qc/shot-qc-report.json` | 单镜头 QC 状态 | `director-room` | 每批渲染后 | 按镜头状态持续更新 |
| `qc/episode-qc-report.md` | 本集成片 QC | `director-room` | 粗剪或成片后 | 记录残留风险 |
| `edit/edit-plan.md` | 剪辑策略 | `director-room` | accepted 镜头足够后 | 根据节奏和镜头可用性调整 |
| `edit/edit-decision-list.json` | 剪辑决策列表 | `director-room` | 粗剪时 | 保留镜头顺序、时长、转场、音频引用 |
| `audio/voice-bible.md` | 角色声音圣经 | `director-room` | 单集后期前 | 按角色声音设定原地修订 |
| `audio/dialogue-plan.json` | AI 配音任务表 | `director-room` | 字幕/对白整理后 | 保持 dialogue id 稳定 |
| `audio/audio-manifest.json` | 音频文件索引 | `director-room` | AI 音频生成后 | 记录 take、最终文件和使用位置 |
| `audio/audio-qc.md` | 音频 QC 报告 | `director-room` | 音频生成后 | 记录重配和残留风险 |
| `audio/dialogue/` | AI 对白音频 | `director-room` | AI TTS 后 | 最终短名，废稿进 takes/history |
| `audio/sfx/` | 音效 | `director-room` | 后期阶段 | 可 AI 生成或素材化 |
| `audio/music/` | 配乐 | `director-room` | 后期阶段 | 可 AI 生成或素材化 |
| `post/post-production-plan.md` | 后期计划 | `director-room` | 粗剪后 | 调色、字幕、声音策略修订 |
| `post/subtitle-script.md` | 字幕文本 | `director-room` | 后期阶段 | 对照 final-script 和实际剪辑修订 |
| `post/sound-plan.md` | 音效、环境声、配乐计划 | `director-room` | 后期阶段 | 按剪辑节奏修订 |
| `post/color-plan.md` | 调色方案 | `director-room` | 后期阶段 | 按全剧规则修订 |
| `post/delivery-qc-report.md` | 交付 QC | `director-room` | 最终输出后 | 记录通过/阻塞项 |
| `logs/*-agent-calls.jsonl` | 代理调用记录 | 各 skill | 各阶段运行时 | 只追加，不作为剧情事实源 |
| `memory/current-state.md` | 本集状态摘要 | 三方写回 | 每集阶段结束 | 只写确认状态 |
| `memory/failure-patterns.json` | 本集失败模式 | `director-room` 主导 | QC 后 | 可晋升到项目级 memory |
| `memory/evolution-notes.md` | 本集流程改进建议 | 三方写回 | 复盘后 | 需要批准后才改 skill |

## 16. 环节生成与下游读取清单

下表固定每一环节的生成文件和下一环节读取文件。下游只能读取表中固定输入；需要额外输入时，先修改本方案，再修改 skill。

| 环节 | Owner | 本环节生成/更新 | 下一环节固定读取 |
|---|---|---|---|
| 旧项目迁移 | `writer-room`、`director-room`、`art-room` | `legacy/`、`migration/migration-map.json`、`migration/backfill-plan.md`、`migration/migration-report.md`、必要的 canonical 项目级和单集级文件 | 迁移后进入 `全剧基础创建`、`全剧视频规则`、`全剧母资产规划` 或指定单集阶段；下游只读取通过迁移 QC 的 canonical 文件，不直接读取 `legacy/` |
| 全剧基础创建 | `writer-room` | `project.json`、`bible/world.md`、`bible/geography.md`、`bible/factions.md`、`bible/timeline.md`、`bible/characters.md`、`bible/scenes.md`、`bible/continuity.md`、`bible/visual-style.md`、`outline/series-outline.md`、`outline/episode-outline-index.md`、`synopsis/story-synopsis.md` | `director-room` 读取 `bible/characters.md`、`bible/scenes.md`、`bible/continuity.md`、`bible/visual-style.md`；`art-room` 读取 `bible/characters.md`、`bible/scenes.md`、`bible/visual-style.md` |
| 全剧视频规则 | `director-room` | `production/series-video-rules.md` | `director-room` 单集分镜读取；`art-room` 资产风格规划读取 |
| 全剧母资产规划 | `art-room` | `art/series-asset-plan.md`、`assets/asset-index.json`、`assets/characters/*`、`assets/locations/*`、`assets/props/*`、`assets/costumes/*`、`assets/style/*` | `director-room` 读取 `assets/asset-index.json`；`art-room` 单集资产读取 `art/series-asset-plan.md` 和 `assets/asset-index.json`。项目级 `assets/` 只承载 `*_master_card` 和全剧 style reference，不承载 `*episode*` 状态卡 |
| 单集剧本 | `writer-room` | `{episode-id}/brief/episode-brief.md`、`{episode-id}/script/episode-outline.md`、`{episode-id}/script/script-v01.md`、`{episode-id}/script/final-script.md`、`{episode-id}/reports/critique-v01.md`、`{episode-id}/reports/continuity-report.md`、`{episode-id}/reports/script-score.md` | `director-room` 读取 `bible/characters.md`、`bible/scenes.md`、`{episode-id}/script/final-script.md`、`{episode-id}/reports/continuity-report.md`、`{episode-id}/reports/script-score.md` |
| 资产前导演分镜包 | `director-room` | `{episode-id}/director/director-brief.md`、`{episode-id}/shots/scene-breakdown.json`、`{episode-id}/shots/shot-list.json`、`{episode-id}/director/camera-plan.md`、`{episode-id}/storyboard/storyboard-plan.md`、`{episode-id}/continuity/visual-continuity-bible.json`、`{episode-id}/production/generation-plan.json`、`{episode-id}/production/video-production-plan.md`、`{episode-id}/prompts/shot-prompts-draft.json` | `art-room` 读取 `bible/characters.md`、`bible/scenes.md`、`{episode-id}/script/final-script.md`、`{episode-id}/director/director-brief.md`、`{episode-id}/director/camera-plan.md`、`{episode-id}/shots/scene-breakdown.json`、`{episode-id}/shots/shot-list.json`、`{episode-id}/storyboard/storyboard-plan.md`、`{episode-id}/continuity/visual-continuity-bible.json`、`{episode-id}/production/generation-plan.json`、`{episode-id}/prompts/shot-prompts-draft.json` |
| 单集前置资产 | `art-room` | `{episode-id}/art/asset-prep-plan.md`、`{episode-id}/art/asset-manifest.json`、`{episode-id}/art/character-designs.json`、`{episode-id}/art/location-designs.json`、`{episode-id}/art/prop-costume-designs.json`、`{episode-id}/art/style-continuity-bible.json`、`{episode-id}/prompts/art-image-prompts.json`、`{episode-id}/art/thread-plan.json`、`{episode-id}/art/thread-results.json`、`{episode-id}/art/asset-index.json`、`{episode-id}/art/asset-qc-report.md`、`{episode-id}/assets/characters/*`、`{episode-id}/assets/locations/*`、`{episode-id}/assets/props/*`、`{episode-id}/assets/costumes/*`、`{episode-id}/assets/reference-frames/*`、`{episode-id}/assets/shot-overrides/*` | `director-room` 读取 `assets/asset-index.json`、`{episode-id}/art/asset-index.json`、`{episode-id}/art/asset-qc-report.md`、`{episode-id}/prompts/art-image-prompts.json`、canonical image asset paths、`{episode-id}/production/generation-plan.json`、`{episode-id}/prompts/shot-prompts-draft.json` |
| 资产后视频生产包 | `director-room` | `{episode-id}/prompts/comfyui-prompt-brief.md`、`{episode-id}/prompts/comfyui-style-preset.json`、`{episode-id}/prompts/comfyui-asset-prompt-pack.json`、`{episode-id}/prompts/comfyui-shot-prompts.json`、`{episode-id}/prompts/comfyui-workflow-plan.json`、`{episode-id}/production/video-production-plan.md`、`{episode-id}/reports/comfyui-prompt-qc.md` | ComfyUI 生产读取 `{episode-id}/prompts/comfyui-shot-prompts.json`、`{episode-id}/prompts/comfyui-style-preset.json`、`{episode-id}/prompts/comfyui-workflow-plan.json`、`{episode-id}/production/generation-plan.json`、canonical asset paths |
| ComfyUI 渲染登记 | `director-room` 登记 | `{episode-id}/production/render-manifest.json`、`{episode-id}/renders/raw/*` | `director-room` QC 读取 `{episode-id}/production/render-manifest.json`、`{episode-id}/renders/raw/*`、`{episode-id}/shots/shot-list.json`、`{episode-id}/continuity/visual-continuity-bible.json` |
| 镜头 QC 与修复分流 | `director-room` | `{episode-id}/qc/shot-qc-report.json`、`{episode-id}/renders/accepted/*`、`{episode-id}/renders/rejected/*`、`{episode-id}/renders/redraw/*`、`{episode-id}/prompts/comfyui-tuning-log.json` | 剪辑读取 `{episode-id}/qc/shot-qc-report.json`、`{episode-id}/renders/accepted/*`、`{episode-id}/shots/shot-list.json`；若 `needs_asset_fix`，`art-room` 读取相关 QC 记录；若 `needs_script_fix`，`writer-room` 读取相关 QC 记录 |
| 剪辑 | `director-room` | `{episode-id}/edit/edit-plan.md`、`{episode-id}/edit/edit-decision-list.json`、`{episode-id}/qc/episode-qc-report.md` | AI 配音和后期读取 `{episode-id}/edit/edit-decision-list.json`、`{episode-id}/edit/edit-plan.md`、`{episode-id}/script/final-script.md`、`{episode-id}/renders/accepted/*` |
| AI 配音与声音 | `director-room` | `{episode-id}/audio/voice-bible.md`、`{episode-id}/audio/dialogue-plan.json`、`{episode-id}/audio/audio-manifest.json`、`{episode-id}/audio/audio-qc.md`、`{episode-id}/audio/dialogue/*`、`{episode-id}/audio/sfx/*`、`{episode-id}/audio/music/*` | 后期读取 `{episode-id}/audio/audio-manifest.json`、`{episode-id}/audio/audio-qc.md`、`{episode-id}/edit/edit-decision-list.json`、`{episode-id}/post/subtitle-script.md` |
| 后期与交付 QC | `director-room` | `{episode-id}/post/post-production-plan.md`、`{episode-id}/post/subtitle-script.md`、`{episode-id}/post/sound-plan.md`、`{episode-id}/post/color-plan.md`、`{episode-id}/post/delivery-qc-report.md` | 写回读取 `{episode-id}/post/delivery-qc-report.md`、`{episode-id}/qc/episode-qc-report.md`、`{episode-id}/qc/shot-qc-report.json`、`{episode-id}/audio/audio-qc.md`、`{episode-id}/art/asset-qc-report.md` |
| 经验写回 | `writer-room`、`director-room`、`art-room` | `bible/continuity.md`、`memory/current-state.md`、`memory/failure-patterns.json`、`memory/evolution-notes.md`、`assets/asset-index.json`、`{episode-id}/memory/current-state.md`、`{episode-id}/memory/failure-patterns.json`、`{episode-id}/memory/evolution-notes.md` | 下一集 `writer-room` 读取 `bible/continuity.md`、`memory/current-state.md`；下一集 `director-room` 读取 `production/series-video-rules.md`、`memory/failure-patterns.json`；下一集 `art-room` 读取 `art/series-asset-plan.md`、`assets/asset-index.json` |

## 17. 三个 Skill 的文件动作

### 17.1 writer-room

`writer-room` 创建和修复故事事实，不生成分镜、不生成图像、不写 ComfyUI 参数、不生成音频。

创建：

- 项目级 `bible/*`、`outline/*`、`synopsis/*`。
- 单集 `brief/*`、`script/*`、`reports/continuity-report.md`、`reports/script-score.md`。
- 单集和项目级 story memory。

修复：

- 只修故事层文件：剧本、角色文字 bible、场景文字 bible、连续性报告。
- 若分镜、资产、视频或后期阶段发现故事问题，相关部门只能提出 `needs_script_fix`，不能直接改剧本。

### 17.2 director-room

`director-room` 创建镜头生产事实、视频提示词、渲染 QC、剪辑和 AI 音频后期计划，不改故事 canon，不直接生成图片资产。

创建：

- `director/*`
- `shots/*`
- `storyboard/*`
- `continuity/visual-continuity-bible.json`
- `production/*`
- `prompts/comfyui-*`
- `qc/*`
- `edit/*`
- `audio/*`
- `post/*`

修复：

- 镜头失败时先更新 `qc/shot-qc-report.json`。
- 提示词问题修 `comfyui-shot-prompts.json` 和 `comfyui-tuning-log.json`。
- 镜头策略问题修 `generation-plan.json` 或 `video-production-plan.md`。
- 资产问题标记 `needs_asset_fix`，交回 `art-room`。
- 剧本问题标记 `needs_script_fix`，交回 `writer-room`。
- 音频问题修 `audio/dialogue-plan.json`、`audio/audio-manifest.json` 和 `audio/audio-qc.md`。

### 17.3 art-room

`art-room` 创建图像资产计划、角色卡、物品卡、场景卡、资产提示词和资产 QC，不改剧本，不改 shot list。

创建：

- 项目级 `art/series-asset-plan.md`
- 项目级 `assets/*`
- 项目级 `assets/asset-index.json`
- 单集 `art/*`
- 单集 `prompts/art-image-prompts.json`
- 单集 `assets/characters/*`、`assets/locations/*`、`assets/props/*`、`assets/costumes/*`
- 单集 `assets/reference-frames/*` 和 `assets/shot-overrides/*`

修复：

- 最终资产只保留在 canonical `output_path`。
- 中间图、废稿、替代版本进入同级 `history/`，命名为 `.v001`、`.v002`。
- 如果角色脸、物品形态、场景地理与 bible 冲突，不能偷偷改 bible；先标记冲突，再由 owner skill 处理。

## 18. QC / 剪辑 / 后期规则

QC 状态必须机器可读：

```text
accepted
needs_redraw
needs_regenerate
needs_prompt_tuning
needs_asset_fix
needs_script_fix
needs_audio_fix
blocked
```

QC 检查：

- 剧情信息是否正确。
- 角色身份、服装、年龄、物品是否一致。
- 旗帜、徽章、符号、名册等高精度资产是否一致。
- 动作是否有真实重心、惯性、接触反作用和自然速度。
- 画面是否符合超写实、电影级、极致逼真要求。
- 连续镜头的人物位置、方向、伤痕、物品和光线是否可接。
- 对白、字幕、音频文件和剪辑时长是否对齐。
- 是否存在手崩、脸崩、错误文字、穿模、背景闪烁、分辨率/FPS异常。

剪辑不是独立创作新剧情，只根据 `shot-list.json`、`accepted` 镜头、对白长度和实际可用时长组织节奏。后期计划覆盖字幕、声音、调色和交付 QC。

## 19. 写回经验规则

写回必须区分事实和经验：

- 故事事实写回 `writer-room` owner 文件。
- 资产经验写回 `art-room` owner 文件。
- 镜头、视频生产、AI 配音和后期经验写回 `director-room` owner 文件。

失败生成结果不能写成剧情 canon。只有最终成片确认的信息，才允许进入 `bible/continuity.md`。

## 20. 旧项目迁移方案

旧项目不能直接当作新流程的 canonical 项目使用。迁移的目标不是保留旧目录形状，而是把旧剧本、旧分镜、旧资产、旧提示词、旧渲染和旧后期材料映射到本方案固定目录，并由 owner skill 审核后进入正式文件。

### 20.1 迁移原则

- 旧文件先进入 `legacy/` 作为只读证据，不在原地改写。
- 新流程只读取 canonical 文件；`legacy/` 不能成为下游固定输入。
- 能通过 schema、连续性和视觉 QC 的旧内容，可以映射为正式文件。
- 不能通过 QC 的旧内容，只能写入 `migration/backfill-plan.md`，由 owner skill 重建或修复。
- 旧提示词不能原样继承；必须拆成生产元数据和模型可见提示词两层。
- 旧资产不能只按文件名继承；必须补齐 `asset_id`、短文件名、asset subtype、canonical path、source refs、continuity refs 和 QC 状态。
- 旧成片事实只有经过最终确认后，才允许进入 `bible/continuity.md`。

### 20.2 迁移固定文件

```text
legacy/
migration/migration-map.json
migration/backfill-plan.md
migration/migration-report.md
```

`migration/migration-map.json` 记录旧路径、新路径、owner skill、迁移状态和缺口：

```json
{
  "items": [
    {
      "legacy_path": "old/story/episode1.md",
      "canonical_path": "01/script/final-script.md",
      "owner": "writer-room",
      "status": "mapped",
      "needs_backfill": false
    },
    {
      "legacy_path": "old/assets/hero.png",
      "canonical_path": "assets/characters/c001m.png",
      "owner": "art-room",
      "status": "needs_qc",
      "needs_backfill": true,
      "reason": "missing character design fields and asset subtype"
    }
  ]
}
```

`migration/backfill-plan.md` 只列需要补齐或重建的内容，不直接替代正式文件。`migration/migration-report.md` 给出最终结论：哪些旧内容已成为 canonical，哪些被丢弃，哪些需要重新生成。

### 20.3 三个 skill 的迁移分工

`writer-room` 负责迁移故事事实：

```text
旧世界观、旧角色设定、旧剧情梗概、旧剧本
  -> bible/world.md、bible/characters.md、bible/scenes.md、outline/*、script/final-script.md、reports/continuity-report.md
```

`art-room` 负责迁移视觉资产：

```text
旧角色图、旧物品图、旧场景图、旧风格参考、旧资产提示词
  -> art/series-asset-plan.md、assets/asset-index.json、art/asset-manifest.json、character-designs.json、location-designs.json、prop-costume-designs.json、art-image-prompts.json、asset-qc-report.md
```

`director-room` 负责迁移分镜、视频提示词、渲染和后期：

```text
旧分镜、旧 shot list、旧视频提示词、旧渲染、旧剪辑、旧音频、旧字幕
  -> director/*、shots/*、storyboard/*、production/*、prompts/comfyui-*、qc/*、edit/*、audio/*、post/*
```

### 20.4 迁移流程

1. 创建新项目根，把旧材料完整放入 `legacy/`。
2. 建立 `migration/migration-map.json`，逐项标出旧路径、目标 canonical 路径和 owner skill。
3. `writer-room` 先迁移故事基础层，补齐全剧 bible、分集大纲、最终剧本和连续性报告。
4. `director-room` 基于迁移后的最终剧本重建或校准资产前导演分镜包。
5. `art-room` 基于迁移后的 bible 和分镜，迁移可用资产并补齐角色卡、物品卡、场景卡和资产提示词。
6. `director-room` 读取通过 QC 的资产，刷新资产后视频生产包、视频提示词、渲染登记、剪辑和 AI 配音文件。
7. 三方共同更新 `migration/backfill-plan.md` 和 `migration/migration-report.md`，确认哪些内容进入 canonical，哪些内容需要重做。
8. 迁移完成后，下游只读取 canonical 文件，不能继续读取 `legacy/`。

### 20.5 迁移模式选择

推荐默认采用保守迁移：

```text
保留旧剧本事实和可验证资产
  -> 重建资产卡和结构化提示词
  -> 重新做分镜 QC、资产 QC、视频提示词 QC
  -> 只复用通过 QC 的旧渲染或旧音频
```

只有当旧项目本身已有稳定角色卡、资产索引、镜头表、提示词和渲染 QC 时，才采用快速迁移。快速迁移也必须先通过 `migration/migration-report.md`，不能跳过 owner skill 审核。

## 21. Skill 修改开发计划

本节是后续修改 `writer-room`、`director-room`、`art-room` 的执行计划。方案确认前不修改 skill；方案确认后按阶段推进，每一阶段都要同步 skill 文档、agent task cards、schema、测试和本方案。

### 21.1 开发原则

- 先改契约，再改 agent 工作流，最后改示例和测试。
- 每次只让一个 skill 成为主改对象，其他 skill 只做必要的输入/输出兼容。
- 正式文件名、JSON 字段、提示词结构和下游读取文件必须先在本方案确认，再写入 skill。
- skill 内不能保留旧术语、临时说明或补丁痕迹；每次修改后都要重读 `SKILL.md`，确认正文是完整清稿。
- 所有新增 JSON 输出必须有 schema；所有新增 schema 必须有测试覆盖。
- 三个 skill 的边界不能混写：`writer-room` 不生成资产/视频/音频，`art-room` 不改剧本/shot list，`director-room` 不生成资产图片、不改故事 canon。

### 21.2 阶段 0：冻结方案契约

目标：把本方案作为三个 skill 修改的唯一设计输入。

修改对象：

```text
docs/04-project-development/04-design/ai-drama-production-skill-system.md
tests/test_ai_drama_production_skill_plan_doc.py
.factory/memory/current-state.md
```

必须冻结的内容：

```text
文件短名规则
项目级和单集级目录
正式文件修改规则
环节生成与下游读取清单
角色卡/物品卡/场景卡定义
生产元数据与模型可见提示词分层
ComfyUI 资产使用原则
AI 配音与后期方案
```

验收条件：

```text
方案文档无旧术语和补丁痕迹
方案测试覆盖关键术语和交接链
不修改三个 skill 本体
```

### 21.3 阶段 1：修改 writer-room

目标：让 `writer-room` 生成完整全剧基础层和单集剧本层，并写回最终成片 canon。

修改对象：

```text
skills/writer-room/SKILL.md
skills/writer-room/agents/showrunner-agent.md
skills/writer-room/agents/story-architect-agent.md
skills/writer-room/agents/character-agent.md
skills/writer-room/agents/scene-agent.md
skills/writer-room/agents/continuity-agent.md
skills/writer-room/agents/memory-librarian.md
skills/writer-room/agents/learning-evolution-agent.md
skills/writer-room/assets/templates/*
skills/writer-room/schemas/writer-room-project.schema.json
tests/test_writer_room_skill.py
```

需要新增或固定的输出：

```text
bible/world.md
bible/geography.md
bible/factions.md
bible/timeline.md
bible/visual-style.md
outline/episode-outline-index.md
{episode-id}/script/final-script.md
{episode-id}/reports/continuity-report.md
{episode-id}/reports/script-score.md
memory/current-state.md
```

工作流修改：

```text
series mode：创建全剧 bible、分集大纲和故事梗概
episode mode：创建单集 brief、outline、draft、final script、continuity report、score
writeback mode：只把最终成片确认事实写回 bible/continuity.md 和 memory/current-state.md
```

禁止事项：

```text
不生成图片资产
不生成视频提示词
不生成音频
不写 ComfyUI 参数
不把失败生成结果写成剧情 canon
```

验收测试：

```text
test_writer_room_skill.py 覆盖新增 project layout
测试 writer-room 输出包含新增 bible 文件
测试 writer-room 不声明图像资产、视频渲染或音频生产职责
测试 final-script.md 仍是 director-room 固定输入
```

### 21.4 阶段 2：修改 director-room 的导演与视频生产契约

目标：让 `director-room` 产出资产前导演分镜包，并在资产完成后产出资产后视频生产包。

修改对象：

```text
skills/director-room/SKILL.md
skills/director-room/agents/director-agent.md
skills/director-room/agents/scene-breakdown-agent.md
skills/director-room/agents/shot-planner-agent.md
skills/director-room/agents/cinematographer-agent.md
skills/director-room/agents/storyboard-agent.md
skills/director-room/agents/visual-continuity-agent.md
skills/director-room/agents/generation-strategy-agent.md
skills/director-room/agents/shot-prompt-agent.md
skills/director-room/agents/prompt-director-agent.md
skills/director-room/agents/asset-conditioning-agent.md
skills/director-room/agents/shot-prompt-engineer-agent.md
skills/director-room/agents/workflow-parameter-agent.md
skills/director-room/agents/prompt-qc-agent.md
skills/director-room/references/comfyui-prompting-guide.md
skills/director-room/schemas/*
tests/test_director_room_skill.py
```

需要新增或固定的输出：

```text
{episode-id}/production/video-production-plan.md
{episode-id}/production/render-manifest.json
{episode-id}/qc/shot-qc-report.json
{episode-id}/qc/episode-qc-report.md
{episode-id}/edit/edit-plan.md
{episode-id}/edit/edit-decision-list.json
{episode-id}/post/post-production-plan.md
{episode-id}/post/subtitle-script.md
{episode-id}/post/sound-plan.md
{episode-id}/post/color-plan.md
{episode-id}/post/delivery-qc-report.md
```

需要新增或扩展的 schema：

```text
video-production-plan.schema.json
render-manifest.schema.json
shot-qc-report.schema.json
episode-qc-report.schema.json
edit-decision-list.schema.json
post-production-plan.schema.json
delivery-qc-report.schema.json
```

提示词契约修改：

```text
comfyui-shot-prompts.json 分成 production metadata 和 model-visible prompt
模型可见提示词不得包含 output_file、shot_id、generation_method、asset_id、episode_id
生产元数据保留 shot_id、generation_method、asset_refs、duration、fps、aspect_ratio、workflow_hint
```

验收测试：

```text
测试新增输出路径全部出现在 director-room SKILL.md
测试新增 schema 存在并包含 title/type
测试 comfyui-shot-prompts schema 支持 metadata 与 model-visible prompt 分层
测试 director-room 不改 final-script.md，不生成资产图片
测试 QC 状态包含 accepted、needs_redraw、needs_regenerate、needs_prompt_tuning、needs_asset_fix、needs_script_fix、needs_audio_fix、blocked
```

### 21.5 阶段 3：修改 art-room

目标：让 `art-room` 支持全剧母资产和单集前置资产，并固定角色卡、物品卡、场景卡及对应图像提示词结构。

修改对象：

```text
skills/art-room/SKILL.md
skills/art-room/agents/art-director-agent.md
skills/art-room/agents/asset-breakdown-agent.md
skills/art-room/agents/character-design-agent.md
skills/art-room/agents/environment-design-agent.md
skills/art-room/agents/prop-costume-design-agent.md
skills/art-room/agents/style-continuity-agent.md
skills/art-room/agents/image-prompt-agent.md
skills/art-room/agents/thread-plan-agent.md
skills/art-room/agents/asset-qc-agent.md
skills/art-room/references/thread-image-workflow.md
skills/art-room/schemas/*
tests/test_art_room_skill.py
```

需要新增 reference：

```text
skills/art-room/references/asset-card-prompt-templates.md
```

该 reference 固定：

```text
角色卡定义和字段
物品卡定义和字段
场景卡定义和字段
生产元数据字段
模型可见提示词六段结构
短文件名规则
旗帜、徽章、符号和高精度物品策略
```

需要新增或固定的输出：

```text
art/series-asset-plan.md
assets/asset-index.json
{episode-id}/art/asset-prep-plan.md
{episode-id}/art/asset-manifest.json
{episode-id}/art/character-designs.json
{episode-id}/art/location-designs.json
{episode-id}/art/prop-costume-designs.json
{episode-id}/art/style-continuity-bible.json
{episode-id}/prompts/art-image-prompts.json
{episode-id}/art/thread-plan.json
{episode-id}/art/thread-results.json
{episode-id}/art/asset-index.json
{episode-id}/art/asset-qc-report.md
```

需要新增或扩展的 schema：

```text
series-asset-plan.schema.json
asset-prep-plan.schema.json
character-designs.schema.json
location-designs.schema.json
prop-costume-designs.schema.json
style-continuity-bible.schema.json
asset-manifest.schema.json
art-image-prompts.schema.json
asset-index.schema.json
```

资产与提示词契约：

```text
asset-manifest.json 必须包含 asset_id、asset_type、asset_subtype、file、output_path、source_refs、continuity_refs、usage
art-image-prompts.json 必须分离 production metadata 和 model-visible prompt
模型可见提示词不得包含 output_file、asset_id、episode_id、source_refs、usage
角色卡/物品卡/场景卡必须有明确的可见连续性约束和负面提示
```

验收测试：

```text
测试新增 reference 存在并包含角色卡、物品卡、场景卡、模型可见提示词
测试短文件名规则存在且不含扩展名不超过 20 个字符
测试 canonical output_path 不指向 history/
测试 master card 只能指向项目级 `assets/`，episode state card 只能指向 `{episode-id}/assets/`
测试 asset_subtype 枚举包含 character_master_card、character_episode_state_card、prop_master_card、prop_episode_state_card、location_master_scene_card、location_episode_scene_card
测试 art-room 不改剧本、不改 shot list、不写 ComfyUI 工作流参数
```

### 21.6 阶段 4：修改 director-room 的 AI 配音与后期能力

目标：让 `director-room` 支持无真人配音能力时的 AI TTS、字幕、声音和交付 QC 流程。

修改对象：

```text
skills/director-room/SKILL.md
skills/director-room/agents/audio-planner-agent.md
skills/director-room/agents/edit-planner-agent.md
skills/director-room/agents/delivery-qc-agent.md
skills/director-room/schemas/dialogue-plan.schema.json
skills/director-room/schemas/audio-manifest.schema.json
skills/director-room/schemas/audio-qc.schema.json
skills/director-room/schemas/edit-decision-list.schema.json
tests/test_director_room_skill.py
```

需要新增输出：

```text
{episode-id}/audio/voice-bible.md
{episode-id}/audio/dialogue-plan.json
{episode-id}/audio/audio-manifest.json
{episode-id}/audio/audio-qc.md
{episode-id}/audio/dialogue/
{episode-id}/audio/sfx/
{episode-id}/audio/music/
```

音频契约：

```text
对白按 dialogue line 管理，不按每个分镜逐条配音
一个镜头可以引用 0 条、1 条或多条 dialogue line
一条 dialogue line 可以跨多个镜头播放
视频提示词只描述说话状态，不要求模型生成准确台词
AI TTS 输出进入 audio/dialogue/，最终文件使用短文件名
```

验收测试：

```text
测试 audio 输出路径和 schema 存在
测试 dialogue-plan 支持 dialogue_id、speaker、text、emotion、target_duration、linked_shots、output_file
测试 edit-decision-list 支持 audio_refs
测试 QC 状态包含 needs_audio_fix
测试 director-room 文档明确不推荐视频模型直接生成精准对白
```

### 21.7 阶段 5：端到端试点验证

目标：用一个短试点项目验证三间房共享目录、文件交接、提示词结构、资产引用和 AI 音频后期链路。

试点范围：

```text
1 个项目
1 集
3-5 个场景
8-12 个镜头
2 个角色
1 个场景卡
1 个物品卡
1 个旗帜/徽章类高精度资产
3-6 句 AI TTS 对白
```

验证内容：

```text
writer-room 能生成全剧基础层和单集 final-script
director-room 能生成资产前导演分镜包
art-room 能生成前置资产清单和图像提示词
director-room 能基于 asset-index 刷新资产后视频生产包
QC 能把问题分流到 needs_asset_fix、needs_prompt_tuning、needs_audio_fix
音频文件能被 edit-decision-list 引用
经验写回不会把失败生成结果写入 canon
```

验收测试：

```text
新增或扩展三间房 skill tests
新增最小 sample project fixture 或 schema fixture
运行 writer-room / director-room / art-room 相关定向测试
运行 ai-drama-production-skill-system 文档测试
```

### 21.8 开发顺序

按下面顺序实施，避免一次性大改：

1. 冻结本方案和测试。
2. 修改 `writer-room` 全剧基础层和写回规则。
3. 修改 `director-room` 资产前导演分镜包和资产后视频生产包。
4. 修改 `art-room` 资产卡、短文件名、图像提示词和资产 QC。
5. 修改 `director-room` AI 配音、剪辑和后期文件。
6. 做端到端试点。
7. 根据试点问题回到方案修订，再进入下一轮 skill 实现。

## 22. 第一版落地范围

第一版不追求自动完成完整商业级成片，只追求把三间房的目录、文件、提示词、资产和音频交接链跑通。

必须完成：

```text
共享项目根
全剧基础 bible
单集 final-script
资产前导演分镜包
单集资产准备计划
角色卡/物品卡/场景卡格式
模型可见提示词结构
资产后视频生产包
渲染登记和镜头 QC
AI TTS 对白计划
剪辑和后期交付 QC
经验写回
```

暂不要求：

```text
自动调用真实 ComfyUI
自动调用真实 TTS provider
自动完成口型同步
自动完成最终视频合成
自动发布
```

这些能力可以在目录和文件契约稳定后，作为下一阶段运行时工具链集成。
