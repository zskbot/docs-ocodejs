# Execution Plan: Full Documentation and Integration Verification

**Status:** planned execution queue. This document distinguishes completed source inventory from work that still requires file retrieval, isolated execution, or service-owner decisions.

## Phase 1 — Inventory and provenance (partially complete)
- [x] Enumerate recursive Git trees for all 11 requested repositories; record branch, tree SHA, blob counts and Markdown-like counts in `SOURCE-AUDIT.md`.
- [x] Read selected README, architecture, OAuth integration, deployment, readiness and UI specification documents.
- [x] Record the conflicting `velclaw.dev` versus `velclaw.site` canonical-domain declarations.
- [ ] Fetch all first-party documentation files by exact path and store an attribution record: source repository, branch, commit SHA, original path, license, retrieval date and local destination.
- [ ] Separate first-party docs from bundled skill/reference corpora, generated files, dependencies and vendored material.
- [ ] Inventory assets by extension and size; preserve binaries as binaries. Do not decode image/PDF/archive data as text.

## Phase 2 — Documentation consolidation
- [ ] Group docs by product: OCode.js, VelCli, X-BO, OAuth, hosting/deploy, TechDocs, Control Center and design system.
- [ ] Preserve source links and license notices; prefer attributed summaries and canonical links over copying complete duplicate corpora.
- [ ] Deduplicate exact matches by Git blob SHA; flag similar-but-different files for human review.
- [ ] Mark each statement as `documented`, `source-observed`, `runtime-verified`, or `production-ready` with evidence.
- [ ] Generate a link map and broken-link report; do not silently rewrite production URLs.

## Phase 3 — Safe verification (not run yet)
- [ ] For each Node.js project, inspect `package.json`, lockfile and scripts before installing dependencies.
- [ ] Use a disposable branch/container and the lockfile (`npm ci` where applicable); do not run install scripts from untrusted repos in a privileged environment.
- [ ] Run existing test, type-check, lint and build scripts only after reviewing them and confirming no production side effects.
- [ ] Store command, exit code, commit SHA, timestamp and concise output summary. Never store credentials or full environment dumps.
- [ ] For OCode.js, prioritize HTTP timeout/error-path tests, URL/validation edge cases, coverage and package dry-run; do not publish to npm.
- [ ] For X-BO and VelCli, test provider timeout, malformed response, rate limit, cancellation, redaction and bounded input/output.
- [ ] For OAuth, test allowlisted and rejected `return_to`, state/CSRF, callback mismatch, session expiry and secret redaction using test credentials only.
- [ ] For TechDocs, run content tests, type-check, lint and credential-free build before any indexing command requiring Supabase/Gemini.

## Phase 4 — Integration readiness
- [ ] Resolve canonical domain ownership (`velclaw.dev` vs `velclaw.site`) before DNS, OAuth, redirects or deployment changes.
- [ ] Verify OAuth hostname, TLS, exact callback URI and end-to-end login before registering a public callback.
- [ ] Verify database backup and perform a restore to an isolated target before any migration or `DATABASE_URL` change.
- [ ] Verify server-only environment variable boundaries; inspect client bundles for accidental secret exposure without printing secret values.
- [ ] Confirm least-privilege tokens, branch protection, immutable GitHub Actions SHAs and approval gates.
- [ ] Map each deployed service to repository, commit SHA, environment and health endpoint; treat docs as intent until confirmed live.

## Phase 5 — Delivery
- [ ] Review generated changes and provenance.
- [ ] Run Markdown/link validation and the docs build if a supported script exists.
- [ ] Open a focused PR with test evidence and limitations.
- [ ] Do not merge, deploy production, change secrets, create paid resources or modify databases without explicit approval.

## Current blockers
- The GitHub text connector can enumerate trees and fetch text files but did not provide a full ZIP/archive extraction workflow in the current session; binary assets and complete content-level reading remain outstanding.
- Repository trees include large bundled agent/IDE reference corpora; bulk copying them would create noisy, potentially duplicated documentation and may carry separate licenses.
- Canonical domain and the identity of `Velclaw/Velclaw-OCodejs` require owner-level clarification before treating either as authoritative.

## Completion criteria
The project is not considered fully consolidated until all first-party docs are enumerated and read, provenance/licensing is recorded, links/build checks are run in a safe environment, integration conflicts are resolved, and the final PR states precisely what was and was not verified.