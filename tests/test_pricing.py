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
