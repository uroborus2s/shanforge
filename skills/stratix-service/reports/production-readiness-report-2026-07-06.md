# Stratix Service Skill Production Retest

## Verdict

Status: `blocked`

Current latest packages fixed the previous build, release gate, security script, and sensitive config template issues. The skill still must not claim production readiness because startup fails and latest-version doctor metadata is inconsistent.

## Versions

- `@stratix/create@1.1.1`
- `@stratix/core@1.1.1`
- `@stratix/database@1.1.0`
- `@stratix/forge@1.1.3`

## Passing Checks

- `create-stratix --help`, `list templates`, and `list presets`
- `pnpm install`
- `pnpm test:run`
- `pnpm build`
- `build-manifest`
- `release gate`
- `openapi generate`
- generated config reads `sensitiveConfig.server`
- `.env.example` does not expose `PORT/HOST`
- config `validate -> encrypt -> decrypt`
- runtime logs detect `STRATIX_SENSITIVE_CONFIG`

## Failed Checks

- Default install still resolves `@stratix/core@1.1.0` and `@stratix/forge@1.1.2`; `stratix start` fails with `Cannot resolve @stratix/core from the current project`.
- After explicit latest upgrade, `doctor` fails because `.stratix/project.json` still expects `@stratix/core ^1.1.0`.
- `stratix start --config ./src/stratix.config.ts` fails because `src/stratix.config.ts` imports `./config/stratix.generated.js`, while the source file is `stratix.generated.ts`.
- `stratix start --config ./dist/stratix.config.js` still fails when discovery scans `src/stratix.config.ts` and hits the same missing `stratix.generated.js`.

## Conclusion

The skill's process is correct: probe live versions, use the smallest preset, require encrypted config, and block on failed startup. Current upstream still needs a template/discovery fix before the generated service can be called production-ready.
