const C = {
  bg: "#F5F6FA",
  surface: "#FFFFFF",
  primary: "#5B4CF0",
  primarySoft: "#ECEAFF",
  secondary: "#1BAA83",
  secondarySoft: "#E5F7F1",
  warning: "#F5A524",
  warningSoft: "#FFF4DE",
  danger: "#E5485D",
  dangerSoft: "#FDECEF",
  info: "#3676E8",
  infoSoft: "#EAF2FF",
  text: "#172033",
  muted: "#667085",
  border: "#E3E7EF",
  dark: "#111827",
};

function open(page) {
  penpot.openPage(page);
}

function ensurePage(name, renameCurrent = false) {
  let page = penpotUtils.getPageByName(name);
  if (page) return page;
  if (renameCurrent && penpot.currentPage && penpot.currentPage.name === "Page 1") {
    penpot.currentPage.name = name;
    return penpot.currentPage;
  }
  page = penpot.createPage();
  page.name = name;
  return page;
}

function addBoard(page, name, x, y, w, h, fill = C.surface, radius = 24) {
  const existing = page.findShapes({ name, type: "board" })[0];
  if (existing) return { board: existing, created: false };
  open(page);
  const board = penpot.createBoard();
  board.name = name;
  board.x = x;
  board.y = y;
  board.resize(w, h);
  board.fills = [{ fillColor: fill, fillOpacity: 1 }];
  board.borderRadius = radius;
  board.clipContent = true;
  page.root.appendChild(board);
  return { board, created: true };
}

function rect(parent, name, x, y, w, h, fill, radius = 12, stroke = null) {
  const shape = penpot.createRectangle();
  shape.name = name;
  shape.resize(w, h);
  shape.fills = fill ? [{ fillColor: fill, fillOpacity: 1 }] : [];
  shape.borderRadius = radius;
  if (stroke) shape.strokes = [{ strokeColor: stroke, strokeOpacity: 1, strokeWidth: 1 }];
  parent.appendChild(shape);
  penpotUtils.setParentXY(shape, x, y);
  return shape;
}

function ellipse(parent, name, x, y, w, h, fill, opacity = 1) {
  const shape = penpot.createEllipse();
  shape.name = name;
  shape.resize(w, h);
  shape.fills = [{ fillColor: fill, fillOpacity: 1 }];
  shape.opacity = opacity;
  parent.appendChild(shape);
  penpotUtils.setParentXY(shape, x, y);
  return shape;
}

function text(parent, name, value, x, y, size = 16, color = C.text, weight = "400", width = null) {
  const shape = penpot.createText(value);
  if (!shape) throw new Error(`Cannot create text: ${name}`);
  shape.name = name;
  shape.fontSize = String(size);
  shape.fontWeight = { "500": "600", "650": "600", "750": "700" }[String(weight)] || String(weight);
  shape.fills = [{ fillColor: color, fillOpacity: 1 }];
  parent.appendChild(shape);
  penpotUtils.setParentXY(shape, x, y);
  if (width) {
    shape.resize(width, Math.max(size * 1.6, 24));
    shape.growType = "auto-height";
  } else {
    shape.growType = "auto-width";
  }
  return shape;
}

function chip(parent, label, x, y, color = C.primary, bg = C.primarySoft, width = null) {
  const w = width || Math.max(76, label.length * 15 + 28);
  rect(parent, `Chip/${label}`, x, y, w, 34, bg, 17);
  text(parent, `ChipLabel/${label}`, label, x + 14, y + 8, 13, color, "600");
}

function button(parent, label, x, y, w, kind = "primary") {
  const styles = {
    primary: [C.primary, C.surface],
    secondary: [C.primarySoft, C.primary],
    danger: [C.danger, C.surface],
    neutral: [C.surface, C.text],
  };
  const [bg, fg] = styles[kind];
  const base = rect(parent, `Button/${kind}/${label}`, x, y, w, 48, bg, 14, kind === "neutral" ? C.border : null);
  text(parent, `ButtonLabel/${label}`, label, x + 20, y + 14, 15, fg, "600");
  return base;
}

function status(parent, label, x, y, tone = "info") {
  const tones = {
    info: [C.info, C.infoSoft],
    success: [C.secondary, C.secondarySoft],
    warning: [C.warning, C.warningSoft],
    danger: [C.danger, C.dangerSoft],
  };
  const [fg, bg] = tones[tone];
  chip(parent, label, x, y, fg, bg);
}

function phoneChrome(board, platform, title, width, height) {
  rect(board, "System/Background", 0, 0, width, height, C.bg, 0);
  if (platform === "mini") {
    text(board, "System/Time", "9:41", 18, 16, 12, C.text, "600");
    rect(board, "System/Capsule", width - 98, 12, 78, 30, C.surface, 16, C.border);
    text(board, "System/CapsuleText", "••  ◉", width - 79, 19, 12, C.text, "600");
    text(board, "Navigation/Title", title, 20, 60, 22, C.text, "700");
  } else if (platform === "ios") {
    text(board, "System/Time", "9:41", 24, 16, 12, C.text, "600");
    text(board, "System/Status", "●  5G  ▰", width - 100, 16, 11, C.text, "500");
    text(board, "Navigation/Title", title, 22, 56, 28, C.text, "700");
  } else {
    text(board, "System/Time", "9:41", 20, 14, 12, C.text, "600");
    text(board, "System/Status", "▴ 5G  ▰", width - 92, 14, 11, C.text, "500");
    text(board, "Navigation/Title", title, 20, 54, 24, C.text, "700");
  }
  rect(board, "Navigation/TabBar", 0, height - 76, width, 76, C.surface, 0, C.border);
  const tabs = platform === "mini" ? ["首页", "订单", "消息", "我的"] : ["首页", "发现", "订单", "消息", "我的"];
  const cell = width / tabs.length;
  tabs.forEach((label, i) => {
    const active = i === 0;
    ellipse(board, `TabIcon/${label}`, i * cell + cell / 2 - 8, height - 60, 16, 16, active ? C.primary : C.border);
    text(board, `TabLabel/${label}`, label, i * cell + cell / 2 - 14, height - 35, 11, active ? C.primary : C.muted, active ? "600" : "400");
  });
  if (platform === "ios") rect(board, "System/HomeIndicator", width / 2 - 54, height - 8, 108, 4, C.dark, 2);
}

