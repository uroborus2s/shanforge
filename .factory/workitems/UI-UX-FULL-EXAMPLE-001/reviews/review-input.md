# UI-UX-FULL-EXAMPLE-001 评审输入

## 评审范围

- `.factory/workitems/UI-UX-FULL-EXAMPLE-001/**`
- `skills/ui-ux-pro-max/examples/omnichannel-service-platform/**`
- `skills/ui-ux-pro-max/SKILL.md` 的样例入口
- 用户当前连接的 Penpot 文件

## 重点检查

1. 一个新成员能否从 `docs/index.md` 理解系统、进入需求、设计、接口、测试和运维。
2. PRD 是否清楚说明系统目标、用户故事、REQ、AC、NFR，而不是零散任务。
3. 需求追踪矩阵能否按稳定 ID 准确找到模块、数据、API、UI 和测试。
4. 四端是否共享业务语义但保留平台导航、权限、支付、通知和适配差异。
5. 后台是否使用中文业务标题、独立详情页和返回列表，而不是侧边栏详情。
6. OpenAPI 是否详细解释接口用途、幂等、错误、权限和兼容性。
7. 测试用例、结果和报告是否区分“定义”“一次执行事实”“人类结论”。
8. 文档裁剪规则是否能避免空模板和同一事实的平行版本。
9. 管理后台是否统一使用 React + shadcn/ui（Radix / `new-york`）、Lucide 和 CSS/Motion，且没有页面级混用第二套通用组件、图标或动效库。
10. T06 九项资源是否符合已确认 B+A+C 方向、尺寸、裁切、人物连续性、无文字/
    商标/水印、manifest 追溯和 `tmp/` 清理要求。

## 已验证

详见 `../evidence/verification.md`。

## 已知限制

- Penpot 源结构、Token 和原型交互可用。
- shadcn/ui 仓内契约已更新；Penpot 插件当前未连接，管理后台画板的新组件元数据待同步。
- `export_shape` PNG/SVG 均返回 `http error`，没有静态预览。
- 样例不包含业务实现，所以测试报告为 `NO-GO`，不是伪造的通过报告。
- T06 资源包已有本地桌面/移动预览；Penpot 高保真同步尚未执行。

## 期望结论

- `approved`：接受样例结构和视觉，并允许后续把模式吸收进正式方案；
- `changes_requested`：列出需修改的文档、页面或关系；
- 不因静态导出工具故障否认源设计，但应单独决定是否把导出恢复作为批准前门禁。
