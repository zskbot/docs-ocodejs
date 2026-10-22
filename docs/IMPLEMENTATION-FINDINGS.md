# Source Review Findings

Review date: 2026-10-23. Static review of selected files only; no live endpoint or production system was tested.

## Deployment console authorization — high priority to verify

File: https://github.com/Velclaw/velclaw-deploy/blob/main/app/api/deploy/route.ts

The inspected route exposes GET behavior for deployment details/logs/history and POST behavior for creating or promoting a deployment. The route file itself did not show authentication or authorization checks. Middleware or external controls may exist, so this is a potential risk, not proof of public exposure. Review middleware, ownership checks, origin/CSRF controls, rate limits, audit logs and error redaction. Verify using isolated tests only; do not call production deployment APIs.

## Documentation generator — likely scope bug

File: https://github.com/Velclaw/docs.velclaw.ai/blob/main/scripts/generate-docus-content.mjs

Static reading indicates that `locale` is declared in a `for (const locale of locales)` loop and referenced after that loop when building a home index path. Since the variable is block-scoped, this likely throws a `ReferenceError`. The final write string also appears to use literal backslash-n sequences. Move locale-specific writes inside the loop and test both locales plus repeat generation for deterministic output. The script was not executed.

## Framework metadata mismatch

File: https://github.com/Velclaw/docs.velclaw.ai/blob/main/package.json

Package metadata names Nuxt 4, Docus and Nuxt Content with `nuxt generate` and `nuxt typecheck`, while README wording describes Next.js. Confirm the canonical runtime with the repository owner before changing public instructions.

## OAuth and CI

Files: https://github.com/Velclaw/Oauth/blob/main/docs/integration.md and https://github.com/Velclaw/Oauth/blob/main/.github/workflows/ci.yml

Before production callback activation, verify DNS, HTTPS, redirect allowlists, state/CSRF protections, session configuration and end-to-end login. The workflow uses version tags for checkout/setup-node; pin reviewed full commit SHAs if repository policy requires immutable action references.

## Licensing and redistribution

- `Velclaw/docs.velclaw.ai/LICENSE` contains a rights-reservation notice. Do not copy its full content, code or assets into this public hub without written permission.
- `Velclaw/Oauth/LICENSE` is GPL-3.0; preserve applicable license and source notices for any approved redistribution.
- A root LICENSE was not found at the inspected paths for `Velclaw/velclaw-deploy` and `Velclaw/Velclaw-velclaw-docs-ui-reference`. Absence of a license is not permission to redistribute.

## Scope and evidence

No source repository was modified, and no build, automated test, or live endpoint was run as part of this static review. Treat these as source-observed findings until independently verified in a disposable non-production environment.
