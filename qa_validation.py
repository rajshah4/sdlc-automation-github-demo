#!/usr/bin/env python3
"""
QA validation script for training level filter feature.
Validates the implementation without requiring pytest.
"""

import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from petstore_app.catalog import search_pets, PETS


def run_test(name: str, test_func):
    """Run a test and report results."""
    try:
        test_func()
        print(f"✓ {name}")
        return True
    except AssertionError as e:
        print(f"✗ {name}: {e}")
        return False
    except Exception as e:
        print(f"✗ {name}: Unexpected error: {e}")
        return False


def test_basic_training_level():
    """Scenario: Filter by basic training level"""
    results = search_pets(training_level="basic")
    expected = ["Mochi", "Pip"]
    actual = [pet.name for pet in results]
    assert actual == expected, f"Expected {expected}, got {actual}"


def test_intermediate_training_level():
    """Scenario: Filter by intermediate training level"""
    results = search_pets(training_level="intermediate")
    expected = ["Scout"]
    actual = [pet.name for pet in results]
    assert actual == expected, f"Expected {expected}, got {actual}"


def test_advanced_training_level():
    """Scenario: Filter by advanced training level (pending pet)"""
    results = search_pets(training_level="advanced", status="pending")
    expected = ["Nova"]
    actual = [pet.name for pet in results]
    assert actual == expected, f"Expected {expected}, got {actual}"


def test_no_training_level_filter():
    """Scenario: No training level filter applied"""
    results = search_pets()
    expected = ["Mochi", "Scout", "Pip"]  # Available pets only
    actual = [pet.name for pet in results]
    assert actual == expected, f"Expected {expected}, got {actual}"


def test_training_level_respects_status():
    """Scenario: Filter respects existing status filter"""
    # Nova has advanced training but is pending, should be excluded with default status
    results = search_pets(training_level="advanced")
    assert results == [], f"Expected no results (Nova is pending), got {[p.name for p in results]}"


def test_combine_training_with_species():
    """Scenario: Combine training level with other filters"""
    results = search_pets(species="dog", training_level="intermediate")
    expected = ["Scout"]
    actual = [pet.name for pet in results]
    assert actual == expected, f"Expected {expected}, got {actual}"


def test_case_insensitive():
    """Training level should be case insensitive"""
    results = search_pets(training_level="BASIC")
    expected = ["Mochi", "Pip"]
    actual = [pet.name for pet in results]
    assert actual == expected, f"Expected {expected}, got {actual}"


def test_whitespace_handling():
    """Training level should handle leading/trailing whitespace"""
    results = search_pets(training_level="  basic  ")
    expected = ["Mochi", "Pip"]
    actual = [pet.name for pet in results]
    assert actual == expected, f"Expected {expected}, got {actual}"


def test_data_integrity():
    """Verify all pets have training level tags"""
    for pet in PETS:
        training_levels = {"basic", "intermediate", "advanced"}
        has_training = any(tag in training_levels for tag in pet.tags)
        assert has_training, f"Pet {pet.name} missing training level tag: {pet.tags}"


def main():
    print("=" * 60)
    print("QA Validation: Training Level Filter (PR #102)")
    print("=" * 60)
    print()
    
    tests = [
        ("Filter by basic training level", test_basic_training_level),
        ("Filter by intermediate training level", test_intermediate_training_level),
        ("Filter by advanced training level", test_advanced_training_level),
        ("No training level filter applied", test_no_training_level_filter),
        ("Training level respects status filter", test_training_level_respects_status),
        ("Combine training with species filter", test_combine_training_with_species),
        ("Case insensitive filtering", test_case_insensitive),
        ("Whitespace handling", test_whitespace_handling),
        ("Data integrity check", test_data_integrity),
    ]
    
    results = [run_test(name, func) for name, func in tests]
    
    print()
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print(f"✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
