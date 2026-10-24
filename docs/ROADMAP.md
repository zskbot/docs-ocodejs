# OCode.js & Velclaw Ecosystem — Roadmap

**Status:** working roadmap, not a promise that listed features already exist.  
**Last reviewed:** 2026-10-24  
**Canonical UI:** [OCode.js Design System](../DESIGN_SYSTEM.md)

## Principles

- Keep OCode.js utility-library claims separate from the broader Velclaw workspace and from any proposed full-stack framework.
- Prefer small, testable changes with reproducible checks.
- Do not run production deploys, migrate databases, or change secrets as part of documentation work.
- The canonical OCode.js interface is protected. Feature and documentation work must not redesign it without explicit owner approval.
- State the evidence level for every important claim: documented, source-observed, test-verified, or runtime-verified.

## Phase 1 — Documentation baseline

- [x] Maintain a central repository inventory and source audit.
- [x] Publish canonical UI preservation rules.
- [ ] Ensure README, docs navigation and API links resolve to real files.
- [ ] Identify stale, duplicated, conflicting or unlicensed content before synchronizing it.
- [ ] Record source repository and revision for each cross-project claim.

**Exit gate:** broken-link review completed; no unsupported runtime or release claims; UI remains unchanged.

## Phase 2 — OCode.js library quality

- [ ] Review package metadata, supported Node.js versions, module format and public exports against source code.
- [ ] Add or complete HTTP timeout, abort, network failure and response parsing tests where the implementation supports them.
- [ ] Add tests for URL normalization, validation edge cases, string/object helpers and async error paths.
- [ ] Confirm TypeScript strict checks and documented examples match actual signatures.
- [ ] Generate coverage reports and record the actual threshold; do not claim coverage without CI evidence.
- [ ] Review package contents and licensing before publishing.

**Exit gate:** clean install, tests, type checks and package dry-run pass on a clean runner; API docs match exports.

## Phase 3 — Architecture decisions

- [ ] Decide whether router, layout, rendering and API handlers belong in OCode.js itself or in a separately named framework project.
- [ ] Document the decision, module boundaries, compatibility policy and migration strategy before implementation.
- [ ] Define SSR/SSG/CSR and routing requirements only if the owner approves the full-stack framework scope.
- [ ] Build a minimal proof of concept behind tests; do not advertise it as supported until the exit gate passes.

**Exit gate:** approved architecture record, explicit support matrix, tests, examples and a compatibility review.

## Phase 4 — Ecosystem integrations

- [ ] Keep VelCli, X-BO, VelclawHost, OAuth and deployment-console responsibilities distinct.
- [ ] Define versioned contracts for provider adapters, OAuth callbacks, deployment requests and shared docs.
- [ ] Verify authentication, authorization, secret redaction, rate limits, timeout handling and audit logging in isolated staging.
- [ ] Preserve each source repository's license and attribution; never assume public visibility grants redistribution rights.

**Exit gate:** contract tests pass in staging; security and ownership review is recorded; no production change is implied.

## Phase 5 — Documentation automation

- [ ] Validate inventory JSON and link targets in CI.
- [ ] Detect accidental changes to canonical UI files separately from content updates.
- [ ] Require explicit owner approval for any intended change to the canonical interface.
- [ ] Make sync jobs idempotent, scoped, auditable and safe to rerun.
- [ ] Fail closed when required tokens are missing; never print token values.
- [ ] Produce a report of skipped repositories and reasons instead of silently claiming full synchronization.

**Exit gate:** validation succeeds on a test branch; a second run produces no unintended diff; secrets are absent from logs and artifacts.

## Phase 6 — Release and operations

- [ ] Use a branch and pull request for source changes where practical.
- [ ] Require build, tests, security checks and documentation validation before release.
- [ ] Keep staging separate from production and record rollback steps.
- [ ] Verify actual deployment status before saying a site or feature is live.
- [ ] Maintain a release note with commit, checks, limitations and follow-up items.

**Exit gate:** all required checks have recorded results, rollback is documented, and the owner approves release.

## Priority order

1. Resolve documentation conflicts and links.
2. Test the existing OCode.js API; do not invent exports.
3. Decide framework scope before adding router/rendering promises.
4. Verify security-sensitive ecosystem integrations in staging.
5. Enforce safe documentation sync and release gates.

## Progress tracking

Mark an item complete only after its evidence is linked (commit, passing check, test report, or approved decision). A planned task is not a completed feature.
