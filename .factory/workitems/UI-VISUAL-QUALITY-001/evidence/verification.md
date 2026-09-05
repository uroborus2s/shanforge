# 集中验证证据

## 评审整改后最新结果

独立复审 approved / 96 / C0-I0-M0 后同步关闭事实，再运行 `uv run pytest -q`：exit 0，403 passed / 11 subtests passed，10.83s；目标 Ruff、diff check、JSON/JSONL 解析和本工作项事件唯一性均通过。最初唯一性临时检查错误地要求旧 review-ledger 所有历史行都符合当前 ID 格式，失败后改为全文件只验证 JSON、本工作项验证 ID 唯一性；未改范围外历史行。

原 worker 完成 I1/I2/I3 后，父级新鲜 `uv run pytest -q`：exit 0，403 passed / 11 subtests passed，11.04s。同轮目标 Ruff、五文件代码形状、skill validator 与 diff check 均 exit 0。T01 最终 41 passed、T02 15 passed。

I1 原生字段负向、I2 landing 真实错误均有 RED→GREEN；I3 初始新增结构断言为 1 failed / 14 passed，补齐结构化实验输入后 15 passed。额外发现原 UTF-8 保护删除回归：`PYTHONIOENCODING=ascii` 中文 CLI 抛 UnicodeEncodeError；仅 CLI main 恢复标准流 UTF-8，加入 ASCII/cp1252 成功 JSON 和失败 stderr 三项回归。库导入不改变宿主流。

12 brief 明确为合成实验输入，非用户正式稿；固定记录及数量/状态、优惠金额、计时步骤，非 new 有具体 token、区域布局、组件状态与允许/保护边界。仍未运行真实视觉 A/B。以下为首轮历史快照，不覆盖本节最新结果。

## 首轮集中验证快照

日期：2026-09-05。代码基线 HEAD 为 `e39241a`；两个 worker 确认最终写入稳定后，由父控制器重跑。

| 命令 | exit | 结果 |
|---|---|---|
| `uv run pytest -q` | 0 | 395 passed，11 subtests passed，9.96s |
| `uv run ruff check tests/test_ui_design_candidates.py tests/test_ui_ux_pro_max_skill.py` | 0 | All checks passed |
| `uv run python skills/tdd-workflow/scripts/check_code_shape.py skills/ui-ux-pro-max/scripts/core.py skills/ui-ux-pro-max/scripts/design_system.py skills/ui-ux-pro-max/scripts/search.py tests/test_ui_design_candidates.py tests/test_ui_ux_pro_max_skill.py` | 0 | 无嵌套命名函数或 lambda；8 个单调用 helper 候选须人工判断 |
| `uv run python /Users/uroborus/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/ui-ux-pro-max` | 0 | Skill is valid |
| `git diff --check` | 0 | 无输出 |
| `ls -ld /Users/uroborus/.codex/skills/ui-ux-pro-max` | 0 | 当前宿主是指向仓内 skill 的 symlink，无需复制同步 |
| `uv run python /Users/uroborus/.codex/skills/ui-ux-pro-max/scripts/search.py '中文无匹配核查' --design-system --platform mini-program --surface operate --locale zh-CN --json` | 0 | 宿主回读 kind=design_candidates/status=candidate；四域空列表，各有 no BM25 matches 未决项及 CJK 证据要求；不生成默认设计 |

worker 定向：T01 初始 RED 5 failed，最终 33 passed；T02 最终 15 passed。父级中间并发检查曾读到 RED/实现交错，见作者自检，不计最终结论。两次 uv 静态调用最初因现有缓存访问权限未能运行，获准读取缓存后按同命令成功。

helper 人工理由：CSV 读取、域推断、平台解析各承担独立输入职责；Markdown/普通查询格式化、候选持久化、CLI 参数解析是清晰边界；测试动态加载器负责隔离 sys.path/modules。不为抽象而新增运行时框架。

覆盖：真实 subprocess CLI、JSON/Markdown/ASCII、词法来源/得分/命中词、中文/无命中、全栈映射及冲突、dials 不决定风格、无 persist 零写入、重复候选、固定 UUID 碰撞、I/O 错误与 symlink 路径保护、API 参数；资料和 12 brief 结构契约。

未运行：12 组真实产品 UI 的旧/新 A/B 生成、浏览器/模拟器/真机页面与交互、美术盲评、用户视觉认可。当前任务没有产品服务，不启动端口、不写业务数据、不进行生产验收或远端发布。原始参考截图观察只证明看过来源，不能替代产品验证。
