# Source Review Findings

Review date: 2026-10-23. This is a static review of selected files, not a live-service test. No source repository was modified.

## Deployment console — authorization review required

File: [app/api/deploy/route.ts](https://github.com/Velclaw/velclaw-deploy/blob/main/app/api/deploy/route.ts), blob `1efa73bff1930b1d864455e939417c5a82f29bfc`.

The visible GET handler returns deployment details, logs and history. The POST handler can create a deployment or promote one. This route file does not show an authentication or authorization check. Other external controls may exist, so verify the full app and live configuration before concluding the endpoint is exposed.

Before production use, verify authenticated access, project/deployment ownership, origin/CSRF protections, rate limiting, audit logging and error redaction. Test unauthorized requests in an isolated environment. No Vercel API calls or deployments were made.

## Documentation generator — likely JavaScript scope bug

File: [scripts/generate-docus-content.mjs](https://github.com/Velclaw/docs.velclaw.ai/blob/main/scripts/generate-docus-content.mjs), blob `f8337881df0c260b196f26870f6c24c1fa26faa6`.

The script declares `locale` in `for (const locale of locales)`, then references `locale` after the loop when constructing `homeIndexPath`. Since `locale` is block-scoped, the final reference should throw `ReferenceError` after the locale loop. The final write string also appears to contain literal backslash-n sequences. Fix by moving the home-index update inside the loop and using actual newline escapes; test both locales and repeat generation to verify stable output. This finding is from static reading; the script was not run.

## Documentation architecture mismatch

File: [package.json](https://github.com/Velclaw/docs.velclaw.ai/blob/main/package.json), blob `56928f175d6d7f67e1bf507c3e3e6aa1d911da0d`.

The README describes Next.js, while the package manifest uses Nuxt 4/Docus and scripts such as `nuxt generate` and `nuxt typecheck`. Confirm the canonical runtime before updating the public docs.

## OAuth deployment and CI

Files: [integration guide](https://github.com/Velclaw/Oauth/blob/main/docs/integration.md) and [CI workflow](https://github.com/Velclaw/Oauth/blob/main/.github/workflows/ci.yml).

The guide explicitly requires DNS, HTTPS, a verified live response, an allowlisted redirect origin and end-to-end login tests before setting a production callback. CI currently uses `actions/checkout@v4` and `actions/setup-node@v4` tags; pin to reviewed full commit SHAs if repository policy requires it.

## License and redistribution

- [Velclaw/docs.velclaw.ai/LICENSE](https://github.com/Velclaw/docs.velclaw.ai/blob/main/LICENSE) reserves all rights. Do not copy its full docs, code or assets into the public hub without written permission.
- [Velclaw/Oauth/LICENSE](https://github.com/Velclaw/Oauth/blob/main/LICENSE) is GPL-3.0; preserve required license notices for any approved redistribution.
- A root LICENSE file was not found at the inspected path for `Velclaw/velclaw-deploy` or `Velclaw/Velclaw-velclaw-docs-ui-reference`. Missing license does not grant permission to redistribute.

## Scope

Selected source files and metadata were read. No builds/tests or live endpoints were run. Keep findings marked as source-level until verified in an isolated test environment.