function addHome(board, platform, width, height) {
  const top = platform === "mini" ? 102 : 106;
  rect(board, "Hero/Background", 16, top, width - 32, 154, C.primary, 24);
  ellipse(board, "Hero/GlowA", width - 120, top - 16, 150, 150, "#8D82FF", 0.55);
  ellipse(board, "Hero/GlowB", width - 35, top + 70, 90, 90, "#A89FFF", 0.45);
  text(board, "Hero/Kicker", "悦享服务 · 省心预约", 34, top + 25, 14, "#EAE7FF", "600");
  text(board, "Hero/Title", "今天，也要好好照顾自己", 34, top + 55, 24, C.surface, "700", width - 100);
  text(board, "Hero/Subtitle", "专业服务 · 明码标价 · 售后保障", 34, top + 100, 13, "#EAE7FF", "400");
  rect(board, "Search/Field", 16, top + 174, width - 32, 48, C.surface, 14, C.border);
  text(board, "Search/Icon", "⌕", 32, top + 188, 20, C.muted, "500");
  text(board, "Search/Placeholder", "搜索按摩、保洁、家电清洗", 62, top + 190, 14, C.muted, "400");
  text(board, "Section/Categories", "热门服务", 20, top + 244, 18, C.text, "700");
  ["按摩理疗", "家庭保洁", "家电清洗", "宠物护理"].forEach((label, i) => {
    const x = 16 + i * ((width - 32) / 4);
    ellipse(board, `CategoryIcon/${label}`, x + 14, top + 282, 46, 46, i % 2 ? C.secondarySoft : C.primarySoft);
    text(board, `CategoryLabel/${label}`, label, x + 7, top + 338, 12, C.text, "500");
  });
  text(board, "Section/Recommended", "为你推荐", 20, top + 382, 18, C.text, "700");
  for (let i = 0; i < 2; i += 1) {
    const y = top + 420 + i * 116;
    rect(board, `ServiceCard/${i + 1}`, 16, y, width - 32, 100, C.surface, 18, C.border);
    rect(board, `ServiceImage/${i + 1}`, 28, y + 12, 78, 76, i ? C.secondarySoft : C.primarySoft, 14);
    text(board, `ServiceTitle/${i + 1}`, i ? "全屋深度保洁 · 4小时" : "肩颈舒缓理疗 · 60分钟", 122, y + 16, 15, C.text, "650", width - 150);
    text(board, `ServiceMeta/${i + 1}`, i ? "4.9分 · 已服务 1,280 次" : "4.8分 · 已服务 2,316 次", 122, y + 46, 12, C.muted, "400");
    text(board, `ServicePrice/${i + 1}`, i ? "¥299 起" : "¥168 起", 122, y + 69, 16, C.danger, "700");
  }
}

function addDetail(board, platform, width, height) {
  const top = platform === "mini" ? 104 : 100;
  rect(board, "Service/Hero", 0, top, width, 220, C.primarySoft, 0);
  ellipse(board, "Service/HeroMark", width / 2 - 68, top + 40, 136, 136, "#D7D2FF", 1);
  text(board, "Navigation/Back", "‹", 20, top + 14, 32, C.text, "500");
  text(board, "Service/Title", "肩颈舒缓理疗", 20, top + 244, 24, C.text, "700");
  text(board, "Service/Subtitle", "专业理疗师上门服务 · 60分钟", 20, top + 280, 14, C.muted, "400");
  status(board, "平台保障", 20, top + 316, "success");
  status(board, "可取消", 124, top + 316, "info");
  text(board, "Service/Price", "¥168 起", width - 112, top + 248, 20, C.danger, "700");
  rect(board, "Provider/Card", 16, top + 370, width - 32, 112, C.surface, 18, C.border);
  ellipse(board, "Provider/Avatar", 30, top + 388, 58, 58, C.secondarySoft);
  text(board, "Provider/Name", "林晓 · 高级理疗师", 102, top + 388, 16, C.text, "650");
  text(board, "Provider/Meta", "4.9分 · 3年经验 · 已服务 856 次", 102, top + 418, 12, C.muted, "400");
  text(board, "Provider/Availability", "今天 14:30 后可约", 102, top + 444, 13, C.secondary, "600");
  text(board, "Service/DescriptionTitle", "服务说明", 20, top + 510, 18, C.text, "700");
  text(board, "Service/Description", "包含评估、热敷、肩颈放松和居家建议。\n如有特殊病史，请在下单前告知服务人员。", 20, top + 548, 14, C.muted, "400", width - 40);
  button(board, "选择时间", 20, height - 142, width - 40, "primary");
}

