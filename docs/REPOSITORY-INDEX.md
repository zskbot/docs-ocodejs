# Repository Inventory and Reading Checklist

## Source repositories
1. https://github.com/Velclaw/VelCli — README, AGENTS.md, docs.html, application docs, apps/assets.
2. https://github.com/zskbot/X-BO — README, frontend/backend, chat API, provider routing, deployment config.
3. https://github.com/OCodejs/OCodejs — README, docs/, documentation/, getting-started/, framework/, tests/, package metadata.
4. https://github.com/Velclaw/OCodejs — compare against OCodejs/OCodejs; README content and blob SHA matched during this review.
5. https://github.com/Velclaw/VelclawHost — architecture, domains, control plane, setup, DNS/ingress and environment docs.
6. https://github.com/Velclaw/velclaw-deploy — deployment console, .env.example, Next.js and Vercel integration.
7. https://github.com/Velclaw/Oauth — README and docs/integration.md; verify callback host and HTTPS.
8. https://github.com/Velclaw/docs.velclaw.ai — MDX docs, Supabase schema, content indexing and app routes.
9. https://github.com/Velclaw/VELCLAW — README, docs/CONTROL-CENTER.md, docs/ECOSYSTEM.md and integrations.
10. https://github.com/Velclaw/Velclaw-velclaw-docs-ui-reference — design reference and docs UI standards.
11. https://github.com/Velclaw/Velclaw-OCodejs — README appeared identical to VELCLAW Control Center in this review; verify purpose.

## Full audit checklist
- [ ] Enumerate recursive Git tree and default branch for each repository.
- [ ] Read all Markdown/MDX documentation, ADRs, API references and deployment guides.
- [ ] Inventory code/config separately from documentation.
- [ ] Preserve binary assets as binaries; do not decode as UTF-8 text.
- [ ] Inspect only variable names in .env.example; never copy populated secrets.
- [ ] Identify duplicate content, conflicting names, obsolete URLs, unsupported production claims and license requirements.
- [ ] Record source URL, branch, commit SHA, path, review date and summary for every imported document.
- [ ] Add selected sanitized docs with attribution; link to large source/binary assets rather than copying indiscriminately.
- [ ] Validate links and run any docs build/test scripts available.
- [ ] Open a PR and review the diff before merging.

## Scope statement
This index does not claim every file across the 11 repositories has been downloaded or read. The initial pass reviewed public metadata and selected README files. Recursive file-level audit and archive extraction remain outstanding.