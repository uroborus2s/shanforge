# UI 设计决策与美术质量实施计划

- work_item_id: `UI-VISUAL-QUALITY-001`
- status: `completed`
- input: 用户已批准前轮八项重构方案及新增优秀 UI 美术学习。
- architecture: 保持 skill-first；主入口约束关键决定，单个新增 reference 承载视觉学习与质量细则；Python 标准库检索只返回候选及证据。
- upstream: `brief.md`、`docs/05-design/technical-selection.md`、`docs/05-design/system-architecture.md`。
- risk: `high`（已公布 CLI 的输出与持久化语义变化）；用户已批准根因与改法，独立计划评审后执行。

## Work Breakdown

| id | parent_id | title | status |
|---|---|---|---|
| WBS-UI-VISUAL-QUALITY-01 | | 候选检索与正式规则保护 | completed |
| WBS-UI-VISUAL-QUALITY-02 | | 美术学习与设计流程 | completed |
| WBS-UI-VISUAL-QUALITY-03 | | 集中验证、独立评审与交付 | completed |

TaskCard 与 WBS 以 task-briefs 中 T01/T02/T03 一一对应；三个任务均为 system，不计产品功能进度。

## 共享 CLI 与交付契约

1. 保留 `--design-system`、`--domain`、`--stack`、`--json`、`--format`、`--persist`、`--page`、`--max-results` 及原有 dials 入口。设计系统结果明确为候选；不保证原最终设计字典/文案兼容，迁移写入用户指南。
2. 设计系统新增可选 `--platform`（web/mini-program/apple/android/desktop）、`--surface`（persuade/operate/read/experience）、`--locale`。未指定平台可以用确定性的 stack 对应推断；React Native/Flutter 等多端或未知不武断推断。显式冲突报清晰参数错误，不能忽略任何参数。没有上下文仍可查询通用候选，附待决项。
3. 设计系统结果包含 `schema_version`、`kind=design_candidates`、`status=candidate`、query、project_name、context、按域分组的 candidates、advisory reasoning、unresolved、warnings。每条候选保留来源文件与行/ID、匹配依据；排名只表示词法匹配，不是审美或可访问性分数。
4. color/typography/style/product 候选不强行组合，不用行业 priority 污染原始检索；landing 仅在 surface=persuade 时作为候选。零命中返回空列表和 unresolved，不补 Hero/Inter/蓝色；CSV 缺失给真实错误或警告。中文由 agent 在保留原意后提取双语关键词，脚本不翻译。CJK 字体覆盖需要真实字体证据，数据库标签不是验证结论。
5. 栈查询在设计系统分支实际消费。跨域设计候选过滤 CSS Import、GSAP Snippet 等平台代码；原生端绝不注入 Web 代码或 hover 清单。dials 仅记录意图，不决定风格、spacing 或安装运行时。平台规范与项目现有组件高于检索建议。
6. `--json` 输出单个合法 JSON 文档（包括实际 persistence 回执），其他提示走 stderr；max-results 需正整数。互斥 domain/design-system、无效 persist/page/dials 组合报错，不静默忽略。
7. `--persist` 只向 `design-system/<project>/candidates/` 独占创建候选文件，返回真实路径；`--page` 仅作为候选的页面上下文；不得创建/覆盖 MASTER.md 或 pages 下文件，不复用旧自动覆盖规则。普通不 persist 调用不写文件。保留路径安全处理并测相邻正式文件内容不变。
8. CLI 与公开 generate_design_system 用法的签名尽量兼容，旧内部 master/override 生成器若无真实调用则删除，避免保留可误调用的正式写入入口。JSON/Markdown/ASCII 都呈现同一候选语义，不复制业务逻辑。

## T01：候选检索

### 参数与失败规则（计划评审补充）

