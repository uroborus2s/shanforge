const state = { page: "workbench", stack: [], expanded: false };
const sessions = [
  [
    "10:00",
    "11:30 结束",
    "少儿基础班",
    "ITA 城西球馆 · 1 号场",
    "已确认",
    false,
  ],
  [
    "14:00",
    "16:00 结束",
    "成人进阶课",
    "ITA 城西球馆 · 3 号室内硬地",
    "进行中",
    true,
  ],
  [
    "16:30",
    "17:30 结束",
    "田中健 · 私教课",
    "ITA 城西球馆 · 2 号场",
    "已确认",
    false,
  ],
];
function pageTop(title) {
  return `<header class="top"><button class="back" data-back aria-label="返回">‹</button><h1>${title}</h1></header>`;
}
function go(page) {
  if (state.page !== page) state.stack.push(state.page);
  state.page = page;
  render();
}
function workbench() {
  return `<header class="top"><span></span><h1>工作台</h1></header><p class="eyebrow">样例日期 · 2026 年 9 月 5 日 · 08:45 快照 · ITA 城西球馆</p><section class="next-session"><div class="session-time"><b>14:00</b><span>截止 14:10</span></div><div><span class="pill risk">待签到</span><h2>王小雨 · 私教课</h2><p>3 号室内硬地 · 反手落点训练</p></div><button class="text-action" disabled title="静态候选不执行签到">签到不可用</button></section><section class="today-strip"><b>今日 3 节课</b><span>下一节 10:00 · 少儿基础班</span><button data-go="schedule">查看日程 ›</button></section><div class="section"><h2>需要跟进</h2><span class="label">按时限</span></div><section class="follow-list"><button class="follow" data-go="student"><b class="follow-time">12:00</b><span><strong>王小雨课后复盘已逾期</strong><small>有 1 节课待复盘</small></span><i>›</i></button><button class="follow" data-go="schedule"><b class="follow-time">14:00</b><span><strong>成人进阶课已转室内</strong><small>无需教练另行处理</small></span><i>›</i></button></section><div class="compact-stats"><span><b>1</b>待签到</span><span><b>1</b>待复盘</span><span><b>2</b>可安排学员</span></div>`;
}
function schedule() {
  const list = sessions
    .map(
      (x) =>
        `<article class="agenda ${x[5] ? "live" : ""}"><time><b>${x[0]}</b><span>${x[1]}</span></time><div><header><h2>${x[2]}</h2><span class="pill ${x[5] ? "live" : ""}">${x[4]}</span></header><p>${x[3]}</p></div></article>`,
    )
    .join("");
  return `${pageTop("日程")}<p class="eyebrow">样例日期 · 2026 年 9 月 5 日</p><div class="date-band"><span>今日课程</span><span>3 节 · 4.5 小时</span></div><section class="agenda-list">${list}</section><p class="agenda-note">本候选不含学员下钻；保留场次、场地与状态的连续阅读。</p>`;
}
function student() {
  return `${pageTop("学员详情")}<p class="eyebrow">训练档案 · 王小雨</p><section class="training-lead"><div><span class="pill">NTRP 3.0</span><h2>正手回合稳定</h2><p>当前观察：反手击球点偏后</p></div><div class="next-focus"><span>下一次重点</span><b>反手落点控制</b><small>训练前完成 3 组影子挥拍</small></div></section><section class="lesson-line"><span class="pill live">已安排</span><div><b>9 月 5 日 · 反手落点训练</b><small>14:00–16:00 · 3 号室内硬地</small></div></section><section class="observation"><header><h2>长期训练观察</h2><span class="label">教练可见</span></header><p><b>正手上旋</b> 是当前稳定项；连续训练仍需提前反手击球点。</p><button class="expand" data-expand aria-expanded="${state.expanded}">${state.expanded ? "收起训练建议" : "展开训练建议"}</button><div class="detail ${state.expanded ? "open" : ""}"><p>长期观察的下次重点：反手落点控制。</p><p>家庭练习：每次训练前完成 3 组影子挥拍。</p></div></section><section class="review-line"><span>最近复盘 · 2026 年 8 月 30 日 · 对客户可见</span><p>正手上旋稳定，跑动中击球点仍需提前。</p><div class="chips"><span class="chip">反手落点</span><span class="chip">启动步</span></div></section><details class="entitlements"><summary>权益摘要 · 成人私教 8 次卡</summary><div><b>4</b> 可安排　<b>1</b> 已锁定　<b>3</b> 已完成</div><button disabled>安排、改约、取消、完成（候选禁用）</button></details><section class="notice">本候选只呈现样例数据；不保存观察或改动权益。</section>`;
}
function render() {
  const view = { workbench, schedule, student }[state.page]();
  document.querySelector("#app").innerHTML = view;
  document
    .querySelectorAll("[data-go]")
    .forEach((n) => (n.onclick = () => go(n.dataset.go)));
  const back = document.querySelector("[data-back]");
  if (back)
    back.onclick = () => {
      state.page = state.stack.pop() || "workbench";
      render();
    };
  const expand = document.querySelector("[data-expand]");
  if (expand)
    expand.onclick = () => {
      state.expanded = !state.expanded;
      render();
    };
}
render();
