from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Coupon:
    code: str
    percent: int


COUPONS = {"SAVE10": Coupon("SAVE10", 10), "VIP20": Coupon("VIP20", 20)}
BULK_MIN_QTY = 3  # buy >= 3 of one item: that line gets 10% off


def find_coupon(code: str) -> Coupon | None:
    return COUPONS.get(code.upper())


def line_total(price: Decimal, qty: int) -> Decimal:
    total = price * qty
    if qty > BULK_MIN_QTY:
        total = total * Decimal("0.9")
    return total


def cart_total(items: list[tuple[Decimal, int]], coupon_code: str | None = None) -> Decimal:
    subtotal = sum((line_total(p, q) for p, q in items), Decimal("0"))
    if coupon_code:
        coupon = find_coupon(coupon_code)
        subtotal = subtotal * (100 - coupon.percent) / 100
    return subtotal.quantize(Decimal("0.01"))
