.PHONY: verify drive
verify:  ## L1: lint + format + types + tests
	./scripts/verify.sh
drive:   ## L2: run the real CLI on scenarios, write evidence/
	uv run python scripts/drive.py
