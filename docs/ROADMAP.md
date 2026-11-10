# OCode.js Documentation Hub — Roadmap

**Status:** working roadmap; planned work is not a claim that a feature already exists.  
**Last reviewed:** 2026-10-25  
**Canonical UI:** [OCode.js Design System](../DESIGN_SYSTEM.md)

## Principles

- Keep OCode.js utility-library claims separate from the broader Velclaw workspace and from any proposed full-stack framework.
- Prefer small, testable changes with reproducible checks.
- Do not run production deploys, migrate databases, or change secrets as part of documentation work.
- Preserve the existing canonical interface unless a design change is explicitly approved.
- Label evidence accurately: documented, source-observed, test-verified, or runtime-verified.
- Keep this repository focused on its own documentation site. Cross-repository synchronization is discontinued.

## Phase 1 — Documentation baseline

- [x] Maintain a central repository inventory and source audit.
- [x] Publish canonical UI preservation rules.
- [ ] Check internal links and navigation targets across Markdown and HTML.
- [ ] Identify stale, duplicated, conflicting, or unlicensed content before presenting it as authoritative.
- [ ] Record source repository and revision for cross-project claims where available.
- [ ] Verify the published site matches the reviewed source.

**Exit gate:** link checks pass, unsupported runtime/release claims are clearly marked, and the canonical UI remains intact.

## Phase 2 — Documentation site quality

- [ ] Review the homepage navigation and every card/link destination.
- [ ] Test mobile layouts, keyboard navigation, focus visibility, and reduced-motion behavior.
- [ ] Add accessible labels and meaningful alternative text to interactive controls and logo assets.
- [ ] Check page metadata, heading hierarchy, language declaration, and external-link behavior.
- [ ] Keep the site static and compatible with GitHub Pages; do not introduce a paid dependency or server requirement without approval.
- [ ] Add automated checks for broken internal links and malformed inventory JSON.

**Exit gate:** static validation passes and the primary pages remain usable on mobile and desktop.

## Phase 3 — OCode.js library documentation

- [ ] Review package metadata, supported Node.js versions, module format, and public exports against source code.
- [ ] Document HTTP timeout, abort, network failure, and response parsing behavior only where implementation evidence exists.
- [ ] Cover URL normalization, validation edge cases, string/object helpers, and async error paths.
- [ ] Confirm TypeScript examples match actual signatures.
- [ ] Report test and coverage results only when backed by CI evidence.
- [ ] Review package contents and licensing before publishing.

**Exit gate:** API documentation matches the actual exports and examples are reproducible on a clean environment.

## Phase 4 — Architecture decisions

- [ ] Decide whether router, layout, rendering, and API handlers belong in OCode.js itself or in a separately named framework project.
- [ ] Document module boundaries, compatibility policy, and migration strategy before implementation.
- [ ] Define SSR/SSG/CSR and routing requirements only if the owner approves the full-stack framework scope.
- [ ] Keep proposed capabilities clearly separated from supported features.

**Exit gate:** approved architecture record, explicit support matrix, examples, and compatibility review.

## Phase 5 — Reference and integration accuracy

- [ ] Keep VelCli, X-BO, VelclawHost, OAuth, and deployment-console responsibilities distinct.
- [ ] Verify source links and last-reviewed dates for project-specific statements.
- [ ] Preserve each source repository's license and attribution; public visibility alone does not grant redistribution rights.
- [ ] Do not imply that links in this hub mean codebases are merged, synchronized, or deployed.

**Exit gate:** each material cross-project claim has a source and an evidence status.

## Phase 6 — Release and operations

- [ ] Use a branch and pull request for source changes where practical.
- [ ] Require documentation validation and relevant checks before release.
- [ ] Keep staging separate from production and record rollback steps for any deployment change.
- [ ] Verify actual deployment status before saying a site or feature is live.
- [ ] Maintain release notes with commit, checks, limitations, and follow-up items.

**Exit gate:** checks have recorded results, changes are reviewable, and the owner approves release.

## Priority order

1. Validate homepage navigation and internal links.
2. Improve accessibility and mobile behavior without redesigning the approved visual direction.
3. Align OCode.js API documentation with verified source exports.
4. Clarify architecture decisions before documenting new framework features.
5. Keep the repository's own checks reliable and avoid cross-repository write automation.

## Progress tracking

Mark an item complete only when its evidence is linked (commit, passing check, test report, or approved decision). A planned task is not a completed feature.
