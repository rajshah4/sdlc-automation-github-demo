# Change: Pet Size Filter

## Why

Adopters need to find pets that fit their home environment. A small apartment may only accommodate small pets, while a house with a large yard can support large pets. Adding a size filter helps adopters quickly narrow down pets that match their living situation.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-107
- Trigger: Jira webhook automation
- Automation: replicated-factory-20260715-141448

## Assumptions

- Pet size can be categorized as "small", "medium", or "large" based on typical species characteristics
- Cats and rabbits are generally "small"
- Dogs can be "small", "medium", or "large" (we'll default existing dog to "medium" and add variety if needed)
- Size is a descriptive attribute that helps with search; it does not affect adoption eligibility
- The filter is optional; leaving it unset preserves normal catalog behavior
- Size filtering works alongside existing status, species, and tag filters

## Non-Goals

- Dynamic size calculation based on weight or breed
- Size-based adoption restrictions or policies
- UI redesign beyond adding the filter control
- Persistence or database schema changes
- New dependencies or external services

## What Changes

- Add a `size` field to the Pet dataclass
- Update existing pet fixtures with appropriate size values
- Add optional `size` parameter to `search_pets()` function
- Add size filter dropdown to the web UI
- Add focused tests for size filtering behavior

## Impact

- App behavior: Adopters can filter the pet catalog by size (small/medium/large)
- Tests: New tests verify size matching, exclusion, and default behavior
- Humans: Code review and merge approval required before this reaches production

## Human Gates

- Scope approval: Needed if size categorization logic is incorrect
- Review approval: Required for all code changes
- Merge approval: Required by branch protection
- Deployment approval: Required for production release
