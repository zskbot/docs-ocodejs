---
title: Vercel CLI Overview
product: vercel
url: /docs/cli
canonical_url: "https://vercel.com/docs/cli"
last_updated: 2026-10-07
type: reference
prerequisites:
  []
related:
  - /docs/cli/logs
  - /docs/cli/certs
  - /docs/cli/dev
  - /docs/cli/dns
  - /docs/rest-api
summary: Learn how to use the Vercel command-line interface (CLI) to manage and configure your Vercel Projects from the command line.
install_vercel_plugin: npx plugins add vercel/vercel-plugin
---

# Vercel CLI Overview

Vercel gives you multiple ways to interact with and configure your Vercel Projects. With the command-line interface (CLI) you can interact with the Vercel platform using a terminal, or through an automated system, enabling you to [retrieve logs](/docs/cli/logs), manage [certificates](/docs/cli/certs), replicate your deployment environment [locally](/docs/cli/dev), manage Domain Name System (DNS) [records](/docs/cli/dns), and more.


<!-- docsgraph:related -->
## Related pages

> **For AI agents:** Follow these links to understand how this page connects to the rest of the Vercel ecosystem. For the full cross-link map (inbound, outbound, prerequisites, and semantic neighbors), see the .graph.md link below.

- [AI Gateway](https://ai-sdk.dev/providers/ai-sdk-providers/ai-gateway) — Learn how to use the AI Gateway provider with the AI SDK.
- [Vercel Flags](https://flags-sdk.dev/docs/providers/vercel)
- [Terminal commands](https://v0.app/docs/terminal-commands) — v0 can run bash commands in your project sandbox to test, debug, and use platform CLIs. Control its autonomy with three
- [Agent Runs now available in the Vercel MCP and CLI](https://vercel.com/changelog/agent-runs-vercel-mcp-cli)
- [Configure weighted traffic splits for Vercel Flags from the Vercel CLI](https://vercel.com/changelog/configure-weighted-traffic-splits-for-vercel-flags-from-the-vercel-cli)
- [Copy-to-Prompt instructions now available for Flags](https://vercel.com/changelog/copy-to-prompt-instructions-now-available-for-flags)
- [Deploy Hono backends with zero configuration](https://vercel.com/changelog/deploy-hono-backends-with-zero-configuration)
- [Deploy without an account using Vercel CLI](https://vercel.com/changelog/deploy-without-an-account-using-vercel-cli)
- [Can I use my domain on Vercel with A records?](https://vercel.com/kb/guide/a-record-and-caa-with-vercel) — Point your apex domain to Vercel with an A record \\(76.76.21.21 or your domain card's value\\), pair it with a www CNAME,
- [Build AI agents with AI Gateway and AI SDK](https://vercel.com/kb/guide/ai-gateway-and-ai-sdk) — Build AI agents on Vercel with AI Gateway and AI SDK, then make them reliable, capable, and durable with Sandbox, Chat S
- [How to automatically approve tool calls in eve with Jev](https://vercel.com/kb/guide/auto-approve-tool-calls-eve-jev) — Use Jev to review tool calls in eve, allow routine actions, and request human approval when needed. Configure the policy
- [Build with an Express starter template](https://vercel.com/kb/guide/build-with-a-express-starter-template) — Deploy an Express app to Vercel from a template. Browse Express starters from Vercel and the community, then run them lo

Full cross-link map for this page: [/docs/cli.graph.md](/docs/cli.graph.md)
<!-- /docsgraph:related -->

If you'd like to interface with the platform programmatically, check out the [REST API documentation](/docs/rest-api).

## Installing Vercel CLI

To download and install Vercel CLI, run the following command:

**pnpm**

```bash
pnpm i -g vercel
```

**yarn**

```bash
yarn global add vercel
```

**npm**

```bash
npm i -g vercel
```

**bun**

```bash
bun add -g vercel
```

## Updating Vercel CLI

When there is a new release of Vercel CLI, running any command will show you a message letting you know that an update is available.

If you have installed our command-line interface through [npm](http://npmjs.org/) or [Yarn](https://yarnpkg.com), the easiest way to update it is by running the installation command yet again.

**pnpm**

```bash
pnpm i -g vercel@latest
```

**yarn**

```bash
yarn global add vercel@latest
```

**npm**

```bash
npm i -g vercel@latest
```

**bun**

```bash
bun add -g vercel@latest
```

If you see permission errors, please read npm's [official guide](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally). Yarn depends on the same configuration as npm.

To see what changed in each version, browse the [release notes](/docs/cli/release-notes).

## Checking the version

The `--version` option can be used to verify the version of Vercel CLI currently being used.

```bash filename="terminal"
vercel --version
```

*Using the \`vercel\` command with the \`--version\` option.*

## Using in a CI/CD environment

Vercel CLI requires you to log in and authenticate before accessing resources or performing administrative tasks. In a terminal environment, you can use [`vercel login`](/docs/cli/login), which requires manual input. If you don't have a Vercel account yet, you can create one with [`vercel signup`](/docs/cli/signup). In a CI/CD environment where manual input is not possible, you can create a token on your [tokens page](/account/tokens) and then authenticate using one of these methods:

- Set the `VERCEL_TOKEN` environment variable
- Pass the [`--token` option](/docs/cli/global-options#token) to the command

Using the `VERCEL_TOKEN` environment variable is recommended for CI/CD because it avoids exposing the token in command-line arguments, which can be visible in process lists and logs. If both are provided, the `--token` flag takes precedence over the environment variable.

## Experimental native CLI binaries

The standard `vercel` package includes experimental native binaries as optional dependencies for supported platforms. This installation still requires Node.js to run its launcher, even when you use native execution. Install [Vercel CLI](#installing-vercel-cli) with your package manager, keeping optional dependencies enabled, then opt into native execution:

```bash filename="terminal"
vercel upgrade --enable-binary
```

*Enabling native execution for Vercel CLI.*

If the native package is missing because you omitted optional dependencies, reinstall `vercel` with optional dependencies enabled. For an npm installation:

```bash filename="terminal"
npm install --global vercel@latest --include=optional
vercel upgrade --enable-binary
```

*Restoring optional dependencies and enabling native execution.*

Verify the installed version and runtime:

```bash filename="terminal"
vercel --version
```

*Checking the installed Vercel CLI version and execution mode.*

The CLI banner includes `(native)` when it runs the native binary.

On macOS, the package uses its installed native binary by default unless you opt out. To return to Node.js execution, run [`vercel upgrade --disable-binary`](/docs/cli/upgrade#disable-binary).

Linux native packages target glibc. On musl hosts, such as Alpine, the launcher looks for a matching musl package and uses Node.js execution if that package isn't installed. A missing native package falls back to Node.js execution; a failure after native execution starts doesn't retry the command with Node.js execution.

### Migrate from the legacy native package

If you installed `@vercel/vc-native` directly, remove it and install `vercel` with the same package manager. For example, with pnpm:

```bash filename="terminal"
pnpm remove -g @vercel/vc-native
pnpm add -g vercel@latest
vercel upgrade --enable-binary
```

Package-manager upgrades update `vercel`, including when it runs through the native binary. They no longer upgrade the legacy `@vercel/vc-native` wrapper.

## Available Commands

### activity

View activity events for your Vercel project or team, filtered by type, date range, and project.

```bash
vercel activity
vercel activity ls --all --since 30d
vercel activity ls --type deployment --since 7d
```

[Learn more about the activity command](/docs/cli/activity)

### agent

Generate an `AGENTS.md` file in the current project with Vercel deployment best practices for coding agents.

```bash
vercel agent init
vercel agent init --yes
```

[Learn more about the agent command](/docs/cli/agent)

### agent-runs

Find projects with Agent Runs activity, list recent runs, and inspect run metadata and conversation traces.

```bash
vercel agent-runs projects
vercel agent-runs list
vercel agent-runs inspect run_1234567890
vercel agent-runs trace run_1234567890 --json
```

[Learn more about the agent-runs command](/docs/cli/agent-runs)

### ai-gateway

Manage [AI Gateway](/docs/ai-gateway) resources, including API keys, from the CLI.

```bash
vercel ai-gateway api-keys create
vercel ai-gateway api-keys create --name my-key --budget 500 --refresh-period monthly
```

[Learn more about the ai-gateway command](/docs/cli/ai-gateway)

### alerts

List recent alerts for a linked project, a specific project, or an entire team.

```bash
vercel alerts
vercel alerts --all
vercel alerts --project [project-name]
```

[Learn more about the alerts command](/docs/cli/alerts)

### alias

Apply custom domain aliases to your Vercel deployments.

```bash
vercel alias set [deployment-url] [custom-domain]
vercel alias rm [custom-domain]
vercel alias ls
```

[Learn more about the alias command](/docs/cli/alias)

### api

Make authenticated HTTP requests to the Vercel API from your terminal.

```bash
vercel api [endpoint]
vercel api /v2/user
vercel api /v9/projects -X POST -F name=my-project
```

[Learn more about the api command](/docs/cli/api)

### bisect

Perform a binary search on your deployments to help surface issues.

```bash
vercel bisect
vercel bisect --good [deployment-url] --bad [deployment-url]
```

[Learn more about the bisect command](/docs/cli/bisect)

### blob

Interact with Vercel Blob storage to upload, download, list, delete, and copy files.

```bash
vercel blob list
vercel blob put [path-to-file]
vercel blob get [url-or-pathname]
vercel blob del [url-or-pathname]
vercel blob copy [from-url] [to-pathname]
```

[Learn more about the blob command](/docs/cli/blob)

### budgets

Manage your team's [Spend Management](/docs/spend-management) budget: view current on-demand spend, set a budget, and remove it.

```bash
vercel budgets
vercel budgets set --amount 200 --pause --webhook https://example.com/spend
vercel budgets remove --yes
```

[Learn more about the budgets command](/docs/cli/budgets)

### build

Build a Vercel Project locally or in your own CI environment.

```bash
vercel build
vercel build --prod
```

[Learn more about the build command](/docs/cli/build)

### buy

Purchase Vercel products like credits, addons, subscriptions, and domains directly from the CLI.

```bash
vercel buy credits v0 100
vercel buy pro
vercel buy domain example.com
```

[Learn more about the buy command](/docs/cli/buy)

### cache

Manage cache for your project (CDN cache and Data cache).

```bash
vercel cache purge
vercel cache purge --type cdn
vercel cache purge --type data
vercel cache invalidate --tag foo
vercel cache dangerously-delete --tag foo
```

[Learn more about the cache command](/docs/cli/cache)

### certs

Manage certificates for your domains.

```bash
vercel certs ls
vercel certs issue [domain]
vercel certs rm [certificate-id]
```

[Learn more about the certs command](/docs/cli/certs)

### ci

Inspect and rerun [Vercel CI](/docs/ci) runs for your repository. Vercel CI is in Beta.

```bash
vercel ci ls
vercel ci inspect --wait
vercel ci logs --failed
```

[Learn more about the ci command](/docs/cli/ci)

### comments

Review and manage existing [Vercel Toolbar comment threads](/docs/comments) from the terminal.

```bash
vercel comments
vercel comments inspect <thread>
vercel comments resolve <thread> -m 'Fixed in the latest deployment.'
```

[Learn more about the comments command](/docs/cli/comments)

### connect

Manage connectors: create, list, attach to projects, request runtime tokens, and remove them.

```bash
vercel connect create <service>
vercel connect list
vercel connect token <id>
vercel connect attach <id>
vercel connect detach <id>
vercel connect update <id>
vercel connect remove <id>
vercel connect open <id>
```

Run `vercel connect create <service> --help` to see how you can connect to a specific service.

[Learn more about the connect command](/docs/cli/connect)

### contract

View contract commitment information for your Vercel account.

```bash
vercel contract
vercel contract --format json
```

[Learn more about the contract command](/docs/cli/contract)

### crons

Manage [Cron Jobs](/docs/cron-jobs) for a project: add cron entries to `vercel.json`, list them, and trigger them on demand. This command is in beta.

```bash
vercel crons ls
vercel crons add --path /api/cron --schedule "0 10 * * *"
vercel crons run /api/cron
```

[Learn more about the crons command](/docs/cli/crons)

### curl

Make HTTP requests to your Vercel deployments with automatic deployment protection bypass.

```bash
vercel curl [path]
vercel curl /api/hello
vercel curl /api/data --deployment [deployment-url]
```

[Learn more about the curl command](/docs/cli/curl)

### deploy

Deploy your Vercel projects. Default command when no subcommand is specified.

```bash
vercel
vercel deploy
vercel deploy --prod
```

[Learn more about the deploy command](/docs/cli/deploy)

### deploy-hooks

Manage [Deploy Hooks](/docs/deploy-hooks): list, create, and remove deploy hook URLs that trigger new deployments when called.

```bash
vercel deploy-hooks ls
vercel deploy-hooks create cms-rebuild --ref main
vercel deploy-hooks rm hook_abc123
```

[Learn more about the deploy-hooks command](/docs/cli/deploy-hooks)

### dev

Replicate the Vercel deployment environment locally and test your project.

```bash
vercel dev
vercel dev --port 3000
```

[Learn more about the dev command](/docs/cli/dev)

### dns

Manage your DNS records for your domains.

```bash
vercel dns ls [domain]
vercel dns add [domain] [name] [type] [value]
vercel dns rm [record-id]
```

[Learn more about the dns command](/docs/cli/dns)

### domains

Buy, sell, transfer, and manage your domains.

```bash
vercel domains ls
vercel domains add [domain] [project]
vercel domains rm [domain]
vercel domains buy [domain]
vercel domains price [domain] [...domain]
vercel domains check [domain] [...domain]
```

[Learn more about the domains command](/docs/cli/domains)

### env

Manage environment variables in your Vercel Projects.

```bash
vercel env ls
vercel env add [name] [environment]
vercel env update [name] [environment]
vercel env rm [name] [environment]
vercel env pull [file]
vercel env run -- <command>
```

[Learn more about the env command](/docs/cli/env)

### feedback

Send bugs, friction, and feature requests to the Vercel team without logging in or linking a project.

```bash
vercel feedback "The error didn't explain how to fix the issue"
vercel feedback -f product=cli -f type=bug -f actual="Unknown option: --preview"
```

[Learn more about the feedback command](/docs/cli/feedback)

### firewall

Manage your Vercel Firewall: view changes, publish, manage IP blocks, system bypass entries, custom rules, attack mode, and system mitigations.

```bash
vercel firewall overview
vercel firewall publish
vercel firewall ip-blocks block <ip>
vercel firewall rules list
vercel firewall attack-mode enable
```

[Learn more about the firewall command](/docs/cli/firewall)

### flags

Manage feature flags for your Vercel Project.

```bash
vercel flags list
vercel flags evaluations [flag]
vercel flags create [slug]
vercel flags versions [flag] --limit 10
vercel flags versions diff [flag] --revision [number]
vercel flags set [flag] --environment [environment] --variant [variant]
vercel flags segments ls
vercel flags segments create beta-users --add include:user.id=user_123
vercel flags open [flag]
```

[Learn more about the flags command](/docs/cli/flags)

### git

Manage your Git provider connections.

```bash
vercel git ls
vercel git connect
vercel git disconnect [provider]
```

[Learn more about the git command](/docs/cli/git)

### global-config

Manage [Global Config](/docs/global-config) stores: list, create, inspect, update, remove, and manage items, read tokens, and backups. `vercel edge-config` continues to work as an alias.

```bash
vercel global-config list
vercel global-config add flags
vercel global-config items flags --key betaUiEnabled
vercel global-config tokens flags --add "Production read"
vercel global-config backups flags
```

[Learn more about the global-config command](/docs/cli/global-config)

### guidance

Enable or disable guidance messages shown after CLI commands.

```bash
vercel guidance enable
vercel guidance disable
vercel guidance status
```

[Learn more about the guidance command](/docs/cli/guidance)

### help

Get information about all available Vercel CLI commands.

```bash
vercel help
vercel help [command]
```

[Learn more about the help command](/docs/cli/help)

### httpstat

Visualize HTTP request timing statistics for your Vercel deployments with automatic deployment protection bypass.

```bash
vercel httpstat [path]
vercel httpstat /api/hello
vercel httpstat /api/data --deployment [deployment-url]
```

[Learn more about the httpstat command](/docs/cli/httpstat)

### init

Initialize example Vercel Projects locally from the examples repository.

```bash
vercel init
vercel init [project-name]
```

[Learn more about the init command](/docs/cli/init)

### inspect

Retrieve information about your Vercel deployments.

```bash
vercel inspect [deployment-id-or-url]
vercel inspect [deployment-id-or-url] --logs
vercel inspect [deployment-id-or-url] --wait
```

[Learn more about the inspect command](/docs/cli/inspect)

### install

Install a marketplace integration and provision a resource. Alias for `vercel integration add`.

```bash
vercel install <integration-name>
```

[Learn more about the install command](/docs/cli/install)

### integration

Manage marketplace integrations: provision resources, discover available integrations, view setup guides, check balances, and manage individual resources with the nested `resource` subcommand.

```bash
vercel integration add <integration-name> [--claim | --no-claim]
vercel integration list [project]
vercel integration discover
vercel integration guide <integration-name>
vercel integration balance <integration-name>
vercel integration open <integration-name> [resource-name]
vercel integration remove <integration-name>
vercel integration resource connect <resource-name> [project]
vercel integration resource disconnect <resource-name> [project]
vercel integration resource remove <resource-name>
vercel integration resource create-threshold <resource-name> <minimum> <spend> <limit>
vercel integration resource claim [resource-name]
```

The `resource` subcommand is also available as `vercel integration-resource <subcommand>` and `vc ir <subcommand>` (backward-compatible aliases).

[Learn more about the integration command](/docs/cli/integration)

### link

Link a local directory to a Vercel Project.

```bash
vercel link
vercel link [path-to-directory]
```

[Learn more about the link command](/docs/cli/link)

### list

List recent deployments for the current Vercel Project.

```bash
vercel list
vercel list [project-name]
```

[Learn more about the list command](/docs/cli/list)

### login

Login to your Vercel account through CLI.

```bash
vercel login
vercel login [email]
vercel login --github
```

[Learn more about the login command](/docs/cli/login)

### logout

Logout from your Vercel account through CLI.

```bash
vercel logout
```

[Learn more about the logout command](/docs/cli/logout)

### logs

Query runtime log entries and CDN request records for your project.

```bash
vercel logs
vercel logs requests
vercel logs --deployment [deployment-url]
```

[Learn more about the logs command](/docs/cli/logs)

### mcp

Set up MCP client configuration for your Vercel Project.

```bash
vercel mcp
vercel mcp --project
```

[Learn more about the mcp command](/docs/cli/mcp)

### metrics

List and query metrics from your terminal, and inspect the schema to discover available dimensions and aggregations.

```bash
vercel metrics schema
vercel metrics schema <metric-or-prefix>
vercel metrics database.duration_ms --filter 'plan:pro'
vercel metrics <metric_name> --since 7d --granularity 1d --project project-name --prod
vercel metrics <metric_name> --all --group-by projectId --since 24h --prod
```

[Learn more about the metrics command](/docs/cli/metrics)

### microfrontends

Work with microfrontends configuration.

```bash
vercel microfrontends pull
vercel microfrontends pull --dpl [deployment-id]
```

[Learn more about the microfrontends command](/docs/cli/microfrontends)

### monitors

Create, list, inspect, update, and delete monitors for a project or team. Replaces the deprecated `vercel alerts rules` commands.

```bash
vercel monitors ls
vercel monitors add --project my-app --body ./monitor.json
vercel monitors rm [monitor-id]
```

[Learn more about the monitors command](/docs/cli/monitors)

### open

Open your current project in the Vercel Dashboard.

```bash
vercel open
```

[Learn more about the open command](/docs/cli/open)

### pricing

Look up Hobby, Pro, and Enterprise features from the public pricing table.

```bash
vercel pricing
vercel pricing "skew protection"
vercel pricing firewall --json
```

[Learn more about the pricing command](/docs/cli/pricing)

### project

List, add, inspect, remove, and manage your Vercel Projects.

```bash
vercel project ls
vercel project add
vercel project rm
vercel project inspect [project-name]
```

[Learn more about the project command](/docs/cli/project)

### promote

Promote an existing deployment to be the current deployment.

```bash
vercel promote [deployment-id-or-url]
vercel promote status [project]
```

[Learn more about the promote command](/docs/cli/promote)

### pull

Update your local project with remote environment variables and project settings.

```bash
vercel pull
vercel pull --environment=production
```

[Learn more about the pull command](/docs/cli/pull)

### redeploy

Rebuild and redeploy an existing deployment.

```bash
vercel redeploy [deployment-id-or-url]
```

[Learn more about the redeploy command](/docs/cli/redeploy)

### redirects

Manage project-level redirects.

```bash
vercel redirects list
vercel redirects add /old /new --status 301
vercel redirects upload redirects.csv --overwrite
vercel redirects promote <version-id>
```

[Learn more about the redirects command](/docs/cli/redirects)

### remove

Remove deployments either by ID or for a specific Vercel Project.

```bash
vercel remove [deployment-url]
vercel remove [project-name]
```

[Learn more about the remove command](/docs/cli/remove)

### rollback

Roll back production deployments to previous deployments.

```bash
vercel rollback
vercel rollback [deployment-id-or-url]
vercel rollback status [project]
```

[Learn more about the rollback command](/docs/cli/rollback)

### rolling-release

Manage your project's rolling releases to gradually roll out new deployments.

```bash
vercel rolling-release configure --cfg='[config]'
vercel rolling-release start --dpl=[deployment-id]
vercel rolling-release approve --dpl=[deployment-id]
vercel rolling-release complete --dpl=[deployment-id]
```

[Learn more about the rolling-release command](/docs/cli/rolling-release)

### routes

Manage project-level routing rules for your Vercel Project.

```bash
vercel routes list
vercel routes add --ai "Rewrite /api/* to https://backend.internal/*"
vercel routes edit "API Proxy" --dest "https://new-api.example.com/:path*"
vercel routes publish
```

[Learn more about the routes command](/docs/cli/routes)

### sandbox

Interact with [Vercel Sandbox](/docs/sandbox): list, create, connect, and manage sandboxes from the terminal. See the [Sandbox CLI Reference](/docs/sandbox/cli-reference) for the full surface.

```bash
vercel sandbox list
vercel sandbox create --connect
```

[Learn more about the sandbox command](/docs/cli/sandbox)

### security

Inspect the security posture of your Vercel team with checks against vulnerable misconfigurations and settings.

```bash
vercel security
vercel security check --findings
vercel security check [check-name]
```

[Learn more about the security command](/docs/cli/security)

### setup

Set up coding agents for Vercel: install the Vercel plugin for Claude Code and Codex, and connect your agents to AI Gateway.

```bash
vercel setup
vercel setup --gateway
vercel setup --dry-run
```

[Learn more about the setup command](/docs/cli/setup)

### signup

Create a new Vercel account through CLI. Once sign-up is complete, you are signed in with the new account.

```bash
vercel signup
```

[Learn more about the signup command](/docs/cli/signup)

### skills

Discover agent skills relevant to your project, or search the skill catalog.

```bash
vercel skills
vercel skills nextjs
vercel skills nextjs --json
```

[Learn more about the skills command](/docs/cli/skills)

### switch

Switch between different team scopes.

```bash
vercel switch
vercel switch [team-name]
```

[Learn more about the switch command](/docs/cli/switch)

### target

Manage custom environments (targets) and use the `--target` flag on relevant commands.

```bash
vercel target list
vercel target ls
vercel deploy --target=staging
```

[Learn more about the target command](/docs/cli/target)

### teams

List, add, remove, and manage your teams.

```bash
vercel teams list
vercel teams add
vercel teams invite [email]
```

[Learn more about the teams command](/docs/cli/teams)

### telemetry

Enable or disable telemetry collection. Learn [what data Vercel CLI collects](/docs/cli/about-telemetry) and how to opt out.

```bash
vercel telemetry status
vercel telemetry enable
vercel telemetry disable
```

[Learn more about the telemetry command](/docs/cli/telemetry)

### tokens

Manage your personal Vercel authentication tokens: list, create, and revoke API tokens.

```bash
vercel tokens ls
vercel tokens add "CI deploy"
vercel tokens rm tok_abc123
```

[Learn more about the tokens command](/docs/cli/tokens)

### traces

Inspect request traces for your project, and manage the sampling rules that decide which requests Vercel traces.

```bash
vercel traces get [request-id]
vercel traces [request-id]
vercel traces get [request-id] --open
vercel traces config ls
vercel traces config set 25 --environment production
vercel traces config rm --environment production
```

Open a trace directly in the tree or waterfall view:

```bash
vercel traces get [request-id] --open --view=tree
vercel traces get [request-id] --open --view=waterfall
```

[Learn more about the traces command](/docs/cli/traces)

### upgrade

Upgrade the Vercel CLI to the latest version and manage automatic updates.

```bash
vercel upgrade
vercel upgrade --dry-run
vercel upgrade --enable-auto
vercel upgrade --format=json
```

[Learn more about the upgrade command](/docs/cli/upgrade)

### usage

View billing usage and costs for your Vercel account.

```bash
vercel usage
vercel usage --from 2025-01-01 --to 2025-01-31
vercel usage --breakdown daily
```

[Learn more about the usage command](/docs/cli/usage)

### vcr

Manage [Vercel Container Registry](/docs/container-registry) repositories, tags, and images from the terminal. See the [Container Registry CLI Reference](/docs/container-registry/cli-reference) for the full surface.

```bash
vercel vcr ls
vercel vcr login docker
```

[Learn more about the vcr command](/docs/cli/vcr)

### webhooks

Manage webhooks for your account.

```bash
vercel webhooks list
vercel webhooks get <id>
vercel webhooks create <url> --event <event>
vercel webhooks rm <id>
```

[Learn more about the webhooks command](/docs/cli/webhooks)

### whoami

Display the username of the currently logged in user.

```bash
vercel whoami
```

[Learn more about the whoami command](/docs/cli/whoami)


---

[View full sitemap](/docs/sitemap)


If you encounter incorrect information, can’t find what you need, need a capability Vercel doesn’t currently offer, or have any other feedback to report, please do it by following the instructions at https://vercel.com/feedback.md.