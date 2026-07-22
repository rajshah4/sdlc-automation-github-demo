# Change: Fix Pending Pets Appearing in Available Search

## Why

Customers are seeing pets that should not be available yet in the default catalog search. This creates confusion for customers and generates extra work for operations teams who must handle adoption requests for pets that aren't ready. The default search experience must show only pets with `status="available"` to match product expectations and maintain operational efficiency.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-123
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Jira Request To PR

## Assumptions

- The bug is in the catalog search filtering logic, not in data corruption or external integrations.
- The existing `status` parameter default of `"available"` correctly expresses product intent.
- The fix should preserve the ability for support and operations to explicitly search for pending pets when needed.
- No schema, API, or deployment changes are needed.

## Non-Goals

- Changes to pet status workflow or lifecycle management.
- UI redesign or new filter capabilities.
- Changes to adoption flow or pending pet handling beyond visibility.
- Performance optimization or caching improvements.

## What Changes

- Fix the status filter logic in `app/petstore_app/catalog.py` to ensure it always applies when a status parameter is provided.
- Add test coverage for default search behavior to prevent regression.

## Impact

- App behavior: Default catalog search will correctly exclude pending pets. Explicit pending pet searches remain functional.
- Tests: New test added to verify default search excludes pending pets.
- Humans: Operations teams will no longer receive confused customer inquiries about unavailable pets.

## Human Gates

- Scope approval: Automated from Jira ticket creation.
- Review approval: Human code review required before merge.
- Merge approval: Human approval required.
- Deployment approval: Human approval required before production deployment.
