# Infrastructure Control Center — User Guide

## Purpose

The Control Center at `/infra/` is a static, read-only operational view for the OCode.js ecosystem. It loads `ecosystem/services.json`, displays evidence labels, links to source and runbooks, and attempts a browser-side request to the documentation MCP health endpoint.

## Evidence labels

- **Workflow passed · live site not verified:** CI/Pages workflow passed, but a browser-level check has not been recorded.
- **Deployment API verified · HTTP not tested:** Cloudflare confirms the Worker deployment configuration, but the endpoint protocol has not been tested.
- **Blocked:** a required platform permission or resource is unavailable.
- **Runtime verified:** reserve this status for a timestamped HTTP/protocol test against the exact deployment.
- **Production verified:** reserve this status for approved production acceptance and smoke tests.

Never change a service to runtime-verified based only on a successful GitHub Actions workflow or a cloud resource inventory.

## Browser health check

The page attempts a CORS-enabled GET request to the MCP `/health` endpoint with a five-second timeout. A CORS/network error means the browser could not verify the endpoint; it does not prove the Worker is down. Use the direct health link for an independent manual check and then execute the full MCP protocol checklist in the operations runbook.

## Security boundary

The page contains no privileged credentials and performs no writes. Do not add buttons for resource creation, secret editing, DNS changes, deployment promotion or database operations to this static dashboard. Such operations require an authenticated server-side control plane with audit logging, explicit authorization and separate approvals.

## Current Cloudflare account snapshot

Read-only inventory observed on 2026-11-01:
- 12 Workers scripts listed; the OCode.js documentation MCP Worker is present.
- No Workers KV namespaces returned.
- One D1 database named `autoship` returned with zero tables; it is not part of the docs project and must not be modified.
- R2 API returned error 10042: R2 has not been enabled for the account.
- A Pages project was listed but its source did not match `zskbot/docs-ocodejs`; it is not registered as this project's deployment.

This snapshot is not a promise that every account resource is billable/free. No resource was created or modified.
