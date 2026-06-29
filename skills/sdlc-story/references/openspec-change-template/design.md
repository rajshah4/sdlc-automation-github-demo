# Design

## Context

The Petstore catalog stores pet availability in the `status` field. Default search behavior should return available pets only, while explicit status searches can inspect pending pets for support or operational workflows.

## Decision

- Preserve `status="available"` as the default catalog search.
- Ensure web and API available-pets paths do not widen the search to pending pets.
- Add regression coverage for Nova (`pet-103`) staying out of default available results.
- Preserve explicit `status="pending"` searches.

## Risks

- A broad fix could hide pending pets from support workflows that explicitly request them.
- Incident remediation code should stay out of this build path unless the issue explicitly requests operational repair.

## Validation Plan

- Run focused catalog tests for default pending-pet exclusion and explicit pending searches.
- Run cloud/web tests when touched.
- Run the full pytest suite before opening the PR.
