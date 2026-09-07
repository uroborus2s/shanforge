const fs = require("fs");
const path = require("path");
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");

const root = __dirname;
const shots = path.join(root, "screens");
async function assertVisible(page, width, text) {
  if (!(await page.locator("body").innerText()).includes(text))
    throw Error(`missing ${text}`);
  if (
    await page.evaluate(
      () => document.documentElement.scrollWidth > window.innerWidth,
    )
  )
    throw Error(`horizontal overflow at ${width}`);
}

(async () => {
  let browser;
  const checks = [];
  try {
    fs.mkdirSync(shots, { recursive: true });
    browser = await chromium.launch({ headless: true });
    for (const width of [320, 390, 430]) {
      const page = await browser.newPage({ viewport: { width, height: 844 } });
      const errors = [];
      page.on("pageerror", (error) => errors.push(error.message));
      page.on("console", (message) => {
        if (message.type() === "error") errors.push(message.text());
      });
      await page.goto(`file://${path.join(root, "index.html")}`);
      await assertVisible(page, width, "08:45 快照");
      if (
        !(await page.locator(".today-strip span").innerText()).includes(
          "10:00 · 少儿基础班",
        )
      )
        throw Error("wrong next session");
      if (
        !(await page.getByRole("button", { name: "签到不可用" }).isDisabled())
      )
        throw Error("sign-in candidate must stay disabled");
      await page.screenshot({
        path: path.join(shots, `workbench-${width}.png`),
        fullPage: true,
      });
      checks.push(`workbench-${width}`);

      await page.locator('[data-go="schedule"]').last().click();
      for (const text of [
        "少儿基础班",
        "成人进阶课",
        "田中健 · 私教课",
        "3 节 · 4.5 小时",
      ])
        await assertVisible(page, width, text);
      if (await page.locator('[data-go="student"]').count())
        throw Error("schedule must not mis-map sessions to a student");
      await page.screenshot({
        path: path.join(shots, `schedule-${width}.png`),
        fullPage: true,
      });
      checks.push(`schedule-${width}`);

      await page.getByRole("button", { name: "返回" }).click();
      await page.locator('[data-go="student"]').first().click();
      for (const text of [
        "长期训练观察",
        "教练可见",
        "最近复盘 · 2026 年 8 月 30 日 · 对客户可见",
      ])
        await assertVisible(page, width, text);
      await page.getByRole("button", { name: "展开训练建议" }).click();
      if (!(await page.locator(".detail.open").isVisible()))
        throw Error("detail did not expand");
      await assertVisible(page, width, "长期观察的下次重点：反手落点控制。");
      await page.getByRole("button", { name: "收起训练建议" }).click();
      if (await page.locator(".detail.open").isVisible())
        throw Error("detail did not collapse");
      await page.screenshot({
        path: path.join(shots, `student-${width}.png`),
        fullPage: true,
      });
      checks.push(`student-${width}`);
      await page.getByRole("button", { name: "返回" }).click();
      if ((await page.locator("h1").textContent()) !== "工作台")
        throw Error("student return failed");
      if (errors.length) throw Error(errors.join("; "));
      await page.close();
    }
    fs.writeFileSync(
      path.join(root, "verification.json"),
      JSON.stringify(
        {
          status: "passed",
          command: "PLAYWRIGHT_MODULE=… node verify.cjs",
          checks,
          assertions: [
            "fixture values",
            "no pageerror or console error",
            "no horizontal overflow including expanded detail",
            "navigation and return",
            "no erroneous schedule-to-student mapping",
            "disabled sign-in candidate",
            "observation/review provenance",
          ],
          limitations: [
            "Static file URL; no API, login, permission, payment, or WeChat device validation.",
          ],
        },
        null,
        2,
      ),
    );
    console.log(`passed ${checks.length} screenshots`);
  } finally {
    if (browser) await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
