"""
Test to validate that pending pets are never visible in default web UI results.

This test verifies the fix for Jira KAN-148: "Customers are seeing pets that are not available"
Log evidence: docs/logs/pending-pet-visible.ndjson (error code PENDING_PET_VISIBLE)
"""

import pytest

from petstore_app.catalog import search_pets


def test_default_search_excludes_pending_pets_nova() -> None:
    """Regression test: Nova (pet-103, pending) must not appear in default search."""
    results = search_pets()
    
    pet_ids = [pet.id for pet in results]
    pet_names = [pet.name for pet in results]
    
    # Nova (pet-103) must NOT be in default results
    assert "pet-103" not in pet_ids, "Nova (pet-103, pending) should not appear in default available search"
    assert "Nova" not in pet_names, "Nova should not appear in default available search"
    
    # Only available pets should be returned
    for pet in results:
        assert pet.status == "available", f"Pet {pet.name} ({pet.id}) has status {pet.status}, expected 'available'"


def test_search_by_name_nova_returns_empty_by_default() -> None:
    """Searching for Nova by name should return empty results (she is pending, not available)."""
    results = search_pets(query="Nova")
    
    assert len(results) == 0, "Searching for 'Nova' should return no results (she is pending)"


def test_search_dogs_excludes_nova_by_default() -> None:
    """Dog search should return Scout but not Nova (Nova is pending)."""
    results = search_pets(species="dog")
    
    pet_names = [pet.name for pet in results]
    
    assert "Scout" in pet_names, "Scout (available dog) should be in results"
    assert "Nova" not in pet_names, "Nova (pending dog) should NOT be in results"
    assert len(results) == 1, f"Expected 1 dog (Scout), got {len(results)}: {pet_names}"


def test_explicit_pending_search_returns_nova() -> None:
    """Verify that Nova CAN be found when explicitly searching for pending pets."""
    results = search_pets(species="dog", status="pending")
    
    pet_names = [pet.name for pet in results]
    
    assert "Nova" in pet_names, "Nova should be found when explicitly searching for pending dogs"
    assert len(results) == 1, f"Expected 1 pending dog (Nova), got {len(results)}: {pet_names}"
