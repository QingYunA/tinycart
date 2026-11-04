from decimal import Decimal

import pytest

from tinycart.pricing import cart_total


def test_single_item_no_coupon():
    assert cart_total([(Decimal("10.00"), 1)]) == Decimal("10.00")


def test_coupon_save10():
    assert cart_total([(Decimal("10.00"), 1)], "SAVE10") == Decimal("9.00")


def test_unknown_coupon_is_rejected():
    with pytest.raises(ValueError, match="unknown coupon"):
        cart_total([(Decimal("10.00"), 1)], "NOPE")


def test_bulk_discount_applies_at_exactly_three():
    # spec: features/pricing.md -- qty >= 3 gets 10% off that line
    assert cart_total([(Decimal("10.00"), 3)]) == Decimal("27.00")


def test_no_bulk_discount_at_two():
    assert cart_total([(Decimal("10.00"), 2)]) == Decimal("20.00")
