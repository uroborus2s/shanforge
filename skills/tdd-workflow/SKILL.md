---
name: tdd-workflow
description: 在编写新功能、修复 Bug 或重构代码时使用此技能。强制执行测试驱动开发 (TDD)，确保涵盖单元测试、集成测试和端到端 (E2E) 测试的 80% 以上测试覆盖率；修 Bug 时必须先定位根因并禁止用未验证兜底绕过问题。
---

# 测试驱动开发 (TDD) 工作流

此技能确保所有代码开发都遵循 TDD 原则，并具有全面的测试覆盖率。

## 何时激活

- 编写新特性或功能时
- 修复 Bug 或问题时
- 重构现有代码时
- 添加 API 端点时
- 创建新组件时

## 核心原则

### 1. 测试先于代码 (Tests BEFORE Code)
始终先编写测试，然后实现代码以使测试通过。

### 2. Bug 根因先于修复 (Root Cause BEFORE Fix)
修 Bug 时必须先完成根因说明，再修改实现：
- 先复现失败，并记录可观察症状、触发条件和受影响路径。
- 明确直接原因与根源原因：直接原因说明哪一行、哪一个分支或哪一个契约破坏导致失败；根源原因说明为什么系统允许它发生。
- 新增或修改测试必须锁定根因路径，而不是只断言兜底结果。
- 禁止把 `try/except`、默认值、空结果、重试、忽略异常、宽松解析或“兼容一下”当作主要修复，除非已经证明该降级行为是产品契约，并且原始根因已经被修复或被明确登记为接受风险。
- 如果暂时无法定位根因，只允许增加诊断、日志、复现测试或最小探针；不得提交行为修复。

### 3. 覆盖率要求
- 最低 80% 的代码覆盖率（单元测试 + 集成测试 + E2E 测试）
- 覆盖所有边缘情况 (Edge cases)
- 测试错误场景 (Error scenarios)
- 验证边界条件 (Boundary conditions)

### 4. 测试类型

#### 单元测试 (Unit Tests)
- 独立的函数和工具类
- 组件逻辑
- 纯函数
- 辅助函数和工具函数

#### 集成测试 (Integration Tests)
- API 端点
- 数据库操作
- 服务间交互
- 外部 API 调用

#### 端到端测试 (E2E Tests - Playwright)
- 关键用户流程
- 完整的工作流
- 浏览器自动化
- UI 交互

## TDD 工作流步骤

### 步骤 1: 编写用户旅程或 Bug 根因记录
```text
作为一名 [角色]，我想要 [执行动作]，以便于 [获得收益]

示例:
作为一名用户，我想要语义化搜索市场，
以便于即使没有精确的关键词，我也能找到相关的市场。
```

修 Bug 时改用以下根因记录：

```text
Bug 症状：
复现步骤：
失败证据：
直接原因：
根源原因：
修复点：
防回归测试：
是否涉及兜底/降级：是/否；如果是，说明它为什么是既有契约而不是掩盖根因。
```

### 步骤 2: 生成测试用例 (Generate Test Cases)
为每个用户旅程创建全面的测试用例：

```typescript
describe('语义化搜索', () => {
  it('应当为查询返回相关的市场', async () => {
    // 测试实现
  })

  it('应当优雅地处理空查询', async () => {
    // 测试边缘情况
  })

  it('当已契约化的 Redis 降级路径触发时应当记录原因并返回子字符串搜索结果', async () => {
    // 仅测试已确认的降级契约，不用降级掩盖未知根因
  })

  it('应当按相似度得分排序结果', async () => {
    // 测试排序逻辑
  })
})
```

### 步骤 3: 运行测试 (测试应当失败 - RED)
```bash
npm test
# 测试应该失败 - 我们还没有进行实现
```

### 步骤 4: 实现代码 (Implement Code)
编写最小化代码以使测试通过：

- 修 Bug 时只修改造成根因的代码路径。
- 不新增与根因无关的兜底分支。
- 如果确实需要降级行为，把降级契约、触发条件和观测信号写进测试。

```typescript
// 由测试驱动的实现
export async function searchMarkets(query: string) {
  // 在此实现逻辑
}
```

