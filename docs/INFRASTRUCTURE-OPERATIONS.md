# OCode.js Infrastructure Operations

**Last reviewed:** 2026-11-01  
**Default mode:** free/staging/Preview; branch and PR only.

## Service ownership

| Service | Source of truth | Runtime owner | Current operational note |
|---|---|---|---|
| Documentation site | `zskbot/docs-ocodejs` | GitHub Pages workflow | Public URL `https://zskbot.github.io/docs-ocodejs/`; Pages workflow run #124 on `e3af9c4e83e03ef965cec8b953f28d414d124ec1` deployed successfully and passed `/`, `/infra/`, and service-registry HTTP checks |
| Documentation MCP | `cloudflare/ocodejs-docs-mcp` | Cloudflare Worker | Deployment `09409259-93c1-43e4-a8f7-0e1f2a9c209c` at 100% traffic; CI service-token integration is merged, but smoke test remains BLOCKED at secret preflight; no Access service token was present in the read-only inventory |
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
3. Classify the failure: product regression, validator defect, missing repository configuration, unrelated template workflow, or external provider/permission blocker.
4. Fix the narrowest cause and add a regression check where practical.
5. Re-run the affected workflow and inspect all required checks on the PR head SHA.
6. Do not claim success based on a different commit or an unrelated green workflow.

### Latest verified baseline (2026-11-01)

- PR #52 was merged as `50f464f964d96919d0a5b3e871126e141c12ba41`.
- PR #53 (`fix(mcp): prepare private Access service-token CI authentication`) was merged by repository owner `zskbot` at `2026-11-01T13:09:54Z`; merge commit: `e3af9c4e83e03ef965cec8b953f28d414d124ec1`. This merge was observed during the verification session; no merge action was issued by this assistant.
- GitHub Pages workflow run #124 (`41309926019`) deployed commit `e3af9c4e83e03ef965cec8b953f28d414d124ec1` and passed its deployment and post-deploy HTTP checks for `/`, `/infra/`, and `/ecosystem/services.json`. Published URL: `https://zskbot.github.io/docs-ocodejs/`.
- CI run #206 (`41309926028`) on the merge commit passed.
- MCP smoke-test run #12 (`41308763361`) failed at `Verify Cloudflare Access secrets are configured`; the protocol verification step was skipped. This is a missing-configuration preflight failure, not a successful `/health`, `initialize`, or `tools/list` test.
- Maintained workflows use Node.js 24-compatible action releases. The legacy Jekyll validation is manual-only because imported API reference Markdown contains Liquid-like tags unsupported by Jekyll; it is not the Pages deployment pipeline.

### Access-policy blocker found (2026-11-01)

- GitHub Actions received HTTP 403 from `https://ocodejs-docs-mcp.velclaw.workers.dev/health`.
- Read-only Cloudflare inventory shows an account-level Access application named `All Workers` with an allow condition requiring client certificate common name `Velclaw.ai`. This is a possible cause, not a proven root cause; no matching Access authentication event was found for the captured Ray ID.
- Do not disable, weaken, or add a service-token rule to the account-wide `All Workers` application. That could unintentionally affect every Worker protected by the application.
- The chosen CI direction is private authenticated access using a dedicated service token, not public access or an Access bypass.
- A read-only Cloudflare inventory on 2026-11-01 returned an empty account service-token list. The Access application inventory still contains `All Workers` with its existing client-certificate condition (`common_name: Velclaw.ai`); it was not changed. The inventory did not show a hostname-scoped Access application explicitly bound to `ocodejs-docs-mcp.velclaw.workers.dev`.
- Do not create or attach a token to `All Workers`. Cloudflare Access scope must first be resolved for the exact MCP hostname; if it overlaps with `All Workers`, stop and redesign the scope without weakening the existing application.

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

The dedicated `.github/workflows/mcp-smoke-test.yml` invokes `scripts/smoke-test-mcp.py` and verifies:
1. GET `/health`: service identity, `ok` status and the four expected read-only tools.
2. POST MCP `initialize` using protocol version `2025-03-26`.
3. POST `tools/list`: exact read-only tool inventory and object input schemas.

The smoke-test client supports Cloudflare Access service-token headers. In CI, it requires both repository secrets and fails early with a clear message if either is missing. Secret values are never printed.

### One-time secure setup for CI

This setup intentionally keeps the MCP endpoint private. Complete these steps in the provider dashboards; do not paste credentials into chat, source files, workflow YAML, issues, or logs.

1. **Cloudflare Access — scope the authorization**
   - Open the Cloudflare Zero Trust dashboard and inspect the existing Access application covering `ocodejs-docs-mcp.velclaw.workers.dev`.
   - Do not disable or edit the account-wide `All Workers` policy.
   - Ensure the MCP hostname has a narrowly scoped Access application/policy that permits the dedicated service token using a **Service Auth** policy and an include rule for that token.
   - The policy must cover only `ocodejs-docs-mcp.velclaw.workers.dev`. Do not add the token to a wildcard or account-wide application.
   - If Cloudflare reports that the hostname overlaps with the existing `All Workers` application, stop; do not force the change. Resolve the application-scope design first without weakening the existing policy.

2. **Cloudflare Access — create the CI service token**
   - In Zero Trust, open **Access → Service Auth → Service Tokens** (menu wording may vary).
   - Create a token named `docs-ocodejs-github-actions`, with a finite expiration (recommended: 1 year or less).
   - Copy the client ID and client secret at creation time. The secret is shown only once; store it directly in GitHub, not in chat.
   - Attach this token to the MCP-only Service Auth policy from step 1.

3. **GitHub — add repository Actions secrets**
   - Open `https://github.com/zskbot/docs-ocodejs/settings/secrets/actions`.
   - Choose **New repository secret** and create:
     - `CF_ACCESS_CLIENT_ID` = Cloudflare service-token Client ID.
     - `CF_ACCESS_CLIENT_SECRET` = Cloudflare service-token Client Secret.
   - Do not create similarly named plaintext variables. Use Actions **Secrets**.
   - Limit repository administration access to trusted maintainers.

4. **Verify**
   - Re-run the `Documentation MCP smoke test` workflow from Actions, or push the follow-up PR after both secrets and the scoped policy exist.
   - Confirm all three checks pass: `/health`, `initialize`, and `tools/list`.
   - Then manually test `list_ocodejs_docs`, `get_ocodejs_document` for `README.md`, and `search_ocodejs_docs`; also confirm malformed paths are rejected and no write tool is exposed.
   - Record the workflow URL, tested commit SHA, UTC timestamp, and service-token expiry date. Never record the token values.

5. **Rotation and incident handling**
   - Rotate the Cloudflare service token before expiry and update the two GitHub secrets together.
   - Re-run the smoke test after rotation; revoke the old token only after the new token passes.
   - If a token is exposed, revoke/rotate it immediately and inspect Access logs. Do not create a public bypass as a workaround.

Until steps 1–3 are complete, the MCP runtime status remains **BLOCKED / NOT VERIFIED**. A code change that merely supports token headers is not proof of successful authentication. The available GitHub connector does not expose a repository Actions-secret write operation, so `CF_ACCESS_CLIENT_ID` and `CF_ACCESS_CLIENT_SECRET` were not created or modified. Do not paste either value into chat.

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
