.PHONY: install install-dev clean test lint format check run run-dev migrate help

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install production dependencies"
	@echo "  install-dev - Install development dependencies"
	@echo "  clean       - Clean up cache and temporary files"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting checks"
	@echo "  format      - Format code with black and isort"
	@echo "  check       - Run type checking with mypy"
	@echo "  run         - Run the application in production mode"
	@echo "  run-dev     - Run the application in development mode"
	@echo "  migrate     - Run database migrations"

# Install production dependencies
install:
	uv sync

# Install development dependencies
install-dev:
	uv sync --dev

# Clean up
clean:
	uv cache clean
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

# Run tests
test:
	uv run pytest

# Run tests with coverage
test-cov:
	uv run pytest --cov=app --cov-report=html --cov-report=term

# Run linting
lint:
	uv run flake8 app tests
	uv run black --check app tests
	uv run isort --check-only app tests

# Format code
format:
	uv run black app tests
	uv run isort app tests

# Type checking
check:
	uv run mypy app

# Run all checks
check-all: lint check test

# Run the application in production mode
run:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Run the application in development mode
run-dev:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

# Run database migrations
migrate:
	uv run python migrate.py

# Create new migration
migrate-create:
	uv run alembic revision --autogenerate -m "$(message)"

# Upgrade database
migrate-upgrade:
	uv run alembic upgrade head

# Downgrade database
migrate-downgrade:
	uv run alembic downgrade -1

# Show migration history
migrate-history:
	uv run alembic history

# Show current migration
migrate-current:
	uv run alembic current

# Install pre-commit hooks
install-hooks:
	uv run pre-commit install

# Update dependencies
update:
	uv lock --upgrade

# Show outdated packages
outdated:
	uv lock --check

# Export requirements
export-requirements:
	uv export --format requirements-txt > requirements.txt

# Export requirements with dev dependencies
export-requirements-dev:
	uv export --format requirements-txt --dev > requirements-dev.txt 