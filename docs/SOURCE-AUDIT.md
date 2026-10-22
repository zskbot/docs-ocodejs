# Ecosystem Source Audit — Initial Recursive Inventory

**Review date:** 2026-10-23  
**Target PR:** https://github.com/zskbot/docs-ocodejs/pull/2  
**Method:** Read-only GitHub API recursive Git-tree inventory plus targeted reads of selected README, architecture, security, readiness and integration documents. No repository archive was downloaded or extracted; no runtime builds/tests were run.

## Summary

- Repositories requested: **11**.
- Recursive tree API returned `truncated=false` for all 11 trees during this pass.
- Total file blobs enumerated: **11,474**.
- Markdown-like files (`.md`, `.mdx`, `.rst`, `.adoc`, `.txt`) enumerated: **7,264**.
- The two OCodejs repositories contain thousands of markdown-like files largely due to bundled agent/IDE skill libraries and references; these counts must not be interpreted as 7,264 product documentation pages.
- A recursive tree inventory enumerates paths and Git blob SHAs; it does not mean each file's contents were read.
- No secrets were intentionally copied. No production deployments, merges, database writes, or infrastructure changes were performed.

## Repository inventory

| Repository | Default branch | Tree commit SHA | File blobs | Markdown-like files |
|---|---|---|---:|---:|
| [Velclaw/VelCli](https://github.com/Velclaw/VelCli) | `main` | `c026445ef3afb25a0d611644ef3b7cbeec2c52d1` | 56 | 10 |
| [zskbot/X-BO](https://github.com/zskbot/X-BO) | `main` | `9c8cfc7d76441df0b9ef5259243a9498e52ef9b5` | 341 | 141 |
| [OCodejs/OCodejs](https://github.com/OCodejs/OCodejs) | `main` | `4f1ea0b3c9ddb5bc506036d688efe256decb7767` | 3,435 | 3,144 |
| [Velclaw/OCodejs](https://github.com/Velclaw/OCodejs) | `main` | `c5ce062768472de3acc2deb4fd43884e49428ba4` | 3,417 | 3,140 |
| [Velclaw/VelclawHost](https://github.com/Velclaw/VelclawHost) | `main` | `571bf824fa0cfb53ca9ccaf9a18e4b5197d16ddb` | 90 | 9 |
| [Velclaw/velclaw-deploy](https://github.com/Velclaw/velclaw-deploy) | `main` | `088782603635116cddd7db2c181de4c20e6c3a99` | 15 | 1 |
| [Velclaw/Oauth](https://github.com/Velclaw/Oauth) | `main` | `2ae96ffae6f026833b94d39031a91e0cfee89754` | 18 | 2 |
| [Velclaw/docs.velclaw.ai](https://github.com/Velclaw/docs.velclaw.ai) | `main` | `ab3bb1790fbbcaa215533faac3fdc2289bd04e97` | 130 | 20 |
| [Velclaw/VELCLAW](https://github.com/Velclaw/VELCLAW) | `main` | `2fde4bbb1f500de50dac2a6f0919e6e81fa008f0` | 1,983 | 396 |
| [Velclaw/Velclaw-velclaw-docs-ui-reference](https://github.com/Velclaw/Velclaw-velclaw-docs-ui-reference) | `main` | `7a0add8d20f910007a33481f6d8fcd659348d3d1` | 4 | 3 |
| [Velclaw/Velclaw-OCodejs](https://github.com/Velclaw/Velclaw-OCodejs) | `main` | `b8d371bbb880b47b2cb6bedb82ed86ed756d29c0` | 1,985 | 398 |

## Source-level findings from targeted document reads

### VelCli
- `docs/BASELINE-AUDIT-2026-10-22.md` explicitly records a source-only review; it did not run a local checkout or modify production.
- API sessions are stored in a process-local `Map`, so sessions are not durable across process restarts and are not shared automatically across multiple instances.
- PostgreSQL-backed records and filesystem fallback both exist in source, but deployed persistence must be verified rather than inferred from code.
- Workspace path checks and command allowlisting are guardrails, not a full OS/container sandbox. Symlink traversal and edge cases need dedicated tests.
- The repository's readiness document records a Render database expiry concern dated 2026-10-11. That historical note is not current-state proof; verify database/backup status through the authorized dashboard before any change. Do not repoint `DATABASE_URL`, expose the database, or perform destructive migrations without a verified restore.
- Existing CI action tags were identified as not immutable full commit SHAs in the baseline audit; validate and pin only to verified SHAs in a separate PR.
- Roadmap acceptance gates include auth/ownership regression tests, workspace traversal/symlink/timeout tests, persistence/restart tests, and explicit approval for GitHub/production actions.

### X-BO
- Architecture document describes a React frontend, Express API, chat router, provider adapters, a local demo path, and a Vercel serverless chat endpoint.
- Deployment guide names `DEFAULT_MODEL`, `OHMABA_URL`, `OHMABA_API_KEY`, and `GEMINI_API_KEY`; these are variable names only. No values were copied.
- Its tree includes many agent skills/reference documents in addition to product docs; separate first-party product docs from bundled or vendored material before importing content.

### OCode.js
- README identifies the project as a JavaScript/TypeScript utility library, not a replacement for Next.js or Vercel; it states the package is not yet published to npm.
- Modules documented include string/object/async/url/validation/http/browser/env/logger helpers.
- README roadmap calls out HTTP timeout/error-path tests, API coverage, npm availability and release checklist as outstanding.
- The two OCodejs repositories have different tree commits and file counts despite matching README blob SHA in the earlier pass. Compare branches and changed paths before choosing a canonical source or copying files.

### OAuth and TechDocs
- OAuth integration requires provider secrets to remain server-side, validates `return_to` against an allowlist, and gates callback registration on verified DNS, HTTPS, live response and end-to-end login.
- TechDocs architecture separates source, CI/CD, infrastructure, domains and documentation; production changes should pass CI/CD before reaching runtime.

## Identity / duplication warnings

1. `Velclaw/Velclaw-OCodejs` has the same general Control Center document set and matching file SHAs as `Velclaw/VELCLAW` for many sampled paths, despite its name. Do not treat it as canonical OCode.js without owner confirmation.
2. `OCodejs/OCodejs` and `Velclaw/OCodejs` are similar but not identical trees. Do not merge them automatically.
3. The docs UI reference is a small design-spec repository and should be linked as a source of truth, not mistaken for the actual docs application.

## Remaining work — not yet completed

- [ ] Read all 11,474 file contents. Current work is an inventory plus targeted document review, not a full content read.
- [ ] Download and extract repository archives where required; the GitHub connector used here supports UTF-8 text fetches but not binary archive downloads.
- [ ] Inspect full code/config trees and check for sensitive files without publishing any values.
- [ ] Build a deduplicated document corpus with per-file source URL, path, branch, SHA, license and provenance.
- [ ] Validate docs links and run tests/builds in safe disposable environments; no build or test has been run in this audit.
- [ ] Check PR CI status and review the complete diff before merge.

## Safe execution policy

Continue using a branch and PR. Do not merge, deploy production, create paid resources, modify environment secrets, change database targets, or perform destructive operations without explicit approval. The audit should prefer source links and attributed summaries over blind repository-wide file copying.