function addBooking(board, platform, width, height) {
  const top = platform === "mini" ? 108 : 106;
  text(board, "Booking/Step", "1  服务人员   2  日期时间   3  确认", 20, top, 13, C.primary, "600", width - 40);
  text(board, "Booking/SectionProvider", "选择服务人员", 20, top + 42, 18, C.text, "700");
  ["林晓 4.9", "周宁 4.8", "系统推荐"].forEach((label, i) => {
    const x = 20 + i * 118;
    rect(board, `ProviderOption/${label}`, x, top + 78, 104, 76, i === 0 ? C.primarySoft : C.surface, 16, i === 0 ? C.primary : C.border);
    ellipse(board, `ProviderOptionAvatar/${label}`, x + 36, top + 88, 32, 32, i === 0 ? "#D7D2FF" : C.bg);
    text(board, `ProviderOptionText/${label}`, label, x + 15, top + 128, 12, i === 0 ? C.primary : C.text, "600");
  });
  text(board, "Booking/SectionDate", "选择日期", 20, top + 184, 18, C.text, "700");
  ["今天\n24", "明天\n25", "周日\n26", "周一\n27", "周二\n28"].forEach((label, i) => {
    const x = 20 + i * 70;
    rect(board, `Date/${label}`, x, top + 222, 58, 68, i === 1 ? C.primary : C.surface, 16, i === 1 ? null : C.border);
    text(board, `DateText/${label}`, label, x + 14, top + 236, 13, i === 1 ? C.surface : C.text, "600");
  });
  text(board, "Booking/SectionTime", "可预约时间", 20, top + 326, 18, C.text, "700");
  ["10:00", "11:30", "14:30", "16:00", "18:30", "20:00"].forEach((label, i) => {
    const x = 20 + (i % 3) * 118;
    const y = top + 366 + Math.floor(i / 3) * 58;
    rect(board, `Time/${label}`, x, y, 104, 42, i === 2 ? C.primarySoft : C.surface, 12, i === 2 ? C.primary : C.border);
    text(board, `TimeText/${label}`, label, x + 29, y + 12, 13, i === 2 ? C.primary : C.text, "600");
  });
  rect(board, "Booking/Summary", 16, top + 500, width - 32, 106, C.surface, 18, C.border);
  text(board, "Booking/SummaryTitle", "预约摘要", 32, top + 518, 15, C.text, "650");
  text(board, "Booking/SummaryText", "肩颈舒缓理疗 · 林晓\n7月25日 14:30 · 上门服务", 32, top + 548, 13, C.muted, "400", width - 64);
  button(board, platform === "mini" ? "微信支付 ¥168" : "确认并支付 ¥168", 20, height - 142, width - 40, "primary");
}

function addPayment(board, platform, width, height) {
  const top = platform === "mini" ? 160 : 148;
  ellipse(board, "Result/IconBg", width / 2 - 48, top, 96, 96, C.secondarySoft);
  text(board, "Result/Icon", "✓", width / 2 - 18, top + 22, 44, C.secondary, "700");
  text(board, "Result/Title", "预约成功", width / 2 - 54, top + 126, 24, C.text, "700");
  text(board, "Result/Subtitle", "服务人员将在出发前与您联系", width / 2 - 102, top + 168, 14, C.muted, "400");
  rect(board, "Result/Card", 20, top + 220, width - 40, 190, C.surface, 20, C.border);
  text(board, "Result/OrderNo", "订单号  YX202607240018", 38, top + 244, 13, C.muted, "400");
  text(board, "Result/Service", "肩颈舒缓理疗 · 60分钟", 38, top + 282, 17, C.text, "650");
  text(board, "Result/Time", "7月25日（周六）14:30", 38, top + 320, 14, C.text, "500");
  text(board, "Result/Address", "上海市徐汇区 · 已隐藏详细地址", 38, top + 354, 13, C.muted, "400");
  button(board, "查看订单", 20, top + 452, width - 40, "primary");
  button(board, "返回首页", 20, top + 516, width - 40, "neutral");
  text(board, "Result/Recovery", platform === "mini" ? "支付回跳失败时，可在「我的订单」恢复查看" : "网络中断不会重复扣款，可在订单页恢复", 28, top + 588, 12, C.muted, "400", width - 56);
}

function addOrder(board, platform, width, height) {
  const top = platform === "mini" ? 112 : 108;
  status(board, "待服务", 20, top, "warning");
  text(board, "Order/No", "YX202607240018", width - 142, top + 8, 12, C.muted, "400");
  rect(board, "Order/Timeline", 16, top + 56, width - 32, 154, C.surface, 18, C.border);
  ["已支付", "服务人员已接单", "等待上门"].forEach((label, i) => {
    ellipse(board, `TimelineDot/${label}`, 34, top + 80 + i * 44, 14, 14, i < 2 ? C.secondary : C.warningSoft);
    text(board, `TimelineText/${label}`, label, 62, top + 77 + i * 44, 14, C.text, i === 2 ? "650" : "500");
  });
  rect(board, "Order/ServiceCard", 16, top + 228, width - 32, 132, C.surface, 18, C.border);
  rect(board, "Order/Image", 30, top + 246, 82, 82, C.primarySoft, 14);
  text(board, "Order/ServiceTitle", "肩颈舒缓理疗 · 60分钟", 128, top + 246, 15, C.text, "650", width - 150);
  text(board, "Order/Provider", "服务人员：林晓", 128, top + 282, 13, C.muted, "400");
  text(board, "Order/Price", "实付 ¥168", 128, top + 312, 15, C.danger, "650");
  text(board, "Order/DetailsTitle", "预约信息", 20, top + 392, 18, C.text, "700");
  text(board, "Order/Details", "时间  7月25日 14:30\n地址  上海市徐汇区（隐私保护）\n联系  虚拟号码，有效期至服务完成", 20, top + 432, 14, C.muted, "400", width - 40);
  button(board, "联系服务人员", 20, top + 554, width - 40, "secondary");
  button(board, "取消或申请售后", 20, top + 618, width - 40, "neutral");
}

