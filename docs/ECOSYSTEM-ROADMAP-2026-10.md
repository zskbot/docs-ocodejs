# Ecosystem Development Roadmap — October 2026

This roadmap coordinates documentation, X-BO, and brand assets without merging their codebases. Work is staged through branches and pull requests; production deployment, database changes, secret migration, and PR merges remain out of scope until explicitly approved.

## 1. Shared delivery rules
- Keep each repository independently buildable and deployable.
- Treat `docs-ocodejs` as the documentation index, not a mirror that blindly overwrites application source.
- Retain source URL, repository, revision, license/attribution, and retrieval date for imported content.
- Never commit populated `.env` files, API keys, OAuth secrets, tokens, cookies, private keys, or environment dumps.
- Make changes on a feature branch, validate them, and open a focused PR. Do not deploy production from an unreviewed branch.
- Label evidence precisely: `documented`, `source-observed`, `test-verified`, or `production-verified`.

## 2. Documentation hub — `zskbot/docs-ocodejs`
### Immediate
- [ ] Resolve cross-repository sync blockers, including token scope and target write access; never copy tokens into files or logs.
- [ ] Keep sync failures isolated per target so one permission error does not hide other results.
- [ ] Add provenance and license fields to the inventory; distinguish source-linked summaries from copied content.
- [ ] Add Markdown link checks and validate the static documentation build.
- [ ] Keep inaccessible repositories marked incomplete until authorized read-only retrieval is available.
### Next
- [ ] Generate product indexes for OCode.js, VelCli, X-BO, OAuth, hosting/deploy, Control Center, and design assets.
- [ ] Report source/documentation drift without changing application files.
- [ ] Add an integration matrix for repository, runtime, CI, deployment target, health endpoint, and evidence status.

## 3. X-BO — `zskbot/X-BO`
### Immediate
- [ ] Keep `vercel.json` valid JSON and align the frontend output directory with Vite's `dist` output.
- [ ] Pin GitHub Actions to full commit SHAs where repository policy requires immutable references.
- [ ] Validate chat input, provider failures, timeouts, cancellation, and safe error responses.
- [ ] Cover JSON and SSE responses, malformed provider payloads, and empty prompts with tests.
- [ ] Ensure provider credentials are server-only and never echoed into errors or logs.
### Next
- [ ] Define a provider adapter contract with consistent timeout, error, and streaming semantics.
- [ ] Add bounded rate limiting and request-size limits to public API routes.
- [ ] Separate liveness/readiness checks from AI-provider calls.
- [ ] Add staging smoke tests and verify the deployed commit before any promotion.

## 4. Brand assets — `zskbot/pages_logo`
- [ ] Maintain a catalog of canonical logos, animations, favicon/app icons, and panda mascot variants.
- [ ] Preserve original files and paths; add new exports instead of replacing artwork without review.
- [ ] Record format, intended background, dimensions, transparency expectations, and canonical raw URLs.
- [ ] Verify SVG validity and actual GIF transparency/frame behavior instead of assuming it.
- [ ] Use consistent OCODE.js spelling and white wordmark on dark backgrounds where specified.
- [ ] Keep X-BO panda identity separate from OCode.js wordmark assets.

## 5. Release gates
1. JSON/YAML/Markdown syntax checks pass for changed files.
2. Relevant tests/build checks pass, or the PR clearly records why they could not run.
3. No secrets, unrelated bulk changes, or production data changes are included.
4. The PR states changed files, validation evidence, known limitations, and whether any deployment occurred.

## 6. Current limitations
The ecosystem audit is a metadata and selected-source review, not a semantic read of every file. Four repositories in the 2026-10-23 audit were unavailable through anonymous clone. Their content must remain marked incomplete until authorized access is available. An inventory alone does not prove production readiness.
