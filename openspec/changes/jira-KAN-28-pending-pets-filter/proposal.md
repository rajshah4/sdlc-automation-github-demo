# Change: Fix Available Pets Catalog Filter

## Why

Support is receiving reports from customers who found animals in the available pets list that the adoption team says are not available yet. This creates confusion when families ask about animals that should not be offered for adoption. The catalog filter must exclude pending pets from the default available-pets experience.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-28
- Trigger: jira:issue_created
- Automation: Jira-to-PR work cell (SDLC Automation Demo)

## Assumptions

- The bug occurs when the status parameter is passed as an empty string or whitespace to the search_pets function
- The default behavior (when status is not provided) correctly filters to available pets only
- Pending pets must still be searchable when explicitly requested with status="pending"
- No changes to cloud resources, deployment settings, or authentication are needed

## Non-Goals

- Not changing the ability to explicitly search for pending pets when requested
- Not modifying the Cloud Run app's incident simulation mode
- Not altering the adoption workflow or validation logic
- Not adding new dependencies or external services

## What Changes

- The search_pets function will treat empty or whitespace-only status parameters as "available" instead of bypassing the filter
- Pending pets will never appear in default or empty-status searches
- Explicit status="pending" searches will continue to work as designed

## Impact

- App behavior: Empty status parameters now default to "available" filter, preventing pending pets from appearing
- Tests: Add regression test to verify empty status strings do not expose pending pets
- Humans: Require review approval and merge approval before deployment

## Human Gates

- Scope approval: Automated (follows Petstore product rules)
- Review approval: Required before merge
- Merge approval: Required
- Deployment approval: Required
