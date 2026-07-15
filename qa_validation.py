#!/usr/bin/env python3
"""Quick validation script for max_age_months feature - no pytest required."""

import sys
sys.path.insert(0, 'app')

from petstore_app.catalog import search_pets, PETS

def test_max_age_filters_correctly():
    """Verify max_age_months=20 returns Mochi (18) and Pip (9), excludes Scout (28)"""
    results = search_pets(max_age_months=20)
    names = [pet.name for pet in results]
    print(f"✓ Test 1: search_pets(max_age_months=20) → {names}")
    assert names == ["Mochi", "Pip"], f"Expected ['Mochi', 'Pip'], got {names}"
    print("  ✓ Correctly returns pets aged ≤20 months")

def test_excludes_older_pets():
    """Verify max_age_months=15 excludes Mochi (18) and Scout (28)"""
    results = search_pets(max_age_months=15)
    names = [pet.name for pet in results]
    print(f"✓ Test 2: search_pets(max_age_months=15) → {names}")
    assert names == ["Pip"], f"Expected ['Pip'], got {names}"
    assert "Mochi" not in names and "Scout" not in names
    print("  ✓ Correctly excludes pets older than 15 months")

def test_optional_parameter():
    """Verify max_age_months is optional (default behavior unchanged)"""
    results_without = search_pets()
    results_with = search_pets(max_age_months=20)
    print(f"✓ Test 3: search_pets() → {len(results_without)} pets")
    print(f"         search_pets(max_age_months=20) → {len(results_with)} pets")
    assert len(results_without) >= len(results_with)
    print("  ✓ Parameter is optional, default behavior preserved")

def test_negative_age_rejected():
    """Verify negative max_age_months raises ValueError"""
    try:
        search_pets(max_age_months=-5)
        assert False, "Should have raised ValueError for negative age"
    except ValueError as e:
        print(f"✓ Test 4: search_pets(max_age_months=-5) → ValueError: {e}")
        assert "max_age_months cannot be negative" in str(e)
        print("  ✓ Negative ages properly rejected")

def test_status_filtering_preserved():
    """Verify status filtering still works with age filter"""
    results = search_pets(max_age_months=30)
    names = [pet.name for pet in results]
    print(f"✓ Test 5: search_pets(max_age_months=30) → {names}")
    assert "Nova" not in names, "Nova (pending) should be excluded by default status filter"
    print("  ✓ Status filtering (default='available') still works")

def test_zero_age_valid():
    """Verify zero age is accepted"""
    results = search_pets(max_age_months=0)
    print(f"✓ Test 6: search_pets(max_age_months=0) → {[pet.name for pet in results]}")
    assert results == [], "No pets aged 0 months in test data"
    print("  ✓ Zero age is valid (no error raised)")

def print_test_data():
    """Show the test data for context"""
    print("\n=== Test Data ===")
    for pet in PETS:
        print(f"  {pet.name:8} {pet.species:7} {pet.status:9} age={pet.age_months:2} months")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("QA Validation: Maximum Age Filter (KAN-112)")
    print("=" * 60)
    print_test_data()
    
    try:
        test_max_age_filters_correctly()
        test_excludes_older_pets()
        test_optional_parameter()
        test_negative_age_rejected()
        test_status_filtering_preserved()
        test_zero_age_valid()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED (6/6)")
        print("=" * 60)
        print("\nAcceptance Criteria Status:")
        print("  ✅ Maximum age is optional")
        print("  ✅ Pets older than limit are excluded")
        print("  ✅ Negative ages are rejected")
        print("  ✅ Default catalog behavior unchanged")
        print("  ✅ Age filter preserves status filtering")
        print("  ✅ Zero age is valid")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
