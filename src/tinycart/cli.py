import argparse
import json
from decimal import Decimal

from tinycart.pricing import cart_total


def main() -> None:
    parser = argparse.ArgumentParser(prog="tinycart")
    parser.add_argument("cart", help='cart JSON: [{"price": "9.99", "qty": 3}, ...]')
    parser.add_argument("--coupon")
    args = parser.parse_args()
    with open(args.cart) as f:
        raw = json.load(f)
    items = [(Decimal(i["price"]), int(i["qty"])) for i in raw]
    try:
        print(f"TOTAL {cart_total(items, args.coupon)}")
    except ValueError as e:
        parser.exit(2, f"error: {e}\n")


if __name__ == "__main__":
    main()
