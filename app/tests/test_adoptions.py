import pytest

from petstore_app.adoptions import create_adoption_order


def test_create_adoption_order_returns_totals_in_cents() -> None:
    order = create_adoption_order(
        "pet-100",
        "casey@example.com",
        donation_cents=2500,
    )

    assert order.pet_id == "pet-100"
    assert order.adoption_fee_cents == 7500
    assert order.donation_cents == 2500
    assert order.total_cents == 10000


def test_create_adoption_order_rejects_pending_pet() -> None:
    with pytest.raises(ValueError, match="not available"):
        create_adoption_order("pet-103", "casey@example.com")


def test_create_adoption_order_rejects_invalid_email() -> None:
    with pytest.raises(ValueError, match="email"):
        create_adoption_order("pet-100", "casey")


def test_create_adoption_order_rejects_negative_donation() -> None:
    with pytest.raises(ValueError, match="donation"):
        create_adoption_order("pet-100", "casey@example.com", donation_cents=-1)


def test_create_adoption_order_trims_leading_whitespace() -> None:
    order = create_adoption_order(" pet-100", "casey@example.com")
    assert order.pet_id == "pet-100"


def test_create_adoption_order_trims_trailing_whitespace() -> None:
    order = create_adoption_order("pet-100 ", "casey@example.com")
    assert order.pet_id == "pet-100"


def test_create_adoption_order_trims_both_whitespace() -> None:
    order = create_adoption_order("  pet-100  ", "casey@example.com")
    assert order.pet_id == "pet-100"


def test_create_adoption_order_rejects_invalid_pet_after_trim() -> None:
    with pytest.raises(ValueError, match="pet_id was not found"):
        create_adoption_order(" pet-999 ", "casey@example.com")

