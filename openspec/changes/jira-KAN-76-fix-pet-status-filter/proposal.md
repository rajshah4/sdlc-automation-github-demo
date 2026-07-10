# Change: Fix Pet Status Filter

## Why

Support reports indicate that customers are able to see and start adoption flows for pets that should not be available yet (pending status). This creates confusion and extra operational work. The pet catalog search has a bug where an empty status string bypasses the status filter entirely, allowing pending pets to appear in search results.

## Source

- GitHub issue: N/A (originated from Jira KAN-76)
- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-76
- Issue title: The filter for pet store isn't working
- Automation: Replicated Factory delegated conversation

## Assumptions

- The default behavior should always filter to available pets only
- Empty string status should not bypass the status filter
- Existing API callers expect status filtering to be enforced
- No UI changes are required; this is a backend logic fix

## Non-Goals

- UI changes or new UI components
- Changes to pet data structure or status values
- New filtering capabilities beyond fixing the existing status filter
- Performance optimization or caching

## What Changes

- Fix status filter logic to handle empty string correctly
- Ensure status filter is always applied when status parameter has a value
- Add test coverage for empty string status edge case

## Impact

- App behavior: Empty status strings will now correctly default to "available" filtering
- Tests: Add new test case for empty string status bug
- Humans: Support team will see fewer confused customers trying to adopt pending pets

## Human Gates

- Scope approval: Required before implementation
- Review approval: Required before merge
- Merge approval: Required by repository owner
- Deployment approval: Required before production rollout
