.PHONY: install test lint format docs docs-build clean help

help:
	@echo "Available targets:"
	@echo "  install     - Install package in development mode with dev dependencies"
	@echo "  test        - Run tests with coverage"
	@echo "  lint        - Run linting checks (ruff and black)"
	@echo "  format      - Format code with ruff and black"
	@echo "  docs        - Serve documentation locally"
	@echo "  docs-build  - Build documentation"
	@echo "  clean       - Remove build artifacts and caches"

install:
	pip install -e ".[dev]"

test:
	pytest tests/ --cov=src/mbse_diagram_parser --cov-report=term-missing

lint:
	ruff check src/ tests/
	black --check src/ tests/

format:
	ruff check --fix src/ tests/
	black src/ tests/

docs:
	mkdocs serve

docs-build:
	mkdocs build

clean:
	rm -rf dist/ build/ *.egg-info site/ .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