| 输入 | 规则 |
|---|---|
| design-system + json + format | json 优先，stdout 始终一个 JSON；format 只控制非 JSON 文本 |
| design-system + stack | stack 指导加入候选结果；不走单独 stack 输出 |
| domain + stack 或 domain + design-system | argparse 错误，exit 2，stderr 说明冲突，stdout 为空 |
| persist/output-dir | persist 仅用于 design-system，output-dir 必须伴随 persist |
| page | 仅用于 design-system，可不 persist，作为页面上下文 |
| platform/surface/locale/dials/format | 仅用于 design-system，否则明确错误；json/max-results 在查询模式仍可用 |
| query 空白或 max-results 小于 1 | exit 2；不创建文件 |
| I/O 写入失败或候选文件碰撞 | 非零退出，stderr 说明失败，不输出成功；不修改既有文件 |

`generate_design_system()` 保留现有位置参数与新增可选关键字参数，仍返回 str；output_format=json 返回候选 JSON 字符串，其他格式返回候选文本。`DesignSystemGenerator.generate()` 返回新的候选 dict；旧最终设计字段不承诺兼容。数据/格式错误使用明确 ValueError，文件冲突保留 FileExistsError 供 CLI 报错；不伪造成功回执。

平台表：react/nextjs/vue/svelte/astro/nuxtjs/nuxt-ui/html-tailwind/shadcn/threejs/angular/laravel 对应 web；swiftui 对应 apple（涵盖 macOS）；jetpack-compose 对应 android；javafx/wpf/winui/uwp 对应 desktop。flutter/react-native/avalonia/uno 是跨端，不自动推断；显式平台支持 web/apple/android/desktop，mini-program 必须另用宿主实现。已知单端栈与显式平台不一致报错。未来未分类 stack 不推断，记录 unresolved；每个现有栈的推断/冲突规则都有参数化测试。

候选文件使用页面安全 slug（未提供则 candidate）+ uuid4 随机后缀，固定 `.json`，以 x 模式独占创建。重复调用生成新文件；碰撞报错不重试覆盖。测试通过冻结 UUID 在函数边界强制碰撞，并核对旧候选、Master、pages 文件字节不变。合法 JSON 的持久化回执包含实际 created_files，不要求保存文件包含其自身路径。

文件与 owner：严格使用 T01 写集（3 个已有脚本和 `tests/test_ui_design_candidates.py`），不得写 T02 文件。

- [x] 用 subprocess 与临时目录覆盖零命中、中文、stack/json、dials、相冲突参数、source 追溯、持久化与页面正式文件保护，记录预期 RED。
- [x] 修改 core 的最小来源支持；在 design_system 删除最终值自动选择与正式写入，将 CLI 参数透传结果构造器。复用已有安全路径和 CSV 检索，不引入新依赖。
- [x] `uv run pytest tests/test_ui_design_candidates.py -q` 通过。
- [x] `uv run python skills/tdd-workflow/scripts/check_code_shape.py skills/ui-ux-pro-max/scripts/core.py skills/ui-ux-pro-max/scripts/design_system.py skills/ui-ux-pro-max/scripts/search.py tests/test_ui_design_candidates.py` 通过；单调用 helper 候选按真实职责人工解释，不定义局部命名函数。

## T02：设计与美术学习

文件与 owner：严格使用 T02 写集；只新增一个视觉 reference、一个 12 brief JSON，复用现有样例和交付结构。

