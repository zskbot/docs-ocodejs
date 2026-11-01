# OCode.js Infrastructure Operations

**Last reviewed:** 2026-11-01  
**Default mode:** free/staging/Preview; branch and PR only.

## Service ownership

| Service | Source of truth | Runtime owner | Current operational note |
|---|---|---|---|
| Documentation site | `zskbot/docs-ocodejs` | GitHub Pages workflow | Public URL `https://zskbot.github.io/docs-ocodejs/`; run #122 on `084a61ebb3f3c3e667c4f589f4e82ec7a62d238f` deployed Pages and passed all static HTTP checks; the combined job later failed only in the MCP step, now isolated |
| Documentation MCP | `cloudflare/ocodejs-docs-mcp` | Cloudflare Worker | Cloudflare API confirms deployment `09409259-93c1-43e4-a8f7-0e1f2a9c209c` at 100% traffic; GitHub Actions PR #51 received HTTP 403 on `/health`; account-level `All Workers` Access policy is a likely blocker |
| Chatbot | `OCodejs/chatbot` | Separate Vercel project | Vercel project listing for `OCodejs/chatbot` returned no connected project; earlier create attempt returned HTTP 403; no public URL is configured |

## Pre-change checklist

- [ ] Read current `main` SHA and branch list.
- [ ] Check open PRs and recent Actions runs.
- [ ] Identify the service and owning repository before editing.
- [ ] Confirm the change is free-tier/staging compatible.
- [ ] Create a branch; never commit directly to `main`.
- [ ] Avoid secrets, populated environment files and production data.
- [ ] Keep application, infrastructure and design changes in separate PRs.

## CI failure triage

1. Identify the exact workflow run, commit SHA, failed job and failed step.
2. Read the job log before changing workflow configuration.
3. Classify the failure:
   - product regression;
   - validator defect;
   - missing repository configuration;
   - unrelated template workflow;
   - external provider or permission blocker.
4. Fix the narrowest cause and add a regression check where practical.
5. Re-run the affected workflow and inspect all required checks on the PR head SHA.
6. Do not claim success based on a different commit or an unrelated green workflow.

### Latest verified baseline (2026-11-01)

- Main commit deployed by Pages workflow run #122: `084a61ebb3f3c3e667c4f589f4e82ec7a62d238f`.
- GitHub Pages deployment and static post-deploy checks PASS: `/`, `/infra/`, and `/ecosystem/services.json` returned successful HTTP responses; registry JSON parsed with a `services` array. Published URL: `https://zskbot.github.io/docs-ocodejs/`.
- The combined workflow run #122 was marked failed only because the separate MCP endpoint check returned HTTP 403. The Pages deploy and static checks themselves passed.
- Maintained workflows now use Node.js 24-compatible action releases. The legacy Jekyll validation was changed to manual-only after it failed on an imported API reference document containing unsupported Liquid `{% data %}` syntax; it is not the Pages deployment pipeline.

### Access-policy blocker found (2026-11-01)

- PR #51's read-only MCP smoke test received HTTP 403 from `https://ocodejs-docs-mcp.velclaw.workers.dev/health`.
- Read-only Cloudflare inventory shows an account-level Access application named `All Workers` with an allow condition requiring client certificate common name `Velclaw.ai`. This is a likely cause of the unauthenticated GitHub Actions request being denied; confirm via request logs before changing policy.
- Do not disable the account-wide policy. If the MCP endpoint is intentionally public and read-only, use a Worker-level bypass scoped only to `ocodejs-docs-mcp`, with explicit approval. Otherwise, use a dedicated Access service token for the CI smoke-test client.

### Historical baseline findings (2026-11-01)

- Earlier main commit at the start of the infrastructure review: `32d914c2c4255a3cdd85dff9966134bb3a8dbfe4`.
- PR #48 head SHA `1b9effd186d0ee950cafee8da6161a038b1f1a0b`: core `CI`, documentation validation, ecosystem inventory validation, service inventory validation, infrastructure validation and Socket Security checks all PASS.
- `Crystal CI`: FAIL because the workflow runs `shards install` but this repository has no `shard.yml`. The repository is a static documentation hub with Python validation scripts, not a Crystal application. Keep the sample Crystal workflow manually invokable only unless Crystal source and a shard manifest are intentionally introduced.
- A documentation-validation run on the preceding SHA `e6cbc1b47167395de1ecffb99420d96c9fed741e` failed because the checker treated upstream-root-relative links in vendored documentation snapshots as links inside this repository. Exclude only those imported corpora from first-party link validation; preserve their source files.

