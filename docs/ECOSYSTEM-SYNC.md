# Ecosystem synchronization — discontinued

**Status:** discontinued on 2026-10-25. This page is retained as a brief historical note only.

The docs-ocodejs project is now focused on developing and validating its own documentation site. Automated cross-repository snapshot pushes and pull-request preparation are out of scope.

The former workflow failed because the Actions token could authenticate but could not push to multiple configured repositories. Repeated retries would not fix those permission failures. The sync workflow and its target registry are being removed rather than asking the owner to keep repairing token access.

## What remains in scope

- Maintain the repository inventory as reference data.
- Link to source projects and record evidence for claims.
- Validate this repository's Markdown, HTML, navigation, and documentation metadata.
- Keep all source repositories independent.

## What is no longer performed

- No scheduled or push-triggered cross-repository synchronization.
- No automated branches or pull requests in other repositories.
- No cross-repository token is required for normal documentation development.
- No claim that linked repositories have received updates.

Historical runs and pull requests remain in GitHub for auditability. This document does not authorize any new synchronization.
