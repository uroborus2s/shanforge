# Stratix 应用开发规范

本页定义所有 Stratix 业务项目应遵守的配置、业务域和 Kysely SQL 开发规范。

## 目录

- [配置入口](#配置入口)
- [运行时取值](#运行时取值)
- [项目与模块配置](#项目与模块配置)
- [三层与业务域](#三层与业务域)
- [API 到 Kysely 完整示例](#api-到-kysely-完整示例)
- [实现顺序](#实现顺序)

## 配置入口

当前 create/forge 生成器直接维护 `src/stratix.config.ts`。不要凭旧指南额外创造 `src/config/stratix.generated.ts`，除非目标项目实际已有该层。

下面是带 `database` preset 的当前生成器兼容模板：

```ts
import type { StratixConfig } from '@stratix/core';
import databasePlugin from '@stratix/database';
import { fileURLToPath } from 'node:url';

interface SensitiveConfig {
  server?: {
    host?: string;
    port?: number | string;
  };
  database?: {
    host?: string;
    port?: number | string;
    database?: string;
    username?: string;
    password?: string;
  };
}

export default function createStratixConfig(
  sensitiveConfig: SensitiveConfig = {}
): StratixConfig {
  const serverConfig = sensitiveConfig.server || {};
  const databaseConfig = sensitiveConfig.database || {};
  const sourceRoot = fileURLToPath(new URL('.', import.meta.url));

  return {
    server: {
      host: serverConfig.host || '0.0.0.0',
      port: Number(serverConfig.port || 3000)
    },
    plugins: [
      {
        name: '@stratix/database',
        plugin: databasePlugin,
        options: {
          connections: {
            default: {
              type: 'mysql' as const,
              host: databaseConfig.host || 'localhost',
              port: Number(databaseConfig.port || 3306),
              database: databaseConfig.database || 'app',
              username: databaseConfig.username || 'root',
              password: databaseConfig.password || ''
            }
          }
        }
      }
    ],
    autoLoad: {},
    discovery: {
      enabled: true,
      rootDir: sourceRoot,
      routing: { enabled: true }
    }
  };
}
```

规则：

- `plugins` 的注册顺序就是加载顺序；基础设施先于消费它的插件。
- `rootDir` 指向当前源码/编译配置所在目录，应用 discovery 才能递归发现模块内组件。
- 全局 API 前缀放 `discovery.routing.prefix`；`@Controller()` 不接收前缀。
- 业务必填配置应在配置函数中失败关闭；不要回退到 `DB_HOST`、`PORT` 等普通业务环境变量。
- `STRATIX_ENCRYPTION_KEY` 不属于 `SensitiveConfig`。Core 在调用配置函数之前已经用它解密 `STRATIX_SENSITIVE_CONFIG`。
- 当前生成器默认写死 MySQL；使用 PostgreSQL 或 SQLite 时按目标驱动显式修改 `type` 和连接字段，不从敏感配置动态选择驱动。

## 运行时取值

### 读取测试模式

```ts
import { isTest } from '@stratix/core/environment';

if (isTest()) {
  // 只放确实需要的测试期行为。
}
```

`isTest()` 精确判断 `NODE_ENV === 'test'`；不会自动 trim 或转小写。未设置时 `getNodeEnv()` 默认返回 `development`。

### 读取加密 key

业务应用通常不需要读取 key：Forge 用它加密，Core 启动期用它解密。只有自定义启动器或专用配置工具确实需要时才读取：

```ts
import { required } from '@stratix/core/environment';

const encryptionKey = required('STRATIX_ENCRYPTION_KEY');
```

不要记录、返回或放入 DI 容器。不要在 `src/stratix.config.ts` 中再用它解密配置。

### 读取业务配置

业务配置只在配置函数参数中读取并映射给插件：

```ts
export default function createStratixConfig(
  sensitiveConfig: SensitiveConfig = {}
): StratixConfig {
  const databaseConfig = sensitiveConfig.database || {};
  // 映射到 plugins[].options
}
```

Controller、Service 和 Repository 不会自动获得 `sensitiveConfig`。如果某项运行时业务配置确实需要注入组件，先在组合入口形成最小 provider；不要让每个类读取 `process.env`。

## 项目与模块配置

### `.stratix/project.json`

这是 Forge 管理的项目 manifest，记录：

- `kind`、`type`、`runtime`
- template id/version
- package manager
- 已启用 presets
- template snapshot 和 policies

`stratix generate`、`add preset`、`doctor`、`build-manifest` 会读取它。业务运行时不要依赖这个文件；它不是应用配置服务。

### `module.yaml`

`stratix generate module billing` 生成：

```yaml
name: billing
title: Billing
root: src/modules/billing
owner: platform-team
tags:
  - Billing
layers:
  controllers: controllers/**/*.ts
  services: services/**/*.ts
  repositories: repositories/**/*.ts
  schemas: schemas/**/*.ts
  tests: tests/**/*.ts
contracts:
  openapiTag: Billing
boundaries:
  owns:
    - billingController
    - billingService
    - billingRepository
  allows:
    imports:
      - core
```

它是 Forge、doctor、graph、testing 读取的工程治理 manifest，不是运行时配置入口，也不会创建模块级 DI 容器。
生成后把默认的 `owner: platform-team` 改成真实责任团队。

诊断：

```bash
stratix doctor modules
stratix graph modules --format mermaid
```

测试中读取生成模块配置：

```ts
import { createModuleFixture } from '@stratix/testing';

const fixture = await createModuleFixture({
  rootDir: process.cwd(),
  module: 'billing'
});

expect(fixture.manifest.name).toBe('billing');
expect(fixture.manifest.layers.repositories).toBe(
  'repositories/**/*.ts'
);
expect(fixture.owns('billingService')).toBe(true);
```

`fixture.manifest` 是 `module.yaml` 的结构化结果。生产业务代码不应调用它。

`createModuleFixture()` 负责读取 fixture，不等于完整验证 manifest。root、必需 layer、token ownership 和跨模块边界仍由 `stratix doctor modules` 检查。

## 三层与业务域

简单项目只有少量资源时，保留生成器默认根级目录：

```text
src/
  controllers/
  services/
  repositories/
    interfaces/
```

当同一业务域文件增多或协作边界明显时，生成模块并把三层一起收拢：

```text
src/
  modules/
    user/
      module.yaml
      index.ts
      controllers/
        UserController.ts
      services/
        UserService.ts
      repositories/
        UserRepository.ts
        interfaces/
          IUserRepository.ts
      tests/
```

职责固定：

```text
HTTP -> Controller -> Service -> Repository -> BaseRepository -> Kysely -> SQL
```

- Controller：Fastify 请求类型、schema、状态码和响应。
- Service：用例编排、业务校验、跨 repository/service 协作。
- Repository：持久化契约、`Either`/`Maybe` 解包、Kysely 查询和事务。
- Domain：只有出现真实业务不变量时才增加无装饰器的纯函数/类型；由 Service 调用，不依赖 Fastify、Stratix 装饰器或 Kysely。

模块只是业务域目录和治理边界，不改变上述调用方向。

## API 到 Kysely 完整示例

下面实现一个 `GET /users`：只返回 active 用户，并按创建时间倒序。

### 1. Repository 契约

`src/modules/user/repositories/interfaces/IUserRepository.ts`

```ts
export interface IUserRecord {
  id: string;
  email: string;
  name: string;
  status: 'active' | 'disabled';
  created_at: string;
}

export interface IUserRepository {
  findActive(): Promise<IUserRecord[]>;
}
```

### 2. Repository 与 Kysely

`src/modules/user/repositories/UserRepository.ts`

```ts
import { Repository, type Logger } from '@stratix/core';
import { isLeft } from '@stratix/core/functional';
import {
  BaseRepository,
  type DatabaseConnectionProvider
} from '@stratix/database';
import type {
  IUserRecord,
  IUserRepository
} from './interfaces/IUserRepository.js';

interface AppDatabase {
  users: IUserRecord;
}

@Repository()
export default class UserRepository
  extends BaseRepository<AppDatabase, 'users'>
  implements IUserRepository
{
  protected readonly tableName = 'users' as const;
  protected readonly logger: Logger;

  constructor(database: DatabaseConnectionProvider, logger: Logger) {
    super({ database });
    this.logger = logger;
  }

  async findActive(): Promise<IUserRecord[]> {
    const result = await this.query(async (db) => {
      return await db
        .selectFrom(this.tableName)
        .select(['id', 'email', 'name', 'status', 'created_at'])
        .where('status', '=', 'active')
        .orderBy('created_at', 'desc')
        .execute();
    });

    if (isLeft(result)) {
      throw result.left;
    }

    return result.right;
  }
}
```

关键点：

- 构造参数名 `database` 与当前 Forge `business-repository` 模板一致。
- `super({ database })` 把数据库连接 provider 交给 `BaseRepository`。
- `this.query(async (db)` 中的 `db` 是 `Kysely<AppDatabase>`。
- `query()` 返回 `Either<DatabaseError, R>`；Repository 解包后才把普通数据交给 Service。
- 写操作使用 `command()` 或 `BaseRepository` 的 `create/update/delete`；多步一致性使用 `tx()`。

### 3. Service

`src/modules/user/services/UserService.ts`

```ts
import { Service, type Logger } from '@stratix/core';
import type UserRepository from '../repositories/UserRepository.js';
import type { IUserRecord } from '../repositories/interfaces/IUserRepository.js';

@Service()
export default class UserService {
  constructor(
    private readonly logger: Logger,
    private readonly userRepository: UserRepository
  ) {}

  async listActive(): Promise<IUserRecord[]> {
    this.logger.debug('Listing active users.');
    return await this.userRepository.findActive();
  }
}
```

Service 只表达用例，不导入 `@stratix/database`，也不接收 Kysely。

### 4. Controller

`src/modules/user/controllers/UserController.ts`

```ts
import {
  Controller,
  Get,
  type FastifyReply,
  type FastifyRequest
} from '@stratix/core';
import type UserService from '../services/UserService.js';

@Controller()
export default class UserController {
  constructor(private readonly userService: UserService) {}

  @Get('/users', {
    config: {
      operationId: 'UserController_list'
    },
    schema: {
      response: {
        200: {
          type: 'object',
          required: ['success', 'data'],
          properties: {
            success: { type: 'boolean' },
            data: {
              type: 'array',
              items: {
                type: 'object',
                required: ['id', 'email', 'name', 'status', 'created_at'],
                properties: {
                  id: { type: 'string' },
                  email: { type: 'string' },
                  name: { type: 'string' },
                  status: { type: 'string', enum: ['active'] },
                  created_at: { type: 'string' }
                }
              }
            }
          }
        }
      }
    }
  })
  async list(
    _request: FastifyRequest,
    reply: FastifyReply
  ): Promise<void> {
    reply.status(200).send({
      success: true,
      data: await this.userService.listActive()
    });
  }
}
```

`operationId` 放在 route `config` 中，响应结构放在 `schema.response` 中。

### 5. SQL 落点

Kysely 最终生成语义等价 SQL：

```sql
SELECT id, email, name, status, created_at
FROM users
WHERE status = 'active'
ORDER BY created_at DESC;
```

真实表和索引必须由迁移或数据库管理流程创建；`BaseRepository.tableSchema` 不是迁移系统。

## 实现顺序

1. `create-stratix app api <name>` 建最小项目。
2. 需要落库时 `stratix add preset database`。
3. 少量资源用 `stratix generate resource user`；需要业务域边界时用 `stratix generate module user`。生成器按输入名生成目录和类名，使用复数输入会得到复数类名。
4. 先定义 Repository 契约和表类型。
5. 实现 Repository/Kysely 并在 Repository 内解包错误。
6. 实现 Service 用例。
7. 实现 Controller schema、operationId、状态码和响应。
8. 运行目标测试、`stratix doctor`、`stratix doctor modules`（有模块时）、build 和接口验证。
