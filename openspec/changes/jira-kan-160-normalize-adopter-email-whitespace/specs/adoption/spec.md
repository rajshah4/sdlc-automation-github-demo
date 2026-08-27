# Spec: Adoption Order Email Normalization

**Capability:** Adoption Order Creation  
**Change:** Email whitespace normalization

## ADDED Requirements

### REQ-ADOPT-001: Trim Leading and Trailing Whitespace

The `create_adoption_order()` function **must** trim leading and trailing whitespace from the `adopter_email` parameter before validation.

**Rationale:** Adopters may accidentally include spaces when copying/pasting email addresses.

### REQ-ADOPT-002: Store Trimmed Email

The adoption order **must** store the trimmed email address, not the original input.

**Rationale:** Consistent email storage enables reliable matching and downstream processing.

## MODIFIED Requirements

### REQ-ADOPT-003: Preserve Validation Rules

Email validation **must** continue to reject invalid emails after trimming.

**Rationale:** Trimming whitespace should not weaken email validation.

### REQ-ADOPT-004: Preserve Existing Behavior

The change **must not** affect:
- Pet availability validation
- Adoption fee calculation
- Donation validation
- Total calculation

**Rationale:** This is a focused input normalization change with no side effects.

## Scenarios

### SCENARIO-001: Valid Email with Leading Whitespace

**Given** a valid email address with leading whitespace  
**When** `create_adoption_order("pet-100", " casey@example.com")` is called  
**Then** the adoption order is created successfully  
**And** the stored email is `"casey@example.com"` (without whitespace)

### SCENARIO-002: Valid Email with Trailing Whitespace

**Given** a valid email address with trailing whitespace  
**When** `create_adoption_order("pet-100", "casey@example.com ")` is called  
**Then** the adoption order is created successfully  
**And** the stored email is `"casey@example.com"` (without whitespace)

### SCENARIO-003: Valid Email with Both Leading and Trailing Whitespace

**Given** a valid email address with both leading and trailing whitespace  
**When** `create_adoption_order("pet-100", "  casey@example.com  ")` is called  
**Then** the adoption order is created successfully  
**And** the stored email is `"casey@example.com"` (without whitespace)

### SCENARIO-004: Invalid Email with Whitespace

**Given** an invalid email address with whitespace  
**When** `create_adoption_order("pet-100", "  casey  ")` is called  
**Then** a `ValueError` is raised with message containing "email"

### SCENARIO-005: Whitespace-Only Input

**Given** a whitespace-only string  
**When** `create_adoption_order("pet-100", "   ")` is called  
**Then** a `ValueError` is raised with message containing "email"

### SCENARIO-006: Valid Email Without Whitespace (Regression)

**Given** a valid email without whitespace  
**When** `create_adoption_order("pet-100", "casey@example.com")` is called  
**Then** the adoption order is created successfully  
**And** the stored email is `"casey@example.com"` (unchanged)

### SCENARIO-007: Preserve Fee Calculation (Regression)

**Given** a valid email with whitespace  
**When** `create_adoption_order("pet-100", " casey@example.com ", donation_cents=2500)` is called  
**Then** the total is correctly calculated as `adoption_fee_cents + donation_cents`

### SCENARIO-008: Preserve Pending Pet Rejection (Regression)

**Given** a pending pet and email with whitespace  
**When** `create_adoption_order("pet-103", " casey@example.com ")` is called  
**Then** a `ValueError` is raised with message containing "not available"

## Acceptance Criteria

- ✅ REQ-ADOPT-001: Whitespace is trimmed before validation
- ✅ REQ-ADOPT-002: Trimmed email is stored in the adoption order
- ✅ REQ-ADOPT-003: Invalid emails are still rejected after trimming
- ✅ REQ-ADOPT-004: Existing behavior (fees, donations, availability) is preserved
- ✅ All scenarios pass with focused regression tests
- ✅ Existing tests remain green (no regressions)
