# Change: Fix Pending Pets Visible in Catalog

## Why

Support reports that customers are able to see and start adoption flows for pets with "pending" status that should not be available yet. This creates confusion for customers and extra work for operations staff who must handle invalid adoption requests.

## Source

- GitHub issue: (Delegated from Jira KAN-105)
- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-105
- Run ID: `replicated-factory-20260715-135634`
- Automation: Replicated Jira Delegated Factory

## Assumptions

- The bug is in the `visible_pets()` function in `cloud_run_app.py` which returns all pets (including "pending" status) when in incident mode
- The default behavior should always filter to "available" status only, regardless of operational mode
- The incident mode is intended for observability and error simulation, not for changing core business logic about which pets are visible
- No UI changes are needed; fixing the backend filter is sufficient

## Non-Goals

- Adding new pet statuses beyond "available" and "pending"
- Implementing a UI toggle to show/hide pending pets
- Adding authentication or authorization for viewing different pet statuses
- Changing the adoption validation logic (already correctly rejects pending pets)
- Adding payment processing, persistence, or new services

## What Changes

- Update `visible_pets()` function to always filter to "available" status only
- Keep incident mode for observability (logging, health check failures) but not for business logic
- Maintain existing test coverage for catalog filtering

## Impact

- App behavior: Customers will only see available pets, even when incident mode is active
- Tests: Existing tests should pass; may add regression test for incident mode
- Humans: Operations team will receive fewer invalid adoption requests

## Human Gates

- Scope approval: Required before implementation
- Review approval: Required before merge
- Merge approval: Required from repository maintainer
- Deployment approval: Required before production rollout
