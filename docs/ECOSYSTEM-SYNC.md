# OCode.js Ecosystem Sync

This repository is the canonical documentation source for the OCode.js ecosystem.

## Behavior

- Runs on commits to `main` and manual workflow dispatch.
- Validates a checked-in target registry.
- Creates one isolated snapshot directory and pull request per configured target.
- Never deletes target files, mirrors with destructive flags, merges pull requests, or deploys production.
- Source README and HTML are renamed to `README.source.md` and `index.source.html` inside snapshots so they cannot replace a target's root website.
- Only allowlisted source paths are accepted. Each destination is a dedicated documentation subdirectory; target application code and root pages are out of scope. The accidental `docs/sercevis` prompt artifact is excluded from generated snapshots.
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

## Failure diagnostics

The sync job authenticates the token once, then checks each configured target independently. A failure for one target must stop work for that target before any clone-dependent copy or Git command runs; the job continues to collect failures from the remaining targets and exits non-zero if any target fails.

| Log symptom | Meaning | Required check |
|---|---|---|
| `Cross-repository token authenticated as ...` followed by `has no effective push permission` | The token is valid but GitHub reports no push permission for this target | Grant the token access to that exact repository with **Contents: write**; organization policy may also restrict access |
| HTTP 403 on push after a successful permission preflight | Git transport push is still blocked despite the REST permission check | Check fine-grained token repository selection, organization token policy, SSO authorization, and branch/ruleset restrictions |
| `Resource not accessible by personal access token` when creating a PR | The token cannot create pull requests in that target | Confirm **Pull requests: write** and that organization policy permits the token |
| `Could not resolve to a Repository` | The token cannot see the repository, or the configured owner/name is wrong | Verify the exact repository URL and that it is included in the token's repository access selection |
| Clone failure followed by missing-directory errors | A downstream error from continuing after clone failed | The workflow must stop that target immediately after clone failure |

A successful `gh api user` check proves authentication only; it does not prove access to every target repository. Never print the token or place it in repository files. Once permissions or repository names are corrected, use **Actions → OCode.js Ecosystem Sync → Run workflow** on `main`. Confirm the resulting run's logs and PR links; a green validation/CI run alone does not establish successful cross-repository sync.

## Important limitation

This workflow creates and updates pull requests only. It deliberately does not auto-merge them or deploy Pages. To publish a target website, that repository's build must explicitly consume the synced path or a maintainer must merge the relevant PR. Automatic PR preparation requires no per-change confirmation after the secret and permissions are configured.

## Extending the registry

Add a target only after checking repository access, licensing, build system, and whether the target site can safely consume the snapshot path. Do not point a destination at a live root `index.html`, application source, environment configuration, or database files. Review each generated PR before merging.
