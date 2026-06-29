# Change: Pet Discovery Budget Filter

## Why

Adoption counselors need to help families find pets within their budget before they visit. The backend catalog search already supports maximum adoption fee filtering, but the static UI does not expose this capability. This change adds a budget filter input to the web interface so families can narrow their search by affordability.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-18
- GitHub issue: N/A (Jira-direct webhook trigger)
- Summary: "Live no-shim test: families need to filter pets by adoption budget"
- Trigger: `jira:issue_created` webhook event from jira-direct source
- Automation: openhands-build work cell for Jira-triggered SDLC Automation Demo

## Assumptions

- The business language "budget" and "afford" maps to the existing `max_adoption_fee_cents` backend parameter based on `docs/wiki/pet-discovery-affordability.md`.
- The backend implementation in `app/petstore_app/catalog.py` already supports fee filtering with comprehensive test coverage.
- The UI change is limited to adding a simple dollar input field that converts to cents for backend compatibility.
- No API changes are required; this is purely a UI enhancement to expose existing backend functionality.

## Non-Goals

- Payment processing, checkout, or billing integration
- Backend API changes (feature already exists)
- Currency conversion or multi-currency support
- Authentication or authorization changes
- New dependencies or external services
- Mobile-specific UI optimizations

## What Changes

- Add a "Max Budget" input field to `app/web/index.html` with dollar amount entry
- Update `app/web/app.js` filter logic to exclude pets above the maximum fee
- Store fee values in cents internally (matching backend convention: `7500` cents = `$75`)
- Display existing fee strings unchanged (e.g., "$75")

## Impact

- App behavior: Families can filter pet search results by maximum adoption fee through the static UI
- Tests: Backend tests already exist and pass; no new backend tests needed for this UI-only change
- Humans: Adoption counselors can share the petstore URL with a budget expectation; families self-filter before visiting

## Human Gates

- Scope approval: Sparse business-language Jira ticket interpreted as UI enhancement for existing backend feature
- Review approval: Draft PR requires human review of UI changes and interpretation assumptions
- Merge approval: Humans decide when to merge based on demo timeline and review feedback
- Deployment approval: Humans control deployment to production or demo environments
