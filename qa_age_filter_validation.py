#!/usr/bin/env python3
"""Manual QA validation for age filter functionality (KAN-52)."""

import sys
sys.path.insert(0, 'app')

from petstore_app.catalog import search_pets, PETS

def test_case(name: str, test_fn):
    """Run a test case and report result."""
    try:
        test_fn()
        print(f"✓ {name}")
        return True
    except AssertionError as e:
        print(f"✗ {name}: {e}")
        return False
    except Exception as e:
        print(f"✗ {name}: {type(e).__name__}: {e}")
        return False

def main():
    print("QA Validation: Age Filter Feature (KAN-52)")
    print("=" * 60)
    print(f"\nTest Data: {len(PETS)} pets")
    for pet in PETS:
        print(f"  - {pet.name} ({pet.species}, {pet.age_months}mo, {pet.status})")
    print()
    
    passed = 0
    total = 0
    
    # Test 1: Filter by minimum age
    def test_min_age():
        results = search_pets(min_age_months=18)
        names = [pet.name for pet in results]
        assert names == ["Mochi", "Scout"], f"Expected ['Mochi', 'Scout'], got {names}"
    total += 1
    if test_case("Filter by minimum age (18 months)", test_min_age):
        passed += 1
    
    # Test 2: Filter by maximum age
    def test_max_age():
        results = search_pets(max_age_months=15)
        names = [pet.name for pet in results]
        assert names == ["Pip"], f"Expected ['Pip'], got {names}"
    total += 1
    if test_case("Filter by maximum age (15 months)", test_max_age):
        passed += 1
    
    # Test 3: Filter by age range
    def test_age_range():
        results = search_pets(min_age_months=10, max_age_months=20)
        names = [pet.name for pet in results]
        assert names == ["Mochi"], f"Expected ['Mochi'], got {names}"
    total += 1
    if test_case("Filter by age range (10-20 months)", test_age_range):
        passed += 1
    
    # Test 4: Combine species and age filters
    def test_species_and_age():
        results = search_pets(species="dog", min_age_months=10, max_age_months=30)
        names = [pet.name for pet in results]
        assert names == ["Scout"], f"Expected ['Scout'], got {names}"
    total += 1
    if test_case("Filter by species (dog) and age range", test_species_and_age):
        passed += 1
    
    # Test 5: Age filter respects default available status
    def test_respects_available():
        results = search_pets(min_age_months=10, max_age_months=20)
        names = [pet.name for pet in results]
        assert names == ["Mochi"], f"Expected ['Mochi'], got {names}"
        for pet in results:
            assert pet.status == "available", f"Expected available, got {pet.status}"
    total += 1
    if test_case("Age filter respects default available status", test_respects_available):
        passed += 1
    
    # Test 6: Age filter works with pending status
    def test_pending_status():
        results = search_pets(min_age_months=10, max_age_months=20, status="pending")
        names = [pet.name for pet in results]
        assert names == ["Nova"], f"Expected ['Nova'], got {names}"
    total += 1
    if test_case("Age filter works with pending status", test_pending_status):
        passed += 1
    
    # Test 7: Reject negative min age
    def test_negative_min():
        try:
            search_pets(min_age_months=-1)
            raise AssertionError("Should have raised ValueError")
        except ValueError as e:
            assert "non-negative" in str(e), f"Wrong error message: {e}"
    total += 1
    if test_case("Reject negative min_age_months", test_negative_min):
        passed += 1
    
    # Test 8: Reject negative max age
    def test_negative_max():
        try:
            search_pets(max_age_months=-1)
            raise AssertionError("Should have raised ValueError")
        except ValueError as e:
            assert "non-negative" in str(e), f"Wrong error message: {e}"
    total += 1
    if test_case("Reject negative max_age_months", test_negative_max):
        passed += 1
    
    # Test 9: Reject inverted age range
    def test_inverted_range():
        try:
            search_pets(min_age_months=20, max_age_months=10)
            raise AssertionError("Should have raised ValueError")
        except ValueError as e:
            assert "min_age_months must be <=" in str(e), f"Wrong error message: {e}"
    total += 1
    if test_case("Reject inverted age range (min > max)", test_inverted_range):
        passed += 1
    
    # Test 10: Accept equal min and max age
    def test_equal_ages():
        results = search_pets(min_age_months=18, max_age_months=18)
        names = [pet.name for pet in results]
        assert names == ["Mochi"], f"Expected ['Mochi'], got {names}"
    total += 1
    if test_case("Accept equal min and max age", test_equal_ages):
        passed += 1
    
    # Test 11: Accept zero age
    def test_zero_age():
        results = search_pets(min_age_months=0, max_age_months=50)
        assert len(results) == 3, f"Expected 3 available pets, got {len(results)}"
    total += 1
    if test_case("Accept zero age", test_zero_age):
        passed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print(f"✗ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
