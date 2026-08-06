# Change: Pet Training Level Filter

## Why

Adopters want to find pets that match their household experience level and available time for training. Adding an optional training level filter helps adopters make better-informed adoption decisions.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-106
- Trigger: Replicated SDLC Factory Jira delegation
- Automation: Story-to-PR work cell

## Assumptions

- Training levels use the existing `tags` field with normalized training keywords
- Training levels include: "basic", "intermediate", "advanced"
- Pets can have zero or one training level tag
- The filter uses substring matching on pet tags to find training levels
- Leaving the filter unset preserves normal catalog behavior (all available pets)
- This is backend-only; no UI changes are required unless explicitly requested

## Non-Goals

- Adding new training level data fields to the Pet dataclass
- Creating a separate training level database or persistence layer
- UI changes (static web interface)
- Training certification or validation systems
- Paid training program features
- Historical training data or progress tracking

## What Changes

- Add optional `training_level` parameter to `search_pets()` function
- Filter pets by training level tag when parameter is provided
- Preserve existing search behavior when training_level is None
- Return only pets with matching training level tags when filter is active

## Impact

- App behavior: Catalog search supports an optional training level filter
- Tests: New tests cover matching, exclusion, and default behavior
- Humans: Code review approval required before merge

## Human Gates

- Scope approval: Story accepted from Jira KAN-106
- Review approval: Required via GitHub PR review
- Merge approval: Required via GitHub PR review
- Deployment approval: Out of scope for this change
