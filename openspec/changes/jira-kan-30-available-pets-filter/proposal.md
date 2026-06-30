# Change: Fix Available Pets Catalog Filter

## Why

The default customer-facing pet catalog is showing pets with `status="pending"` when it should only display pets with `status="available"`. This violates the documented catalog availability rules and creates a poor customer experience by showing animals that cannot be adopted.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-30
- Trigger: Jira webhook event `jira:issue_created`
- Automation: SDLC Automation Demo - Jira-to-PR with context sidekick

### Evidence Waypoints

**Stop 1 - Ticket**: Jira KAN-30 reports that the available pets page includes animals that should not be adoptable.

**Stop 2 - Wiki/Docs**: `docs/wiki/petstore-catalog-availability.md` explicitly states:
- Default customer-facing catalog search must show only pets with `status="available"`
- Support and operations workflows may explicitly request `status="pending"` when investigating a case
- Pending pets must not appear in the default available-pets experience
- Nova is `pet-103` with `status="pending"`

**Stop 3 - Logs**: `docs/logs/pending-pet-visible.ndjson` shows `PENDING_PET_VISIBLE` error:
```json
{"timestamp":"2026-06-29T12:00:00Z","service":"software-factory-petstore","component":"petstore-web","operation":"web.available_pets","severity":"ERROR","error_code":"PENDING_PET_VISIBLE","incident":{"type":"petstore_website_catalog_regression","safe_to_remediate":true},"pending_pet_ids":["pet-103"],"customer_impact":"Pending pets were visible in the available-pets experience."}
```

## Assumptions

- The catalog module is the correct place to enforce this filter
- The web app (`cloud_run_app.py`) has its own incident mode logic that is separate from this fix
- No database or external API changes are required
- The fix should be minimal and focused on the catalog search behavior

## Non-Goals

- Changing the web app's incident mode detection logic
- Modifying the UI beyond what naturally reflects the fixed backend behavior
- Adding new search capabilities or filters
- Changing the behavior of explicit `status="pending"` requests

## What Changes

Fix the `search_pets` function in `app/petstore_app/catalog.py` to properly enforce the default status filter. The current implementation accepts `status` as a parameter but doesn't ensure it defaults correctly when not provided.

## Impact

- App behavior: Default catalog searches will correctly exclude pending pets
- Tests: Add regression test to verify pending pets are excluded from default searches
- Humans: Code review required; QA validation required; merge approval required; deployment decision required

## Human Gates

- Scope approval: Human approves the proposed fix approach
- Review approval: Human reviewer approves the code changes
- Merge approval: Human approves merging the PR
- Deployment approval: Human decides when/if to deploy to production
