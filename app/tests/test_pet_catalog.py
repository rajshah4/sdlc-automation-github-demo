import pytest

from petstore_app.catalog import format_age, search_pets


def test_format_age_years_only() -> None:
    assert format_age(24) == "2 years"
    assert format_age(12) == "1 year"
    assert format_age(36) == "3 years"


def test_format_age_months_only() -> None:
    assert format_age(9) == "9 months"
    assert format_age(1) == "1 month"
    assert format_age(11) == "11 months"


def test_format_age_years_and_months() -> None:
    assert format_age(18) == "1 year 6 months"
    assert format_age(28) == "2 years 4 months"
    assert format_age(14) == "1 year 2 months"
    assert format_age(27) == "2 years 3 months"


def test_format_age_zero() -> None:
    assert format_age(0) == "0 months"


def test_format_age_negative_raises_error() -> None:
    with pytest.raises(ValueError, match="Age cannot be negative"):
        format_age(-1)


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
