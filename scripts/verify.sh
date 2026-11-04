#!/usr/bin/env bash
# L1: one command, deterministic, same locally and in CI. Exit != 0 means not done.
set -euo pipefail
echo "== ruff lint";   uv run ruff check .
echo "== ruff format"; uv run ruff format --check .
echo "== ty";          uv run ty check
echo "== pytest";      uv run pytest -q
echo "VERIFY: PASS"
