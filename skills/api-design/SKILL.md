---
name: api-design
description: REST API 设计模式，包括资源命名、状态码、分页、过滤、错误响应、版本控制和生产级 API 的速率限制。
---

# API 设计模式 (API Design Patterns)

设计一致且对开发者友好的 REST API 的约定与最佳实践。

## 何时启用

- 设计新的 API 端点时。
- 评审现有的 API 契约时。
- 添加分页、过滤或排序功能时。
- 为 API 实施错误处理时。
- 规划 API 版本控制策略时。
- 构建面向公众或合作伙伴的 API 时。

## 资源设计 (Resource Design)

### URL 结构

```
# 资源应为名词、复数、小写、短横线命名 (kebab-case)
GET    /api/v1/users
GET    /api/v1/users/:id
POST   /api/v1/users
PUT    /api/v1/users/:id
PATCH  /api/v1/users/:id
DELETE /api/v1/users/:id

# 关系的子资源
GET    /api/v1/users/:id/orders
POST   /api/v1/users/:id/orders

# 无法映射到 CRUD 的操作（谨慎使用动词）
POST   /api/v1/orders/:id/cancel
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
```

### 命名规则

```
# 推荐 (GOOD)
/api/v1/team-members          # 多单词资源使用 kebab-case
/api/v1/orders?status=active  # 使用查询参数进行过滤
/api/v1/users/123/orders      # 使用嵌套资源表示归属关系

# 避免 (BAD)
/api/v1/getUsers              # URL 中包含动词
/api/v1/user                  # 使用单数（应使用复数）
/api/v1/team_members          # URL 中使用下划线 (snake_case)
/api/v1/users/123/getOrders   # 嵌套资源中包含动词
```

## HTTP 方法与状态码

### 方法语义

| 方法 | 幂等性 | 安全性 | 用途 |
|--------|-----------|------|---------|
| GET | 是 | 是 | 获取资源 |
| POST | 否 | 否 | 创建资源、触发操作 |
| PUT | 是 | 否 | 完整替换资源 |
| PATCH | 否* | 否 | 部分更新资源 |
| DELETE | 是 | 否 | 删除资源 |

*通过适当的实现，PATCH 也可以设计为幂等的。

### 状态码参考

```
# 成功 (Success)
200 OK                    — GET, PUT, PATCH（包含响应体）
201 Created               — POST（需包含 Location 响应头）
204 No Content            — DELETE, PUT（无响应体）

# 客户端错误 (Client Errors)
400 Bad Request           — 验证失败、JSON 格式错误
401 Unauthorized          — 缺失或无效的身份验证
403 Forbidden             — 已验证身份但无操作权限
404 Not Found             — 资源不存在
409 Conflict              — 重复条目、状态冲突
422 Unprocessable Entity  — 语义无效（JSON 正确但数据逻辑错误）
429 Too Many Requests     — 超出速率限制

# 服务器错误 (Server Errors)
500 Internal Server Error — 意外故障（绝不暴露内部细节）
502 Bad Gateway           — 上游服务故障
503 Service Unavailable   — 临时过载，需包含 Retry-After 响应头
```

### 常见错误

```
# 错误做法：所有响应都返回 200
{ "status": 200, "success": false, "error": "Not found" }

# 正确做法：语义化使用 HTTP 状态码
HTTP/1.1 404 Not Found
{ "error": { "code": "not_found", "message": "User not found" } }

# 错误做法：验证错误返回 500
# 正确做法：返回 400 或 422，并包含字段级的详细信息

# 错误做法：创建资源返回 200
# 正确做法：返回 201 并附带 Location 响应头
HTTP/1.1 201 Created
Location: /api/v1/users/abc-123
```

## 响应格式

### 成功响应

```json
{
  "data": {
    "id": "abc-123",
    "email": "alice@example.com",
    "name": "Alice",
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

### 集合响应（带分页）

```json
{
  "data": [
    { "id": "abc-123", "name": "Alice" },
    { "id": "def-456", "name": "Bob" }
  ],
  "meta": {
    "total": 142,
    "page": 1,
    "per_page": 20,
    "total_pages": 8
  },
  "links": {
    "self": "/api/v1/users?page=1&per_page=20",
    "next": "/api/v1/users?page=2&per_page=20",
    "last": "/api/v1/users?page=8&per_page=20"
  }
}
```

### 错误响应

```json
{
  "error": {
    "code": "validation_error",
    "message": "请求验证失败",
    "details": [
      {
        "field": "email",
        "message": "必须是有效的电子邮件地址",
        "code": "invalid_format"
      },
      {
        "field": "age",
        "message": "必须在 0 到 150 之间",
        "code": "out_of_range"
      }
    ]
  }
}
```

### 响应封装变体

```typescript
// 选项 A：带 data 包装器的封装（推荐用于公共 API）
interface ApiResponse<T> {
  data: T;
  meta?: PaginationMeta;
  links?: PaginationLinks;
}

interface ApiError {
  error: {
    code: string;
    message: string;
    details?: FieldError[];
  };
}

// 选项 B：扁平化响应（更简单，常用于内部 API）
// 成功：直接返回资源对象
// 失败：返回错误对象
// 通过 HTTP 状态码区分
```

## 分页 (Pagination)

### 基于偏移量 (Offset-Based / 简单分页)

```
GET /api/v1/users?page=2&per_page=20

# 实现参考
SELECT * FROM users
ORDER BY created_at DESC
LIMIT 20 OFFSET 20;
```

**优点**：易于实现，支持“跳到第 N 页”。
**缺点**：在大偏移量（如 OFFSET 100000）时性能较差，且在并发插入时可能出现数据重复或遗漏。

### 基于游标 (Cursor-Based / 可扩展分页)

```
GET /api/v1/users?cursor=eyJpZCI6MTIzfQ&limit=20

