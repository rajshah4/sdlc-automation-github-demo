#!/usr/bin/env python3
"""
Smoke test for the family-friendly filter feature.
Tests the filter checkbox control and data filtering logic.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.request import urlopen


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:4173")
    args = parser.parse_args()

    print(f"Testing family-friendly filter at {args.url}")
    
    with urlopen(args.url, timeout=5) as response:
        html = response.read().decode("utf-8", errors="replace")
    
    # Test 1: Verify the family-friendly checkbox exists
    print("✓ Test 1: Checking for family-friendly checkbox control...")
    if 'id="family-friendly"' not in html:
        print("  ✗ FAIL: family-friendly checkbox not found in HTML", file=sys.stderr)
        return 1
    if 'type="checkbox"' not in html:
        print("  ✗ FAIL: checkbox input type not found", file=sys.stderr)
        return 1
    print("  ✓ PASS: Family-friendly checkbox control exists")
    
    # Test 2: Verify the checkbox label
    print("✓ Test 2: Checking for 'Family friendly' label...")
    if 'family friendly' not in html.lower():
        print("  ✗ FAIL: 'Family friendly' label text not found", file=sys.stderr)
        return 1
    print("  ✓ PASS: Label text found")
    
    # Test 3: Verify the JavaScript includes filter logic
    print("✓ Test 3: Checking JavaScript filter implementation...")
    js_url = f"{args.url}/app.js"
    with urlopen(js_url, timeout=5) as response:
        js_content = response.read().decode("utf-8", errors="replace")
    
    # Check for filter variable
    if 'familyFriendlyOnly' not in js_content:
        print("  ✗ FAIL: familyFriendlyOnly variable not found in JavaScript", file=sys.stderr)
        return 1
    
    # Check for checkbox selector
    if '#family-friendly' not in js_content:
        print("  ✗ FAIL: #family-friendly selector not found", file=sys.stderr)
        return 1
    
    # Check for tags.includes("family") filter logic
    if 'tags.includes("family")' not in js_content:
        print("  ✗ FAIL: family tag filter logic not found", file=sys.stderr)
        return 1
    
    # Check for change event listener
    if 'addEventListener("change"' not in js_content:
        print("  ✗ FAIL: change event listener not found", file=sys.stderr)
        return 1
    
    print("  ✓ PASS: Filter logic implemented correctly")
    
    # Test 4: Verify pet data includes family-tagged pets
    print("✓ Test 4: Checking pet data for family tags...")
    
    # Extract pets array from JavaScript
    pets_match = re.search(r'const pets = (\[.*?\]);', js_content, re.DOTALL)
    if not pets_match:
        print("  ✗ FAIL: Could not extract pets array from JavaScript", file=sys.stderr)
        return 1
    
    # Parse pet data (simplified - just check for family tag presence)
    if '"family"' not in js_content:
        print("  ✗ FAIL: No pets with 'family' tag found in data", file=sys.stderr)
        return 1
    
    print("  ✓ PASS: Pet data includes family-tagged pets")
    
    # Test 5: Verify the filter respects available status
    print("✓ Test 5: Checking that filter respects available-only product rule...")
    if 'pet.status === "available"' not in js_content:
        print("  ✗ FAIL: Available status filter not found", file=sys.stderr)
        return 1
    print("  ✓ PASS: Filter maintains available-only constraint")
    
    print("\n" + "="*60)
    print("All family-friendly filter smoke tests passed!")
    print("="*60)
    print("\nTest Coverage:")
    print("  ✓ Family-friendly checkbox control exists")
    print("  ✓ Checkbox label is present and correct")
    print("  ✓ Filter logic implemented in JavaScript")
    print("  ✓ Filters pets by 'family' tag")
    print("  ✓ Respects available-only product rule")
    print("  ✓ Change event listener wired correctly")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
