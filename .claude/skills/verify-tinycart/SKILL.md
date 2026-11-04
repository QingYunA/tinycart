---
name: verify-tinycart
description: Use after any change to pricing or the CLI, before saying the task is done.
---
# Verify tinycart

1. **Launch**: `uv sync` (the CLI is installed into .venv as `tinycart`).
2. **Doctor**: `uv run tinycart --help` must print usage. If not, stop and report.
3. **Drive**: `make drive` runs every scenario in scripts/scenarios.json
   through the real CLI. New behavior? Add a scenario first, from features/pricing.md.
4. **Evidence**: paste the OK/FAIL table and the `evidence/` path. Any FAIL = not done.
5. **Cleanup**: nothing persistent; evidence/ is gitignored.

Never edit an `expect` value to make a scenario pass. If the spec looks wrong, ask.
