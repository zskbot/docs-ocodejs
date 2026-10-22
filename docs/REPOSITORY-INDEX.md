# Repository Inventory and Reading Checklist

## Source repositories
1. [Velclaw/VelCli](https://github.com/Velclaw/VelCli) — 56 file blobs, 10 Markdown-like files; source audit, readiness plan and scale-up roadmap reviewed.
2. [zskbot/X-BO](https://github.com/zskbot/X-BO) — 341 file blobs, 141 Markdown-like files (including skill/reference material); README, architecture and deployment guide reviewed.
3. [OCodejs/OCodejs](https://github.com/OCodejs/OCodejs) — 3,435 file blobs, 3,144 Markdown-like files; README reviewed, many files are bundled agent skills/reference libraries.
4. [Velclaw/OCodejs](https://github.com/Velclaw/OCodejs) — 3,417 file blobs, 3,140 Markdown-like files; README blob matched the organization repo during an earlier pass, but recursive tree SHA/count differs.
5. [Velclaw/VelclawHost](https://github.com/Velclaw/VelclawHost) — 90 file blobs, 9 Markdown-like files; README and architecture/setup overview reviewed.
6. [Velclaw/velclaw-deploy](https://github.com/Velclaw/velclaw-deploy) — 15 file blobs, 1 Markdown-like file; README reviewed.
7. [Velclaw/Oauth](https://github.com/Velclaw/Oauth) — 18 file blobs, 2 Markdown-like files; README and docs/integration.md reviewed.
8. [Velclaw/docs.velclaw.ai](https://github.com/Velclaw/docs.velclaw.ai) — 130 file blobs, 20 Markdown-like files; README and architecture.mdx reviewed.
9. [Velclaw/VELCLAW](https://github.com/Velclaw/VELCLAW) — 1,983 file blobs, 396 Markdown-like files; README and selected documentation structure inventoried.
10. [Velclaw/Velclaw-velclaw-docs-ui-reference](https://github.com/Velclaw/Velclaw-velclaw-docs-ui-reference) — 4 file blobs, 3 Markdown-like files; design reference.
11. [Velclaw/Velclaw-OCodejs](https://github.com/Velclaw/Velclaw-OCodejs) — 1,985 file blobs, 398 Markdown-like files; many sampled paths match VELCLAW Control Center. Verify repository identity before reuse.

## Integration contracts

See [INTEGRATION-MATRIX.md](INTEGRATION-MATRIX.md) for documented producer/consumer contracts, server-only credential boundaries, verification requirements and release gates.

See [VERIFICATION-PLAN.md](VERIFICATION-PLAN.md) for the phased full-content audit, safe test execution, integration readiness and delivery criteria.

## Audit results
- [x] Enumerate recursive Git tree/default branch for all 11 repositories; all trees returned `truncated=false`.
- [x] Record tree commit SHA and file counts in [SOURCE-AUDIT.md](SOURCE-AUDIT.md).
- [x] Read selected product README, architecture, OAuth integration, readiness and roadmap documents.
- [ ] Read every file's contents. The current work is an inventory and targeted review, not a full content read.
- [ ] Download/extract all repository archives and preserve binary assets; the GitHub text connector used here does not download repository ZIP archives or binary assets.
- [ ] Inspect all source/configuration and audit sensitive-file names without publishing secret values.
- [ ] Build a deduplicated document corpus with source URL, branch, commit SHA, path, license and provenance.
- [ ] Validate links and run tests/builds in safe disposable environments; no build/test was run as part of this audit.
- [ ] Check PR CI status and review the complete diff before merge.

## Aggregate counts

Across the 11 recursive trees, **11,474 file blobs** and **7,264 Markdown-like files** were enumerated. Many Markdown-like files are vendored or bundled agent skills/reference documents; these totals do not imply they are all product documentation pages.

## Safety and provenance

Never copy populated `.env` files, tokens, API keys, database URLs or private keys. Preserve licensing and source attribution. Keep production deploys, database changes, PR merge, and secret changes behind explicit approval. See [SOURCE-AUDIT.md](SOURCE-AUDIT.md) for findings and limitations.