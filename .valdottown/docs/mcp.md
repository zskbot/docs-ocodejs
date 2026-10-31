---
title: MCP
description: Connect an app to the Val Town remote MCP server
updated: 2026-09-10
---

Val Town’s MCP server lets compatible AI apps read, edit, run, and deploy vals.

First, check the
[setup guide for the AI agent you use](/guides/prompting/plugin). For the most
popular AI agents, the Val Town plugin packages our MCP with platform skills,
and usually takes fewer setup steps.

If you're not able to install the plugin or are using a different AI agent,
continue with these instructions.

## Server details

For an app that supports remote MCP with OAuth, use this server URL:

```text
https://api.val.town/v3/mcp
```

- **Name:** Val Town
- **Transport:** Streamable HTTP
- **Authentication:** OAuth. Sign in to Val Town and approve access when
  prompted.
- **Client ID and secret:** leave optional advanced fields empty.

You don’t need to copy an API key for the OAuth setup.

## Connect your app

- **[Claude web or desktop](/guides/prompting/claude#add-a-custom-connector):**
  add a custom connector, then select Connect.
- **[ChatGPT](/guides/prompting/chatgpt):** install the published Val Town
  plugin. You don’t need developer mode for that path.
- **[Claude Code](/guides/prompting/claude-code#alternative-mcp-only):** add the
  server from your terminal, then use `/mcp` inside Claude Code to authenticate.
- **[Codex](/guides/prompting/openai-codex) or
  [Cursor](/guides/prompting/cursor):** follow the app’s guide for its plugin or
  MCP settings.
- **Another compatible app:** add the server URL in its remote MCP settings,
  save, and complete the browser sign-in flow.

Adding the URL and authorizing access may be separate steps. Avoid adding a
second connection if your installed Val Town plugin already includes one.

## Check the connection

Start a new chat or session and send:

```text
Use Val Town to list my vals. Don’t create or change anything.
```

A response from Val Town listing your vals, even an empty list, confirms the
connection.

## Troubleshooting

- **No tools appear:** check that the server is enabled and start a new session.
- **Authentication required:** select Connect or Authenticate in your app’s MCP
  settings and finish signing in.
- **It works in one app but not another:** each app needs its own setup. Local
  CLI configuration doesn’t configure a hosted web chat.
- **The app rejects the URL:** confirm it supports remote Streamable HTTP MCP
  and OAuth. Follow its current MCP documentation.
- **An administrator blocked the connection:** ask your workspace administrator
  to allow it.

Need help? Tell us your app and the step that failed in
[Discord](https://discord.val.town/). Don’t share tokens or other credentials.