# OCode.js Infrastructure Operations

**Last reviewed:** 2026-11-01  
**Default mode:** free/staging/Preview; branch and PR only.

## Service ownership

| Service | Source of truth | Runtime owner | Current operational note |
|---|---|---|---|
| Documentation site | `zskbot/docs-ocodejs` | GitHub Pages workflow | Pages workflow passed on main SHA `174e4cd1f7495414e7a90569de0599d533d94ff5`; dashboard browser smoke test remains pending |
| Documentation MCP | `cloudflare/ocodejs-docs-mcp` | Cloudflare Worker | Cloudflare API confirms deployment `09409259-93c1-43e4-a8f7-0e1f2a9c209c` at 100% traffic; direct HTTP/MCP verification remains outstanding |
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

### Known baseline findings (2026-11-01)

- Baseline main commit at this review: `174e4cd1f7495414e7a90569de0599d533d94ff5`.
- Core `CI`: PASS for that SHA.
- `Deploy static content to Pages`: PASS for that SHA.
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

A successful Pages action alone does not satisfy this checklist.

## Documentation MCP smoke test

Use the documented endpoint only after confirming it is reachable:
1. GET `/health`; verify the service name, endpoint and tool inventory.
2. POST MCP `initialize` with the supported protocol version.
3. Send `notifications/initialized`.
4. Call `tools/list`; verify the four read-only tools.
5. Call `list_ocodejs_docs` with a small limit.
6. Call `get_ocodejs_document` for `README.md`.
7. Call `search_ocodejs_docs` with a common term.
8. Confirm malformed paths are rejected and no write capability is exposed.
9. Record status codes, response time, Worker deployment version and test timestamp.

Do not interpret the present static `/health` response as proof that GitHub's API is healthy.

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
