#!/usr/bin/env python3
"""
OpenSpec Acceptance Criteria Verification for PR #102
Maps implemented tests to specification scenarios.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "app"))

from petstore_app.catalog import search_pets


def verify_scenario(scenario_name: str, test_func):
    """Verify a scenario from the OpenSpec."""
    try:
        test_func()
        print(f"✓ {scenario_name}")
        return True
    except AssertionError as e:
        print(f"✗ {scenario_name}: {e}")
        return False


def scenario_filter_by_basic():
    """OpenSpec: Filter by basic training level"""
    results = search_pets(training_level="basic")
    names = [p.name for p in results]
    
    # Then only pets with "basic" training tag are returned
    assert all("basic" in p.tags for p in results), "All results should have basic tag"
    
    # And pets with other training levels are excluded
    all_pets = search_pets(status="available")
    intermediate_pets = [p for p in all_pets if "intermediate" in p.tags]
    advanced_pets = [p for p in all_pets if "advanced" in p.tags]
    assert not any(p in results for p in intermediate_pets), "No intermediate pets should be returned"
    assert not any(p in results for p in advanced_pets), "No advanced pets should be returned"


def scenario_filter_by_intermediate():
    """OpenSpec: Filter by intermediate training level"""
    results = search_pets(training_level="intermediate")
    
    # Then only pets with "intermediate" training tag are returned
    assert all("intermediate" in p.tags for p in results), "All results should have intermediate tag"
    assert len(results) == 1 and results[0].name == "Scout", "Should return Scout only"


def scenario_filter_by_advanced():
    """OpenSpec: Filter by advanced training level"""
    results = search_pets(training_level="advanced", status="pending")
    
    # Then only pets with "advanced" training tag are returned
    assert all("advanced" in p.tags for p in results), "All results should have advanced tag"
    assert len(results) == 1 and results[0].name == "Nova", "Should return Nova only"


def scenario_no_training_filter():
    """OpenSpec: No training level filter applied"""
    results = search_pets()
    
    # Then all pets matching other criteria are returned
    # Default status is "available", so should get all available pets
    expected_count = 3  # Mochi, Scout, Pip
    assert len(results) == expected_count, f"Should return {expected_count} available pets"
    
    # And training level does not affect results
    names = [p.name for p in results]
    assert "Mochi" in names and "Scout" in names and "Pip" in names


def scenario_respects_status_filter():
    """OpenSpec: Filter respects existing status filter"""
    results = search_pets(training_level="basic")
    
    # Then only available pets with basic training are returned
    assert all(p.status == "available" for p in results), "All should be available"
    assert all("basic" in p.tags for p in results), "All should have basic training"
    
    # And pending pets are excluded regardless of training level
    assert not any(p.status == "pending" for p in results), "No pending pets should be returned"


def scenario_combine_filters():
    """OpenSpec: Combine training level with other filters"""
    results = search_pets(species="dog", training_level="intermediate")
    
    # Then only dogs with basic training are returned (Scout has intermediate, not basic)
    # Actually the spec says intermediate in the example
    assert len(results) == 1, "Should return one result"
    assert results[0].species == "dog", "Should be a dog"
    assert "intermediate" in results[0].tags, "Should have intermediate training"
    
    # Verify no cats returned
    assert not any(p.species == "cat" for p in results), "No cats should be returned"


def main():
    print("=" * 70)
    print("OpenSpec Acceptance Criteria Verification - PR #102")
    print("Spec: openspec/changes/jira-KAN-106-training-level-filter/")
    print("=" * 70)
    print()
    
    scenarios = [
        ("Scenario: Filter by basic training level", scenario_filter_by_basic),
        ("Scenario: Filter by intermediate training level", scenario_filter_by_intermediate),
        ("Scenario: Filter by advanced training level", scenario_filter_by_advanced),
        ("Scenario: No training level filter applied", scenario_no_training_filter),
        ("Scenario: Filter respects existing status filter", scenario_respects_status_filter),
        ("Scenario: Combine training level with other filters", scenario_combine_filters),
    ]
    
    results = [verify_scenario(name, func) for name, func in scenarios]
    
    print()
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"OpenSpec Compliance: {passed}/{total} scenarios verified")
    
    if passed == total:
        print("✓ All acceptance criteria met!")
        return 0
    else:
        print(f"✗ {total - passed} scenario(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
