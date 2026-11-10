# OCode.js Integration Contracts

**Status:** normative design contract; implementation and provider wiring are not yet asserted.  
**Scope:** OCode.js documentation hub, documentation MCP, chatbot and future Velclaw services.

## 1. API gateway contract

The API gateway is a routing and policy boundary, not a new application database.

- Use versioned paths: `/api/v1/<service>/<resource>`.
- Route only to explicitly registered upstreams; unknown services return `404`.
- Enforce TLS, request size limits, bounded timeouts and per-route rate limits.
- Forward a request ID (`x-request-id`) or generate one; never trust client-supplied identity claims.
- Return stable JSON errors: `{ "error": { "code": "...", "message": "...", "requestId": "..." } }`.
- Do not proxy arbitrary URLs or allow user-controlled upstream hosts.
- Keep service credentials in the gateway's secret manager and use a distinct credential per upstream.
- Require idempotency keys for retryable state-changing operations.
- The documentation MCP remains read-only and must not be routed through a privileged write scope.

### Versioning and compatibility

- Additive response fields are backward-compatible.
- Breaking changes require a new API version and a migration window.
- Publish OpenAPI schemas and contract tests before enabling a route.
- Do not advertise a gateway endpoint until the owning Worker/project, DNS and auth policy are independently verified.

## 2. Identity and authorization contract

No shared identity provider is considered configured by this repository.

When identity integration is approved:
- Use OIDC Authorization Code with PKCE for browser/public clients.
- Validate issuer, audience, signature, expiry, nonce, state and redirect URI server-side.
- Use exact redirect URI allowlists; no wildcard callback domains.
- Map external identity to an immutable subject (`iss + sub`), not mutable email alone.
- Keep provider tokens server-side; never store client secrets in static assets.
- Use short-lived sessions, secure/httpOnly/sameSite cookies, CSRF protection and session rotation.
- Define roles/scopes explicitly; default deny and least privilege.
- Separate service-to-service identity from end-user sessions.
- Document account linking, unlinking, revocation and recovery before enabling cross-product SSO.

## 3. Event and webhook contract

- Verify webhook signatures over the raw request body.
- Enforce timestamp tolerance and replay protection.
- Persist an event ID or idempotency key before processing to prevent duplicate side effects.
- Acknowledge quickly and process long-running work asynchronously.
- Retry only transient failures with bounded exponential backoff and jitter.
- Send exhausted events to a dead-letter path only when a real queue and retention policy exist.
- Never include secrets or unnecessary personal data in event payloads or logs.

## 4. Observability contract

Every runtime service should provide:
- liveness endpoint independent of paid upstreams;
- readiness endpoint for required dependencies;
- service name, build SHA and deployment version;
- structured logs with request ID, severity and secret redaction;
- bounded metrics for request count, error rate and latency;
- alert thresholds with an owner, runbook and rollback path.

Do not expose environment variables, authorization headers, tokens, message contents or database connection strings in logs.

## 5. Resilience and recovery

- Set explicit connect/read/overall timeouts for upstream calls.
- Retry only idempotent or idempotency-key-protected operations.
- Use circuit breakers for unstable upstreams; fail closed for authorization and payment/security decisions.
- Keep backups for stateful services and test restores into isolated environments.
- Document recovery point and recovery time objectives only after measured restore exercises.
- Keep deployment rollback separate from database rollback; schema changes should use expand/contract migrations.

## 6. Staging acceptance gates

Before any integration is considered ready:
1. A dedicated staging/Preview environment exists and has a verified owner.
2. No production secrets or customer data are copied into staging.
3. The contract schema and negative tests pass.
4. Auth rejects invalid issuer, audience, expired tokens, replayed state and unapproved redirect URIs.
5. Gateway rejects unknown routes, oversized payloads, open redirects and arbitrary upstream hosts.
6. Webhooks reject invalid signatures and duplicate events.
7. Logs redact credentials and personal data.
8. Rollback and recovery steps are exercised.
9. Cost and quota impact are documented for any non-free resource.

## 7. Explicit non-goals

This document does not create DNS records, Cloudflare routes, Workers, KV/D1/R2 resources, Vercel projects, OAuth applications, database schemas, API keys or production deployments.
