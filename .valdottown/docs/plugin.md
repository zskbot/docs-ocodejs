---
title: Plugin
description: Connect Claude, ChatGPT, Claude Code, Codex, or Cursor to Val Town
updated: 2026-09-10
---

Connect your AI agent to Val Town to read, build, and deploy vals. Choose the AI
agent surface you use for its shortest setup path:

| Your AI agent                       | Start here                                                              |
| ----------------------------------- | ----------------------------------------------------------------------- |
| Claude web or desktop               | [Install the plugin or add a connector](/guides/prompting/claude)       |
| ChatGPT web or desktop              | [Open the Val Town plugin listing](/guides/prompting/chatgpt)           |
| Claude Code CLI                     | [Install from Claude Code’s marketplace](/guides/prompting/claude-code) |
| Codex desktop or CLI                | [Install from the plugin browser](/guides/prompting/openai-codex)       |
| Cursor                              | [Install from Cursor’s plugin browser](/guides/prompting/cursor)        |
| Another app with remote MCP support | [Add the Val Town MCP server](/guides/prompting/mcp)                    |

You’ll install the integration, connect your Val Town account, then check it in
a new chat.

## Plugin, connector, or MCP?

- **MCP** is the protocol your agent uses to call Val Town tools, such as
  reading files, editing code, and checking logs.
- A **connector** is the connection to your Val Town account. You authorize it
  by signing in and approving access.
- A **plugin** packages tools and instructions for a particular AI app. The Val
  Town plugin includes its MCP connection and platform skills.
- **Skills** teach the agent Val Town conventions, including HTTP handlers, cron
  jobs, email, storage, and integrations.

These names vary between apps. Installing a plugin and connecting your account
can be separate steps. Follow the guide for the AI app you use; you don’t need
to configure MCP separately if its plugin already provides it.

## Check the connection

Start a new chat or session after installation and send:

```text
Use Val Town to list my vals. Don’t create or change anything.
```

A response from Val Town listing your vals, even an empty list, confirms the
connection. If the agent only explains how to list vals, ask it to use the Val
Town tools.

## Troubleshooting

- **Installed, but the agent can’t see Val Town:** start a new chat or session
  and check that the plugin is enabled.
- **Val Town appears, but requests fail:** finish signing in through the plugin
  or connector settings. Reconnect if authorization has expired.
- **No plugin or connector controls:** check your app’s plan and workspace
  policy. A workspace administrator may need to allow the integration. The
  [Claude guide](/guides/prompting/claude) also has a custom connector option.
- **The agent tries to run an installer in a web chat:** use the app’s plugin or
  connector settings instead.
- **A command ran, but nothing was installed:** check whether it only added a
  marketplace. In Codex, you still need to open the plugin browser and install
  Val Town.

If you need help, tell us your app, whether you use web, desktop, or CLI, and
which step failed in [Discord](https://discord.val.town/). Don’t share tokens or
other credentials.

## What you can build

The plugin can list, read, create, edit, run, and deploy vals; view logs; query
SQLite and Blob storage; and work with environment variables, branches, and
version history.

After checking the connection, try: “Build a daily email digest on Val Town.”

Explore the plugin’s source and skills at
[github.com/val-town/plugins](https://github.com/val-town/plugins).