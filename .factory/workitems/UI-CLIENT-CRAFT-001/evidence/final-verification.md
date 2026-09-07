# UI skill 与候选验证

- 日期：2026-09-07
- Work item：UI-CLIENT-CRAFT-001
- 验证者：主线程；独立评审另行记录。
- 结论：passed（限定为本次 skill 修改、场景输入与隔离候选的已列检查；不是美术批准或 ita-club 验收）。

## 1. 报告控制

| 字段 | 内容 |
|---|---|
| 精确候选 | 5f28867b4039dfcfc631c9b5fb11ef529539c319b878e9336cf13934cb9a6884 |
| 批次验证结论 | passed |
| 范围 | Shanforge UI skill、场景输入与静态候选；非产品发布 |

候选为下列文件按列出顺序执行 `shasum -a 256 <files> | shasum -a 256` 的摘要：skills/ui-ux-pro-max/SKILL.md、references/visual-direction-and-quality.md、references/mobile-high-fidelity.md、references/design-workflow-and-deliverables.md（后三者同属该 skill）、docs/02-user-guide/user-guide.md、tests/test_ui_ux_pro_max_skill.py、tests/fixtures/ui-craft-cases.json、evidence/pilot/ 的 index.html、styles.css、app.js、verify.cjs、input.json（后五者位于本 work item）。不含随评审更新的治理投影。

## 新鲜命令与结果

以下命令均从 Shanforge 根目录执行；uv 使用 `UV_CACHE_DIR=/tmp/shanforge-ui-uv-cache`。

| 完整命令 | exit code | 真实结果 |
|---|---|---|
| `UV_CACHE_DIR=/tmp/shanforge-ui-uv-cache uv run pytest -q tests/test_ui_ux_pro_max_skill.py tests/test_ui_design_candidates.py` | 0 | 57 passed |
| `UV_CACHE_DIR=/tmp/shanforge-ui-uv-cache uv run pytest -q` | 0 | 406 passed, 11 subtests passed |
| `UV_CACHE_DIR=/tmp/shanforge-ui-uv-cache uv run ruff check tests/test_ui_ux_pro_max_skill.py` | 0 | All checks passed! |
| `UV_CACHE_DIR=/tmp/shanforge-ui-uv-cache uv run python skills/tdd-workflow/scripts/check_code_shape.py tests/test_ui_ux_pro_max_skill.py` | 0 | 无错误输出 |
| `UV_CACHE_DIR=/tmp/shanforge-ui-uv-cache uv run python /Users/uroborus/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/ui-ux-pro-max` | 0 | Skill is valid! |
| `PLAYWRIGHT_MODULE=/Users/uroborus/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright /Users/uroborus/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node .factory/workitems/UI-CLIENT-CRAFT-001/evidence/pilot/verify.cjs` | 0 | passed 9 screenshots |
| `git diff --check` | 0 | 无错误输出 |
| `UV_CACHE_DIR=/tmp/shanforge-ui-uv-cache uv run python skills/document-templates/scripts/validate_test_documents.py --report .factory/workitems/UI-CLIENT-CRAFT-001/evidence/final-verification.md` | 0 | report: valid |

## 5. 结果汇总

| 总数 | 通过 | 失败 | 错误 | 阻塞 | 跳过 | 未运行 | 取消 |
|---|---|---|---|---|---|---|---|
| 406 | 406 | 0 | 0 | 0 | 0 | 0 | 0 |

统计仅为 pytest 本次收集的主测试节点，另有 11 subtests passed；不重复加计其子集 57 定向测试或浏览器截图。这不是正式产品完整验收目录，不能据此计算 ita-club 项目测试通过率。

- 建议：`GO`

该建议只表示已列工程检查通过，可交独立评审及归档；不是部署、正式采用视觉稿或产品发布授权。

## 浏览器环境与覆盖

- 输入：`evidence/pilot/index.html` 的静态 file URL；无独立服务，端口/健康接口/服务停止为 N/A。浏览器在 finally 中关闭，无用户登录态、无业务 API。
- 默认沙箱首次启动被 macOS MachPort 权限拒绝；隔离启动权限下复验成功。未绕过浏览器安全提示、未降低业务系统权限。
- 320/390/430 × 工作台/日程/学员详情，共 9 张实际页面截图。
- 断言快照时间与下一节、三个课程标题/时长、禁用签到、无错误学员下钻、观察/复盘来源、导航返回、训练建议展开/收起、展开后横向溢出与页面错误。
- 主线程实际查看三张 390 截图并退回一次集中视觉整改；问题与证据边界见 `pilot-observations.md`。最终画面是有反馈整改候选，不是零指导生成或 A/B improved。

## Red / Green 与需求核对

- T01 执行者先运行新 fixture 完整性测试，缺文件导致 1 failed / 56 passed（exit 1）；补入 fixture 后 57 passed（exit 0），主线程再次独立重跑得到相同 Green。这个 Red 只证明场景输入缺失可被捕获，不证明美术质量。
- T02 空白页面错误、事实/导航问题经运行与回源暴露，整改后主线程重新运行 browser verify 为 exit 0。不能用首张空白 PNG 的文件存在作为成功。
- 已把普通高频业务页/复杂状态纳入样板选择；被退回为粗糙的范围回到样板整改；未退回的批准首页与局部修复边界保留。
- 业务对象关系、真实参考转化、样板/正式资源职责、设计质量/实现还原/功能验证分别记录；原生控件与位图边界未改变。
- 四类新增 fixture 是可执行输入目录，不是四次已运行的模型实验。测试只检查其完整性与引用。
- `ls -ld /Users/uroborus/.codex/skills/ui-ux-pro-max` 确认当前宿主链接指向本仓库 skill，无需安装；没有修改该链接或其他宿主。

## 未验证与残余风险

未运行受控同模型同预算 A/B、四类场景逐一模型试做、人工盲评、微信真机/Taro 对齐、长文案与多权益完整组合、完整无障碍或真实业务验收。原稿的状态与 generated_at 并非实时一致，候选保留其源快照与样例标注，不把 fixture 改成真实今日数据。

新规则与截图返工可以暴露和阻止不合格候选扩页，不保证所有模型一次生成优秀画面。最终采用仍需要用户确认；本轮仅归档候选，不修改 ita-club。

文档校验入口首次无参数调用返回 exit 2（要求指定 --catalog/--report），不是测试失败；随后以本报告为 --report 进行正式七态/候选/建议一致性校验。

独立评审已返回 approved / 98 / C0-I0-M1；M-01 仅要求正式采用时移出内部说明，作为未批准静态候选归档不阻塞。人工美术、真机与产品采用边界不变。
