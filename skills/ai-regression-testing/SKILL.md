---
name: ai-regression-testing
description: AI 辅助开发中的回归测试策略。包括无数据库依赖的沙盒模式 API 测试、自动化 Bug 检查工作流，以及针对“同一模型既写代码又审代码”导致的 AI 盲点捕捉模式。
---

# AI 回归测试 (AI Regression Testing)

专门为 AI 辅助开发设计的测试模式，针对“同一个模型既编写代码又评审代码”所产生的系统性盲点——这些盲点只有通过自动化测试才能捕捉到。

## 何时启用

- AI 代理（Claude Code、Gemini Cli、Codex）修改了 API 路由或后端逻辑。
- 发现并修复了一个 Bug —— 需要防止其再次出现。
- 项目拥有可以利用的沙盒/模拟 (Sandbox/Mock) 模式，用于无数据库测试。
- 在代码更改后运行 `/bug-check` 或类似的评审命令。
- 存在多个代码路径（沙盒 vs 生产、特性标志等）。

## 核心问题

当 AI 编写代码并随后评审自己的工作时，它会在两个步骤中携带相同的假设。这会产生一个可预测的失败模式：

```
AI 编写修复方案 → AI 评审修复方案 → AI 说“看起来正确” → Bug 仍然存在
```

**真实案例**（在生产环境中观察到）：

```
修复 1：在 API 响应中添加了 notification_settings
  → 忘记将其添加到 SELECT 查询中
  → AI 进行了评审并漏掉了这一点（同样的盲点）

修复 2：将其添加到 SELECT 查询中
  → TypeScript 构建错误（生成的类型中没有该列）
  → AI 评审了修复 1，但没发现 SELECT 的问题

修复 3：更改为 SELECT *
  → 修复了生产路径，但忘记了沙盒路径
  → AI 进行了评审，再次漏掉了这一点（第 4 次发生）

修复 4：测试在第一次运行时立即捕捉到了它 ✅
```

结论：**沙盒/生产路径的不一致**是 AI 引入的第一大回归问题。

## 沙盒模式 API 测试

大多数具有对 AI 友好架构的项目都有沙盒/模拟模式。这是实现快速、无数据库 API 测试的关键。

### 设置 (Vitest + Next.js App Router)

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import path from "path";

export default defineConfig({
  test: {
    environment: "node",
    globals: true,
    include: ["__tests__/**/*.test.ts"],
    setupFiles: ["__tests__/setup.ts"],
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "."),
    },
  },
});
```

```typescript
// __tests__/setup.ts
// 强制开启沙盒模式 — 无需数据库
process.env.SANDBOX_MODE = "true";
process.env.NEXT_PUBLIC_SUPABASE_URL = "";
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = "";
```

### Next.js API 路由测试辅助函数

```typescript
// __tests__/helpers.ts
import { NextRequest } from "next/server";

export function createTestRequest(
  url: string,
  options?: {
    method?: string;
    body?: Record<string, unknown>;
    headers?: Record<string, string>;
    sandboxUserId?: string;
  },
): NextRequest {
  const { method = "GET", body, headers = {}, sandboxUserId } = options || {};
  const fullUrl = url.startsWith("http") ? url : `http://localhost:3000${url}`;
  const reqHeaders: Record<string, string> = { ...headers };

  if (sandboxUserId) {
    reqHeaders["x-sandbox-user-id"] = sandboxUserId;
  }

  const init: { method: string; headers: Record<string, string>; body?: string } = {
    method,
    headers: reqHeaders,
  };

  if (body) {
    init.body = JSON.stringify(body);
    reqHeaders["content-type"] = "application/json";
  }

  return new NextRequest(fullUrl, init);
}

export async function parseResponse(response: Response) {
  const json = await response.json();
  return { status: response.status, json };
}
```

### 编写回归测试

核心原则：**为发现的 Bug 编写测试，而不是为正常运行的代码编写测试**。

```typescript
// __tests__/api/user/profile.test.ts
import { describe, it, expect } from "vitest";
import { createTestRequest, parseResponse } from "../../helpers";
import { GET, PATCH } from "@/app/api/user/profile/route";

