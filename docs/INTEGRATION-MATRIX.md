# Integration Matrix and Operational Contracts

**Purpose:** capture cross-repository integration contracts from the source documents reviewed so far. This is a source-level plan, not a live health report.

## Integration map

| Producer | Consumer / target | Contract evidenced in source | Verification required |
|---|---|---|---|
| VelCli | AI model providers | Model-router/provider adapters and bounded agent runtime are described in VelCli audit/roadmap. | Exercise provider success, malformed output, retries exhausted, cancellation and redacted errors in tests. |
| VelCli | Workspace filesystem / commands | Workspace root, path resolution and command allowlist exist; they are explicitly not a full sandbox. | Test traversal, symlink escape, timeout, output caps, approval rejection; never execute untrusted code in the API process. |
| VelCli | PostgreSQL / filesystem fallback | PostgreSQL structured records are used when `DATABASE_URL` is configured; filesystem fallback also exists. | Verify actual deployment, backup/restore, restart persistence and ownership checks in isolated test data. Do not switch or delete a database until a restore is verified. |
| VelCli | GitHub / CI | Product roadmap proposes user-approved branch/commit/PR flows. | Least-privilege permissions; inspect diff; no automatic merge or production deploy without explicit approval. |
| VelCli | VelclawHost | Repositories describe an intended hosting integration boundary. | Confirm authenticated API contract, authorization, deployment lifecycle and live service status before calling it operational. |
| X-BO | AI providers | Frontend calls `/api/chat`; backend selects provider by model and uses provider adapters. | Validate model allowlist, bounded request input, timeout, provider errors and secret redaction. |
| velclaw-deploy | Vercel API | Next.js App Router console uses a server-side Vercel REST API integration; `VERCEL_TOKEN` is server-only. | Verify permissions/scopes and preview-only workflow first; never expose token via `NEXT_PUBLIC_`. |
| Velclaw/Oauth | Velclaw workspace / identity provider | `/api/oauth/authorize`, `/oauth/callback`; `return_to` must be allowlisted; provider credentials server-side only. | DNS, HTTPS certificate, live response, exact callback URL and end-to-end login must pass before registering a production callback. |
| TechDocs | Gemini / Supabase pgvector | MDX content, Gemini-backed assistant and embeddings; `GEMINI_API_KEY` and `SUPABASE_SERVICE_ROLE_KEY` server-only. | Run content tests, type-check, lint and build; check schema/vector extension; never expose service-role key to client. |
| VELCLAW Control Center | GitHub / Render / Vercel / Cloudflare / databases | Registry-oriented architecture aims to map repos, deployments, domains, databases, integrations and audit events. | Treat registry claims as declarations until live metadata and health checks are linked to each service. |
| Docs UI Reference | TechDocs | UI spec defines dark/near-black surfaces, purple accent, square corners, compact header, mobile drawer, reader-first layout and code-copy affordance. | Compare actual app implementation to spec and verify keyboard/focus/responsive behavior. |

## Configuration boundaries

### Server-only credentials
- `VERCEL_TOKEN` and optional `VERCEL_TEAM_ID`: deployment console server-side only.
- `GEMINI_API_KEY`, `SUPABASE_SERVICE_ROLE_KEY`: TechDocs server-side only; never prefix these secrets with `NEXT_PUBLIC_`.
- `GITHUB_CLIENT_SECRET`, `SESSION_SECRET`: OAuth service-side only.
- `OHMABA_API_KEY`, `GEMINI_API_KEY`, `HF_TOKEN`: X-BO deployment guide lists these as variable names; values must remain in platform secret settings.
- `DATABASE_URL`: treat as sensitive; do not print, copy to docs, or change targets without verified backup/restore.

Variable names above are taken from repository docs. No values are included here.

## Cross-project release gates

1. **Identity:** verify domain, TLS, callback URL, redirect allowlist, session policy and end-to-end login.
2. **Data:** prove backup exists, restore into an isolated target, compare counts and representative records, then verify restart persistence. Do not use production as a test fixture.
3. **Agent execution:** keep plan-only mode read-only; maintain approvals for mutations; treat allowlists as guardrails, not sandbox isolation.
4. **Deployments:** require explicit user approval for production promotion and PR merge; keep Vercel tokens server-side.
5. **Observability:** each service should expose a documented health endpoint and have a verifiable deploy/commit mapping.
6. **Documentation UI:** use the Docs UI Reference as design guidance while preserving each product's distinct brand and content.
7. **Evidence:** store source URL, branch, commit SHA, command/test result and timestamp for each verified claim.

## Status definitions

- **Documented:** stated in source documentation.
- **Source-observed:** code or configuration was inspected, but runtime behavior was not exercised.
- **Runtime-verified:** endpoint or workflow was actually tested and the evidence recorded.
- **Production-ready:** all applicable security, persistence, rollback, CI and operational gates have passed.

## Newly confirmed documentation conflicts

### Canonical domain is unresolved

- [Velclaw/VELCLAW `docs/ECOSYSTEM.md`](https://github.com/Velclaw/VELCLAW/blob/main/docs/ECOSYSTEM.md) names `https://velclaw.dev` as the canonical product domain and says DNS/OAuth/production paths still require live verification.
- [VelclawHost README](https://github.com/Velclaw/VelclawHost/blob/main/README.md) instead describes `velclaw.site` as the primary platform namespace, with `api.velclaw.site` and `app.velclaw.site` as service surfaces.
- These are conflicting **documentation declarations**, not proof of current DNS or deployment state. Do not rewrite DNS, OAuth callbacks, redirects, or production URLs based on either document alone. Resolve ownership and canonical-domain decisions, then verify DNS records, TLS, live endpoints, and service-to-domain mapping.

### Documentation UI contract

The [Docs UI Reference](https://github.com/Velclaw/Velclaw-velclaw-docs-ui-reference) explicitly defines square corners (`border-radius: 0`), dark/purple styling, compact header, keyboard-visible focus states, a mobile sidebar drawer, desktop three-column reader layout, and copyable code blocks. Treat it as the UI specification for TechDocs, not as evidence that every item is already implemented.

### Evidence level

The above are source-document observations. No live DNS, OAuth callback, hosting deployment, database restore, or frontend accessibility test was performed during this pass.

Do not promote a row to Runtime-verified or Production-ready based only on README text, a planned integration, or a green unrelated workflow.