.PHONY: install run lint build

install:
	uv sync --locked

run:
	uv run --locked database

lint:
	uv run --locked ruff check .

build:
	uv build
