# Change: Adoption Fee Breakdown Display

## Why

Adopters need to understand what they are paying for when they adopt a pet. Currently, the pet detail page only shows a single total adoption fee, which doesn't provide transparency about the individual cost components. By showing a breakdown of the base fee, vaccination fee, and microchip fee, adopters can make more informed decisions and understand the value they're receiving.

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-143
- Trigger: Jira webhook `jira:issue_created`
- Automation: SDLC Automation Demo - Jira Request To PR

## Assumptions

- The fee breakdown (base, vaccination, microchip) is stored data per pet, not computed dynamically.
- Each pet may have different fee structures based on their specific needs.
- The total adoption fee equals the sum of base fee + vaccination fee + microchip fee.
- Money is represented as integer cents throughout the system (existing product rule).
- This change affects only the display layer; no payment processing or billing logic changes are needed.

## Non-Goals

- Payment processing or checkout flow changes
- Billing system integration
- Fee calculation logic or pricing engine
- Backend API for dynamic fee computation
- Admin interface for updating fees
- Fee breakdown for historical or completed adoptions

## What Changes

- Backend: Add `base_fee_cents`, `vaccination_fee_cents`, and `microchip_fee_cents` fields to the Pet dataclass
- Backend: Update existing pet data to include fee breakdowns
- Frontend: Display fee breakdown as separate line items in the pet detail view
- Frontend: Keep total fee visible alongside the breakdown
- Tests: Add tests to verify fee breakdown fields are present and sum correctly

## Impact

- App behavior: Pet listings will show detailed fee breakdown instead of just a total
- Tests: Existing tests continue to work; new tests verify breakdown display
- Humans: Adopters gain transparency into adoption costs; requires review and merge approval before deployment

## Human Gates

- Scope approval: Jira issue KAN-143 defines the acceptance criteria
- Review approval: Pull request must be reviewed by humans before merge
- Merge approval: Humans decide when to merge this change
- Deployment approval: Humans control when merged code reaches production
