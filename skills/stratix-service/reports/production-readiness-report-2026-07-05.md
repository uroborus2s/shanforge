# Stratix Service Skill Production Readiness Report

## Scope

This report evaluates whether `skills/stratix-service` can guide an agent to generate a production-ready Stratix backend application.

## Current Verdict

Status: `blocked`

The skill is now production-safe in behavior because it refuses to claim readiness when generated projects fail build/start/release checks. The current public Stratix toolchain is not yet proven to generate a production-ready API project without manual toolchain fixes.

## Versions Tested

Npm dist-tags checked on 2026-07-05:

- `@stratix/create`: `1.1.0`
- `@stratix/core`: `1.1.0`
- `@stratix/database`: `1.1.0`
- `@stratix/forge`: `1.1.2`

## Commands Tested

```bash
npx --yes @stratix/create@1.1.0 app api demo-api --preset testing --no-install
pnpm install
pnpm approve-builds --all
pnpm add -D @stratix/forge@1.1.2
pnpm exec stratix --help
pnpm exec stratix doctor
pnpm test:run
pnpm build
pnpm exec stratix build-manifest --output .stratix/production-manifest.json
pnpm exec stratix release gate --dry-run --manifest .stratix/production-manifest.json
pnpm exec stratix start --type web --config ./src/stratix.config.ts --host 127.0.0.1 --port 3107
pnpm exec stratix openapi generate --output openapi.json
pnpm exec stratix config validate sensitive.local.json --strict
pnpm exec stratix config encrypt sensitive.local.json --key "$STRATIX_ENCRYPTION_KEY" --output .env.sensitive
pnpm exec stratix config decrypt "$STRATIX_SENSITIVE_CONFIG" --key "$STRATIX_ENCRYPTION_KEY" --output tmp/decrypted.json
```

## Passing Checks

- Template listing and project generation passed.
- Default tests passed.
- `build-manifest` passed.
- Config CLI `validate -> encrypt -> decrypt` passed with a 32-byte raw `STRATIX_ENCRYPTION_KEY`.
- `openapi generate` passed through project-local `pnpm exec stratix`.

## Failed Checks

- Initial `pnpm install` failed under pnpm 11 until `pnpm approve-builds --all` approved `esbuild@0.28.1` build scripts.
- `pnpm exec stratix doctor` failed after upgrading forge to `1.1.2`: `.stratix/project.json` still expects `@stratix/forge ^1.1.0`.
- `pnpm build` failed because generated `operationId` is not accepted by `FastifySchema`.
- `release gate` failed because the generated project lacks a security/audit script required by forge.
- `stratix start` failed because forge resolves `@stratix/core` through `createRequire().resolve()`, while core exposes only an ESM import export.
- Generated `src/config/stratix.generated.ts` reads `process.env.PORT`, and `.env.example` exposes `PORT/HOST`; this does not satisfy the production requirement that application config flows through encrypted `STRATIX_SENSITIVE_CONFIG`.
- Runtime `STRATIX_SENSITIVE_CONFIG` injection could not be verified because the generated app cannot start. This keeps the readiness verdict at `blocked`.

## Skill Changes Required

Implemented:

- Prefer dynamic version discovery over fixed 1.1.x assumptions.
- Probe npm dist-tags and project installed versions before choosing commands.
- Use project-local `pnpm exec stratix`.
- Use `stratix openapi generate --output openapi.json`, not bare `stratix openapi`.
- Keep 1.1.x failures as compatibility notes, not permanent facts.
- Require sensitive app config to flow through JSON -> encrypt -> `STRATIX_SENSITIVE_CONFIG`.
- Test skill output against an official latest control project before deciding whether a failure is a skill bug or a Stratix toolchain/template bug.
- Mark readiness as `blocked` whenever runtime sensitive config injection cannot be verified.

## Production Standard

The skill should only mark a generated app as production-ready when all of these pass freshly:

- Version and command capability probe.
- Project generation.
- Sensitive config validation, encryption, injection, and decrypt or start verification.
- `stratix doctor`.
- Tests.
- TypeScript build.
- Production manifest generation.
- Release gate.
- Startup check.

Current latest toolchain does not meet that standard without upstream fixes.

## Retest After User Reported Upstream Fix

Retest directory: `/private/tmp/stratix-skill-test-PNQNO3`

Npm latest remained unchanged:

- `@stratix/create@1.1.0`
- `@stratix/core@1.1.0`
- `@stratix/database@1.1.0`
- `@stratix/forge@1.1.2`

Generated projects installed `@stratix/core@1.1.0` and `@stratix/forge@1.1.0`.

Retest results:

- `create-stratix --help`, `list templates`, and `list presets` passed.
- Official control project and skill-guided project were both created.
- Initial `pnpm install` still failed under pnpm 11 until `pnpm approve-builds --all` approved `esbuild@0.28.1`.
- `pnpm exec stratix doctor` passed in both projects.
- `pnpm test:run` passed in both projects.
- Official control `pnpm build` still failed on `operationId` / `FastifySchema`.
- Skill-guided project passed config `validate -> encrypt -> decrypt`; after the minimal route schema fix, it passed `pnpm build`.
- `pnpm exec stratix openapi generate --output openapi.json` passed in both projects.
- `pnpm exec stratix start --help` failed with `Cannot resolve @stratix/core from the current project`, so runtime `STRATIX_SENSITIVE_CONFIG` injection remains unverified.

Code review follow-up fixed stale guidance in linked references:

- `runtime-realities.md` no longer says ordinary `.env` is suitable for application config.
- `ecosystem-map.md` now describes plugin configuration as `sensitiveConfig` paths instead of env keys.
- `cli-workflow.md` now says to map plugin options from `sensitiveConfig`.

Retest verdict remains `blocked`: the skill can guide safer generation and local correction, but current public packages still do not prove a complete production-ready generated backend because startup and runtime sensitive config injection are not verified.
