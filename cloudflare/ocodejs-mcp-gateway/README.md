# OCode.js OAuth-protected MCP Gateway

Combined OAuth Resource Server and read-only OCode.js Docs MCP.

## Target endpoints

- MCP: https://mcp.ocodejs.dev/mcp
- Health: https://mcp.ocodejs.dev/health
- OAuth Protected Resource Metadata: https://mcp.ocodejs.dev/.well-known/oauth-protected-resource/mcp
- Authorization Server: https://auth.ocodejs.dev

## Tools

- `whoami`, `server_info`
- `search_ocodejs_docs`
- `list_ocodejs_docs`
- `get_ocodejs_document`
- `get_ocodejs_project_overview`

Documentation tools only read public files from zskbot/docs-ocodejs main. No GitHub token is needed.

## Security

Every POST to /mcp requires an opaque Bearer token found in the shared OAUTH_KV namespace, with the mcp scope and exact resource claim `https://mcp.ocodejs.dev/mcp`. Token values are never logged or returned. The Worker rejects tokens without the resource claim. Authorization Code + PKCE S256 remains the public-client flow. Health and OAuth metadata are public and non-sensitive. Requests are size- and batch-limited.

## Deployment blockers / prerequisites

1. Cloudflare zone `ocodejs.dev` must become Active.
2. Update and deploy the Authorization Worker at `auth.ocodejs.dev`; it must bind issued access tokens to the exact resource URL and preserve the existing OAUTH_KV namespace and secret bindings.
3. Update the GitHub OAuth App callback URL to `https://auth.ocodejs.dev/github/callback`; this external setting cannot be changed through this repository.
4. Deploy this gateway with the existing OAUTH_KV namespace and attach custom domain `mcp.ocodejs.dev`.
5. Verify OAuth PKCE, token audience rejection, initialize, tools/list and all read-only tools.

The currently inspected live Authorization Worker does not yet store an OAuth resource/audience claim. This gateway intentionally rejects tokens without it, so do not deploy this gateway until the Authorization Worker is upgraded in lockstep. The Cloudflare zone was observed in `initializing` state; custom-domain attachment is blocked until Active.

No secrets are committed. The KV namespace ID is a resource identifier, not a credential.
