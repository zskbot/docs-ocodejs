# OCode.js OAuth Authorization Worker

Source for the OAuth authorization server at `https://auth.ocodejs.dev`.

- Authorization Code grant only.
- PKCE S256 required.
- Dynamic public-client registration validates HTTPS redirect URIs (localhost allowed for development).
- GitHub OAuth is the upstream identity provider.
- Access tokens are opaque, random, single-hour KV records.
- Resource indicator is mandatory and fixed to `https://mcp.ocodejs.dev/mcp`.
- Resource is carried through authorization transaction, authorization code and token record; token exchange verifies it exactly.
- Existing GitHub OAuth client ID/secret remain Cloudflare secret bindings and are never committed.

Before deploying, update the GitHub OAuth App callback URL to `https://auth.ocodejs.dev/github/callback`. Preserve the existing OAUTH_KV namespace and secret bindings. Do not deploy until zone `ocodejs.dev` is Active and custom domain TLS is ready.