// 定义契约 — 响应中必须包含哪些字段
const REQUIRED_FIELDS = [
  "id",
  "email",
  "full_name",
  "phone",
  "role",
  "created_at",
  "avatar_url",
  "notification_settings",  // ← 在发现缺失后添加
];

describe("GET /api/user/profile", () => {
  it("返回所有必需字段", async () => {
    const req = createTestRequest("/api/user/profile");
    const res = await GET(req);
    const { status, json } = await parseResponse(res);

    expect(status).toBe(200);
    for (const field of REQUIRED_FIELDS) {
      expect(json.data).toHaveProperty(field);
    }
  });

  // 回归测试 — 这个具体的 Bug 曾被 AI 引入了 4 次
  it("notification_settings 不应为 undefined (BUG-R1 回归测试)", async () => {
    const req = createTestRequest("/api/user/profile");
    const res = await GET(req);
    const { json } = await parseResponse(res);

    expect("notification_settings" in json.data).toBe(true);
    const ns = json.data.notification_settings;
    expect(ns === null || typeof ns === "object").toBe(true);
  });
});
```

### 测试沙盒/生产的一致性

最常见的 AI 回归问题：修复了生产路径但忘记了沙盒路径（反之亦然）。

```typescript
// 测试沙盒响应是否符合预期的契约
describe("GET /api/user/messages (对话列表)", () => {
  it("在沙盒模式下包含 partner_name", async () => {
    const req = createTestRequest("/api/user/messages", {
      sandboxUserId: "user-001",
    });
    const res = await GET(req);
    const { json } = await parseResponse(res);

    // 这捕捉到了一个 Bug：partner_name 被添加到生产路径
    // 但没被添加到沙盒路径
    if (json.data.length > 0) {
      for (const conv of json.data) {
        expect("partner_name" in conv).toBe(true);
      }
    }
  });
});
```

## 将测试集成到 Bug 检查工作流中

### 自定义命令定义

```markdown
<!-- .claude/commands/bug-check.md -->
# Bug 检查 (Bug Check)

## 第 1 步：自动化测试（强制执行，不可跳过）

在进行任何代码评审之前，先运行以下命令：

    npm run test       # Vitest 测试套件
    npm run build      # TypeScript 类型检查 + 构建

- 如果测试失败 → 作为最高优先级 Bug 报告
- 如果构建失败 → 将类型错误作为最高优先级报告
- 只有两者都通过后，才进入第 2 步

## 第 2 步：代码评审（AI 评审）

1. 沙盒/生产路径的一致性
2. API 响应结构符合前端预期
3. SELECT 子句的完整性
4. 带有回滚机制的错误处理
5. 乐观更新的竞态条件

## 第 3 步：针对每个修复的 Bug，提议一个回归测试
```

### 工作流示例

```
用户: "バグチェックして" (或 "/bug-check")
  │
  ├─ 第 1 步: npm run test
  │   ├─ 失败 → 机械地发现 Bug (不需要 AI 的主观判断)
  │   └─ 通过 → 继续
  │
  ├─ 第 2 步: npm run build
  │   ├─ 失败 → 机械地发现类型错误
  │   └─ 通过 → 继续
  │
  ├─ 第 3 步: AI 代码评审 (带着已知的盲点进行)
  │   └─ 报告发现的问题
  │
  └─ 第 4 步: 针对每个修复，编写回归测试
      └─ 下一次 Bug 检查如果破坏了修复，将被捕捉到
```

## 常见的 AI 回归模式

### 模式 1：沙盒/生产路径不匹配

**频率**：最常见（在 4 分之 3 的回归中观察到）

```typescript
// ❌ AI 仅在生产路径添加了字段
if (isSandboxMode()) {
  return { data: { id, email, name } };  // 缺失新字段
}
// 生产路径
return { data: { id, email, name, notification_settings } };

