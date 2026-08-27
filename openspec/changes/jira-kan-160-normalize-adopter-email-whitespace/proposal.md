# Change: Normalize Adopter Email Whitespace in Adoption Orders

**Status:** Draft  
**Created:** 2026-08-27

## Source

- Jira issue: https://rajiv-shah.atlassian.net/browse/KAN-160
- Reporter: OpenHands Agent
- Priority: Medium
- Automation: `sdlc-story`

## Why

Adopters sometimes paste email addresses with accidental leading or trailing whitespace when submitting adoption orders. The current implementation stores the email exactly as provided, including whitespace. This can cause:

- Validation failures for otherwise-valid email addresses
- Storage of malformed email values that fail downstream processing
- Inconsistent email matching if the same adopter submits orders with different whitespace patterns
- Poor user experience when valid-looking emails are rejected

## What Changes

Add whitespace normalization to the `create_adoption_order()` function in `app/petstore_app/adoptions.py`:

1. Trim leading and trailing whitespace from the `adopter_email` parameter before validation
2. Store the trimmed email address in the `AdoptionOrder` dataclass
3. Continue to reject emails that remain invalid after trimming (e.g., missing "@" symbol)
4. Preserve all existing behavior for pet availability checks, fee calculation, donation validation, and total calculation

## Impact

**Users:**
- Adoption orders with whitespace-wrapped emails will now succeed instead of failing
- No change to valid adoption orders (trimming valid emails has no effect)

**System:**
- Single-point change in `create_adoption_order()` function
- Follows existing input normalization pattern used in `catalog.py` for search queries
- No database, API, or UI changes required

**Testing:**
- Add focused regression tests for leading, trailing, and both-sided whitespace
- Verify existing tests remain green (no regression in fee/donation/total/pending behavior)

## Assumptions

1. **Silent normalization is acceptable**: The system will trim whitespace without notifying the user or logging the change
2. **Standard whitespace only**: Python's `.strip()` handles space, tab, newline, and carriage return characters (sufficient for this use case)
3. **No case normalization**: Email case should be preserved as entered (not explicitly requested)
4. **Backend-only change**: No UI updates needed because adoption orders are not displayed in the web interface
5. **Single email field**: Only the adopter email in adoption orders needs normalization (catalog searches already handle input trimming)

## Non-Goals

- Implementing comprehensive email validation (regex, domain checks, length limits)
- Normalizing email case (lowercasing)
- Validating email deliverability
- Trimming internal whitespace (e.g., "casey @ example.com")
- Applying normalization to other email fields or other user inputs
- Changing error messages to indicate trimming occurred

## Human Gates

**Before implementation:**
- Confirm silent normalization is acceptable (no user notification or logging)
- Confirm `.strip()` whitespace handling is sufficient (space, tab, newline, carriage return)

**Before merge:**
- Human code review of implementation and tests
- Human approval of pull request
- Human-controlled merge to main branch
