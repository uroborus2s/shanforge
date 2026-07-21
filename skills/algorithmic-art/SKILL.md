---
name: algorithmic-art
description: 使用 p5.js 创建原创算法艺术。适用于用户请求代码生成艺术、交互式生成作品、种子随机、流场、粒子系统或参数化视觉实验；输出可复现、可运行、可验证的 HTML/JS 作品，避免模仿在世艺术家或复制受版权保护风格。
license: 完整条款请参阅 LICENSE.txt
---

# Algorithmic Art

用于把创作意图实现为原创 p5.js 生成艺术。默认交付可运行作品；只有用户需要创作说明时，才额外写概念短文。

## 何时使用

- 用户要求用代码创作生成艺术、算法艺术、流场、粒子、噪声、参数化图形或交互式视觉实验。
- 作品需要种子随机、参数滑块、可复现输出、导出图片或自包含 HTML 查看器。
- 用户给出抽象主题，需要转成数学、运动、颜色和交互规则。

## 不使用

- 用户要照片、插画、图标、品牌视觉稿或普通图片编辑；改用图像生成或 UI/UX 技能。
- 用户要求模仿具体在世艺术家、复制受版权保护作品或复刻现有作品。
- 任务只是普通前端页面，不需要生成算法。
- 用户只要静态 SVG/Canvas 小图标，且不需要 p5.js 或交互参数。

## 工作方式

1. 先明确交付物：自包含 HTML、独立 JS、概念说明，或三者组合。
2. 生成交互式作品前必须读取 `templates/viewer.html`；需要算法结构参考时读取 `templates/generator_template.js`。
3. 使用种子控制 `randomSeed` 与 `noiseSeed`，相同种子必须产出相同画面。
4. 参数数量保持少而有效；优先控制密度、尺度、运动、颜色、噪声、迭代次数。
5. 颜色和运动服务主题，不堆随机特效；性能不足时减少粒子数或缓存计算。

## 输出契约

非 Shanforge work item 的轻量交付至少回写：

- `status`: `done` 或 `blocked`
- `outputs`: 生成的 `.html`、`.js`、`.md` 文件路径和默认 seed
- `evidence`: 已读取模板、实现文件、截图/运行记录、关键参数说明
- `verification`: 浏览器 smoke check、控制台错误、seed 复现、导出功能或性能观察；未运行要说明原因
- `needs`: 仍需用户选择的主题、尺寸、色彩方向、导出格式或交互范围

若在 Shanforge work item 中使用，只回写状态包，不替 `using-shanforge` 决定 review、人工确认、提交或下一步 skill：

```text
工作结果：
- work_item: <WORKITEM-ID or none>
- skill: algorithmic-art
- status: ready_for_review | blocked | needs_user_input
- outputs:
  - <html/js/md paths>
- evidence:
  - <template reads, screenshot/smoke check, seed reproduction notes, or evidence path>
- ledger_event: <event id or none>
- needs:
  - review | user_input | none
```

## 验证要求

- HTML 必须能独立打开或按项目方式运行。
- 同一 seed 的构图、颜色和参数结果稳定。
- 交互控件可用，下载/重置等承诺功能可用。
- 浏览器控制台不能有阻断错误；高负载算法要有粒子数或质量参数。

## Blocked 语义

返回 `blocked` 的情况包括：模板文件不可读、用户要求侵权式风格复刻、运行环境无法验证、缺少必须的尺寸/输出格式且无法合理默认。`blocked` 必须说明已完成的创作决策、阻塞证据和继续所需的最小输入。

`needs_user_input` 用于必须由用户选择主题、尺寸、色彩方向、交互范围或导出格式的情况；能用安全默认值继续实现时不要阻塞。

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
