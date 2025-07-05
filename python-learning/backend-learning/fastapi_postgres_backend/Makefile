.PHONY: test test-tdd test-unit test-integration test-cov clean install-dev sync

# Install dependencies using uv
install-dev:
	uv sync --dev

# Sync dependencies
sync:
	uv sync

# Run all tests
test:
	uv run pytest test/ -v --asyncio-mode=auto

# Run TDD cycle
test-tdd:
	uv run python test/run_all_tests.py --tdd

# Run unit tests only
test-unit:
	uv run pytest test/ -v -m "not integration" --asyncio-mode=auto

# Run integration tests only
test-integration:
	uv run pytest test/ -v -m "integration" --asyncio-mode=auto

# Run with coverage
test-cov:
	uv run pytest test/ -v --cov=app --cov-report=html --asyncio-mode=auto

# Run specific test class
test-class:
	uv run python test/run_all_tests.py --class $(CLASS)

# Run tests in watch mode
test-watch:
	uv run ptw test/ -- -v --asyncio-mode=auto

# Run tests with specific markers
test-markers:
	uv run pytest test/ -v -m "$(MARKERS)" --asyncio-mode=auto

# Run linting
lint:
	uv run black app/ test/
	uv run isort app/ test/
	uv run flake8 app/ test/

# Run type checking
type-check:
	uv run mypy app/

# Run all checks (lint + type-check + test)
check: lint type-check test

# Clean up
clean:
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	rm -rf .mypy_cache/
	rm -rf .coverage

# Install project in editable mode
install:
	uv pip install -e .

# Update dependencies
update:
	uv lock --upgrade

# Show dependency tree
deps:
	uv tree

# Run the application
run:
	uv run uvicorn app.main:app --reload

# Run the application in production mode
run-prod:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

# Database migrations
migrate:
	uv run alembic upgrade head

# Create new migration
migrate-create:
	uv run alembic revision --autogenerate -m "$(MESSAGE)"

# Reset database (for development)
reset-db:
	uv run python migrate.py 