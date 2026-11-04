"""Guards for mistakes agents made more than once. Each message says how to fix it."""

import ast
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src" / "tinycart"


def test_no_float_in_money_code():
    hits = [
        f"{p.name}:{n.lineno}"
        for p in SRC.rglob("*.py")
        for n in ast.walk(ast.parse(p.read_text()))
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "float"
    ]
    assert not hits, (
        f"float() in money code at {hits}. Money stays Decimal end to end. "
        'For JSON, emit a string: {"total": str(total)} -> "27.00". See AGENTS.md#rules.'
    )
