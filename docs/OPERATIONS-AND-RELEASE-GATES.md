# Ecosystem Operations and Release Gates

This runbook defines a repeatable release process for the public repositories tracked by this documentation hub. It is a checklist, not a claim that every external deployment or integration is currently healthy.

## Repository responsibilities

| Repository | Responsibility | Minimum verification |
|---|---|---|
| [docs-ocodejs](https://github.com/zskbot/docs-ocodejs) | Canonical documentation index and ecosystem inventory | Markdown/link checks, inventory validation, static build where configured |
| [X-BO](https://github.com/zskbot/X-BO) | Node.js/Vite AI-agent application | npm test, Vercel config validation, frontend build, then a separate staging smoke test |
| [pages_logo](https://github.com/zskbot/pages_logo) | Public brand assets | Manifest validation, SVG/GIF parsing, static-site build |

Other Velclaw repositories are indexed in the ecosystem documents, but should not be assumed to share a runtime, release process, secrets, or deployment target.

## Change workflow

1. Inspect the default branch, current workflow files, open pull requests, and recent run results before changing files.
2. Create a narrowly scoped branch. Do not mix brand changes, runtime changes, and infrastructure changes into one pull request.
3. Add or update regression tests for behavior and security changes. Prefer deterministic tests that do not require paid services or production credentials.
4. Run the repository's configured validation in CI. A successful build does not prove a live deployment is healthy.
5. Review the diff for secrets, populated environment files, unrelated generated files, destructive database changes, and accidental production configuration changes.
6. Open a pull request and report exactly which checks passed, failed, or remain pending.
7. Merge or deploy only through an explicitly authorized release decision. Staging verification must be separate from production deployment.

## X-BO security and runtime gates

- Keep provider credentials server-side in environment variables; never place them in frontend bundles, documentation, asset manifests, or committed example values.
- URL-fetching tools must reject non-public address ranges, validate every redirect target, pin the validated DNS address to the socket, bound response bytes, and enforce a timeout.
- Chat and API routes must validate method and payload, return generic client-facing errors, and avoid leaking provider exception details.
- Treat in-memory rate limits as per-process protection only; they are not a shared/global quota across serverless instances.
- Keep readiness checks shallow and truthful. Do not claim that external providers are healthy unless the check actually verifies them.
- Do not run live provider tests in CI unless credentials and cost are intentionally configured for that workflow.

## Deployment verification

For a staging deployment, record the exact URL and commit SHA, then verify:

- the root page loads without a blank screen or browser-console runtime error;
- the documented health endpoint returns the expected response;
- chat/API routes return a safe validation error for malformed requests and do not expose stack traces;
- a valid provider-backed request succeeds only when staging credentials are configured;
- the logs contain no credentials, tokens, or personal message content beyond the application's documented retention policy.

A repository CI pass is not a substitute for these live checks. If deployment access, secrets, or the hosting project is not available, report the live checks as NOT VERIFIED.

## Reporting status

Use only these labels:

- PASS — the specific check ran and succeeded.
- FAIL — the specific check ran and failed; include the actionable failure.
- PENDING — the check is still running.
- NOT VERIFIED — the check requires unavailable deployment access, credentials, or manual confirmation.

Do not describe all repository workflows as green when only the core project CI passed. Third-party workflows should be repaired only when they correspond to an actual project capability; remove or disable unrelated templates through a separate reviewed change, not as part of a routine feature fix.

## Safety boundaries

This runbook does not authorize production deployments, secret rotation, database migrations, deletion of source files, or merging pull requests. Keep changes branch-based until their checks and review are complete.
