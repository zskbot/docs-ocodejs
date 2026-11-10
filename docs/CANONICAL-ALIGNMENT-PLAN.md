# Ecosystem Documentation Alignment Plan

**Review date:** 2026-10-23  
**Status:** documentation governance proposal; no source code or production configuration changed.

## Goal

Make the public documentation hub consistent across the 11 indexed repositories without pretending that similarly named repositories are one product, that README claims prove runtime behavior, or that inaccessible files have been fully reviewed.

## Canonical product boundaries

| Product / repository | Documentation role | Must not be described as |
|---|---|---|
| [OCodejs/OCodejs](https://github.com/OCodejs/OCodejs) and [Velclaw/OCodejs](https://github.com/Velclaw/OCodejs) | JavaScript/TypeScript utility library documented by their identical root README (MIT, v0.1.0, Node.js >=18; README says not yet published to npm). | A Next.js replacement, full-stack App Router framework, or published npm package without repository evidence and an approved product decision. |
| [Velclaw/Velclaw-OCodejs](https://github.com/Velclaw/Velclaw-OCodejs) and [Velclaw/VELCLAW](https://github.com/Velclaw/VELCLAW) | Broader VELCLAW Control Center / AI engineering workspace, based on their identical root README. | The OCode.js utility library solely because the repository name contains OCodejs. |
| [Velclaw/VelCli](https://github.com/Velclaw/VelCli) | AI engineering workspace and agent/IDE integration project. | A verified durable cloud runtime until persistence, sandboxing, and restart behavior are tested. |
| [zskbot/X-BO](https://github.com/zskbot/X-BO) | Chat/agent product with frontend, API and provider adapters as described in its README. | A provider-agnostic production service until provider-specific streaming, timeouts, rate limits and redaction are tested. |
| [Velclaw/VelclawHost](https://github.com/Velclaw/VelclawHost) | Hosting/control-plane concept and related operational docs. | A source of truth for production domains until the domain map is approved and verified. |
| [Velclaw/velclaw-deploy](https://github.com/Velclaw/velclaw-deploy) | Deployment console. | Safe for public deployment operations until route authorization and project ownership are verified. |
| [Velclaw/Oauth](https://github.com/Velclaw/Oauth) | OAuth integration project; inspected LICENSE is GPL-3.0. | Production-ready before callback allowlisting, state/CSRF, session and end-to-end tests pass. |
| [Velclaw/docs.velclaw.ai](https://github.com/Velclaw/docs.velclaw.ai) | Private-notice documentation site; package metadata identifies Nuxt 4, Docus and Nuxt Content. | A Next.js app based on README wording alone, or a source from which to copy full content into this public hub without written permission. |
| [Velclaw/Velclaw-velclaw-docs-ui-reference](https://github.com/Velclaw/Velclaw-velclaw-docs-ui-reference) | UI/design reference for the docs application. | Evidence that the production docs site implements or deploys the design. |

## Terminology and evidence rules

Use these terms consistently in every consolidated page:

- **Documented** — stated by a source file; not independently verified.
- **Source-observed** — verified by reading a specified source/configuration file at a recorded revision.
- **Test-verified** — a named automated or manual test passed for a specified commit/environment.
- **Runtime-verified** — an endpoint or process was executed in a specified non-production environment with a recorded result.
- **Production-ready** — only after security, persistence, integration, rollback, monitoring and owner-approval gates have evidence.

Never use “implemented”, “secure”, “persistent”, “live”, “deployed”, “supported” or “production-ready” based only on a roadmap, mockup or README claim.

## Cross-document conflicts to resolve

1. **OCode.js scope:** preserve the utility-library identity unless the product owner explicitly approves a separate framework specification. If a full-stack framework is planned, document it as a distinct product/version and define compatibility boundaries before merging terminology.
2. **Canonical repository:** both OCode.js repositories have the same root README blob SHA, but that does not prove identical trees or ownership. Compare package metadata, source trees, histories, release tags and maintainers before selecting a canonical repo. Until then, link both and state the evidence limit.
3. **VELCLAW duplicate README:** the VELCLAW and Velclaw-OCodejs root README blobs match; do not infer tree identity.
4. **Domains:** VelclawHost documentation refers to `velclaw.site` / `app.velclaw.site`, while VELCLAW documentation has referenced `velclaw.dev`. Treat this as unresolved. Do not edit DNS, OAuth callback URLs, TLS settings or production environment variables without an owner-approved domain map and a tested change plan.
5. **Docs runtime:** `docs.velclaw.ai/package.json` identifies Nuxt 4/Docus, while README wording describes Next.js. Align README and deployment instructions to the actual package scripts after source-owner review; do not change the framework as part of a documentation-only PR.
6. **Licensing:** the inspected `docs.velclaw.ai/LICENSE` reserves rights; do not copy its full docs/code/assets into this public repository without written permission. Preserve GPL-3.0 obligations for approved redistribution from Oauth. Missing a LICENSE file is not permission to redistribute.
7. **Access gaps:** anonymous clone failures do not prove a repository is private. Selected files were retrievable through the connected GitHub file interface, but full recursive content coverage remains incomplete.

## Prioritized remediation queue

### P0 — security and access boundaries
- [ ] Review all middleware, route handlers, session checks and deployment provider calls around `velclaw-deploy/app/api/deploy/route.ts`. The route file alone did not show auth checks; this is a potential issue, not proof of public exposure.
- [ ] Add isolated tests for anonymous requests, authenticated non-owner requests, cross-project IDs, CSRF/origin checks, rate limiting, audit events and secret-safe error output.
- [ ] Keep deployment creation/promotion disabled in any test until the authorization model is verified. Do not call production provider APIs during review.
- [ ] Verify OAuth state/nonce, redirect allowlists, session cookie flags, callback host and CSRF protections before live enablement.

### P1 — correctness and build reproducibility
- [ ] Fix and test the suspected block-scoped `locale` reference in `docs.velclaw.ai/scripts/generate-docus-content.mjs`; move locale-specific writes inside the locale loop and verify newline generation.
- [ ] Run content generation twice and compare outputs for deterministic results, then run `npm run type-check`, `npm run lint` and `npm run build` in a disposable environment after confirming lockfile and Node version.
- [ ] Align README framework claims with the Nuxt/Docus package metadata only after owner review.
- [ ] Pin GitHub Actions to reviewed full-length commit SHAs where repository policy requires immutable action references.

### P2 — product and integration contracts
- [ ] Select the canonical OCode.js repository only after comparing full source trees, package names, release history and maintainers.
- [ ] Specify each integration contract: endpoint, request/response schema, auth model, timeout/retry, error shape, rate limits, persistence, logging/redaction and versioning.
- [ ] For VelCli and X-BO, test stream termination, provider errors, HTTP timeouts, malformed payloads, cancellation, rate limits and secret redaction.
- [ ] Test PostgreSQL persistence across process restart and ephemeral-filesystem assumptions in a non-production environment; a successful health response is not persistence proof.
- [ ] Create an approved domain map before changing VelclawHost URLs, OAuth callbacks or deployment configuration.

### P3 — documentation quality and release process
- [ ] Generate a manifest containing source repository, default branch, source commit SHA, path, blob SHA, license signal and review status for each included document.
- [ ] Separate first-party authored docs from generated docs, vendored references, bundled skills, assets and binaries.
- [ ] Add a link checker and terminology checks for product names, runtime claims, domains and stale deployment URLs.
- [ ] Require review of license/provenance and secret scanning before any copied document or asset is published.
- [ ] Keep changes in topic branches and PRs; no automatic merge or production deploy.

## Release gate

A documentation PR is ready for review only when:
1. all changed links resolve or are explicitly marked as planned;
2. product identity and architecture claims match source metadata;
3. each implementation claim has a source path or test evidence;
4. domains and callback URLs match an approved map;
5. license/provenance checks permit the content;
6. secret scanning and documentation validation pass;
7. any unresolved issue is listed with an owner and next action.

A green documentation CI is necessary but does not prove runtime security, production health, or licensing permission.

## Evidence references

- [Source audit](./SOURCE-AUDIT.md)
- [Content review of 11 root READMEs](./CONTENT-REVIEW.md)
- [Integration matrix](./INTEGRATION-MATRIX.md)
- [Verification plan](./VERIFICATION-PLAN.md)
- [Implementation findings](https://github.com/zskbot/docs-ocodejs/blob/ops/run-safe-ecosystem-audit/docs/IMPLEMENTATION-FINDINGS.md) — currently on the open audit PR branch until that PR is resolved.
- [Audit run](https://github.com/zskbot/docs-ocodejs/actions/runs/39871263933)
