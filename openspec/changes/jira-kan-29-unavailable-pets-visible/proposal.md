# Change: Fix available pets list showing unavailable animals

## Why

Customers report that the available pets page includes animals that should not be adoptable. According to the Petstore catalog availability rules, the default customer-facing catalog search must show only pets with `status="available"`. Pending pets must not appear in the default available-pets experience.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-29
- Trigger: Jira webhook `jira:issue_created` with label `control-experiment`
- Automation: SDLC Automation Demo - Jira-to-PR control work cell

## Assumptions

- The bug is in the backend `search_pets()` catalog filter logic
- No schema migration, auth changes, or new dependencies are needed
- The fix can be validated with existing test infrastructure
- Pending pets must remain queryable when explicitly requested via `status="pending"`

## Non-Goals

- Changing the UI behavior beyond reflecting the corrected backend filter
- Modifying pet data structure or adding new status values
- Altering cloud deployment, secrets, or infrastructure
- Changing adoption workflow or payment logic

## What Changes

- Fix the catalog filter in `app/petstore_app/catalog.py` to ensure empty status parameters are treated as requests for available pets only
- Add regression tests to verify pending pets never appear in default available-pet searches
- Validate that explicit pending-status searches still work correctly

## Impact

- App behavior: Default pet searches will correctly exclude pending pets; explicit pending searches remain functional
- Tests: New regression tests added to prevent future catalog filter bugs
- Humans: Requires PR review, merge approval, and deployment approval

## Human Gates

- Scope approval: Automation proposes fix; humans verify scope matches business requirement
- Review approval: Humans review code changes, tests, and evidence
- Merge approval: Humans approve merge after review
- Deployment approval: Humans control deployment to production