function addMobilePage(page, platform, specs) {
  const size = platform === "ios" ? [390, 844] : platform === "android" ? [412, 915] : [375, 812];
  const gap = size[0] + 80;
  const screens = [];
  specs.forEach((spec, i) => {
    const { board, created } = addBoard(page, spec.id, i * gap, 0, size[0], size[1], C.surface, platform === "android" ? 28 : 38);
    screens.push(board);
    if (!created) return;
    phoneChrome(board, platform, spec.title, size[0], size[1]);
    if (spec.kind === "home") addHome(board, platform, size[0], size[1]);
    if (spec.kind === "detail") addDetail(board, platform, size[0], size[1]);
    if (spec.kind === "booking") addBooking(board, platform, size[0], size[1]);
    if (spec.kind === "payment") addPayment(board, platform, size[0], size[1]);
    if (spec.kind === "order") addOrder(board, platform, size[0], size[1]);
    board.setPluginData("ui-id", spec.id);
    board.setPluginData("platform", platform);
    board.setPluginData("purpose", spec.purpose);
  });
  const existingFlow = page.flows.find((flow) => flow.name === `${platform}-P0-预约闭环`);
  if (!existingFlow && screens[0]) page.createFlow(`${platform}-P0-预约闭环`, screens[0]);
  for (let i = 0; i < screens.length - 1; i += 1) {
    const trigger = screens[i].children.find((s) => s.name === "ServiceCard / 1")
      || screens[i].children.find((s) => s.name.startsWith("Button / primary"));
    if (trigger && trigger.interactions.length === 0) {
      trigger.addInteraction("click", { type: "navigate-to", destination: screens[i + 1] });
    }
  }
}

function adminChrome(board, title) {
  rect(board, "Admin/Background", 0, 0, 1440, 1024, C.bg, 0);
  rect(board, "Admin/Sidebar", 0, 0, 252, 1024, C.dark, 0);
  text(board, "Admin/Brand", "悦享服务 · 运营中心", 28, 28, 18, C.surface, "700");
  ["总览", "订单", "服务与价格", "门店与人员", "用户", "营销", "权限", "审计日志"].forEach((label, i) => {
    const active = label === title || (title === "订单详情" && label === "订单");
    if (active) rect(board, `Admin/NavActive/${label}`, 16, 92 + i * 56, 220, 44, C.primary, 12);
    text(board, `Admin/Nav/${label}`, label, 40, 105 + i * 56, 14, active ? C.surface : "#AAB2C2", active ? "650" : "400");
  });
  rect(board, "Admin/Topbar", 252, 0, 1188, 72, C.surface, 0, C.border);
  text(board, "Admin/PageTitle", title, 292, 22, 24, C.text, "700");
  text(board, "Admin/Search", "⌕  搜索订单、用户或服务", 970, 25, 13, C.muted, "400");
  ellipse(board, "Admin/UserAvatar", 1376, 18, 36, 36, C.primarySoft);
}

function addAdminDashboard(board) {
  const cards = [
    ["今日成交额", "¥68,420", "+12.6%", "success"],
    ["待服务订单", "128", "需关注 8", "warning"],
    ["退款申请", "6", "超时 1", "danger"],
    ["活跃服务人员", "216", "在线 184", "info"],
  ];
  cards.forEach((item, i) => {
    const x = 292 + i * 270;
    rect(board, `Metric/${item[0]}`, x, 104, 244, 132, C.surface, 18, C.border);
    text(board, `MetricLabel/${item[0]}`, item[0], x + 20, 124, 13, C.muted, "500");
    text(board, `MetricValue/${item[0]}`, item[1], x + 20, 158, 28, C.text, "700");
    status(board, item[2], x + 20, 196, item[3]);
  });
  rect(board, "Chart/Card", 292, 268, 700, 310, C.surface, 18, C.border);
  text(board, "Chart/Title", "近 7 日成交趋势", 316, 292, 18, C.text, "700");
  [110, 150, 124, 198, 176, 230, 206].forEach((h, i) => {
    rect(board, `Chart/Bar/${i}`, 336 + i * 84, 530 - h, 38, h, i === 6 ? C.primary : C.primarySoft, 8);
    text(board, `Chart/Day/${i}`, `7/${18 + i}`, 332 + i * 84, 544, 11, C.muted, "400");
  });
  rect(board, "Alert/Card", 1020, 268, 380, 310, C.surface, 18, C.border);
  text(board, "Alert/Title", "需要处理", 1044, 292, 18, C.text, "700");
  [["退款超时", "1", "danger"], ["服务人员迟到", "3", "warning"], ["库存低于阈值", "2", "info"]].forEach((item, i) => {
    rect(board, `Alert/${item[0]}`, 1044, 336 + i * 72, 332, 56, C.bg, 12);
    text(board, `AlertLabel/${item[0]}`, item[0], 1060, 353 + i * 72, 14, C.text, "600");
    status(board, item[1], 1316, 347 + i * 72, item[2]);
  });
  addTable(board, "最近订单", 292, 610, 1108, ["订单号", "客户", "服务", "时间", "金额", "状态"], [
    ["YX0018", "王女士", "肩颈理疗", "14:30", "¥168", "待服务"],
    ["YX0017", "李先生", "深度保洁", "13:00", "¥299", "服务中"],
    ["YX0016", "周女士", "空调清洗", "11:30", "¥238", "已完成"],
  ]);
}

