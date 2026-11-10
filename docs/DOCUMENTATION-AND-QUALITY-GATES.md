# Documentation, Testing & Change-Control Standard

This standard applies to this documentation hub and its ecosystem integrations. It complements the protected interface rules in [DESIGN_SYSTEM.md](../DESIGN_SYSTEM.md).

## Evidence labels

Use these labels in reviews and reports:

| Label | Meaning | Minimum evidence |
|---|---|---|
| Documented | A source claims or describes it | Link to the source document |
| Source-observed | A specific file/configuration was inspected | Repository, path and revision |
| Test-verified | A named test passed | Command/workflow, commit and result |
| Runtime-verified | A process or endpoint was exercised | Environment, steps and observed result |
| Production-ready | Release gates and owner approval are complete | Security, reliability, rollback, monitoring and approval evidence |

Do not upgrade the label without new evidence.

## Change safety

1. Inspect the current file and repository state before editing.
2. Keep the diff limited to the requested task; do not combine unrelated UI changes.
3. Preserve secrets: do not write tokens, API keys, credentials, populated environment files or private customer data into docs, issues, logs or commits.
4. Never change production environment variables, databases, DNS, OAuth callbacks or deployment targets as a side effect of documentation work.
5. For source changes, prefer a branch and pull request. If a direct commit is explicitly used, report that fact plainly.
6. Re-read every changed file after writing and check links, filenames, case sensitivity and Markdown structure.
7. Report checks that were actually run. If no runner or deployment status is available, say so.

## Canonical interface protection

The OCode.js interface is the default design reference. Without explicit owner approval, do not change its:

- layout, section order, spacing or responsive behavior;
- colors, typography, border thickness or effects;
- animated logo, brand mark or navigation;
- page shell or reusable visual components.

Content, API, test and documentation changes should avoid touching the canonical UI. If a task appears to require a UI change, stop and ask for specific authorization. See [DESIGN_SYSTEM.md](../DESIGN_SYSTEM.md).

## Documentation quality checklist

- [ ] Product identity and repository name are correct.
- [ ] Statements are supported by source or clearly labeled as plans.
- [ ] Code examples use real, verified APIs and do not invent package exports.
- [ ] Node/runtime/package requirements match package metadata and CI.
- [ ] Links point to existing files and use correct case.
- [ ] External assets have appropriate licensing and attribution.
- [ ] Security-sensitive instructions include staging, authorization and rollback notes.
- [ ] No secrets, personal data or production credentials are included.
- [ ] Canonical UI files are unchanged unless specifically authorized.
- [ ] The change log identifies commit and actual verification status.

## Library and framework release gates

For the utility library:
- clean dependency installation;
- unit and edge-case tests;
- TypeScript/type checks where configured;
- HTTP timeout, cancellation and failure tests where applicable;
- package-content dry run and license review;
- API reference reconciled with actual exports.

For a proposed full-stack framework:
- owner-approved scope and architecture decision;
- explicit routing, rendering, handler and compatibility contracts;
- end-to-end examples and tests;
- security review for request handling, secrets and server/client boundaries;
- no public support claims before the documented gates pass.

## Ecosystem sync requirements

- Validate the target list before running.
- Skip repositories whose license or permissions do not permit copying.
- Never overwrite project-specific content without a reviewed diff.
- Keep sync changes idempotent and scoped.
- Log repository name, commit/PR link, result and reason for skips; never log secret values.
- Do not equate a successful file write with a successful Pages deployment.
