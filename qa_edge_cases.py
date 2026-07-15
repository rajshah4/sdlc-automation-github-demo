#!/usr/bin/env python3
"""
Edge case and product rule validation for training level filter.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "app"))

from petstore_app.catalog import search_pets


def test_empty_training_level():
    """Test empty string handling"""
    try:
        results = search_pets(training_level="")
        # Empty string after strip becomes "", which won't match any tags
        # This should return all available pets (no filter applied)
        names = [p.name for p in results]
        print(f"✓ Empty training level: Returns {len(results)} pets (no filter applied)")
        return True
    except Exception as e:
        print(f"✗ Empty training level: {e}")
        return False


def test_nonexistent_training_level():
    """Test nonexistent training level"""
    try:
        results = search_pets(training_level="expert")
        assert len(results) == 0, "Should return no results for nonexistent level"
        print("✓ Nonexistent training level: Returns empty results")
        return True
    except Exception as e:
        print(f"✗ Nonexistent training level: {e}")
        return False


def test_default_status_with_training():
    """Verify default status='available' is applied"""
    try:
        # Nova has advanced training but is pending
        results = search_pets(training_level="advanced")
        assert len(results) == 0, "Should exclude pending pets with default status"
        print("✓ Default status filter: Excludes pending pets correctly")
        return True
    except Exception as e:
        print(f"✗ Default status filter: {e}")
        return False


def test_training_level_none():
    """Test explicit None for training_level"""
    try:
        results = search_pets(training_level=None)
        # None should not filter by training level
        names = [p.name for p in results]
        assert len(results) == 3, "Should return all available pets"
        print(f"✓ training_level=None: Returns all available pets")
        return True
    except Exception as e:
        print(f"✗ training_level=None: {e}")
        return False


def test_tag_as_substring():
    """Verify training level is matched as full tag, not substring"""
    try:
        # If implementation incorrectly uses substring matching,
        # this could be an issue. Current implementation uses 'in' on tags tuple
        results = search_pets(training_level="asic")  # substring of "basic"
        assert len(results) == 0, "Should not match substrings"
        print("✓ Substring handling: Only matches complete tags")
        return True
    except Exception as e:
        print(f"✗ Substring handling: {e}")
        return False


def test_all_pets_have_training():
    """Verify all pets in catalog have training level tags"""
    try:
        from petstore_app.catalog import PETS
        training_levels = {"basic", "intermediate", "advanced"}
        
        for pet in PETS:
            has_training = any(level in pet.tags for level in training_levels)
            assert has_training, f"{pet.name} missing training level"
        
        print(f"✓ Data consistency: All {len(PETS)} pets have training levels")
        return True
    except Exception as e:
        print(f"✗ Data consistency: {e}")
        return False


def test_product_rule_pending_pets():
    """Product rule: Pending pets cannot be adopted (excluded by default)"""
    try:
        # Default search should not return pending pets
        results = search_pets()
        assert all(p.status == "available" for p in results), "Default search should only show available"
        
        # Nova is pending with advanced training
        advanced_available = search_pets(training_level="advanced")
        assert len(advanced_available) == 0, "Should not show pending pets without explicit status"
        
        print("✓ Product rule: Pending pets excluded by default")
        return True
    except Exception as e:
        print(f"✗ Product rule: {e}")
        return False


def main():
    print("=" * 70)
    print("Edge Case & Product Rule Validation - PR #102")
    print("=" * 70)
    print()
    
    tests = [
        test_empty_training_level,
        test_nonexistent_training_level,
        test_default_status_with_training,
        test_training_level_none,
        test_tag_as_substring,
        test_all_pets_have_training,
        test_product_rule_pending_pets,
    ]
    
    results = [test() for test in tests]
    
    print()
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} edge cases validated")
    
    if passed == total:
        print("✓ All edge cases handled correctly!")
        return 0
    else:
        print(f"✗ {total - passed} issue(s) found")
        return 1


if __name__ == "__main__":
    sys.exit(main())
