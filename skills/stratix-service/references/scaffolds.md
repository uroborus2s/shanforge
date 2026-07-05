# Stratix Service Scaffolds

## 创建项目

API 项目：

```bash
create-stratix app api demo-api --preset database,testing --no-install
cd demo-api
pnpm install
stratix doctor
```

Worker 项目：

```bash
create-stratix app worker demo-worker --preset redis,queue,testing --no-install
```

Data 插件：

```bash
create-stratix plugin data @demo/data-plugin --no-install
```

## 应用目录

```text
.stratix/
  project.json
src/
  index.ts
  stratix.config.ts
  config/
  controllers/
  services/
  repositories/
  repositories/interfaces/
  components/
  types/
```

`app api` 默认会生成健康检查 controller/service 和 testing preset。后续业务资源优先用：

```bash
stratix generate resource user
```

## 最小入口

```ts
import { Stratix } from '@stratix/core';

await Stratix.run();
```

## 最小配置

```ts
import type { StratixConfig } from '@stratix/core';
import database from '@stratix/database';
import redis from '@stratix/redis';

const required = <T>(value: T | undefined, name: string): T => {
  if (value === undefined || value === null || value === '') {
    throw new Error(`Missing sensitive config: ${name}`);
  }
  return value;
};

export default (sensitiveConfig: Record<string, any> = {}): StratixConfig => {
  const appConfig = sensitiveConfig.app || {};
  const serverConfig = sensitiveConfig.server || {};
  const databaseConfig = sensitiveConfig.database || {};
  const redisConfig = sensitiveConfig.redis || {};

  return {
    server: {
      host: required(serverConfig.host, 'server.host'),
      port: Number(required(serverConfig.port, 'server.port'))
    },
    plugins: [
      {
        name: '@stratix/database',
        plugin: database,
        options: {
          connections: {
            default: {
              type: appConfig.databaseType || 'mysql',
              host: required(databaseConfig.host, 'database.host'),
              port: Number(required(databaseConfig.port, 'database.port')),
              database: required(databaseConfig.database, 'database.database'),
              username: required(databaseConfig.username, 'database.username'),
              password: required(databaseConfig.password, 'database.password')
            }
          }
        }
      },
      {
        name: '@stratix/redis',
        plugin: redis,
        options: {
          single: {
            host: required(redisConfig.host, 'redis.host'),
            port: Number(required(redisConfig.port, 'redis.port')),
            password: redisConfig.password || undefined,
            db: Number(redisConfig.db || 0)
          }
        }
      }
    ],
    applicationAutoDI: {
      enabled: true
    }
  };
};
```

## Controller / Service / Repository

```ts
import { Controller, Get, type FastifyReply, type FastifyRequest } from '@stratix/core';
import UserService from '../services/UserService.js';

@Controller()
export default class UserController {
  constructor(private readonly userService: UserService) {}

  @Get('/api/users')
  async list(_request: FastifyRequest, reply: FastifyReply) {
    const users = await this.userService.list();
    return reply.send({ data: users });
  }
}
```

```ts
import { Service, type Logger } from '@stratix/core';
import UserRepository from '../repositories/UserRepository.js';

@Service()
export default class UserService {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly logger: Logger
  ) {}

  async list() {
    this.logger.info('Listing users');
    return this.userRepository.findAllActive();
  }
}
```

```ts
import { Repository, type Logger } from '@stratix/core';
import { BaseRepository } from '@stratix/database';

type AppDatabase = {
  users: {
    id: string;
    name: string;
    status: string;
  };
};

@Repository()
export default class UserRepository extends BaseRepository<AppDatabase, 'users'> {
  protected readonly tableName = 'users' as const;

  constructor(private readonly logger: Logger) {
    super();
  }

  async findAllActive() {
    return await this.query(async (db) => {
      return await db
        .selectFrom(this.tableName)
        .selectAll()
        .where('status', '=', 'active')
        .execute();
    });
  }
}
```

Service 层不要直接注入 `databaseApi`。多表业务单元优先使用：

```bash
stratix generate business-repository workflow-execution
```

## 插件目录

```text
.stratix/
  plugin.json
src/
  index.ts
  config/
  adapters/
  controllers/
  services/
  repositories/
  components/
  types/
```

插件入口保持具名函数：

```ts
import type { FastifyPluginAsync } from '@stratix/core';
import { withRegisterAutoDI } from '@stratix/core/plugin';

export interface ExamplePluginOptions {
  endpoint: string;
  timeout?: number;
}

const examplePlugin: FastifyPluginAsync<ExamplePluginOptions> = async () => {};

export default withRegisterAutoDI(examplePlugin, {
  discovery: {
    patterns: [
      'controllers/*.{ts,js}',
      'services/*.{ts,js}',
      'repositories/*.{ts,js}'
    ]
  },
  services: {
    enabled: true,
    patterns: ['adapters/*.{ts,js}']
  },
  parameterProcessor: (options) => ({
    timeout: 30000,
    ...options
  }),
  parameterValidator: (options) => {
    return Boolean(options && typeof options === 'object' && 'endpoint' in options);
  },
  lifecycle: {
    enabled: true
  }
});
```

如果 adapter 名为 `ClientAdapter` 且 `adapterName = 'client'`，消费方 token 形如 `examplePluginClient`。插件函数名变化会改变 token。
