# tinycart — agent guide

A tiny cart-total CLI. Money is `Decimal`, always.

## Done means
- `make verify` exits 0 (ruff + ty + pytest). Paste its last line.
- For behavior changes: `make drive` and attach `evidence/` output.
- Never say "should work". Show the command and its output.

## Map
- `src/tinycart/pricing.py` — pricing rules (bulk discount, coupons)
- `src/tinycart/cli.py` — CLI entrypoint only, no business logic
- `features/` — what each feature does, from the user's view
- `scripts/drive.py` — runs the real CLI, writes `evidence/`

## Rules (each one is enforced; see the check)
| Rule | Enforced by |
| --- | --- |
| Handle `None` from lookups | ty (`unresolved-attribute`) |
| Bug fix = failing test first | PR template + review |

## Do not
- Edit tests to make them pass. Add a new test instead.
- Touch `.github/` or `pyproject.toml` without saying why.