function addTable(board, titleValue, x, y, w, headers, rows) {
  const rowH = 54;
  rect(board, `Table/${titleValue}`, x, y, w, 82 + rows.length * rowH, C.surface, 18, C.border);
  text(board, `TableTitle/${titleValue}`, titleValue, x + 22, y + 20, 18, C.text, "700");
  rect(board, `TableHeader/${titleValue}`, x + 16, y + 54, w - 32, 42, C.bg, 10);
  const colW = (w - 48) / headers.length;
  headers.forEach((label, i) => text(board, `Header/${titleValue}/${label}`, label, x + 26 + i * colW, y + 67, 12, C.muted, "600"));
  rows.forEach((row, ri) => {
    const yy = y + 104 + ri * rowH;
    row.forEach((value, ci) => text(board, `Cell/${titleValue}/${ri}/${ci}`, value, x + 26 + ci * colW, yy + 14, 13, ci === 0 ? C.primary : C.text, ci === 0 ? "600" : "400"));
  });
}

function addAdminOrders(board) {
  rect(board, "Filters/Card", 292, 104, 1108, 112, C.surface, 18, C.border);
  ["状态：全部", "日期：近30天", "渠道：全部", "服务：全部"].forEach((label, i) => chip(board, label, 316 + i * 160, 130, C.text, C.bg, 142));
  button(board, "导出当前结果", 1190, 128, 180, "secondary");
  addTable(board, "订单列表", 292, 248, 1108, ["订单号", "客户", "渠道", "预约时间", "金额", "状态", "操作"], [
    ["YX0018", "王女士", "iOS", "07-25 14:30", "¥168", "待服务", "查看"],
    ["YX0017", "李先生", "微信小程序", "07-25 13:00", "¥299", "服务中", "查看"],
    ["YX0016", "周女士", "Android", "07-24 11:30", "¥238", "退款审核", "处理"],
    ["YX0015", "郑先生", "微信小程序", "07-24 10:00", "¥99", "已完成", "查看"],
    ["YX0014", "陈女士", "iOS", "07-23 18:30", "¥188", "已取消", "查看"],
  ]);
  text(board, "Pagination/Info", "共 2,316 条 · 第 1 / 232 页", 292, 736, 13, C.muted, "400");
  button(board, "下一页", 1270, 720, 130, "neutral");
}

function addAdminOrderDetail(board) {
  text(board, "OrderDetail/Back", "‹ 返回订单列表", 292, 104, 14, C.primary, "600");
  rect(board, "OrderDetail/Summary", 292, 144, 1108, 142, C.surface, 18, C.border);
  text(board, "OrderDetail/No", "订单 YX202607240018", 316, 168, 20, C.text, "700");
  status(board, "待服务", 316, 212, "warning");
  text(board, "OrderDetail/Amount", "实付 ¥168", 1234, 170, 22, C.danger, "700");
  button(board, "联系客户", 1060, 220, 142, "secondary");
  button(board, "取消订单", 1218, 220, 142, "danger");
  rect(board, "OrderDetail/Timeline", 292, 318, 700, 278, C.surface, 18, C.border);
  text(board, "OrderDetail/TimelineTitle", "订单进度", 316, 342, 18, C.text, "700");
  ["10:12 创建订单", "10:13 微信支付成功", "10:15 服务人员接单", "等待 7月25日 14:30 上门"].forEach((label, i) => {
    ellipse(board, `OrderDetail/Dot/${i}`, 324, 390 + i * 48, 14, 14, i < 3 ? C.secondary : C.warning);
    text(board, `OrderDetail/Step/${i}`, label, 356, 386 + i * 48, 14, C.text, i === 3 ? "650" : "400");
  });
  rect(board, "OrderDetail/Customer", 1020, 318, 380, 278, C.surface, 18, C.border);
  text(board, "OrderDetail/CustomerTitle", "客户与隐私", 1044, 342, 18, C.text, "700");
  text(board, "OrderDetail/CustomerText", "王女士  138****2468\n上海市徐汇区（按权限脱敏）\n虚拟号码有效至服务完成\n渠道：微信小程序", 1044, 390, 14, C.muted, "400", 320);
  addTable(board, "支付与售后", 292, 628, 1108, ["支付单", "支付方式", "支付时间", "金额", "退款状态", "操作"], [
    ["PAY7826", "微信支付", "07-24 10:13", "¥168", "无退款", "查看流水"],
  ]);
}