### 步骤 5: 再次运行测试 (测试应当通过 - GREEN)
```bash
npm test
# 测试现在应该通过了
```

### 步骤 6: 重构 (Refactor)
在保持测试通过的前提下改善代码质量：
- 消除重复代码
- 改善命名
- 优化性能
- 增强可读性

### 步骤 7: 验证覆盖率 (Verify Coverage)
```bash
npm run test:coverage
# 验证是否达到了 80% 以上的覆盖率
```

## 测试模式 (Testing Patterns)

### 单元测试模式 (Jest/Vitest)
```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

describe('Button 组件', () => {
  it('应当使用正确的文本进行渲染', () => {
    render(<Button>点击我</Button>)
    expect(screen.getByText('点击我')).toBeInTheDocument()
  })

  it('点击时应当调用 onClick', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>点击</Button>)

    fireEvent.click(screen.getByRole('button'))

    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('当 disabled 属性为 true 时应当被禁用', () => {
    render(<Button disabled>点击</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })
})
```

### API 集成测试模式
```typescript
import { NextRequest } from 'next/server'
import { GET } from './route'

describe('GET /api/markets', () => {
  it('应当成功返回市场数据', async () => {
    const request = new NextRequest('http://localhost/api/markets')
    const response = await GET(request)
    const data = await response.json()

    expect(response.status).toBe(200)
    expect(data.success).toBe(true)
    expect(Array.isArray(data.data)).toBe(true)
  })

  it('应当验证查询参数', async () => {
    const request = new NextRequest('http://localhost/api/markets?limit=invalid')
    const response = await GET(request)

    expect(response.status).toBe(400)
  })

  it('应当优雅地处理数据库错误', async () => {
    // 模拟数据库失败
    const request = new NextRequest('http://localhost/api/markets')
    // 测试错误处理逻辑
  })
})
```

### E2E 测试模式 (Playwright)
```typescript
import { test, expect } from '@playwright/test'

test('用户可以搜索和过滤市场', async ({ page }) => {
  // 导航到市场页面
  await page.goto('/')
  await page.click('a[href="/markets"]')

  // 验证页面已加载
  await expect(page.locator('h1')).toContainText('Markets')

  // 搜索市场
  await page.fill('input[placeholder="Search markets"]', 'election')

  // 等待防抖和结果
  await page.waitForTimeout(600)

  // 验证搜索结果已显示
  const results = page.locator('[data-testid="market-card"]')
  await expect(results).toHaveCount(5, { timeout: 5000 })

  // 验证结果包含搜索词
  const firstResult = results.first()
  await expect(firstResult).toContainText('election', { ignoreCase: true })

  // 按状态过滤
  await page.click('button:has-text("Active")')

  // 验证过滤后的结果
  await expect(results).toHaveCount(3)
})

test('用户可以创建一个新市场', async ({ page }) => {
  // 首先登录
  await page.goto('/creator-dashboard')

  // 填写创建市场表单
  await page.fill('input[name="name"]', '测试市场')
  await page.fill('textarea[name="description"]', '测试描述')
  await page.fill('input[name="endDate"]', '2025-12-31')

  // 提交表单
  await page.click('button[type="submit"]')

  // 验证成功信息
  await expect(page.locator('text=Market created successfully')).toBeVisible()

  // 验证重定向到市场页面
  await expect(page).toHaveURL(/\/markets\/test-market/)
})
```

## 测试文件组织

```text
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx          # 单元测试
│   │   └── Button.stories.tsx       # Storybook
│   └── MarketCard/
│       ├── MarketCard.tsx
│       └── MarketCard.test.tsx
├── app/
│   └── api/
│       └── markets/
│           ├── route.ts
│           └── route.test.ts         # 集成测试
└── e2e/
    ├── markets.spec.ts               # E2E 测试
    ├── trading.spec.ts
    └── auth.spec.ts
```

## 模拟外部服务 (Mocking External Services)

### 模拟 Supabase
```typescript
jest.mock('@/lib/supabase', () => ({
  supabase: {
    from: jest.fn(() => ({
      select: jest.fn(() => ({
        eq: jest.fn(() => Promise.resolve({
          data: [{ id: 1, name: '测试市场' }],
          error: null
        }))
      }))
    }))
  }
}))
```