## Control Center

The read-only dashboard is published from `infra/index.html` at `/infra/` after the Pages workflow deploys a merged commit. It loads the service registry and attempts a browser-side MCP health request. A CORS/network failure is **not** proof that the Worker is down. See [Control Center User Guide](CONTROL-CENTER-USER-GUIDE.md).

## Static site smoke test

For a verified Preview or published site:
- confirm the root page returns HTTP 200;
- confirm the OCode.js logo, CSS and scripts load;
- test desktop and mobile navigation, Escape close, focus visibility and reduced motion;
- open at least one documentation anchor and one code-copy control;
- inspect browser console and network failures;
- record URL, commit SHA and UTC timestamp.

The automated Pages workflow checks HTTP success for `/` and `/infra/` and validates the JSON service registry after deployment. MCP availability is tested by a separate workflow so an Access-policy issue cannot mark a successful Pages deployment as failed. Visual browser checks (responsive navigation, focus, anchors, code-copy and console errors) remain a separate manual acceptance gate.

## Documentation MCP smoke test

The dedicated `.github/workflows/mcp-smoke-test.yml` runs on relevant pull requests and pushes. It invokes `scripts/smoke-test-mcp.py` and verifies:
1. GET `/health`: service identity, `ok` status and the four expected read-only tools.
2. POST MCP `initialize` using protocol version `2025-03-26`.
3. POST `tools/list`: exact read-only tool inventory and object input schemas.

Current result: GitHub Actions receives HTTP 403 from `/health`. Cloudflare's read-only account inventory shows an account-level `All Workers` Access application with an allow condition requiring client certificate common name `Velclaw.ai`; this is a likely blocker for unauthenticated CI requests. Do not disable the account-wide policy. If the MCP endpoint is intentionally public, authorize a Worker-level bypass scoped only to `ocodejs-docs-mcp`; otherwise configure a dedicated Access service token for CI.

These protocol checks do not prove GitHub upstream document fetch availability. After access is resolved, manually call `list_ocodejs_docs`, `get_ocodejs_document` for `README.md`, and `search_ocodejs_docs`; also confirm malformed paths are rejected and no write tool is exposed.

## Chatbot Preview smoke test

Do not configure the public launcher until a separate Vercel project is accessible and a Preview deployment is READY.

- Verify the deployed commit SHA and framework/root directory.
- Confirm required environment variables exist by name only; never copy values into logs or documentation.
- Confirm database/Redis dependencies are actually provisioned before enabling dependent features.
- Test sign-in, session persistence, streamed responses, cancellation and safe provider errors.
- Verify CORS/frame policy for the documentation origin.
- Confirm no API keys appear in browser bundles, source maps, client errors or logs.
- Keep `chatbot-config.js` unset until a verified public HTTPS URL is approved.

## Incident response

1. Identify affected service and the first failing timestamp.
2. Compare current deployment SHA with the last known-good SHA.
3. Check provider/platform status before changing application code.
4. Prefer rollback to the last known-good Preview/deployment where supported.
5. Preserve logs with secrets and personal content redacted.
6. Record impact, root cause, mitigation and follow-up PR.
7. Production rollback or DNS changes require explicit authorization.

## Recovery and data safety

- The docs site and read-only MCP are intended to be stateless.
- Treat chatbot databases and object storage as stateful and independently owned.
- Before any migration, verify a recent backup and perform a restore into an isolated environment.
- Never test destructive migrations against production.
- Do not delete or replace a database, volume, bucket or repository as part of documentation work.

## Status vocabulary

- `PASS`: exact check ran and succeeded.
- `FAIL`: exact check ran and failed.
- `PENDING`: check is still running.
- `NOT VERIFIED`: required access, runtime or evidence is unavailable.
- `BLOCKED`: a known permission or external dependency prevents the step.

Every report should include the commit SHA, check URL and time window where available.
