import pytest

from petstore_app.catalog import search_pets


def test_search_pets_filters_by_species_and_status() -> None:
    results = search_pets(species="dog")

    assert [pet.id for pet in results] == ["pet-101"]


def test_search_pets_can_find_pending_pets_when_requested() -> None:
    results = search_pets(species="dog", status="pending")

    assert [pet.name for pet in results] == ["Nova"]


def test_search_pets_filters_by_tag() -> None:
    results = search_pets(tag="indoor")

    assert [pet.name for pet in results] == ["Mochi", "Pip"]


@pytest.mark.parametrize("max_results", [0, 51])
def test_search_pets_validates_max_results(max_results: int) -> None:
    with pytest.raises(ValueError, match="max_results"):
        search_pets(max_results=max_results)


def test_search_pets_filters_by_max_fee() -> None:
    # Mochi=$75 (7500¢) and Pip=$45 (4500¢) are under $120; Scout=$125 (12500¢) is excluded.
    results = search_pets(max_fee_cents=12000)

    assert [pet.name for pet in results] == ["Mochi", "Pip"]


def test_search_pets_includes_pets_at_exact_fee_boundary() -> None:
    results = search_pets(max_fee_cents=7500)

    assert any(pet.name == "Mochi" for pet in results)


def test_search_pets_rejects_negative_max_fee() -> None:
    with pytest.raises(ValueError, match="max_fee_cents"):
        search_pets(max_fee_cents=-1)


def test_search_pets_no_fee_filter_when_max_fee_none() -> None:
    all_available = search_pets()
    with_none = search_pets(max_fee_cents=None)

    assert [pet.id for pet in all_available] == [pet.id for pet in with_none]


def test_search_pets_filters_by_minimum_age() -> None:
    # Mochi=18mo, Scout=28mo, Pip=9mo are available; Nova=14mo is pending.
    # With min_age_months=15, only Scout (28mo) and Mochi (18mo) match.
    results = search_pets(min_age_months=15)

    assert [pet.name for pet in results] == ["Mochi", "Scout"]


def test_search_pets_filters_by_maximum_age() -> None:
    # With max_age_months=20, Mochi (18mo) and Pip (9mo) match; Scout (28mo) is excluded.
    results = search_pets(max_age_months=20)

    assert [pet.name for pet in results] == ["Mochi", "Pip"]


def test_search_pets_filters_by_age_range() -> None:
    # With range 10-20 months, Mochi (18mo) matches; Pip (9mo) and Scout (28mo) are excluded.
    results = search_pets(min_age_months=10, max_age_months=20)

    assert [pet.name for pet in results] == ["Mochi"]


def test_search_pets_includes_pets_at_exact_age_boundaries() -> None:
    # Mochi is exactly 18 months; boundary should be inclusive.
    results = search_pets(min_age_months=18, max_age_months=18)

    assert any(pet.name == "Mochi" for pet in results)


def test_search_pets_rejects_negative_min_age() -> None:
    with pytest.raises(ValueError, match="min_age_months"):
        search_pets(min_age_months=-1)


def test_search_pets_rejects_negative_max_age() -> None:
    with pytest.raises(ValueError, match="max_age_months"):
        search_pets(max_age_months=-5)


def test_search_pets_rejects_inverted_age_range() -> None:
    with pytest.raises(ValueError, match="min_age_months cannot exceed max_age_months"):
        search_pets(min_age_months=30, max_age_months=10)


def test_search_pets_no_age_filter_when_ages_none() -> None:
    all_available = search_pets()
    with_none = search_pets(min_age_months=None, max_age_months=None)

    assert [pet.id for pet in all_available] == [pet.id for pet in with_none]


def test_search_pets_min_age_only_is_valid() -> None:
    # Only min_age_months specified; should work without error.
    results = search_pets(min_age_months=10)

    assert len(results) > 0


def test_search_pets_max_age_only_is_valid() -> None:
    # Only max_age_months specified; should work without error.
    results = search_pets(max_age_months=25)

    assert len(results) > 0
