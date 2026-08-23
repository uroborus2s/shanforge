---
name: webapp-testing
description: 使用 Playwright 或项目已有测试栈验证本地 Web 应用。适用于可重复的本地页面检查、交互断言、截图、控制台日志和回归验证；一次性操作真实浏览器、登录态 Chrome、外部网站或用户明确要求 browser-use 时交给 `browser-control`。
---

# Web 应用测试

## 与 browser-control 的边界

- 用 `webapp-testing`：本地应用、localhost、可重复脚本、断言、截图证据、控制台日志、回归验证。
- 用 `browser-control`：用户要“用本地浏览器/Chrome/browser-use 打开”、依赖现有登录态或扩展、检查当前浏览器标签、外部网站、一次性人工式点击读取。
- 不确定时先看任务是否需要可重复验证。需要可重复验证就用本 skill。

## 任务分支

| 分支 | 动作 |
|---|---|
| 项目已有测试栈 | 优先用仓内现有 Playwright/Vitest/Cypress/npm 脚本；不要强行新写 Python 脚本。 |
| 静态 HTML | 读取 HTML 识别选择器，必要时用 `file://` 跑最小 Playwright 检查。 |
| 动态本地应用，服务器未运行 | 先执行 `python <skill-dir>/scripts/with_server.py --help`，再用它包住 dev server 和测试脚本。 |
| 动态本地应用，服务器已运行 | 导航、等待稳定、截图/DOM 勘查，再写最小断言。 |
| 调试失败页面 | 捕获 screenshot、HTML、console logs、network error 摘要；先定位失败点再改代码。 |

辅助脚本作为黑盒使用，先看帮助，不先读源码：

以下 `<skill-dir>` 表示当前 `SKILL.md` 所在目录；执行前替换为该目录的实际绝对路径，不假设目标项目包含本 Skill 的 `scripts/`。

```bash
python <skill-dir>/scripts/with_server.py --help
python <skill-dir>/scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

## 最小 Playwright 模式

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:5173")
    page.wait_for_load_state("networkidle")
    page.screenshot(path="/tmp/webapp-test.png", full_page=True)
    browser.close()
```

## 安全写入

- 测试脚本、截图和日志写到 `/tmp`、任务 evidence 目录或用户指定路径。
- 不修改应用数据、远端环境或真实账号，除非用户明确要求并说明测试数据。
- 表单提交、删除、支付、发信等有副作用的流程必须使用测试环境或先停在确认前。
- 不把临时测试脚本当正式测试提交，除非用户要求保留。

## 验证

- 对关键交互写断言，不只截图。
- 动态应用在读取 DOM 前等待稳定状态；必要时等待具体 selector。
- 失败时保留截图、URL、控制台错误和断言信息。
- 移动端或响应式问题要至少检查目标 viewport。

## 可复现测试环境

- 正式 UI 用例使用稳定 `TEST-UI-*` ID，并在 evidence 中建立 `需求 -> 任务 -> 测试 -> 证据` 关系。
- 动态页面在执行前记录启动命令、端口、健康检查和关闭方式；测试结束必须执行关闭与临时数据清理。
- 静态 HTML 无需伪造服务：启动命令、端口和关闭方式可写 `N/A`，但必须说明静态文件路径，并以文件存在、可解析和目标 DOM 断言作为健康检查。
- 使用动态分配端口时，记录实际端口和占用进程；禁止默认复用一个可能已被占用的端口。
- 任何字段确实不适用时写 `N/A` 和原因，不得写“待补充”；缺少必填环境信息时停止并输出 `needs: test_environment_contract`。

## 输出清单

交付时列出：

- 被测 URL、启动命令和端口。
- 健康检查和关闭方式；不适用项的 `N/A` 原因。
- `TEST-UI-*` ID 及其需求、任务和 evidence 关联。
- 使用的测试命令或临时脚本路径。
- 截图、日志或 HTML evidence 路径。
- 断言结果、失败数量和未覆盖风险。

## 失败处理

- dev server 启动失败、端口冲突、依赖缺失：`status: blocked`，列出命令和 stderr。
- 需要登录态、扩展或真实浏览器状态：`status: needs_user_input` 或转交 `browser-control` 边界说明。
- 断言失败：`status: blocked`，保留证据并说明复现步骤。
- 只能完成截图无断言：报告 partial，不宣称回归通过。

## Shanforge 状态包

```text
工作结果：
- work_item: <WORKITEM-ID>
- skill: webapp-testing
- status: ready_for_review | partial | blocked | needs_user_input
- outputs:
  - <script/screenshot/log path>
- evidence:
  - <command/url/assertion summary>
- ledger_event: <event id or none>
- needs:
  - review | verification | test_environment_contract | user_input | none
```

项目化执行时，沿用 [工作 Skill 回写契约](../using-shanforge/references/work-skill-return-contract.md)；本 skill 的现有专业输出和失败语义不变。
