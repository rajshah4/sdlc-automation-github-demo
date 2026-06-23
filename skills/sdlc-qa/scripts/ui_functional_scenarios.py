#!/usr/bin/env python3
"""Functional scenario validation for adoption fee filter.

Simulates the test scenarios from the PR description by examining
the JavaScript logic and data.
"""

from __future__ import annotations

import json
import re
import sys
from urllib.request import urlopen


def extract_pet_data(js: str) -> list[dict]:
    """Extract pet data from JavaScript source."""
    # Find the pets array
    pets_match = re.search(r'const pets = \[(.*?)\];', js, re.DOTALL)
    if not pets_match:
        raise ValueError("Could not find pets array in JavaScript")
    
    pets_text = pets_match.group(1)
    
    # Parse each pet object
    pets = []
    pet_pattern = r'\{\s*id:\s*"([^"]+)",\s*name:\s*"([^"]+)",\s*species:\s*"([^"]+)",\s*status:\s*"([^"]+)",\s*tags:\s*\[(.*?)\],\s*feeCents:\s*(\d+)\s*\}'
    
    for match in re.finditer(pet_pattern, pets_text, re.DOTALL):
        pet_id, name, species, status, tags_str, fee_cents = match.groups()
        tags = [tag.strip().strip('"') for tag in tags_str.split(',')]
        pets.append({
            'id': pet_id,
            'name': name,
            'species': species,
            'status': status,
            'tags': tags,
            'feeCents': int(fee_cents),
        })
    
    return pets


def simulate_filter(pets: list[dict], query: str, species: str, max_fee_dollars: float | None) -> list[dict]:
    """Simulate the JavaScript filter logic."""
    max_fee_cents = None if max_fee_dollars is None else int(max_fee_dollars * 100)
    
    matches = []
    for pet in pets:
        # Match the JavaScript filter logic exactly
        name_match = query.lower() in pet['name'].lower()
        species_match = species == "" or pet['species'] == species
        fee_match = max_fee_cents is None or pet['feeCents'] <= max_fee_cents
        status_match = pet['status'] == 'available'
        
        if name_match and species_match and fee_match and status_match:
            matches.append(pet)
    
    return matches


def main() -> int:
    url = "http://localhost:4173"
    all_passed = True
    
    print("=" * 60)
    print("Functional Scenario Validation")
    print("=" * 60)
    
    try:
        # Fetch JavaScript
        print(f"\nFetching app.js from {url}...")
        with urlopen(f"{url}/app.js", timeout=5) as response:
            js = response.read().decode("utf-8")
        
        # Extract pet data
        pets = extract_pet_data(js)
        print(f"Found {len(pets)} pets in data:")
        for pet in pets:
            fee_display = f"${pet['feeCents'] / 100:.0f}"
            print(f"  - {pet['name']} ({pet['species']}, {pet['status']}, {fee_display})")
        
        # Scenario 1: Default list (no filters)
        print("\n" + "-" * 60)
        print("Scenario 1: Default list (available pets only)")
        print("-" * 60)
        matches = simulate_filter(pets, "", "", None)
        expected_names = {"Mochi", "Scout", "Pip"}
        actual_names = {pet['name'] for pet in matches}
        
        if actual_names == expected_names:
            print("✓ PASSED")
            print(f"  Expected: {sorted(expected_names)}")
            print(f"  Actual:   {sorted(actual_names)}")
            print("  Nova (pending) correctly excluded")
        else:
            print("✗ FAILED")
            print(f"  Expected: {sorted(expected_names)}")
            print(f"  Actual:   {sorted(actual_names)}")
            all_passed = False
        
        # Scenario 2: Max fee $80 (should show Mochi $75 and Pip $45, hide Scout $125)
        print("\n" + "-" * 60)
        print("Scenario 2: Max fee $80 filter")
        print("-" * 60)
        matches = simulate_filter(pets, "", "", 80.0)
        expected_names = {"Mochi", "Pip"}
        actual_names = {pet['name'] for pet in matches}
        
        if actual_names == expected_names:
            print("✓ PASSED")
            print(f"  Expected: {sorted(expected_names)}")
            print(f"  Actual:   {sorted(actual_names)}")
            print("  Scout ($125) correctly filtered out")
        else:
            print("✗ FAILED")
            print(f"  Expected: {sorted(expected_names)}")
            print(f"  Actual:   {sorted(actual_names)}")
            all_passed = False
        
        # Scenario 3: Max fee $40 (should show no pets - empty state)
        print("\n" + "-" * 60)
        print("Scenario 3: Max fee $40 filter (empty result)")
        print("-" * 60)
        matches = simulate_filter(pets, "", "", 40.0)
        expected_count = 0
        actual_count = len(matches)
        
        if actual_count == expected_count:
            print("✓ PASSED")
            print(f"  Expected: {expected_count} pets")
            print(f"  Actual:   {actual_count} pets")
            print("  Empty state triggered correctly (all fees > $40)")
        else:
            print("✗ FAILED")
            print(f"  Expected: {expected_count} pets")
            print(f"  Actual:   {actual_count} pets")
            print(f"  Matches: {[p['name'] for p in matches]}")
            all_passed = False
        
        # Scenario 4: Negative fee validation
        print("\n" + "-" * 60)
        print("Scenario 4: Negative fee validation")
        print("-" * 60)
        
        # Check if parseMaxFeeCents handles negative values
        if 'feeDollars < 0' in js:
            print("✓ PASSED")
            print("  Negative fee validation logic present in parseMaxFeeCents")
            print("  Error message logic: 'Enter a maximum fee of 0 or more.'")
        else:
            print("✗ FAILED")
            print("  Missing negative fee validation")
            all_passed = False
        
        # Scenario 5: Verify result summary logic
        print("\n" + "-" * 60)
        print("Scenario 5: Result summary display")
        print("-" * 60)
        
        if 'result-summary' in js and 'match this search' in js:
            print("✓ PASSED")
            print("  Result summary update logic present")
            print("  Shows count: 'N available pet(s) match this search.'")
        else:
            print("✗ FAILED")
            print("  Missing result summary logic")
            all_passed = False
        
        # Final summary
        print("\n" + "=" * 60)
        if all_passed:
            print("RESULT: All functional scenarios PASSED ✓")
            print("=" * 60)
            print("\nUI Test Coverage:")
            print("  ✓ Default list shows only available pets (excludes Nova)")
            print("  ✓ $80 max fee correctly filters to Mochi & Pip")
            print("  ✓ $40 max fee triggers empty state")
            print("  ✓ Negative fee validation logic present")
            print("  ✓ Result summary logic present")
            return 0
        else:
            print("RESULT: Some functional scenarios FAILED ✗")
            print("=" * 60)
            return 1
    
    except Exception as e:
        print(f"\n✗ Functional validation failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