- [x] 入口任务分流：新建/整体重设计比较方向，既有批准方向继承，局部修改直接做，只读评审不写。目标平台约束在选视觉前确定。
- [x] 新 reference 写具体案例学习法：先找实际界面/原作者案例，观察目标页面和交互；记录 URL、日期、实际看见的内容、学习方法、适用条件、拟转化与禁止照抄部分。默认少量互补案例，同领域任务可用性+跨领域视觉表达；来源无法查看时明确证据缺口，不能说已经看图学习。旧方向和小修改按需，不强制每次调研。收集链接数量、Star、获奖不能替代视觉依据。
- [x] 差异方向同内容同视口比较，至少构图/信息组织/字体/影像的真实差异；只换颜色不算。默认每方向一个关键页，选定后扩展状态；已有选择不重复确认。
- [x] 加入中文排版（字面、字重、标点、数字、换行、混排、字体覆盖与授权）、品牌影像一致性、克制装饰与实际截图评审。位图只用于需要摄影/插画/纹理，组件/文字/图标保持原生或代码；共享素材规范进入通用 reference，mobile 保留平台特有事项。
- [x] 补平台组件契约和动效降级，修 admin 的 UI 动画资产归属冲突。shadcn 基线仍沿用，明确产品构图与品牌可定制。
- [x] 更新来源登记采用 frontend-design / Impeccable 的方法，补原始优秀设计案例入口与学习示例；只采纳实际核对的来源，不声称抓取了未看过截图。用户指南提供新的 CLI 行为、候选持久化路径、设计学习流程和宿主同步边界。
- [x] 12 个真实可执行 brief 覆盖 4 种页面任务、中文/双语、多端、既有设计保护、局部修改；含稳定 ID、prompt、context、可观察成功条件。说明旧/新同模型同预算、盲评、原始画面与行为证据；当前不预填运行结果。
- [x] 修改既有 UI skill 测试以适应新参考及候选 CLI；保留真实链接/元数据检查，不增加大段精确文案断言冒充行为检验。
- [x] `uv run pytest tests/test_ui_ux_pro_max_skill.py -q`；`uv run python /Users/uroborus/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/ui-ux-pro-max`；`git diff --check`。

## 集中质量与交付

视觉实验协议：每个 fixture 固定 ID、用户 prompt、真实样本文案/数据、页面与状态、平台/栈、主视口及适用的第二视口、期望截图与行为证据。运行时固定旧/新 skill commit、模型、工具、预算，产物随机标 A/B，由未参与生成的 reviewer 盲评并记录身份。构图层级、中文排版、内容/品牌特异性、影像一致性和细节完成度各记 1–5（1=明显缺陷、3=满足、5=充分且有具体证据）；同条件新方案多数维度更好且无主要可用性回退才记该案例 improved，否则 unchanged/regressed/incomplete。汇总原始观察与每例结论，不以平均分掩盖回退、不将未运行计通过。本次仅交付实验输入与协议，不预填评审人或 A/B 运行结果。

1. T01、T02 同层且写集隔离，共享契约固定后并行；worker 按 AGENTS 的 Terra/medium，reviewer Terra/high 独立只读。
2. 父级运行新鲜 `uv run pytest -q`（skill 主入口/测试跨路由影响，仓库规模可控）、`uv run ruff check tests/test_ui_design_candidates.py tests/test_ui_ux_pro_max_skill.py`、skill validator、代码形状与 diff 检查；无软件服务/API运行时，不启动无关端口。
3. 一套 `evidence/verification.md`、`reports/implementation.md`、`reviews/review-input.md` 记录候选、覆盖与未覆盖；独立 reviewer 做代码/语义/中文审查和最小前向输入检查。Critical/Important 同范围整改后复测复审。
4. 12 brief 语料与检查方法是本次重构产物，真实 12 组产品 UI 截图 A/B 未运行必须披露；不能因自动检查通过宣布已消除一切模板化。
5. 更新当前 work item 与 `.factory/memory/agent-session.md`、`current-state.md`、`tasks.summary.md`、`tests.summary.md`、`skill-updates.summary.md`、`review-ledger.jsonl`。不写全局 memories。
6. 通过后按用户 AGENTS 用 gitcommitzh 只提交当前范围，不 push。以现有 `scripts/sync-codex-skills --help` 查找单 skill 同步入口；如支持，按权限同步并 readback，否则明确宿主尚未同步。

## 计划自审

规格覆盖：八项方案与案例学习均对应 T01/T02，验证与交付对应 T03。文件没有共享写入，跨任务唯一共享接口为本计划中的候选 CLI。用户批准的行为变化显式记录迁移，旧正式文件无需迁移且不得触碰。无占位步骤；命令与退出条件可执行。正式视觉效果使用独立产物评估，未运行项不伪报。