function addAdminServices(board) {
  rect(board, "ServiceAdmin/Toolbar", 292, 104, 1108, 82, C.surface, 18, C.border);
  chip(board, "全部分类", 316, 128, C.text, C.bg, 120);
  chip(board, "在售", 452, 128, C.secondary, C.secondarySoft, 92);
  button(board, "新建服务", 1240, 120, 136, "primary");
  addTable(board, "服务与价格", 292, 218, 680, ["服务", "分类", "基础价", "状态", "操作"], [
    ["肩颈舒缓理疗", "健康", "¥168", "在售", "编辑"],
    ["全屋深度保洁", "家政", "¥299", "在售", "编辑"],
    ["空调深度清洗", "家电", "¥238", "在售", "编辑"],
    ["宠物基础护理", "宠物", "¥99", "草稿", "编辑"],
  ]);
  rect(board, "ServiceAdmin/Editor", 1000, 218, 400, 590, C.surface, 18, C.border);
  text(board, "ServiceAdmin/EditorTitle", "编辑：肩颈舒缓理疗", 1024, 244, 18, C.text, "700");
  ["服务名称", "所属分类", "服务时长", "基础价格", "可取消时间", "服务说明"].forEach((label, i) => {
    text(board, `EditorLabel/${label}`, label, 1024, 294 + i * 72, 12, C.muted, "600");
    rect(board, `EditorField/${label}`, 1024, 314 + i * 72, 352, 42, C.surface, 10, C.border);
    text(board, `EditorValue/${label}`, ["肩颈舒缓理疗", "健康理疗", "60 分钟", "168.00", "开始前 2 小时", "专业理疗师上门服务"][i], 1038, 326 + i * 72, 13, C.text, "400");
  });
  button(board, "保存修改", 1024, 748, 352, "primary");
}

function addAdminAccess(board) {
  addTable(board, "角色与数据范围", 292, 104, 520, ["角色", "数据范围", "成员", "状态"], [
    ["客服", "所属城市", "42", "启用"],
    ["运营", "所属区域", "18", "启用"],
    ["财务", "退款与对账", "8", "启用"],
    ["管理员", "全组织", "3", "受保护"],
  ]);
  rect(board, "Access/Permissions", 840, 104, 560, 422, C.surface, 18, C.border);
  text(board, "Access/PermissionsTitle", "运营角色权限", 864, 128, 18, C.text, "700");
  ["查看脱敏订单", "查看完整联系方式", "发起退款", "修改未来价格", "分配角色"].forEach((label, i) => {
    text(board, `Access/Permission/${label}`, label, 864, 184 + i * 56, 14, C.text, "500");
    const enabled = i === 0 || i === 3;
    chip(board, enabled ? "允许" : "不允许", 1250, 172 + i * 56, enabled ? C.secondary : C.muted, enabled ? C.secondarySoft : C.bg, 102);
  });
  button(board, "保存角色权限", 1168, 456, 184, "primary");
  addTable(board, "最近审计事件", 292, 560, 1108, ["时间", "操作者", "操作", "对象", "原因", "结果"], [
    ["10:42", "管理员 张敏", "修改价格", "肩颈理疗", "暑期活动", "成功"],
    ["10:18", "客服 李华", "查看完整电话", "YX0018", "联系上门", "成功"],
    ["09:56", "运营 王晨", "申请退款", "YX0016", "服务异常", "待审核"],
  ]);
}

function addAdminPage(page) {
  const componentMap = JSON.stringify({
    shell: "Sidebar",
    metrics: "Card",
    lists: "Table + Data Table",
    forms: "FieldGroup + Field",
    status: "Badge",
    destructive: "AlertDialog",
    loading: "Skeleton",
    empty: "Empty",
    feedback: "Sonner",
    icons: "Lucide",
    motion: "CSS + motion/react",
  });
  const specs = [
    ["UI-ADM-001-运营总览", "总览", addAdminDashboard],
    ["UI-ADM-002-订单列表", "订单", addAdminOrders],
    ["UI-ADM-003-订单详情", "订单详情", addAdminOrderDetail],
    ["UI-ADM-004-服务管理", "服务与价格", addAdminServices],
    ["UI-ADM-005-权限与审计", "权限", addAdminAccess],
  ];
  specs.forEach(([id, titleValue, renderer], i) => {
    const x = (i % 2) * 1500;
    const y = Math.floor(i / 2) * 1084;
    const { board, created } = addBoard(page, id, x, y, 1440, 1024, C.surface, 20);
    if (created) {
      adminChrome(board, titleValue);
      renderer(board);
    }
    board.setPluginData("ui-id", id);
    board.setPluginData("platform", "admin-web");
    board.setPluginData("component-library", "shadcn/ui");
    board.setPluginData("component-map", componentMap);
    board.setPluginData("icon-library", "lucide-react");
    board.setPluginData("motion-library", "CSS + motion/react");
    let implementationLabel = board.children.find((shape) => shape.name === "Implementation / ComponentLibrary");
    if (!implementationLabel) {
      implementationLabel = text(board, "Implementation/ComponentLibrary", "React · shadcn/ui · Lucide", 780, 26, 12, C.muted, "600");
    } else {
      implementationLabel.characters = "React · shadcn/ui · Lucide";
    }
  });
  const start = page.findShapes({ name: "UI-ADM-001-运营总览", type: "board" })[0];
  if (start && !page.flows.find((f) => f.name === "admin-P0-订单处理")) page.createFlow("admin-P0-订单处理", start);
  const orders = page.findShapes({ name: "UI-ADM-002-订单列表", type: "board" })[0];
  const detail = page.findShapes({ name: "UI-ADM-003-订单详情", type: "board" })[0];
  const openDetail = orders && orders.children.find((s) => s.name === "Cell / 订单列表 / 0 / 6");
  const backToOrders = detail && detail.children.find((s) => s.name === "OrderDetail / Back");
  if (openDetail && detail && openDetail.interactions.length === 0) openDetail.addInteraction("click", { type: "navigate-to", destination: detail });
  if (backToOrders && orders && backToOrders.interactions.length === 0) backToOrders.addInteraction("click", { type: "navigate-to", destination: orders });
}

