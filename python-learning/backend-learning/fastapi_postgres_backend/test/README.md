# Test Suite for FastAPI PostgreSQL Backend

This directory contains comprehensive tests for the FastAPI PostgreSQL Backend application.

## Test Structure

```
test/
├── __init__.py              # Makes test directory a Python package
├── conftest.py              # Pytest fixtures and configuration
├── test_users.py            # User API endpoint tests
├── pytest.ini              # Pytest configuration
├── run_tests.py             # Test runner script
└── README.md                # This file
```

## Running Tests

### Basic Test Commands

```bash
# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run tests with coverage
uv run pytest --cov=app --cov-report=html --cov-report=term

# Run specific test file
uv run pytest test/test_users.py

# Run specific test class
uv run pytest test/test_users.py::TestUserCreate

# Run specific test method
uv run pytest test/test_users.py::TestUserCreate::test_create_user_success
```

### Using the Test Runner Script

```bash
# Run all tests
python test/run_tests.py

# Run with verbose output
python test/run_tests.py --verbose

# Run with coverage
python test/run_tests.py --coverage

# Run specific test file
python test/run_tests.py --test-file test/test_users.py
```

### Using Makefile Commands

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov
```

## Test Categories

### Unit Tests
- Test individual functions and methods
- Mock external dependencies
- Fast execution

### Integration Tests
- Test API endpoints with database
- Test complete workflows
- Use test database

### Validation Tests
- Test input validation
- Test error handling
- Test edge cases

## Test Database

Tests use an in-memory SQLite database for fast execution and isolation. The database is:
- Created fresh for each test session
- Dropped after tests complete
- Isolated from your development database

## Fixtures

### Available Fixtures

- `client`: AsyncClient for making HTTP requests
- `db_session`: AsyncSession for database operations
- `test_user_data`: Sample user data dictionary
- `test_user_create`: UserCreate object
- `test_users_data`: List of sample user data

### Using Fixtures

```python
async def test_example(client: AsyncClient, test_user_data: dict):
    response = await client.post("/users/", json=test_user_data)
    assert response.status_code == 200
```

## Test Coverage

The test suite covers:

### User API Endpoints
- ✅ POST /users/ - Create user
- ✅ GET /users/ - Get all users
- ✅ PUT /users/{user_id} - Update user

### Test Scenarios
- ✅ Successful operations
- ✅ Error handling
- ✅ Input validation
- ✅ Edge cases
- ✅ Integration workflows

## Adding New Tests

1. Create a new test file: `test/test_<feature>.py`
2. Import required fixtures from `conftest.py`
3. Write test classes and methods
4. Use descriptive test names
5. Add appropriate assertions

### Example Test Structure

```python
import pytest
from httpx import AsyncClient

class TestNewFeature:
    """Test new feature endpoints."""
    
    async def test_feature_success(self, client: AsyncClient):
        """Test successful feature operation."""
        # Test implementation
        pass
    
    async def test_feature_error(self, client: AsyncClient):
        """Test feature error handling."""
        # Test implementation
        pass
```

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Descriptive Names**: Use clear, descriptive test names
3. **Arrange-Act-Assert**: Structure tests with clear sections
4. **Test Data**: Use fixtures for consistent test data
5. **Error Testing**: Always test error conditions
6. **Coverage**: Aim for high test coverage

## Debugging Tests

To debug tests in VS Code/Cursor:

1. Set breakpoints in test files
2. Use the "Python: Debug Tests" configuration
3. Or run with `--pdb` flag: `uv run pytest --pdb`

## Continuous Integration

Tests are designed to run in CI/CD pipelines:
- Fast execution
- No external dependencies
- Clear pass/fail results
- Coverage reporting 