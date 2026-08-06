# Change: Fix Pending Pet Visibility in Default Search

## Why

Support reports that customers are seeing pets with "pending" status in the default available-pets catalog experience. This creates confusion for customers who try to start adoption flows for pets that are not yet ready for adoption, and generates extra work for operations teams who must explain the situation. The default catalog search must show only pets with status="available" to protect customers and operations from incomplete adoption workflows.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-109
- Trigger: Replicated Jira delegated factory
- Automation: story-to-pr work cell
- Run ID: replicated-factory-20260715-144519

## Assumptions

- The catalog availability rules in `docs/wiki/petstore-catalog-availability.md` are correct: default search must show only available pets.
- The log evidence in `docs/logs/pending-pet-visible.ndjson` with error code `PENDING_PET_VISIBLE` is accurate and indicates a catalog regression.
- Nova (pet-103) is a known demo pet with `status="pending"` that should not appear in default available-pets results.
- Explicit `status="pending"` searches by support and operations must continue to work.
- The bug is caused by incorrect handling of empty or falsy status values in the search filter logic.

## Non-Goals

- Schema changes or new database fields
- UI changes (the fix is backend-only)
- New payment, billing, or authentication features
- Changes to adoption workflows beyond catalog filtering
- Infrastructure or deployment changes

## What Changes

- Fix the status filter logic in `app/petstore_app/catalog.py` to enforce default `status="available"` filtering even when empty strings or other falsy status values are provided.
- Add focused regression tests to prove pending pets stay out of default search results.

## Impact

- App behavior: Default catalog search will correctly filter out pending pets.
- Tests: New tests will prevent regression of this catalog availability bug.
- Humans: Operations will receive fewer customer confusion escalations; code review and merge approval are required before deployment.

## Human Gates

- Scope approval: Automated based on sparse Jira ticket; human can reject or refine during PR review.
- Review approval: Required before merge.
- Merge approval: Required.
- Deployment approval: Required before changes reach production.
