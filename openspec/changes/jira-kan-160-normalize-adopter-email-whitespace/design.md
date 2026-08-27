# Design: Normalize Adopter Email Whitespace

**Change Folder:** `openspec/changes/jira-kan-160-normalize-adopter-email-whitespace/`

## Context

**Current Behavior:**
- The `create_adoption_order()` function in `app/petstore_app/adoptions.py` validates email addresses using a simple "@" check (line 36)
- Email input is stored directly without normalization
- Whitespace-wrapped emails like " casey@example.com " pass validation but store the malformed value

**Problem:**
- Users accidentally paste emails with leading/trailing whitespace
- Storage of untrimmed emails causes inconsistent matching and downstream issues

**Existing Pattern:**
- `app/petstore_app/catalog.py` already uses `.strip()` to normalize user input (query, species, status, tag) at lines 39-42
- This change follows the established repo pattern

## Decision

Add email whitespace normalization using `.strip()` before validation in the `create_adoption_order()` function.

### The Smallest Safe Implementation

**File:** `app/petstore_app/adoptions.py`  
**Function:** `create_adoption_order()` (lines 26-47)  
**Change:** Add email normalization after line 32 (after pet lookup, before email validation)

```python
def create_adoption_order(
    pet_id: str,
    adopter_email: str,
    *,
    donation_cents: int = 0,
) -> AdoptionOrder:
    """Create a reviewable adoption order summary."""
    pet = _find_pet(pet_id)
    
    # Normalize email whitespace before validation
    adopter_email = adopter_email.strip()
    
    if pet.status != "available":
        raise ValueError("pet is not available for adoption")
    if "@" not in adopter_email:
        raise ValueError("adopter_email must be a valid email address")
    if donation_cents < 0:
        raise ValueError("donation_cents cannot be negative")

    return AdoptionOrder(
        pet_id=pet.id,
        adopter_email=adopter_email,  # Stores trimmed email
        adoption_fee_cents=pet.adoption_fee_cents,
        donation_cents=donation_cents,
        total_cents=pet.adoption_fee_cents + donation_cents,
    )
```

### Why This Works

1. **Single-point change:** One normalization line affects all adoption order creation paths
2. **Follows existing pattern:** `catalog.py` uses `.strip()` for user input normalization (lines 39-42)
3. **Preserves validation:** Email validation occurs after trimming, so invalid emails are still rejected
4. **Stores clean data:** The `AdoptionOrder` dataclass receives the trimmed email
5. **No side effects:** Pet lookup, availability check, fee calculation, and donation validation remain unchanged

### Alternative Approaches Considered

**Option 1: Validate then trim** ❌
- Would store untrimmed email even if validation passes
- Violates REQ-2 (store trimmed email)

**Option 2: Trim in AdoptionOrder constructor** ❌
- Dataclass is frozen (immutable)
- Would require unfreezing or custom `__post_init__`
- More complex than needed

**Option 3: Add a separate `normalize_email()` function** ❌
- Over-engineering for a single `.strip()` call
- No reuse case (only one email field exists)

**Option 4: Use email validation library (e.g., `email-validator`)** ❌
- Adds external dependency
- Out of scope (not requested in acceptance criteria)
- Current validation is intentionally simple ("@" check)

## Test Strategy

**File:** `app/tests/test_adoptions.py`

Add three focused regression tests after the existing tests:

1. `test_create_adoption_order_trims_leading_whitespace()` - Verify " casey@example.com" succeeds and stores "casey@example.com"
2. `test_create_adoption_order_trims_trailing_whitespace()` - Verify "casey@example.com " succeeds and stores "casey@example.com"
3. `test_create_adoption_order_trims_both_whitespace()` - Verify "  casey@example.com  " succeeds and stores "casey@example.com"
4. `test_create_adoption_order_rejects_whitespace_only_email()` - Verify "   " raises ValueError

**Regression coverage:**
- Existing 4 tests verify no breakage in fee calculation, pending pet rejection, invalid email rejection, and negative donation rejection

## Validation Plan

```bash
# Run focused adoption tests
python3 -m pytest -q app/tests/test_adoptions.py

# Expected: 8 passed (4 existing + 4 new)
```

## Risks

**Low risk change:**
- Single line of code change in isolated function
- Established pattern in the codebase (catalog.py uses same approach)
- No dependencies, database, or external service changes
- Comprehensive test coverage (8 tests total)

**Edge cases covered:**
- Empty string after trim → fails "@" validation ✅
- Already-valid email → no behavior change ✅
- Invalid email with whitespace → still rejected ✅
- Pending pet + whitespace email → availability check still rejects ✅
- Fee/donation/total calculation → unchanged ✅

**No breaking changes:**
- Trimming only makes previously-rejected input valid
- Does not invalidate previously-accepted input

## Evidence Waypoints

### Stop 1 - Ticket
**Source:** [Jira KAN-160](https://rajiv-shah.atlassian.net/browse/KAN-160)  
**Clue:** "Adopters sometimes paste an email address with accidental spaces before or after it"

### Stop 2 - Wiki/Docs
**Checked:**
- `docs/wiki/petstore-catalog-availability.md` - Confirmed adoption rules (available pets only)
- `docs/repo-memory/petstore-intelligence.md` - Confirmed adoption implementation files
- `AGENTS.md` - Confirmed test command and money-as-cents rule

**Relevance:** Confirms adoption order validation rules and test patterns

### Stop 3 - Logs
**Checked:** `docs/logs/` directory
**Finding:** No adoption-specific log fixtures found (logs are catalog-focused)
**Conclusion:** Not applicable to this input validation change

### Stop 4 - Repo/Files
**Implementation:** `app/petstore_app/adoptions.py` line 36 (email validation)  
**Tests:** `app/tests/test_adoptions.py` lines 24-26 (existing email validation test)  
**Pattern:** `app/petstore_app/catalog.py` lines 39-42 (existing `.strip()` usage)

### Stop 5 - Tests/PR
**Validation:** `python3 -m pytest -q app/tests/test_adoptions.py`  
**Coverage:** 4 new tests for whitespace scenarios + 4 existing tests for regression  
**PR:** Draft PR to be created with OpenSpec change link