# 实现参考
SELECT * FROM users
WHERE id > :cursor_id
ORDER BY id ASC
LIMIT 21;  -- 多取一条以确定是否有下一页 (has_next)
```

```json
{
  "data": [...],
  "meta": {
    "has_next": true,
    "next_cursor": "eyJpZCI6MTQzfQ"
  }
}
```

**优点**：无论位置如何，性能始终保持稳定；在并发插入时表现稳定。
**缺点**：无法跳转到任意页码，游标通常是不透明的。

### 如何选择

| 使用场景 | 分页类型 |
|----------|----------------|
| 管理后台、小型数据集 (<10K) | 偏移量 (Offset) |
| 无限滚动、Feed 流、大型数据集 | 游标 (Cursor) |
| 公共 API | 默认游标，可选偏移量 |
| 搜索结果 | 偏移量（用户通常期望看到页码） |

## 过滤、排序与搜索

### 过滤 (Filtering)

```
# 简单等值过滤
GET /api/v1/orders?status=active&customer_id=abc-123

# 比较操作符（使用括号标记）
GET /api/v1/products?price[gte]=10&price[lte]=100
GET /api/v1/orders?created_at[after]=2025-01-01

# 多值过滤（逗号分隔）
GET /api/v1/products?category=electronics,clothing

# 嵌套字段（点号标记）
GET /api/v1/orders?customer.country=US
```

### 排序 (Sorting)

```
# 单字段排序（前缀 - 表示降序）
GET /api/v1/products?sort=-created_at

# 多字段排序（逗号分隔）
GET /api/v1/products?sort=-featured,price,-created_at
```

### 全文搜索 (Full-Text Search)

```
# 全局搜索参数
GET /api/v1/products?q=wireless+headphones

# 针对特定字段的搜索
GET /api/v1/users?email=alice
```

### 稀疏字段集 (Sparse Fieldsets)

```
# 仅返回指定字段（减小负载）
GET /api/v1/users?fields=id,name,email
GET /api/v1/orders?fields=id,total,status&include=customer.name
```

## 认证与授权 (Authentication and Authorization)

### 基于令牌的认证

```
# 在 Authorization 响应头中使用 Bearer 令牌
GET /api/v1/users
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

# API 密钥（用于服务器间调用）
GET /api/v1/data
X-API-Key: sk_live_abc123
```

### 授权模式

```typescript
// 资源级：检查所有权
app.get("/api/v1/orders/:id", async (req, res) => {
  const order = await Order.findById(req.params.id);
  if (!order) return res.status(404).json({ error: { code: "not_found" } });
  if (order.userId !== req.user.id) return res.status(403).json({ error: { code: "forbidden" } });
  return res.json({ data: order });
});

// 角色级：检查权限
app.delete("/api/v1/users/:id", requireRole("admin"), async (req, res) => {
  await User.delete(req.params.id);
  return res.status(204).send();
});
```

## 速率限制 (Rate Limiting)

### 响应头

```
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000

# 当超出限制时
HTTP/1.1 429 Too Many Requests
Retry-After: 60
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "速率限制超出。请在 60 秒后重试。"
  }
}
```

### 速率限制分层

| 层级 | 限制 | 时间窗口 | 使用场景 |
|------|-------|--------|----------|
| 匿名用户 | 30/min | 按 IP | 公共端点 |
| 已验证用户 | 100/min | 按用户 | 标准 API 访问 |
| 高级用户 | 1000/min | 按 API 密钥 | 付费 API 套餐 |
| 内部服务 | 10000/min | 按服务 | 服务间通信 |

## 版本控制 (Versioning)

### URL 路径版本控制（推荐）

```
/api/v1/users
/api/v2/users
```

**优点**：显式、易于路由、可缓存。
**缺点**：版本更新时 URL 会发生变化。

### 响应头版本控制

```
GET /api/users
Accept: application/vnd.myapp.v2+json
```

**优点**：URL 保持整洁。
**缺点**：较难测试，容易遗漏。

### 版本控制策略

1. 从 `/api/v1/` 开始 —— 除非必要，否则不要引入新版本。
2. 最多维持 2 个活跃版本（当前版本 + 上一版本）。
3. 弃用时间表：
   - 发布弃用公告（公共 API 提前 6 个月通知）。
   - 添加 Sunset 响应头：`Sunset: Sat, 01 Jan 2026 00:00:00 GMT`。
   - 在 Sunset 日期后返回 `410 Gone`。
4. **非破坏性变更**不需要新版本：
   - 在响应中添加新字段。
   - 添加新的可选查询参数。
   - 添加新的端点。
5. **破坏性变更**必须发布新版本：
   - 删除或重命名字段。
   - 更改字段类型。
   - 更改 URL 结构。
   - 更改身份验证方法。

## API 设计自查表 (API Design Checklist)

在发布新端点之前：

- [ ] 资源 URL 符合命名约定（复数、kebab-case、无动词）。
- [ ] 使用了正确的 HTTP 方法（读取用 GET，创建用 POST 等）。
- [ ] 返回了适当的状态码（不要全部返回 200）。
- [ ] 输入已通过模式验证 (Zod, Pydantic, Bean Validation 等)。
- [ ] 错误响应符合标准格式，包含代码和信息。
- [ ] 列表端点已实施分页（游标或偏移量）。
- [ ] 要求身份验证（或明确标记为公开）。
- [ ] 检查了授权逻辑（用户只能访问自己的资源）。
- [ ] 已配置速率限制。
- [ ] 响应中没有泄露内部细节（堆栈跟踪、SQL 错误）。
- [ ] 命名与现有端点保持一致（camelCase vs snake_case）。
- [ ] 文档已更新 (OpenAPI/Swagger 规范)。