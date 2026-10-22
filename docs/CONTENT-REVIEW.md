# Content-Level Review — 11 Repository READMEs

**Review date:** 2026-10-23  
**Scope:** Read the root `README.md` from each of the 11 source repositories and compare product scope, documented integration boundaries, deployment claims, licensing signals, and duplicate content. This is a first-party entry-point review, not a claim that every documentation file has been read.

## Executive result

- **11/11 root README files retrieved and reviewed** from the default branch exposed by GitHub.
- **Two exact README-content duplicates detected by blob SHA:** `OCodejs/OCodejs` and `Velclaw/OCodejs`; and `Velclaw/VELCLAW` and `Velclaw/Velclaw-OCodejs`. These are duplicate README blobs, not proof that every file or commit in each repository is identical.
- **Product identity must remain separate:** OCode.js is documented as a JS/TS utility library (v0.1.0, early development, not published to npm), while VELCLAW / Velclaw-OCodejs documents a broader AI-native Control Center.
- **Integration and production statements remain evidence-gated.** A README is a source claim, not runtime verification.
- No source repository was modified by this review.

## Per-repository review

| Source repository | Root README blob SHA | What the README documents | Review notes / follow-up |
|---|---|---|---|
| [Velclaw/VelCli](https://github.com/Velclaw/VelCli) | `9039b5d2c8e1e8f4305d3040e2685bf575108591` | AI engineering workspace, agent plan endpoint, editor, projects/chat, VelclawHost integration, Render deployment, PostgreSQL and environment-variable guidance. | README explicitly warns that an HTTP 200 health response does not prove database persistence; session memory, ephemeral filesystem and command sandbox limitations need runtime tests. README names a Render service URL; verify ownership/status before treating it as current. |
| [zskbot/X-BO](https://github.com/zskbot/X-BO) | `930cb5713ea236ac49eb0f31e65d08be741b703b` | React/Vite frontend, Node/Express API, provider adapters, SSE chat, `POST /api/chat`, environment configuration and Vercel deployment guidance. | README identifies Apache-2.0. Validate provider-specific stream behavior, timeouts, malformed responses, rate limits and secret redaction. Keep provider keys server-side. |
| [OCodejs/OCodejs](https://github.com/OCodejs/OCodejs) | `985ee9aedc773c0172a3aaa07bebe8b877c8fa91` | OCode.js utility toolkit: string, object, async, URL, validation, HTTP, browser storage, env and logger modules. | Exact README duplicate of `Velclaw/OCodejs`. README identifies MIT, Node.js >=18, v0.1.0, and says npm publication has not happened. Do not describe this repository as a Next.js replacement or full-stack framework without a separate approved product decision. |
| [Velclaw/OCodejs](https://github.com/Velclaw/OCodejs) | `985ee9aedc773c0172a3aaa07bebe8b877c8fa91` | Same README content as `OCodejs/OCodejs`. | Exact README duplicate only; compare repository histories, package metadata, source trees and release ownership before choosing a canonical repository. |
| [Velclaw/VelclawHost](https://github.com/Velclaw/VelclawHost) | `faabeec166c9ce16abbbab553a7158b94f036375` | Large hosting/control-plane concept covering custom domains, DNS/TLS, monitoring, alerts, DB optimization, AI diagnostics, 2FA and reporting. | README references `velclaw.site` and `app.velclaw.site`, conflicting with VELCLAW's documented canonical `velclaw.dev`. Do not rewrite DNS, OAuth callbacks or production URLs until an owner-approved domain map is verified. Treat feature descriptions as intended design until tests/live evidence exist. |
| [Velclaw/velclaw-deploy](https://github.com/Velclaw/velclaw-deploy) | `a543eb6a60470aa7efcd068727c8a6f086f18041` | Short deployment-console README: stack, local setup, environment, deployment flow, product language and release. | Entry point is too brief to establish supported providers, rollback behavior or production safety. Review package/config/workflow files before executing any release path. |
| [Velclaw/Oauth](https://github.com/Velclaw/Oauth) | `ddce9d228e72d2621e806148952173b80292bbbe` | Minimal README with workspace integration. | Insufficient detail to establish provider callbacks, state/CSRF protections, session persistence, redirect allowlists or deployment status. Review implementation and tests before enabling public OAuth routes. |
| [Velclaw/docs.velclaw.ai](https://github.com/Velclaw/docs.velclaw.ai) | `4d1d9041120cc023ba40202136b0d3caff55413a` | TechDocs setup, Supabase schema, security, commands and deployment. | Any setup step that applies a schema or invokes Supabase/Gemini must be reviewed separately and run only in an isolated, approved environment. Never include credentials in documentation artifacts. |
| [Velclaw/VELCLAW](https://github.com/Velclaw/VELCLAW) | `60d483d907e1b1849b4525e9d969918ab60a15f1` | VELCLAW Control Center and broader AI-native software workspace architecture, integrations, security, domains and deployment workflow. | Exact README duplicate of `Velclaw/Velclaw-OCodejs`. README itself says registry coverage and production health are incomplete; preserve this distinction in summaries. |
| [Velclaw/Velclaw-velclaw-docs-ui-reference](https://github.com/Velclaw/Velclaw-velclaw-docs-ui-reference) | `7abbdf9be3aafabaec797747e67adefbde6f5243` | UI source of truth for Velclaw Docs: dark theme, purple accent, square corners, responsive drawer, three-column desktop layout, keyboard focus and code-copy affordance. | Design specification, not evidence that the docs application currently implements or deploys these details. |
| [Velclaw/Velclaw-OCodejs](https://github.com/Velclaw/Velclaw-OCodejs) | `60d483d907e1b1849b4525e9d969918ab60a15f1` | Same README content as `Velclaw/VELCLAW`, describing VELCLAW Control Center rather than OCode.js utility APIs. | Repository name can be confused with the OCode.js library. Keep its product identity separate; verify source tree and ownership before treating it as the canonical OCode.js repository. |

## Duplicate and identity handling

1. Preserve both OCode.js repositories in the inventory, but link their identical README content to each other rather than copying the same text twice.
2. Preserve both VELCLAW Control Center repositories in the inventory, but do not infer that their full source trees are identical from README SHA equality.
3. Do not combine OCode.js utility-library docs with VELCLAW Control Center docs based on repository naming alone.
4. Keep the VelclawHost `.site` URLs and VELCLAW `.dev` policy as a documented conflict until DNS, TLS, routing and OAuth callbacks are verified by the service owner.
5. Do not copy bundled skills, generated docs, vendored dependencies or binary archives into the canonical documentation set without provenance and license review.

## Verification vocabulary

Use these labels consistently in the consolidated docs:

- **Documented:** stated in a source file; not independently verified.
- **Source-observed:** confirmed by reading source/configuration at a recorded commit.
- **Runtime-verified:** command or endpoint executed against a specified commit/environment with recorded result.
- **Production-ready:** only after required security, persistence, integration, rollback and owner-approval gates have passed.

## Next steps

- [ ] Record root README commit SHA (not only blob SHA) for every source repo in the machine-generated manifest.
- [ ] Review each repository's LICENSE/COPYING and package/workflow metadata before redistributing full documents.
- [ ] Enumerate first-party documentation separately from bundled skills/reference corpora and generated output.
- [ ] Run the audit workflow only after reviewing artifact visibility and secret-screening limitations; do not publish the raw corpus artifact publicly until it has been reviewed.
- [ ] Run project checks in a disposable environment after inspecting package scripts and lockfiles.
- [ ] Resolve domain and canonical-repository conflicts with source-owner evidence.

## Provenance

This review records the root README blob SHAs returned by GitHub when each file was fetched. Blob SHA equality proves identical file content for those README files; it does not prove identical repository history, license, or entire tree. For the full recursive tree inventory and source commit SHAs, see [SOURCE-AUDIT.md](./SOURCE-AUDIT.md). For integration contracts and release gates, see [INTEGRATION-MATRIX.md](./INTEGRATION-MATRIX.md).
