# OCodeJS Brand Standardization and Repository Identity Audit

**Audit date:** 2026-11-12  
**Status:** initial inventory and migration plan; no repository slug, default branch, production setting, or secret was changed.

## Objective

Standardize first-party OCodeJS products under one recognizable brand while preserving each product's real identity, package compatibility, repository history, licenses, and deployment contracts.

This is not an instruction to rename every repository owned by `zskbot` or `OCodejs`. Ownership alone does not make a repository an OCodeJS product.

## Access and inventory evidence

- GitHub App installations for `zskbot` (157989553) and `OCodejs` (178697698) now report `repository_selection=all`.
- GitHub repository search for `user:zskbot` returned 558 results across six pages (100 + 100 + 100 + 100 + 100 + 58).
- GitHub repository search for `org:OCodejs` returned 39 results. The organization installation repository listing returned 45 repositories. Search and installation listing are different API views; use the installation listing as the organization access inventory and investigate the six-item discrepancy before claiming a fully reconciled inventory.
- The installation repository listing endpoint returned only the first 100 `zskbot` entries; search pagination was used to establish the 558-result search inventory.
- Search results are a point-in-time inventory, not proof that every repository is first-party, active, non-fork, or eligible for branding changes.

## Canonical brand rules

1. Public product brand: **OCodeJS**. Use **OCode.js** only where it is the established product/package spelling and changing it would create compatibility or historical confusion.
2. Repository slugs use lowercase kebab-case and a clear product prefix where the repository is first-party and the new slug is unambiguous.
3. Package names are independent from repository slugs. Do not rename an npm package solely to match a repository slug; preserve published package identifiers and semver compatibility.
4. Keep independent products independent. Authentication, chat, docs, profile, CLI, framework, and utility-library repositories may use the OCodeJS brand but must retain distinct product names and README scopes.
5. Do not rebrand upstream forks, vendored source, examples, mirrors, or third-party projects. Preserve upstream attribution and license terms.
6. Never rename a repository until workflows, badges, package repository URLs, GitHub Pages settings, deployment integrations, OAuth callback URLs, webhooks, docs links, and consumer references have been inventoried.
7. All source changes go through a topic branch and PR. No merge, production deployment, DNS edit, secret change, database migration, or paid resource action is included in this plan.

## First-party candidate inventory

The following candidates are supported by repository names and the sampled README/package metadata. Each still needs a complete tree/fork/consumer audit before a slug change.

| Current repository | Observed identity | Recommended display identity | Slug decision |
|---|---|---|---|
| `OCodejs/OCodejs` | JavaScript/TypeScript utility library; package `ocode-js` v0.1.0; README says early development and not yet published to npm | OCodeJS Utility Library | Keep current slug as canonical candidate. Package identity remains `ocode-js`. |
| `zskbot/OCodeJS` | Utility toolkit README; package `ocode-js`; README links canonical issues and CI to `OCodejs/OCodejs` | OCodeJS Utility Library mirror/candidate duplicate | Do not rename or merge until fork status, tree divergence, release history and ownership are compared. |
| `zskbot/ask-ocodejs` | React/Vite AI agent/chat app; package `ask-ocodejs` | Ask OCodeJS | Current slug is already clear; standardize display spelling and badges after CI/link audit. |
| `OCodejs/ask-chatbot` | OCodeJS chatbot application (metadata sampled by repository inventory only) | OCodeJS Chatbot | Candidate slug: `ocodejs-chatbot`; verify overlap with Ask OCodeJS before choosing one canonical app. |
| `zskbot/docs-ocodejs` | OCodeJS documentation hub and ecosystem governance docs | OCodeJS Documentation Hub | Current slug is already clear; keep. |
| `OCodejs/ocodejs.github.io` | OCodeJS GitHub Pages/docs/dashboard repository | OCodeJS Developer Portal | Current slug is already clear; keep. |
| `zskbot/ocodejs-api` | API project | OCodeJS API | Current slug is already clear; keep. |
| `OCodejs/mcp.auth.ocodejs` | OCodeJS authentication/MCP service | OCodeJS Auth | Candidate slug: `ocodejs-auth`; first reconcile with `zskbot/mcp.server.auth`. |
| `zskbot/mcp.server.auth` | README identifies Velclaw Identity Auth; package is `mcp-server-auth`; Auth.js, Prisma/PostgreSQL | Velclaw Identity Auth (not OCodeJS by default) | Keep outside OCodeJS rebrand unless product owner explicitly confirms it is the shared OCodeJS auth service. |
| `zskbot/OCodejs-Profile` | Profile repository; only minimal README observed | OCodeJS Profile | Candidate slug: `ocodejs-profile`; verify owner, dependencies, and deployment links first. |
| `OCodejs/cli`, `OCodejs/cli-hub`, `OCodejs/studio` | CLI, hub, and studio products by repository identity | OCodeJS CLI / CLI Hub / Studio | Keep separate; inspect package metadata and user-facing names before any slug change. |
| `OCodejs/THU365` | THU365 product | THU365 | Keep independent; do not force OCodeJS prefix. |

## Separate products and upstream/source repositories

- `zskbot/woww`: treat as the Woww framework product, not as OCodeJS merely because it is owned by the same account. A future integration may be documented as a separate product.
- `zskbot/v0-sdk`, `zskbot/claude-code-action`, `zskbot/codespaces-nextjs`, `zskbot/skills-github-pages`, and other upstream-derived repositories: inspect fork metadata and LICENSE before any rename or branding. Do not erase upstream identity.
- `zskbot/skills.md` and skill collections: preserve source attribution and distinguish authored OCodeJS skills from imported/vendor content.
- Repositories unrelated to OCodeJS (including personal experiments, infrastructure, and unrelated upstream mirrors) are excluded from this brand migration even though they appear in the owner's GitHub inventory.

## Required gates before a repository slug change

For each candidate, record:

- repository ID, owner, visibility, fork/parent, archived status, default branch, and latest commit;
- package name/version, `repository`, `homepage`, `bugs`, lockfile/workspace references;
- README badges, raw GitHub URLs, Pages source/custom domain, Actions workflows and checkout references;
- Vercel/Netlify/Cloudflare project linkage, webhook and deploy integration references;
- OAuth redirect/callback URLs and API consumers;
- docs, issue templates, release workflows, npm provenance, and external backlinks;
- license/provenance and any mirrored upstream content.

A slug rename must preserve repository ID/history and be followed by a verified redirect and updated references. If the connector cannot perform a repository rename, do not simulate it by creating a new repository; use GitHub's supported repository settings workflow only after the audit and owner approval.

## Execution sequence

1. Reconcile the 45 organization installation entries with the 39 organization search results.
2. Build a deduplicated inventory of all 603 search/list results and classify first-party, fork, mirror, archived, upstream, and unrelated projects.
3. Compare the two `ocode-js` repositories and resolve the canonical source.
4. Resolve overlap between `OCodejs/ask-chatbot` and `zskbot/ask-ocodejs`, and between the two auth repositories.
5. Standardize display names, README headings, descriptions, badges and metadata for confirmed first-party projects in small PRs.
6. Prepare an exact old-slug → new-slug map with dependency evidence.
7. Perform slug changes only through a supported GitHub repository rename operation, then update and verify all references.
8. Run CI and Preview checks; leave all PRs unmerged until owner review.

## Current execution limits

The connected GitHub toolset supports repository file changes, branches and pull requests, but the available actions do not expose a repository-rename operation. Therefore this PR establishes the verified inventory and safe migration plan; it does not claim that repository slugs have been changed. No production systems or secrets were touched.
