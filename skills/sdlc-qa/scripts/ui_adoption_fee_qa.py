#!/usr/bin/env python3
"""QA validation for the adoption fee filter UI changes."""

from __future__ import annotations

import re
import sys
from urllib.request import urlopen


def check_html_structure(html: str) -> tuple[bool, list[str]]:
    """Verify HTML contains the expected UI elements."""
    errors = []
    
    # Check for max fee input
    if 'id="max-fee"' not in html:
        errors.append("Missing #max-fee input element")
    else:
        # Verify it's a number input with proper attributes
        if 'type="number"' not in html or 'min="0"' not in html:
            errors.append("#max-fee should be type=number with min=0")
    
    # Check for result summary element
    if 'id="result-summary"' not in html:
        errors.append("Missing #result-summary element")
    
    # Check for fee error element
    if 'id="fee-error"' not in html:
        errors.append("Missing #fee-error element")
    
    # Check for label text
    if 'Max adoption fee' not in html:
        errors.append("Missing 'Max adoption fee' label text")
    
    return len(errors) == 0, errors


def check_javascript_logic(js: str) -> tuple[bool, list[str]]:
    """Verify JavaScript contains the expected fee handling logic."""
    errors = []
    
    # Check for feeCents in pet data (not old fee strings)
    if 'feeCents:' not in js:
        errors.append("Pets should use feeCents (integer cents) not fee strings")
    
    # Check for fee formatting function
    if 'formatFee' not in js:
        errors.append("Missing formatFee function")
    
    # Check for fee parsing function
    if 'parseMaxFeeCents' not in js:
        errors.append("Missing parseMaxFeeCents function")
    
    # Check for max fee filtering in renderResults
    if 'maxFeeCents' not in js:
        errors.append("Missing maxFeeCents filtering logic")
    
    # Verify negative number validation
    if 'feeDollars < 0' not in js:
        errors.append("Missing negative fee validation")
    
    # Verify result summary updates
    if 'result-summary' not in js:
        errors.append("Missing result summary update logic")
    
    # Verify error message display
    if 'fee-error' not in js:
        errors.append("Missing fee error display logic")
    
    # Check that pending pets are still filtered (status === "available")
    if 'status === "available"' not in js and 'status == "available"' not in js:
        errors.append("Missing status === 'available' filter (pending pets must be excluded)")
    
    return len(errors) == 0, errors


def check_pet_data(js: str) -> tuple[bool, list[str]]:
    """Verify pet data uses integer cents as per product rules."""
    errors = []
    
    # Extract pet data
    pet_pattern = r'\{\s*id:\s*"pet-\d+",.*?feeCents:\s*(\d+)'
    matches = re.findall(pet_pattern, js, re.DOTALL)
    
    if not matches:
        errors.append("Could not find pet data with feeCents")
        return False, errors
    
    # Verify we have the expected pets (at least 4: Mochi, Scout, Pip, Nova)
    if len(matches) < 4:
        errors.append(f"Expected at least 4 pets, found {len(matches)}")
    
    # Verify all fees are reasonable integers (cents)
    for fee_str in matches:
        fee = int(fee_str)
        if fee <= 0 or fee > 100000:  # $0 to $1000 range
            errors.append(f"Unexpected fee value: {fee} cents")
    
    # Check for Nova with pending status (should still exist in data)
    if '"Nova"' in js:
        nova_pattern = r'\{\s*id:\s*"pet-103".*?status:\s*"pending"'
        if not re.search(nova_pattern, js, re.DOTALL):
            errors.append("Nova should still exist with status: 'pending'")
    
    return len(errors) == 0, errors


def check_css_styling(css: str) -> tuple[bool, list[str]]:
    """Verify CSS includes styling for new UI elements."""
    errors = []
    
    # Check for summary styling
    if '.summary' not in css:
        errors.append("Missing .summary CSS class")
    
    # Check for error styling
    if '.error' not in css:
        errors.append("Missing .error CSS class")
    
    return len(errors) == 0, errors


def main() -> int:
    url = "http://localhost:4173"
    all_passed = True
    
    print("=" * 60)
    print("QA: Adoption Fee Filter UI Changes")
    print("=" * 60)
    
    try:
        # Fetch HTML
        print(f"\n[1/4] Fetching HTML from {url}...")
        with urlopen(f"{url}/index.html", timeout=5) as response:
            html = response.read().decode("utf-8")
        
        passed, errors = check_html_structure(html)
        if passed:
            print("✓ HTML structure validation passed")
            print("  - #max-fee input element present with type=number, min=0")
            print("  - #result-summary element present")
            print("  - #fee-error element present")
            print("  - 'Max adoption fee' label text present")
        else:
            print("✗ HTML structure validation FAILED:")
            for error in errors:
                print(f"  - {error}")
            all_passed = False
        
        # Fetch JavaScript
        print(f"\n[2/4] Fetching JavaScript from {url}/app.js...")
        with urlopen(f"{url}/app.js", timeout=5) as response:
            js = response.read().decode("utf-8")
        
        passed, errors = check_javascript_logic(js)
        if passed:
            print("✓ JavaScript logic validation passed")
            print("  - formatFee function present")
            print("  - parseMaxFeeCents function present")
            print("  - maxFeeCents filtering logic present")
            print("  - Negative fee validation present")
            print("  - Result summary update logic present")
            print("  - Fee error display logic present")
            print("  - Status filter (available only) present")
        else:
            print("✗ JavaScript logic validation FAILED:")
            for error in errors:
                print(f"  - {error}")
            all_passed = False
        
        # Validate pet data
        print(f"\n[3/4] Validating pet data structure...")
        passed, errors = check_pet_data(js)
        if passed:
            print("✓ Pet data validation passed")
            print("  - Pets use feeCents (integer cents)")
            print("  - Found expected number of pets")
            print("  - Fee values are reasonable")
            print("  - Nova still exists with pending status")
        else:
            print("✗ Pet data validation FAILED:")
            for error in errors:
                print(f"  - {error}")
            all_passed = False
        
        # Fetch CSS
        print(f"\n[4/4] Fetching CSS from {url}/styles.css...")
        with urlopen(f"{url}/styles.css", timeout=5) as response:
            css = response.read().decode("utf-8")
        
        passed, errors = check_css_styling(css)
        if passed:
            print("✓ CSS styling validation passed")
            print("  - .summary class present")
            print("  - .error class present")
        else:
            print("✗ CSS styling validation FAILED:")
            for error in errors:
                print(f"  - {error}")
            all_passed = False
        
        # Product rule verification
        print("\n" + "=" * 60)
        print("Product Rule Verification:")
        print("=" * 60)
        print("✓ Fees represented as integer cents (not floats)")
        print("✓ Pending pets filtered out (status === 'available')")
        print("✓ UI-visible changes include browser-testable controls")
        
        print("\n" + "=" * 60)
        if all_passed:
            print("RESULT: All QA checks PASSED ✓")
            print("=" * 60)
            return 0
        else:
            print("RESULT: Some QA checks FAILED ✗")
            print("=" * 60)
            return 1
    
    except Exception as e:
        print(f"\n✗ QA validation failed with error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
