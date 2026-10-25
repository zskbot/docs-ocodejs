# OCode.js Docs MCP

Read-only remote MCP server for the public [zskbot/docs-ocodejs](https://github.com/zskbot/docs-ocodejs) repository.

## Endpoint

- MCP Streamable HTTP: `https://ocodejs-docs-mcp.<your-subdomain>.workers.dev/mcp`
- Health: `https://ocodejs-docs-mcp.<your-subdomain>.workers.dev/health`

## Tools

- `search_ocodejs_docs({ query, limit? })` — search relevant documentation and return excerpts.
- `list_ocodejs_docs({ prefix?, limit? })` — list repository documentation paths.
- `get_ocodejs_document({ path })` — read a specific public text document.
- `get_ocodejs_project_overview({})` — return the project overview, roadmap, and design references.

## Security and scope

This server only reads public text files from the repository's `main` branch. It does not write to GitHub, access private repositories, or expose API keys. It has no GitHub token or other secret binding. It is intentionally stateless and read-only.

## Connect

Configure an MCP client with the deployed `/mcp` endpoint and Streamable HTTP transport. Verify the live endpoint using `/health` before connecting a client.
