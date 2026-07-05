# Stratix Environment And Sensitive Config

## 普通开发环境

所有应用配置先写入 JSON，再加密成 `STRATIX_SENSITIVE_CONFIG`。普通 `.env` 不承载应用配置，只保留进程级变量：

```dotenv
NODE_ENV=development
STRATIX_ENCRYPTION_KEY=12345678901234567890123456789012
```

`loadEnvironment()` 在没有进程级 `STRATIX_SENSITIVE_CONFIG` 时按顺序加载：

1. `.env`
2. `.env.<NODE_ENV>`
3. `.env.<NODE_ENV>.local`
4. `.env.local`

后加载覆盖先加载。生产环境排除 `.local` 文件。

## 生产环境

生产环境推荐由部署平台注入：

```bash
NODE_ENV=production
STRATIX_ENCRYPTION_KEY="12345678901234567890123456789012"
STRATIX_SENSITIVE_CONFIG="iv.authTag.encrypted"
```

生产环境不要依赖默认加密 key，也不要依赖 `.env.local`。不要把明文应用配置提交进仓库。

## 敏感配置 JSON

建议把敏感配置组织成与 `src/stratix.config.ts` 中读取路径一致的对象：

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
    "username": "root",
    "password": "secret"
  },
  "redis": {
    "host": "127.0.0.1",
    "port": 6379,
    "password": "",
    "db": 0
  }
}
```

先校验：

```bash
stratix config validate sensitive.local.json --required database --strict
```

## 默认 key 加密与解密

仅限本地临时开发：

```bash
stratix config encrypt sensitive.local.json --output .env.sensitive
stratix config decrypt "$STRATIX_SENSITIVE_CONFIG" --output tmp/decrypted.json
```

缺省时，forge 配置工具会先读取环境变量 `STRATIX_ENCRYPTION_KEY`；如果没有，会回退到内置开发 key。core 运行时在非生产环境也允许默认 key，因此这种方式只适合本地临时验证。

## 显式 key 加密与解密

当前最稳妥的跨 forge/core 用法是使用 32 字节原始字符串：

```bash
export STRATIX_ENCRYPTION_KEY="12345678901234567890123456789012"
stratix config encrypt sensitive.prod.json --key "$STRATIX_ENCRYPTION_KEY" --output .env.sensitive
stratix config decrypt "$STRATIX_SENSITIVE_CONFIG" --key "$STRATIX_ENCRYPTION_KEY" --output tmp/decrypted.json
```

加密和运行时解密必须使用同一把 key。不要在生产环境使用默认 key。

`stratix config generate-key --length 32 --format hex|base64` 可以生成随机材料，但当前 core 运行时直接把 key 字符串作为字节使用；若使用 hex/base64 字符串，先做一次真实启动或解密验证，确认 forge 和 core 的 key 处理兼容。保守做法仍是使用 32 字节原始字符串。

## 用 .env 文件承载 STRATIX_SENSITIVE_CONFIG

`stratix config encrypt ... --output .env.sensitive` 默认写出：

```dotenv
STRATIX_SENSITIVE_CONFIG="..."
```

注意当前 `loadEnvironment()` 会先检查进程环境中的 `STRATIX_SENSITIVE_CONFIG`，找不到才加载 dotenv 文件；它不会在同一次调用中从 `.env.sensitive` 读出变量后再回头解密。

因此如果使用 `.env.sensitive`，需要在启动前预加载：

```bash
set -a
. ./.env.sensitive
set +a
STRATIX_ENCRYPTION_KEY="12345678901234567890123456789012" stratix start --type web --config ./src/stratix.config.ts
```

或让 CI、systemd、Docker、Kubernetes 直接注入 `STRATIX_SENSITIVE_CONFIG` 和 `STRATIX_ENCRYPTION_KEY`。
