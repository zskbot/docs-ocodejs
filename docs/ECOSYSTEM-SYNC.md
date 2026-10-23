# OCode.js Ecosystem Sync

This repository is the canonical documentation source for the OCode.js ecosystem.

## Behavior

- Runs on commits to `main` and manual workflow dispatch.
- Validates a checked-in target registry.
- Creates one isolated snapshot directory and pull request per configured target.
- Never deletes target files, mirrors with destructive flags, merges pull requests, or deploys production.
- Source README and HTML are renamed to `README.source.md` and `index.source.html` inside the snapshot so they cannot replace a target's root website.
- Add additional repositories to `.sync/targets.json`; only allowlisted source paths are accepted.

## One-time authorization

Create a GitHub fine-grained personal access token (or GitHub App installation token) with access to these repositories:

- `zskbot/docs-ocodejs` (read)
- `zskbot/docs` (Contents: read/write, Pull requests: read/write)
- `Velclaw/OCodejs` (Contents: read/write, Pull requests: read/write)
- `Velclaw/VelclawHost` (Contents: read/write, Pull requests: read/write)

Store it as Actions secret `OCODEJS_SYNC_TOKEN` in `zskbot/docs-ocodejs`:
https://github.com/zskbot/docs-ocodejs/settings/secrets/actions/new

Do not commit the token or put it in source files. Prefer a GitHub App token or short-lived fine-grained token over a classic PAT.

## Important limitation

This first rollout creates and updates pull requests; it deliberately does not auto-merge them or deploy Pages. To publish a target website, that repository's build must explicitly consume the synced path or a maintainer must merge the PR. Automatic PR creation requires no per-change confirmation after the secret is configured.

## Extending the registry

Each target has a dedicated destination path. New targets should be added only after checking repository permissions, build system, and whether the target site can safely consume that path. Do not point a destination at a live root `index.html`, source code, environment configuration, or database files.
