.PHONY: fmt lint test quickstart

fmt:
	ruff check --fix .
	python -m pip install black >/dev/null 2>&1 || true
	black src tests

lint:
	ruff check .

test:
	pytest -q

quickstart:
	aitestgen generate --in examples/login.feature.yaml --out tests/test_generated_login.py --cases 6 --offline
