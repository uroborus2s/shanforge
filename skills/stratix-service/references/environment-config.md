# Stratix 环境与敏感配置

## 配置链路

```text
sensitive.json
  -> Forge 使用 STRATIX_ENCRYPTION_KEY 加密
  -> STRATIX_SENSITIVE_CONFIG
  -> Core 使用同一 key 解密
  -> src/stratix.config.ts(sensitiveConfig)
  -> plugins[].options
```

业务配置不从 `DB_HOST`、`REDIS_HOST`、`PORT` 等普通环境变量回退。

## 进程级环境变量

普通 `.env` 只保留启动所需进程变量：

```dotenv
NODE_ENV=development
STRATIX_ENCRYPTION_KEY=<32-byte-key>
```

生产环境由部署平台同时注入：

```dotenv
NODE_ENV=production
STRATIX_ENCRYPTION_KEY=<32-byte-key>
STRATIX_SENSITIVE_CONFIG=<ciphertext>
```

Core 支持三种 AES-256 key 表示：

- 恰好 32 bytes 的原始文本。
- 64 位 hex，解码后 32 bytes。
- 标准 base64，解码后 32 bytes。

其他长度直接失败。生产环境不允许 Core 回退到内置开发 key。

## 项目中读取 key 与测试模式

业务代码通常不读取 key；Forge/Core 已负责加解密。自定义启动器或专用配置工具确实需要时：

```ts
import {
  isTest,
  required
} from '@stratix/core/environment';

const encryptionKey = required('STRATIX_ENCRYPTION_KEY');
const testMode = isTest();
```

- `required('STRATIX_ENCRYPTION_KEY')` 缺值时抛错。
- `isTest()` 判断 `NODE_ENV === 'test'`。
- 不记录、返回或注册 `encryptionKey`。
- 不在业务类里自行解密 `STRATIX_SENSITIVE_CONFIG`。

## 敏感配置 JSON

结构与 `src/stratix.config.ts` 的读取路径保持一致：

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 3000
  },
  "database": {
    "host": "127.0.0.1",
    "port": 3306,
    "database": "app",
    "username": "app",
    "password": "secret"
  }
}
```

## Forge 命令

Forge 配置 CLI 只从进程环境读取 key，不接受 `--key`。不要通过命令行参数传密钥。

```bash
pnpm exec stratix config validate sensitive.local.json --required server,database --strict
export STRATIX_ENCRYPTION_KEY="$(pnpm exec stratix config generate-key --length 32 --format base64)"
pnpm exec stratix config encrypt sensitive.local.json --output .env.sensitive
```

解密验证：

```bash
set -a
. ./.env.sensitive
set +a
pnpm exec stratix config decrypt "$STRATIX_SENSITIVE_CONFIG" --output tmp/decrypted.json
```

加密、CLI 解密和 Core 运行时必须使用同一个 `STRATIX_ENCRYPTION_KEY`。

## `.env.sensitive` 启动边界

Core 启动时先检查进程环境中的 `STRATIX_SENSITIVE_CONFIG`：

- 已存在：立即解密并把对象传给配置函数。
- 不存在：加载 dotenv 文件，返回空 `sensitiveConfig`；同一次启动不会再回头解密刚从 dotenv 读到的密文。

因此启动前必须预加载：

```bash
set -a
. ./.env.sensitive
set +a
pnpm exec stratix start --type web --config ./src/stratix.config.ts
```

生产环境优先让 CI、systemd、Docker 或 Kubernetes 直接注入两个变量，不提交明文 JSON、key 或解密结果。
