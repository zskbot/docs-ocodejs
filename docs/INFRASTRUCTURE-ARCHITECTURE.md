# OCode.js Infrastructure Architecture

**Status:** architecture and evidence register  
**Last reviewed:** 2026-11-01  
**Scope:** `zskbot/docs-ocodejs`, its public documentation delivery, the read-only documentation MCP, and the separately hosted chatbot integration.

This document separates verified repository facts from deployment claims that still need live checks. It does not authorize production changes.

## 1. Target architecture

```text
                         Public users / MCP clients
                                    |
                    +---------------+----------------+
                    |                                |
             Documentation site                 MCP clients
                    |                                |
          GitHub Pages static output        Cloudflare Workers edge
                    |                                |
             Git repository                  Read-only MCP API
                    |                                |
           GitHub Actions CI                 GitHub public Contents API
                    |
             Pull request gates
                    |
              main branch
                    |
             Pages deployment

       Separate application boundary (not hosted by Pages)
                    |
          OCodejs/chatbot Next.js app
                    |
             Vercel deployment
                    |
       PostgreSQL / Redis / optional AI services
       (configuration and live health NOT VERIFIED)
```

## 2. Current components and evidence

| Component | Responsibility | Evidence on 2026-11-01 | Remaining verification |
|---|---|---|---|
| Documentation source | Canonical public docs and infrastructure records | Repository `zskbot/docs-ocodejs`; main SHA `5645479f4bd45df12dd3cfd08b334a75c36edd86` | Content review and link validation |
| Static documentation delivery | Publish static files | GitHub Actions Pages workflow succeeded for the recorded main SHA | Open the canonical Pages URL and test browser rendering, assets, mobile navigation |
| Documentation MCP | Read-only search/list/read tools for public docs | Worker source and Wrangler config exist; PR #43 records a deployment | Live health check, MCP initialize, tools/list, tool calls, CORS and rate-limit behavior |
| Chatbot | Interactive AI assistant, independent server runtime | Integration page and launcher/config exist; PR #44 records Vercel project creation blocked with HTTP 403 | Create/authorize a separate Vercel project, configure required services, deploy Preview, smoke-test |
| CI and quality gates | Validate docs, inventory, HTML and deployment workflow | Core CI and Pages succeeded on recorded SHA; Crystal CI failed because `shard.yml` is absent | Keep repository-relevant checks green and unrelated templates non-blocking |

Evidence labels are intentionally conservative. A successful Pages workflow is not the same as a browser smoke test. A Worker health response is not proof that its GitHub upstream is reachable. A README endpoint is not proof of a live deployment.

## 3. Network and service boundaries

### Public documentation
- Static assets and documentation are served by the configured static host.
- The site must not contain runtime credentials or privileged API calls.
- Client-side configuration files may contain public URLs only.

### Documentation MCP
- The documented Worker endpoint is `https://ocodejs-docs-mcp.velclaw.workers.dev/mcp`.
- The intended data source is the public `main` branch of `zskbot/docs-ocodejs`.
- The MCP tools are read-only: search, list paths, read one document, and return a project overview.
- The Worker must not receive a GitHub write token for this use case.
- Its `/health` response reports Worker metadata. It must not be described as an upstream dependency check.
- Follow-up hardening: bound upstream response sizes and timeouts, validate tool arguments, add abuse/rate controls, and test protocol compatibility with a real MCP client.

### Chatbot runtime
- The chatbot is a separate Next.js service; GitHub Pages cannot host its API routes, sessions, streaming, or database connections.
- Vercel is the intended hosting boundary documented by the integration guide.
- PostgreSQL, Redis, Blob and AI Gateway are configuration references, not proof that those resources are provisioned or connected.
- Do not point the public documentation launcher at an unverified or private Preview URL.

## 4. Identity, secrets and data

- No shared identity provider is currently asserted by this documentation hub.
- Do not assume the chatbot shares OCode.js or Velclaw sessions until an explicit OIDC/OAuth contract, issuer, audience, callback allowlist and session model have been tested.
- Store credentials in the owning platform's secret manager (GitHub Actions, Cloudflare, or Vercel).
- Never commit populated `.env` files, OAuth client secrets, API keys, access tokens, database URLs, private keys or session secrets.
- The documentation site and MCP should not store user chat history.
- Any chatbot persistence must have documented retention, deletion, backup and restore behavior before production use.

## 5. Delivery flow

1. Inspect the default branch, open PRs and latest workflow runs.
2. Create a scoped feature branch from the current `main`.
3. Update source, documentation and dependency-free validators.
4. Run local syntax/validation checks where available.
5. Open a PR; require documentation validation, inventory validation, core CI and relevant security checks.
6. Inspect failed job logs and correct only repository-relevant failures.
7. Verify a Preview deployment against its exact commit SHA.
8. Merge and promote only after explicit authorization. Production promotion is outside this workstream.

## 6. Reliability and observability targets

Each runtime service should eventually publish:
- a documented HTTPS health endpoint;
- a shallow liveness response that does not call paid providers;
- a separate readiness/dependency check where useful;
- deployment commit SHA and build timestamp;
- structured logs with request IDs and secret redaction;
- bounded request duration, body size and upstream response size;
- an incident owner and rollback procedure.

Do not invent uptime, latency, availability or cost figures. Add metrics only when a real source is connected.

## 7. Expansion sequence

### Phase A — Documentation control plane
- Machine-readable service registry.
- Offline validation and CI gate for service metadata.
- Clear evidence levels and deployment ownership.
- Operational runbooks and architecture map.

### Phase B — Public service verification
- Test GitHub Pages rendering and canonical URL.
- Verify Cloudflare Worker health and full MCP protocol handshake.
- Verify chatbot Vercel Preview after project access is available.
- Record exact URLs, commit SHAs, timestamps and test results.

### Phase C — Shared integration contracts
- Define OIDC identity boundaries only after issuer and ownership decisions.
- Define webhook signatures, replay protection and idempotency.
- Define service-to-service authorization and least-privilege scopes.
- Add contract tests without coupling independent repositories.

### Phase D — Production readiness
- Backups and restore drills for stateful services.
- Observability, alerting, incident response and rollback.
- Security review and dependency scanning.
- Explicit production approval after staging evidence is complete.

## 8. Non-goals

This architecture does not merge repositories, create cloud resources, rotate credentials, migrate databases, configure DNS, enable public chatbot access, or promote a production deployment.
