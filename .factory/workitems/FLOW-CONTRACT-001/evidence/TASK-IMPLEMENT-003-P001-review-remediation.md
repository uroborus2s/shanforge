# TASK-IMPLEMENT-003-P001 独立审查整改证据

- 审查轮次：implementation review iteration 1
- 当前状态：第四轮独立终审 `approved / 98 / C0-I0-M0`
- 范围：项目知识 SQLite 索引、只读静态站点、CLI 与缓存安全

## 已落实整改

1. PM 高频字段由仅存 `field_values_json` 改为同时投影到 13 类业务表的 typed columns。
2. 需求、任务、代码和测试使用专用详情结构，显式展示目标、范围、验收、进度、关联和定向来源。
3. alias、module、document revision、memory checkpoint、render view 和 cache entry 已接入生产写入路径。
4. CLI 删除未实现的 `--open`、`--serve` 参数；第一版只生成静态文件。
5. 来源、SQLite、HTML 和 CLI receipt 统一使用确定性敏感值脱敏策略。
6. 来源发现缓存仅在完整索引成功发布后提交；失败构建不能污染下一次增量判断。
7. HTML 缓存命中校验 profile、current 指针、路径边界、属主、精确权限、路由集合和文件元数据，并对 manifest 内每个页面无条件重算 SHA-256；新增“篡改后保持相同 size/mtime”负例。APFS 使用 copy-on-write 克隆复用页面，不修改旧构建元数据。
8. 代码地图按代码文件生成详情页，文件内保留每个 AST 符号的稳定锚点、类型、签名和状态；当前站点从 4,300 余页收敛到约 760 页，不丢失符号级定向查看能力。
9. SQLite 仅留 current + previous 两代；单个既有、无跨来源所有权冲突的 Python 来源变化使用事务增量补丁，其他变化保持完整事务替换。

## 第三轮反馈核实与根因

- Feedback：`PKI-R3-I-001`，同一独立 reviewer，severity `Important`。
- 技术要求：装饰过的函数、异步函数和类在代码详情“签名”列必须显示 `def`、`async def` 或 `class` 定义头，不能显示第一条装饰器。
- 核实结论：成立；与既有只读代码地图决策一致，不涉及新增功能或兼容兜底。
- 稳定复现：`PythonExtractor` 输入 decorated function / async function / class，实际依次输出 `@factory(...)`、`@logged`、`@sealed`。
- 直接原因：`_SymbolVisitor._visit_symbol()` 使用 `ast.unparse(node).split("\\n", 1)[0]`；`ast.unparse()` 正确保留装饰器，因此第一行天然是 decorator。
- 根源原因：原 extractor 测试只断言稳定 ID 和 signature digest，没有冻结 decorated symbol 的人类可读 `signature_text` 合同；HTML 测试使用手写未装饰 DTO，未覆盖 extractor → DTO → 页面链。
- 单一修复点：从不含 `decorator_list`、body 仅含占位节点的浅 AST 副本生成定义头，保持原 AST、稳定 ID 和 digest 不变。
- 防回归：先增加 decorated function / async function / class extractor 失败夹具，再增加代码详情页签名断言和桌面/窄屏 Chromium + axe 样本。
- 授权依据：用户已明确确认本实现修复方案和按独立评审清零 Important 后提交的 Gate；本项在原范围内，第三轮 reviewer 也判定 `human_confirmation_required=false`，不扩展用户授权边界。

## 第三轮整改和浏览器补证

- RED：新增 decorated function / async function / class 夹具后，三个 `signature_text` 均错误地以 `@` 开头；代码详情链路回归也先冻结“页面必须显示定义头、不得显示 decorator”合同。
- GREEN：`_signature_text()` 对 AST 节点做浅复制，移除 `decorator_list` 并以 `Pass` 替换 body 后再 `ast.unparse()`；原 AST、稳定 ID 与 signature digest 不变。Python extractor 版本升级为 `python-ast-v2`，真实仓重新解析既有 Python 来源，避免 SQLite 保留旧签名。
- 当前生成站点的 `extractors.py` 代码详情页显示 `class Extractor(Protocol):`、`def extract(...)` 等定义头；代码详情页签名列没有以 `@` 开头的记录。
- 同一 reviewer 的 Minor 浏览器覆盖已补齐：代码详情页在 1440×900 与 390×844 均检查返回按钮、稳定符号锚点、只读约束、本地链接和表格可用性。
- 真实浏览器补证先发现 390px 下长稳定 ID 撑宽 body；根因是 `.nested-definition` 与 breadcrumb 未继承长文本换行。修复后四视口均无页面级横向溢出。
- axe 随后发现横向滚动区不能键盘聚焦；表格容器现使用 `role="region" tabindex="0"` 和中文 `aria-label`。渲染器升级为 `ProjectSiteRenderer/v5` 并进入页面输入指纹，确保模板升级不会错误复用旧 HTML。

## 性能证据

测量环境：macOS/APFS、本地 Python 3.12 虚拟环境、当前工作树约 462 个登记来源、约 760 个静态页面。P95 使用最近秩。

| 场景 | 结果 | 合同判断 |
|---|---:|---|
| 同一进程无变化 snapshot，20 次 | P95 `32.884 ms`；包含全部页面摘要校验 | 通过 `≤100 ms` |
| 10,000 JSON artifact 单来源提取，5 次 | P95 `402.268 ms`，产出 30,000 entities | 通过 extractor `≤500 ms`；不冒充完整 SQLite 发布 |
| 当前仓冷 rebuild + HTML | `3.00 s`，462/462 来源解析 | 位于冷建目标边界 |
| 单个既有 Python 来源变化 + 完整 CLI，连续 5 次 | `0.69, 0.69, 0.69, 0.69, 0.70 s`；P95 `0.70 s`；每次 1 个来源解析、6 页重建、759 页复用 | 通过同步单变化 `≤800 ms` |

性能修复没有缩小计时范围：五个样本都包含来源发现、SQLite generation、PM 投影、HTML DTO/渲染、所有页面 SHA-256 校验、COW 候选和原子发布。代码符号改为文件页内稳定锚点后，页面壳不再重复；来源级事务补丁只在严格前置条件成立时启用，前置条件不满足会回退完整投影。

## 当前验证

- 项目知识定向测试：`87 passed`。
- 性能测试：`3 passed`，包含 20 次 warm P95 与 10,000 artifact extractor P95。
- `mypy src`：`Success: no issues found in 279 source files`。
- Chromium 四视口、代码详情桌面/手机、键盘、打印和链接：`1 passed`，共 8 张截图；axe-core 7 页 `violation_count=0`。首页与手机代码页渐变/状态色对比度仍为工具 `incomplete`，不冒充完整 WCAG 认证。
- 同一独立 reviewer 第四轮终审：`approved / 98 / C0-I0-M0`；全部历史 Finding 关闭，`human_confirmation_required=false`。
- 完整 pytest、文档结构与 Git hygiene：待最终候选执行。