### 模拟 Redis
```typescript
jest.mock('@/lib/redis', () => ({
  searchMarketsByVector: jest.fn(() => Promise.resolve([
    { slug: 'test-market', similarity_score: 0.95 }
  ])),
  checkRedisHealth: jest.fn(() => Promise.resolve({ connected: true }))
}))
```

### 模拟 OpenAI
```typescript
jest.mock('@/lib/openai', () => ({
  generateEmbedding: jest.fn(() => Promise.resolve(
    new Array(1536).fill(0.1) // 模拟 1536 维度的嵌入向量
  ))
}))
```

## 测试覆盖率验证

### 运行覆盖率报告
```bash
npm run test:coverage
```

### 覆盖率阈值配置
```json
{
  "jest": {
    "coverageThresholds": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

## 常见的测试误区 (Common Testing Mistakes to Avoid)

### ❌ 错误：测试内部实现细节
```typescript
// 不要测试内部状态
expect(component.state.count).toBe(5)
```

### ✅ 正确：测试用户可见的行为
```typescript
// 测试用户实际看到的内容
expect(screen.getByText('数量: 5')).toBeInTheDocument()
```

### ❌ 错误：脆弱的选择器
```typescript
// 很容易因为结构变化而损坏
await page.click('.css-class-xyz')
```

### ✅ 正确：语义化选择器
```typescript
// 对 UI 变更更具韧性
await page.click('button:has-text("提交")')
await page.click('[data-testid="submit-button"]')
```

### ❌ 错误：测试之间存在依赖（缺乏隔离）
```typescript
// 测试相互依赖
test('创建用户', () => { /* ... */ })
test('更新同一个用户', () => { /* 依赖了上一个测试 */ })
```

### ✅ 正确：独立的测试
```typescript
// 每个测试都应该设置自己所需的数据
test('创建用户', () => {
  const user = createTestUser()
  // 测试逻辑
})

test('更新用户', () => {
  const user = createTestUser()
  // 更新逻辑
})
```

## 持续测试 (Continuous Testing)

### 开发时的监视模式 (Watch Mode)
```bash
npm test -- --watch
# 在文件保存更改时自动运行测试
```

### Git 提交前置钩子 (Pre-Commit Hook)
```bash
# 在每次 commit 之前运行
npm test && npm run lint
```

### CI/CD 集成
```yaml
# GitHub Actions
- name: Run Tests
  run: npm test -- --coverage
- name: Upload Coverage
  uses: codecov/codecov-action@v3
```

## 最佳实践 (Best Practices)

1. **测试先行 (Write Tests First)** - 始终贯彻 TDD。
2. **每个测试只断言一件事 (One Assert Per Test)** - 聚焦于单一的行为。
3. **描述性的测试名称 (Descriptive Test Names)** - 解释到底在测试什么。
4. **准备-执行-断言 (Arrange-Act-Assert)** - 保持清晰的测试代码结构。
5. **模拟外部依赖 (Mock External Dependencies)** - 隔离单元测试。
6. **测试边缘情况 (Test Edge Cases)** - 包括 Null、undefined、空值、极大极小值。
7. **测试错误路径 (Test Error Paths)** - 不要只测试理想情况 (Happy paths)。
8. **保持测试快速执行 (Keep Tests Fast)** - 每个单元测试应该在 50ms 以内。
9. **测试后清理 (Clean Up After Tests)** - 不要留下副作用。
10. **审查覆盖率报告 (Review Coverage Reports)** - 找出未测试到的盲区。

## 成功指标 (Success Metrics)

- 达到了 80%+ 的代码覆盖率
- 所有的测试都通过（全绿）
- 没有跳过或被禁用的测试
- 测试执行速度快（单元测试套件跑完 < 30秒）
- E2E 测试覆盖了所有关键的用户流程
- 测试能够在发布到生产环境前捕获到 Bug

---

**谨记**: 测试不是可选项。它们是一张安全网，能让你更加自信地进行重构、实现快速开发，并保障生产环境的可靠性。