function addCover(page) {
  const { board, created } = addBoard(page, "YUEXIANG-OMNICHANNEL-DESIGN", 0, 0, 1440, 1024, C.bg, 28);
  if (!created) {
    const output = board.children.find((shape) => shape.name === "Cover / OutputList");
    if (output) output.characters = "✓ 6 个 Penpot 语义页面\n✓ 19 个关键流程画板\n✓ 共享 Token 与组件\n✓ 四端平台差异矩阵\n✓ OpenAPI 3.1 契约\n✓ 测试、发布与运维样例";
    return;
  }
  rect(board, "Cover/Accent", 0, 0, 18, 1024, C.primary, 0);
  ellipse(board, "Cover/GlowA", 1040, -180, 620, 620, C.primarySoft, 0.9);
  ellipse(board, "Cover/GlowB", 1180, 460, 420, 420, C.secondarySoft, 0.9);
  text(board, "Cover/Kicker", "UI / UX DELIVERY REFERENCE", 92, 86, 14, C.primary, "700");
  text(board, "Cover/Title", "悦享服务\n全渠道应用设计样例", 92, 134, 54, C.text, "750", 760);
  text(board, "Cover/Subtitle", "Android · iOS · 微信小程序 · 运营管理后台", 96, 286, 22, C.muted, "500");
  text(board, "Cover/Description", "用同一套产品语义、需求 ID、设计 Token 与验收标准，\n展示从发现服务到预约、支付、履约、售后和运营管理的完整闭环。", 96, 346, 18, C.muted, "400", 760);
  ["产品与需求", "跨端体验", "设计系统", "API 与数据", "测试与发布"].forEach((label, i) => chip(board, label, 96 + i * 154, 446, C.primary, C.surface, 138));
  rect(board, "Cover/FlowCard", 92, 540, 820, 318, C.surface, 24, C.border);
  text(board, "Cover/FlowTitle", "P0 核心闭环", 120, 568, 20, C.text, "700");
  ["发现服务", "查看详情", "选择时间", "支付确认", "履约提醒", "评价售后"].forEach((label, i) => {
    const x = 122 + (i % 3) * 244;
    const y = 626 + Math.floor(i / 3) * 100;
    ellipse(board, `Cover/StepDot/${label}`, x, y, 42, 42, i < 4 ? C.primary : C.secondary);
    text(board, `Cover/StepNo/${label}`, String(i + 1), x + 15, y + 11, 14, C.surface, "700");
    text(board, `Cover/StepLabel/${label}`, label, x + 56, y + 10, 15, C.text, "650");
  });
  rect(board, "Cover/OutputCard", 964, 540, 382, 318, C.dark, 24);
  text(board, "Cover/OutputTitle", "交付物", 992, 570, 20, C.surface, "700");
  text(board, "Cover/OutputList", "✓ 6 个 Penpot 语义页面\n✓ 19 个关键流程画板\n✓ 共享 Token 与组件\n✓ 四端平台差异矩阵\n✓ OpenAPI 3.1 契约\n✓ 测试、发布与运维样例", 992, 620, 16, "#D4D9E4", "400", 310);
  text(board, "Cover/Footer", "样例版本 0.1.0 · 2026-07-24 · 仅作为 Skill 参考实现", 94, 932, 13, C.muted, "400");
}

