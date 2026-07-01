#!/usr/bin/env python3
"""Simple test runner for catalog tests without pytest."""

import sys
sys.path.insert(0, 'app')

from petstore_app.catalog import search_pets

def test_default_search_excludes_pending_pets():
    """Regression test for KAN-65: pending pets must not appear in default search."""
    results = search_pets()
    
    assert all(pet.status == "available" for pet in results), "Default search returned non-available pets"
    assert "pet-103" not in [pet.id for pet in results], "Nova (pet-103) appeared in default search"
    print("✅ test_default_search_excludes_pending_pets PASSED")


def test_empty_status_defaults_to_available():
    """Empty or whitespace status should default to available, not return all pets."""
    empty_results = search_pets(status="")
    whitespace_results = search_pets(status="   ")
    
    assert all(pet.status == "available" for pet in empty_results), "Empty status returned non-available pets"
    assert all(pet.status == "available" for pet in whitespace_results), "Whitespace status returned non-available pets"
    assert "pet-103" not in [pet.id for pet in empty_results], "Nova appeared with empty status"
    assert "pet-103" not in [pet.id for pet in whitespace_results], "Nova appeared with whitespace status"
    print("✅ test_empty_status_defaults_to_available PASSED")


def test_existing_functionality():
    """Test that existing catalog functionality still works."""
    # Test explicit pending search
    pending_results = search_pets(status="pending")
    assert len(pending_results) == 1, "Should find one pending pet"
    assert pending_results[0].name == "Nova", "Pending search should find Nova"
    print("✅ test_existing_functionality PASSED (explicit pending search works)")
    
    # Test species filter
    dog_results = search_pets(species="dog")
    assert len(dog_results) == 1, "Should find one available dog"
    assert dog_results[0].name == "Scout", "Should find Scout (not Nova)"
    print("✅ test_existing_functionality PASSED (species filter works)")
    
    # Test tag filter
    indoor_results = search_pets(tag="indoor")
    assert len(indoor_results) == 2, "Should find two indoor pets"
    assert all(pet.name in ["Mochi", "Pip"] for pet in indoor_results), "Should find Mochi and Pip"
    print("✅ test_existing_functionality PASSED (tag filter works)")


if __name__ == "__main__":
    print("Running catalog tests for KAN-65 fix...\n")
    
    try:
        test_default_search_excludes_pending_pets()
        test_empty_status_defaults_to_available()
        test_existing_functionality()
        print("\n✅ All backend tests PASSED")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
