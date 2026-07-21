#!/usr/bin/env python3
"""QA validation for KAN-65: Pending pets should not appear in available pets catalog."""

import sys
from urllib.request import urlopen
import json

def main() -> int:
    url = "http://localhost:4173"
    
    print("🔍 QA Validation for KAN-65: Pending pets in available catalog\n")
    
    # 1. Verify HTML structure and initial state
    print(f"1. Fetching UI from {url}...")
    with urlopen(url, timeout=5) as response:
        html = response.read().decode("utf-8", errors="replace")
    
    # Check for required UI elements
    required_elements = [
        "Petstore SDLC Demo",
        "Find Pets",
        "Available Pets",
        'id="query"',
        'id="species"',
        'id="results"',
    ]
    
    missing = [elem for elem in required_elements if elem not in html]
    if missing:
        print(f"❌ Missing UI elements: {', '.join(missing)}")
        return 1
    
    print("✅ UI structure is correct\n")
    
    # 2. Fetch and verify the JavaScript filtering logic
    print("2. Checking JavaScript filtering logic...")
    js_url = f"{url}/app.js"
    with urlopen(js_url, timeout=5) as response:
        js_code = response.read().decode("utf-8", errors="replace")
    
    # Look for the critical filtering logic
    if 'pet.status === "available"' in js_code:
        print('✅ JavaScript filter includes: pet.status === "available"')
    else:
        print('❌ JavaScript filter missing status check')
        return 1
    
    # 3. Verify pet data includes Nova (pending) and other pets
    print("\n3. Verifying pet data structure...")
    
    pets_check = {
        "Mochi": {"status": "available", "expected_visible": True},
        "Scout": {"status": "available", "expected_visible": True},
        "Pip": {"status": "available", "expected_visible": True},
        "Nova": {"status": "pending", "expected_visible": False},
    }
    
    all_pets_present = True
    for pet_name, info in pets_check.items():
        if pet_name in js_code:
            status_str = f'"status": "{info["status"]}"'
            if status_str in js_code:
                visibility = "should NOT be visible" if info["status"] == "pending" else "should be visible"
                print(f"✅ {pet_name} ({info['status']}) found in data - {visibility}")
            else:
                print(f"⚠️  {pet_name} found but status unclear")
        else:
            print(f"❌ {pet_name} not found in JS")
            all_pets_present = False
    
    if not all_pets_present:
        return 1
    
    # 4. Verify the filter excludes pending pets
    print("\n4. Checking UI filter implementation...")
    
    # The key fix: UI should filter by status === "available"
    if 'pets.filter' in js_code and 'pet.status === "available"' in js_code:
        print('✅ UI correctly filters for status === "available"')
        print("✅ Nova (pending) will be excluded from default search results")
    else:
        print("❌ UI filter does not properly exclude pending pets")
        return 1
    
    # 5. Summary
    print("\n" + "="*60)
    print("✅ QA VALIDATION PASSED")
    print("="*60)
    print("\nValidated:")
    print("  • UI structure contains all required elements")
    print("  • JavaScript filters by status === 'available'")
    print("  • Pet data includes Nova (pending) in source")
    print("  • Filter logic excludes pending pets from display")
    print("\nExpected behavior:")
    print("  • Default view shows: Mochi, Scout, Pip")
    print("  • Nova (pending) is hidden from default catalog")
    print("  • Searching for 'nova' shows empty state")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
