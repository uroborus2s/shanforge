# Stratix 1.1.x 推荐脚手架

当前参考以本仓库真实版本为准：

- `@stratix/cli@1.1.0`
- `@stratix/core@1.1.0`
- `@stratix/database@1.1.0`

CLI 优先，不手工起项目骨架。典型起手顺序：

```bash
stratix init app api demo-api --no-install
stratix add preset database --no-install
stratix generate resource user
stratix generate business-repository workflow-execution
stratix doctor
```

## 应用项目

```text
.stratix/
  project.json
src/
  index.ts
  stratix.config.ts
  controllers/
  services/
  repositories/
  executors/
  config/
  types/
  utils/
```

### 最小入口

```ts
import { Stratix } from '@stratix/core';

await Stratix.run();
```

### 最小配置

```ts
import type { StratixConfig } from '@stratix/core';
import database from '@stratix/database';
import redis from '@stratix/redis';

export default (sensitiveConfig: Record<string, any> = {}): StratixConfig => ({
  server: {
    host: '0.0.0.0',
    port: Number(process.env.PORT || 3000)
  },
  plugins: [
    {
      name: '@stratix/database',
      plugin: database,
      options: {
        connections: {
          default: {
            type: 'mysql' as const,
            host: sensitiveConfig.DB_HOST || 'localhost',
            port: Number(sensitiveConfig.DB_PORT || 3306),
            database: sensitiveConfig.DB_NAME || 'app',
            username: sensitiveConfig.DB_USERNAME || 'root',
            password: sensitiveConfig.DB_PASSWORD || ''
          }
        }
      }
    },
    {
      name: '@stratix/redis',
      plugin: redis,
      options: {
        single: {
          host: sensitiveConfig.REDIS_HOST || 'localhost',
          port: Number(sensitiveConfig.REDIS_PORT || 6379)
        }
      }
    }
  ],
  applicationAutoDI: {
    enabled: true
  }
});
```

这里要特别注意：

- `plugins[].name` 不决定 adapter token，只是插件注册项名称。
- `database` 插件的消费侧公开模型已经切到 `BaseRepository` 优先。
- CLI `database` preset 默认使用 `DB_HOST`、`DB_PORT`、`DB_NAME`、`DB_USERNAME`、`DB_PASSWORD`。

### 控制器与服务

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
import type { Logger } from '@stratix/core';
import UserRepository from '../repositories/UserRepository.js';

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
import type { Logger } from '@stratix/core';
import { BaseRepository } from '@stratix/database';

type AppDatabase = {
  users: {
    id: string;
    name: string;
    status: string;
  };
};

export default class UserRepository extends BaseRepository<AppDatabase, 'users'> {
  protected readonly tableName = 'users' as const;
  protected readonly logger: Logger;

  constructor(logger: Logger) {
    super();
    this.logger = logger;
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

如果仓储天然跨多张表，或者要承载 claim/checkpoint/finalize 这类长流程状态迁移，优先直接使用：

```bash
stratix generate business-repository workflow-execution
```

如果不使用 `BaseRepository`，也应只在 repository 层内部保留兼容性的 `databaseApi` 注入，不要让 service 直接调用 database plugin。

## 生态插件项目

```text
.stratix/
  project.json
src/
  index.ts
  config/
    plugin-config.ts
  adapters/
    client.adapter.ts
  controllers/
  services/
  repositories/
  executors/
```

### 最小插件入口

```ts
import type { FastifyPluginAsync } from '@stratix/core';
import { withRegisterAutoDI } from '@stratix/core';

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
      'repositories/*.{ts,js}',
      'executors/*.{ts,js}'
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

### 最小适配器

```ts
import type { AwilixContainer } from '@stratix/core';

export default class ClientAdapter {
  static adapterName = 'client';

  constructor(private readonly container: AwilixContainer) {}

  getConfig() {
    return this.container.resolve('config');
  }
}
```

消费方最终看到的 token 是 `examplePluginClient`。如果你把插件函数名改掉，对外注入 token 也会一起变化。

如果插件内部接入数据库，也保持 `controller -> service -> repository` 分层，repository 优先继承 `BaseRepository`，而不是让 service 直接注入 `databaseApi`。