function addDesignSystem(page) {
  const { board, created } = addBoard(page, "DS-001-共享设计系统", 0, 0, 1600, 1320, C.bg, 24);
  if (!created) return;
  text(board, "DS/Title", "悦享设计系统", 64, 54, 36, C.text, "750");
  text(board, "DS/Subtitle", "产品语义共享，导航、控件和系统能力按平台映射", 66, 106, 16, C.muted, "400");
  text(board, "DS/ColorTitle", "语义颜色", 64, 166, 22, C.text, "700");
  [
    ["Primary", C.primary],
    ["Success", C.secondary],
    ["Warning", C.warning],
    ["Danger", C.danger],
    ["Info", C.info],
    ["Surface", C.surface],
  ].forEach(([name, color], i) => {
    const x = 64 + i * 238;
    rect(board, `Color/${name}`, x, 210, 206, 126, color, 18, name === "Surface" ? C.border : null);
    text(board, `ColorName/${name}`, name, x + 18, 228, 14, name === "Surface" ? C.text : C.surface, "650");
    text(board, `ColorValue/${name}`, color, x + 18, 294, 13, name === "Surface" ? C.muted : C.surface, "400");
  });
  text(board, "DS/TypeTitle", "排版", 64, 390, 22, C.text, "700");
  text(board, "DS/Display", "Display / 36 / 750", 64, 438, 36, C.text, "750");
  text(board, "DS/Heading", "Heading / 24 / 700", 64, 504, 24, C.text, "700");
  text(board, "DS/Body", "Body / 16 / 400 · 中文正文应简洁、可扫描并支持动态字体。", 64, 554, 16, C.muted, "400");
  text(board, "DS/ComponentTitle", "核心组件与状态", 64, 630, 22, C.text, "700");
  button(board, "主要操作", 64, 680, 180, "primary");
  button(board, "次要操作", 264, 680, 180, "secondary");
  button(board, "危险操作", 464, 680, 180, "danger");
  button(board, "中性操作", 664, 680, 180, "neutral");
  status(board, "已支付", 64, 756, "success");
  status(board, "待服务", 172, 756, "warning");
  status(board, "退款中", 280, 756, "danger");
  status(board, "草稿", 388, 756, "info");
  rect(board, "Field/Default", 64, 842, 360, 64, C.surface, 14, C.border);
  text(board, "Field/Label", "预约地址", 80, 854, 11, C.muted, "600");
  text(board, "Field/Value", "上海市徐汇区 · 已保护详细地址", 80, 878, 14, C.text, "400");
  rect(board, "Card/Service", 464, 842, 420, 118, C.surface, 18, C.border);
  rect(board, "Card/Image", 480, 858, 86, 86, C.primarySoft, 14);
  text(board, "Card/Title", "肩颈舒缓理疗 · 60分钟", 586, 862, 16, C.text, "650");
  text(board, "Card/Meta", "4.9分 · 明码标价 · 售后保障", 586, 896, 13, C.muted, "400");
  text(board, "Card/Price", "¥168 起", 586, 924, 16, C.danger, "700");
  text(board, "DS/PlatformTitle", "平台映射", 64, 1028, 22, C.text, "700");
  const rows = [
    ["返回", "边缘返回手势", "系统 Back/预测返回", "页面栈返回", "浏览器历史/面包屑"],
    ["支付", "Apple/聚合支付", "聚合支付", "微信支付", "仅查看与退款审核"],
    ["导航", "Tab + NavigationStack", "Bottom Nav + Top App Bar", "宿主 TabBar + 胶囊", "侧栏 + 路由"],
  ];
  addTable(board, "跨端语义映射", 64, 1076, 1472, ["能力", "iOS", "Android", "微信小程序", "管理后台"], rows);
}

function ensureTokens() {
  const catalog = penpot.library.local.tokens;
  let set = catalog.sets.find((item) => item.name === "Yuexiang/Semantic");
  if (!set) set = catalog.addSet({ name: "Yuexiang/Semantic" });
  if (!set.active) set.toggleActive();
  const definitions = [
    ["color", "color.action.primary", C.primary],
    ["color", "color.feedback.success", C.secondary],
    ["color", "color.feedback.warning", C.warning],
    ["color", "color.feedback.danger", C.danger],
    ["color", "color.surface.default", C.surface],
    ["color", "color.content.primary", C.text],
    ["color", "color.content.secondary", C.muted],
    ["spacing", "space.2", "8"],
    ["spacing", "space.3", "12"],
    ["spacing", "space.4", "16"],
    ["spacing", "space.6", "24"],
    ["borderRadius", "radius.control", "14"],
    ["borderRadius", "radius.card", "18"],
    ["fontSizes", "font.body", "16"],
    ["fontSizes", "font.title", "24"],
  ];
  definitions.forEach(([type, name, value]) => {
    if (!set.tokens.find((token) => token.name === name)) set.addToken({ type, name, value });
  });
  return { set: set.name, tokens: definitions.length };
}

const pages = {
  cover: ensurePage("00-说明", true),
  system: ensurePage("01-设计系统"),
  ios: ensurePage("02-iOS"),
  android: ensurePage("03-Android"),
  mini: ensurePage("04-微信小程序"),
  admin: ensurePage("05-管理后台"),
};

const commonSpecs = [
  { id: "UI-MOB-001-首页", title: "悦享服务", kind: "home", purpose: "发现和搜索服务" },
  { id: "UI-MOB-002-服务详情", title: "服务详情", kind: "detail", purpose: "理解服务并选择预约" },
  { id: "UI-MOB-003-预约确认", title: "确认预约", kind: "booking", purpose: "选择服务人员和时间" },
  { id: "UI-MOB-004-支付结果", title: "支付结果", kind: "payment", purpose: "确认支付与恢复路径" },
  { id: "UI-MOB-005-订单详情", title: "订单详情", kind: "order", purpose: "跟踪履约和发起售后" },
];
const tokenResult = ensureTokens();
const activePage = penpot.currentPage.name;
if (activePage === "00-说明") addCover(pages.cover);
if (activePage === "01-设计系统") addDesignSystem(pages.system);
if (activePage === "02-iOS") addMobilePage(pages.ios, "ios", commonSpecs.map((item) => ({ ...item, id: item.id.replace("MOB", "IOS") })));
if (activePage === "03-Android") addMobilePage(pages.android, "android", commonSpecs.map((item) => ({ ...item, id: item.id.replace("MOB", "AND") })));
if (activePage === "04-微信小程序") addMobilePage(pages.mini, "mini", commonSpecs.slice(0, 4).map((item) => ({ ...item, id: item.id.replace("MOB", "WX") })));
if (activePage === "05-管理后台") addAdminPage(pages.admin);

return {
  activePage,
  pages: penpotUtils.getPages(),
  tokenResult,
  boards: penpot.currentPage.findShapes({ type: "board" }).map((board) => ({ id: board.id, name: board.name })),
};
