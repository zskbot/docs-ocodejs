# OCode.js Ecosystem Sync

This repository is the canonical documentation source for the OCode.js ecosystem.

## Behavior

- Runs on commits to `main` and manual workflow dispatch.
- Validates a checked-in target registry.
- Creates one isolated snapshot directory and pull request per configured target.
- Never deletes target files, mirrors with destructive flags, merges pull requests, or deploys production.
- Source README and HTML are renamed to `README.source.md` and `index.source.html` inside snapshots so they cannot replace a target's root website.
- Only allowlisted source paths are accepted. Each destination is a dedicated documentation subdirectory; target application code and root pages are out of scope.
- A successful sync run means snapshot PRs were prepared, not that those target websites consume the snapshot or that a Pages deployment succeeded.

## Configured targets

The registry currently includes these 12 repositories:

| Repository | Snapshot destination |
|---|---|
| `zskbot/docs` | `ecosystem/ocodejs` |
| `Velclaw/OCodejs` | `docs/ecosystem/central` |
| `OCodejs/OCodejs` | `docs/ecosystem/canonical` |
| `Velclaw/VelclawHost` | `docs/ocodejs-ecosystem` |
| `Velclaw/VelCli` | `docs/ecosystem/ocodejs` |
| `zskbot/X-BO` | `docs/ecosystem/ocodejs` |
| `Velclaw/velclaw-deploy` | `docs/ecosystem/ocodejs` |
| `Velclaw/Oauth` | `docs/ecosystem/ocodejs` |
| `Velclaw/docs.velclaw.ai` | `docs/ecosystem/ocodejs` |
| `Velclaw/VELCLAW` | `docs/ecosystem/ocodejs` |
| `Velclaw/Velclaw-velclaw-docs-ui-reference` | `docs/ecosystem/ocodejs` |
| `Velclaw/Velclaw-OCodejs` | `docs/ecosystem/ocodejs` |

The connected GitHub integration can currently read and write all 12 target repositories, including `OCodejs/OCodejs`. This confirms access for the connected integration only; it does **not** prove that the separate Actions secret below has the same repository selection or permissions.

## One-time authorization

Create a GitHub fine-grained personal access token (or GitHub App installation token) with access to `zskbot/docs-ocodejs` (read) and **every configured target repository** (Contents: read/write and Pull requests: read/write). If a target is not selected in the token's repository access list, the sync workflow will fail for that target and report an overall failure even if other targets succeed.

Store it as Actions secret `OCODEJS_SYNC_TOKEN` in `zskbot/docs-ocodejs`:
https://github.com/zskbot/docs-ocodejs/settings/secrets/actions/new

Do not commit the token or put it in source files. Prefer a GitHub App token or short-lived fine-grained token over a classic PAT. Earlier sync attempts reported HTTP 403 for `Velclaw/OCodejs`; re-check the token's repository selection and Contents/Pull requests permissions before expecting all targets to pass. Never paste the token into chat, an issue, or a committed file.

## Important limitation

This workflow creates and updates pull requests only. It deliberately does not auto-merge them or deploy Pages. To publish a target website, that repository's build must explicitly consume the synced path or a maintainer must merge the relevant PR. Automatic PR preparation requires no per-change confirmation after the secret and permissions are configured.

## Extending the registry

Add a target only after checking repository access, licensing, build system, and whether the target site can safely consume the snapshot path. Do not point a destination at a live root `index.html`, application source, environment configuration, or database files. Review each generated PR before merging.
