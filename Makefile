.PHONY: install test lint fmt check

install:
	uv sync

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check .

fmt:
	uv run ruff format .

check: lint test
