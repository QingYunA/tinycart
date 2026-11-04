# Pricing

## Sub-features
- 行小计 = 单价 × 数量
- 批量折扣：同一商品买 **满 3 件（≥3）**，该行 9 折
- 优惠券：SAVE10 = 9 折，VIP20 = 8 折；未知券码报错，退出码 2
- 总价保留 2 位小数

## How to get to it (user POV)
写一个 cart.json，然后 `tinycart cart.json --coupon SAVE10`，看最后一行 `TOTAL x.xx`。

## Driving it with scripts/drive.py
`make drive` 会用 scripts/scenarios.json 里的每个场景生成临时 cart.json，
调用真实安装的 `tinycart` 命令，把 stdout / stderr / 退出码写进 `evidence/<时间戳>/`。

## Gotchas
- 金额永远是 `Decimal`，cart.json 里价格写字符串 `"9.99"`。
- 折扣先按行算，再算优惠券。
