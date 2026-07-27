# 移动端高保真美术方向

## 确认记录

- 确认日期：2026-07-24
- 确认结论：以 B“现代城市服务”为基础，吸收 A 的温暖摄影风格和 C 的少量材质感。
- 状态：美术方向和资源清单均已确认；最终资源已通过独立评审。

## 确认来源

| 来源 | 角色 |
|---|---|
| [`approved/b-primary-ui-direction.png`](approved/b-primary-ui-direction.png) | 主参考：信息架构、蓝色主基线、状态层级和操作效率 |
| [`approved/a-warm-photography-reference.png`](approved/a-warm-photography-reference.png) | 辅助参考：自然暖光、真实生活服务摄影和亲近感 |
| [`approved/c-material-reference.png`](approved/c-material-reference.png) | 辅助参考：暖石色、纸张/矿物质感和安静留白 |

三张确认图只约束视觉方向，不作为可直接开发的页面位图；正式文字、图标和组件必须在 Penpot 与代码中重建。

## 稳定方向

- 信息气质：专业、高效、清醒，但不做成企业后台。
- 主色：冷白和深靛蓝/钴蓝建立可信与状态层级；青绿色只用于成功或辅助强调。
- 摄影：使用自然暖光、真实空间和真实服务过程；肤色自然，避免棚拍塑料感和无关素材拼贴。
- 材质：纸张或矿物纹理只用于大面积背景的低强度层，建议不透明度不超过 6%，不得影响文字对比度。
- 字体：各平台系统字体；品牌标题可增加字重和字距，不把文字烘焙进图片。
- 图标：使用平台或项目既有线性图标；不生成装饰性 3D 图标。
- 组件：清晰分区、克制圆角、细边框和轻阴影；价格、状态和主操作保持最高可读性。

## 平台映射

- iOS、Android、微信小程序共享内容、语义 token、摄影和材质方向。
- 导航、返回、系统栏、安全区、触控目标、字体缩放和支付交互分别遵守平台规范。
- 同一摄影源允许按平台比例确定性裁切，不为每个平台重新生成不同人物或场景。

## 排除

- 低保真线框直接美化后交付。
- 荧光渐变、重玻璃拟态、红金传统符号和书法堆砌。
- 把综合生活服务做成理疗或 SPA 专门应用。
- AI 生成错字、伪文字、伪图标进入正式页面。

## 后续生成关键词

`modern urban service, warm natural lifestyle photography, cool white and deep indigo UI, restrained jade accent, subtle warm-stone paper texture, authentic Chinese home-service scene, clear commercial mobile product hierarchy`

资源清单见 [`sprite-spec.md`](sprite-spec.md)；最终候选见
[`preview/preview.html`](preview/preview.html)。