// ✅ 两个路径必须返回相同的结构
if (isSandboxMode()) {
  return { data: { id, email, name, notification_settings: null } };
}
return { data: { id, email, name, notification_settings } };
```

**捕捉它的测试**：

```typescript
it("沙盒和生产环境返回相同的字段", async () => {
  // 在测试环境中，沙盒模式被强制开启
  const res = await GET(createTestRequest("/api/user/profile"));
  const { json } = await parseResponse(res);

  for (const field of REQUIRED_FIELDS) {
    expect(json.data).toHaveProperty(field);
  }
});
```

### 模式 2：SELECT 子句遗漏

**频率**：在使用 Supabase/Prisma 添加新列时很常见

```typescript
// ❌ 响应中添加了新列，但 SELECT 中没有
const { data } = await supabase
  .from("users")
  .select("id, email, name")  // 这里没有 notification_settings
  .single();

return { data: { ...data, notification_settings: data.notification_settings } };
// → notification_settings 始终为 undefined

// ✅ 使用 SELECT * 或明确包含新列
const { data } = await supabase
  .from("users")
  .select("*")
  .single();
```

### 模式 3：错误状态泄露

**频率**：中等 —— 为现有组件添加错误处理时发生

```typescript
// ❌ 设置了错误状态但未清除旧数据
catch (err) {
  setError("加载失败");
  // reservations 仍然显示前一个标签页的数据！
}

// ✅ 出错时清除相关状态
catch (err) {
  setReservations([]);  // 清除陈旧数据
  setError("加载失败");
}
```

### 模式 4：没有正确回滚的乐观更新

```typescript
// ❌ 失败时没有回滚
const handleRemove = async (id: string) => {
  setItems(prev => prev.filter(i => i.id !== id));
  await fetch(`/api/items/${id}`, { method: "DELETE" });
  // 如果 API 失败，项目在 UI 中消失了，但仍然存在于数据库中
};

// ✅ 捕获之前状态并在失败时回滚
const handleRemove = async (id: string) => {
  const prevItems = [...items];
  setItems(prev => prev.filter(i => i.id !== id));
  try {
    const res = await fetch(`/api/items/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error("API 错误");
  } catch {
    setItems(prevItems);  // 回滚
    alert("删除失败");
  }
};
```

## 策略：在发现 Bug 的地方编写测试

不要追求 100% 的覆盖率。相反：

```
在 /api/user/profile 发现 Bug     → 为 profile API 编写测试
在 /api/user/messages 发现 Bug    → 为 messages API 编写测试
在 /api/user/favorites 发现 Bug   → 为 favorites API 编写测试
在 /api/user/notifications 无 Bug → （暂时）不编写测试
```

**为什么这在 AI 开发中有效：**

1. AI 往往会重复犯**同一类错误**。
2. Bug 会聚集在复杂区域（鉴权、多路径逻辑、状态管理）。
3. 一旦经过测试，该具体的回归**就不会再次发生**。
4. 测试数量随着 Bug 修复有机增长 —— 没有浪费的精力。

## 快速参考

| AI 回归模式 | 测试策略 | 优先级 |
|---|---|---|
| 沙盒/生产不匹配 | 断言沙盒模式下具有相同的响应结构 | 🔴 高 |
| SELECT 子句遗漏 | 断言响应中包含所有必需字段 | 🔴 高 |
| 错误状态泄露 | 断言出错时清理状态 | 🟡 中 |
| 缺失回滚 | 断言 API 失败时恢复状态 | 🟡 中 |
| 类型转换掩盖 null | 断言字段不为 undefined | 🟡 中 |

## 应当 / 禁止

**应当：**
- 发现 Bug 后立即编写测试（如果可能，在修复之前）。
- 测试 API 响应的结构，而不是具体的实现细节。
- 将运行测试作为每次 Bug 检查的第一步。
- 保持测试快速（在沙盒模式下总计 < 1 秒）。
- 以它们所防止的 Bug 命名测试（例如 "BUG-R1 回归测试"）。

**禁止：**
- 为从未出过 Bug 的代码编写测试。
- 信任 AI 的自我评审来替代自动化测试。
- 跳过沙盒路径测试，认为“那只是模拟数据”。
- 在单元测试足以解决问题时编写集成测试。
- 追求覆盖率百分比 —— 追求回归预防。
