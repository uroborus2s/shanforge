# Stratix 生成入口

本页只记录脚手架入口。配置、三层、模块和 Kysely 的完整实现见 [application development](application-development.md)。

## 项目

```bash
create-stratix app api demo-api --preset testing --no-install
create-stratix app worker demo-worker --preset redis,queue,testing --no-install
create-stratix plugin data @demo/data-plugin --no-install
```

生成后：

```bash
cd demo-api
pnpm install
pnpm exec stratix doctor
pnpm build
pnpm test
```

## 业务资源

少量简单资源：

```bash
pnpm exec stratix generate resource user
```

按业务域收拢：

```bash
pnpm exec stratix generate module billing
pnpm exec stratix doctor modules
```

多表一致性或耐久化状态：

```bash
pnpm exec stratix add preset database
pnpm exec stratix generate business-repository workflow-execution
```

不要把生成文件当成最终业务实现。module 的 Repository 仍是返回空数组的占位文件，即使项目已有 database preset，也要按真实表、输入契约和用例补 Repository/Kysely、Service、Controller 与测试。
