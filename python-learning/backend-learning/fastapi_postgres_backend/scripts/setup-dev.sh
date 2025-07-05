#!/bin/bash

echo "�� Setting up FastAPI Backend Development Environment with uv..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source ~/.bashrc  # or source ~/.zshrc for zsh
fi

echo "✅ uv is installed"

# Install dependencies
echo "📦 Installing dependencies..."
uv sync --dev

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "�� Creating .env file..."
    cp env-sample .env
    echo "⚠️  Please update .env file with your database credentials"
fi

# Run database migrations
echo "��️  Running database migrations..."
uv run alembic upgrade head

# Run tests to verify setup
echo "🧪 Running tests to verify setup..."
uv run pytest test/ -v

echo "✅ Development environment setup complete!"
echo ""
echo "�� Available commands:"
echo "  uv run pytest test/ -v                    # Run all tests"
echo "  uv run python test/run_all_tests.py --tdd # Run TDD cycle"
echo "  uv run uvicorn app.main:app --reload      # Run development server"
echo "  make test                                 # Run tests (using Makefile)"
echo "  make test-tdd                             # Run TDD cycle (using Makefile)" 