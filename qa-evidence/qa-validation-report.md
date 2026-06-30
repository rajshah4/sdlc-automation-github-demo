# QA Validation Report: PR #44 - Fix KAN-36

**PR Title:** Fix KAN-36: Prevent pending pets from appearing in customer catalog  
**Branch:** fix/kan-36-pending-pets-visible  
**Base:** sidekick-context-experiment  
**QA Date:** 2026-06-30  
**Status:** ✅ PASS

---

## Summary

All acceptance criteria validated successfully. The fix correctly prevents pending pets (like Nova/pet-103) from appearing in the default customer catalog while maintaining the ability for staff to explicitly search for pending pets.

---

## Changes Validated

### Code Changes
1. **app/petstore_app/cloud_run_app.py**
   - Replaced `visible_pets()` calls with `search_pets()` in two locations:
     - `render_home()` - home page rendering
     - `/api/pets` endpoint handler
   - Ensures default status="available" filter is applied

2. **app/tests/test_pet_catalog.py**
   - Added `test_search_pets_default_excludes_pending_pets()` regression test
   - Validates that pet-103 (Nova) is excluded from default results
   - Confirms all default results have status="available"

---

## Acceptance Criteria Coverage

### ✅ Scenario 1: Customer requests catalog without specifying status
**Requirement:** `/api/pets` without status filter returns only available pets

**Test Method:** HTTP GET to `/api/pets`  
**Result:** PASS
- Returned pets: pet-100 (Mochi), pet-101 (Scout), pet-102 (Pip)
- All have status="available"
- Nova (pet-103, status="pending") correctly excluded

**Evidence:** `api-pets-response.json`

---

### ✅ Scenario 2: Customer views home page
**Requirement:** Home page displays only available pets

**Test Method:** HTTP GET to `/` and HTML inspection  
**Result:** PASS
- Displayed pets: Mochi (cat), Scout (dog), Pip (rabbit)
- Nova (pending dog) correctly absent from HTML
- HTML grep for "Nova" returned no matches

**Evidence:** `home-page.html`

---

### ✅ Scenario 3: Staff can explicitly search for pending pets
**Requirement:** `search_pets(status="pending")` returns pending pets

**Test Method:** Direct Python function call  
**Result:** PASS
- `search_pets(status="pending")` returned pet-103 (Nova)
- `search_pets(species="dog", status="pending")` returned pet-103 (Nova)
- Support workflow capability preserved

**Evidence:** Backend test output

---

## Test Execution Summary

### Backend Tests
```
Test 1: Default search excludes pending pets
  Found 3 pets: ['pet-100', 'pet-101', 'pet-102']
  Statuses: ['available', 'available', 'available']
  ✓ PASS: Default search excludes pending pets

Test 2: Can explicitly search for pending pets
  Found 1 pending pets: ['pet-103']
  ✓ PASS: Explicit search finds pending pets

Test 3: Species + status filter
  Found 1 pending dogs: ['pet-103']
  ✓ PASS: Species + status filter works correctly

✓ All backend tests passed!
```

### API Validation
```
GET /api/pets
Status: 200 OK
Pets returned: 3 (pet-100, pet-101, pet-102)
Pending pets (pet-103): Correctly excluded ✓
```

### UI Validation
```
GET /
Status: 200 OK
Pets displayed: Mochi, Scout, Pip
Nova (pending): Not present in HTML ✓
```

---

## Risk Assessment

**Overall Risk:** LOW

### What Changed
- Replaced direct PETS list filtering with `search_pets()` function
- Function defaults to status="available", preventing pending pets from appearing

### What's Protected
- ✅ Default customer catalog (API + UI) excludes pending pets
- ✅ Staff can still search for pending pets explicitly
- ✅ Existing test suite updated with regression test
- ✅ No breaking changes to API contract

### Remaining Considerations
1. **Incident Mode Behavior:** The old `visible_pets()` returned all pets during incident mode. This behavior is removed. If incident mode should show pending pets, additional logic may be needed.
2. **No UI Automation:** Validation performed via HTTP/HTML inspection and API testing. No browser automation (Playwright) required for this change.

---

## Files Changed

- `app/petstore_app/cloud_run_app.py` (3 lines modified)
- `app/tests/test_pet_catalog.py` (11 lines added)
- OpenSpec documentation (4 new files)

---

## Recommendation

**✅ Ready to merge** after human review and CI validation.

The implementation correctly addresses KAN-36 by filtering pending pets from the default customer-facing catalog while preserving the ability for staff to access them through explicit filtering.

---

## QA Artifacts

- `api-pets-response.json` - API response showing only available pets
- `home-page.html` - Home page HTML showing only available pets
- `qa-validation-report.md` - This report
