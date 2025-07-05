# Fixtures - Test Setup and Teardown

This section covers pytest fixtures, which are powerful tools for setting up test data, managing resources, and handling test dependencies.

## 📋 What You'll Learn

1. **Basic Fixtures**
   - Creating simple fixtures
   - Fixture scope and lifecycle
   - Fixture dependencies

2. **Fixture Scopes**
   - Function scope (default)
   - Class scope
   - Module scope
   - Session scope

3. **Advanced Fixtures**
   - Parametrized fixtures
   - Fixture factories
   - Conditional fixtures
   - Fixture teardown

4. **Real-World Examples**
   - Database connections
   - File operations
   - API clients
   - Mock objects

## 🚀 Step-by-Step Guide

### Step 1: Basic Fixtures

Fixtures are functions that provide test data or setup. They use the `@pytest.fixture` decorator:

```python
import pytest

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

def test_with_fixture(sample_data):
    assert len(sample_data) == 5
    assert sum(sample_data) == 15
```

### Step 2: Fixture Scopes

Fixtures have different scopes that determine how often they're created:

```python
@pytest.fixture(scope="function")  # Default - created for each test
def function_fixture():
    return "function_scope"

@pytest.fixture(scope="class")     # Created once per test class
def class_fixture():
    return "class_scope"

@pytest.fixture(scope="module")    # Created once per module
def module_fixture():
    return "module_scope"

@pytest.fixture(scope="session")   # Created once per test session
def session_fixture():
    return "session_scope"
```

### Step 3: Fixture Dependencies

Fixtures can depend on other fixtures:

```python
@pytest.fixture
def user_data():
    return {"name": "John", "age": 30}

@pytest.fixture
def user_service(user_data):  # Depends on user_data fixture
    return UserService(user_data)

def test_user_service(user_service):
    assert user_service.get_name() == "John"
```

### Step 4: Fixture Setup and Teardown

Fixtures can handle setup and cleanup:

```python
@pytest.fixture
def database_connection():
    # Setup
    connection = create_database_connection()
    yield connection  # Provide the fixture value
    # Teardown (after yield)
    connection.close()
```

## 📁 File Structure

```
02_fixtures/
├── README.md
├── test_basic_fixtures.py
├── test_fixture_scopes.py
├── test_fixture_dependencies.py
├── test_parametrized_fixtures.py
├── test_fixture_factories.py
├── test_database_fixtures.py
├── test_file_fixtures.py
├── conftest.py
├── sample_data.json
└── temp_files/
```

## 🎯 Key Concepts

### 1. Fixture Basics
- Use `@pytest.fixture` decorator
- Return values or use `yield` for setup/teardown
- Automatically injected into test functions

### 2. Fixture Scopes
- **function**: Created for each test (default)
- **class**: Created once per test class
- **module**: Created once per test module
- **session**: Created once per test session

### 3. Fixture Dependencies
- Fixtures can depend on other fixtures
- Dependencies are automatically resolved
- Circular dependencies are detected

### 4. Fixture Lifecycle
1. **Setup**: Code before `yield` or `return`
2. **Provide**: Value provided to test
3. **Teardown**: Code after `yield` (if using `yield`)

## 🔧 Advanced Patterns

### Parametrized Fixtures
```python
@pytest.fixture(params=[1, 2, 3])
def number_fixture(request):
    return request.param

def test_with_parametrized_fixture(number_fixture):
    assert number_fixture > 0
```

### Fixture Factories
```python
@pytest.fixture
def user_factory():
    def create_user(name="John", age=30):
        return User(name=name, age=age)
    return create_user

def test_user_creation(user_factory):
    user = user_factory(name="Alice", age=25)
    assert user.name == "Alice"
```

### Conditional Fixtures
```python
@pytest.fixture
def database_connection(request):
    if request.config.getoption("--use-real-db"):
        return create_real_connection()
    else:
        return create_mock_connection()
```

## 📊 Best Practices

### 1. Fixture Naming
- Use descriptive names
- Follow snake_case convention
- Make purpose clear

### 2. Fixture Organization
- Put shared fixtures in `conftest.py`
- Group related fixtures together
- Use appropriate scopes

### 3. Resource Management
- Always clean up resources
- Use `yield` for setup/teardown
- Handle exceptions properly

### 4. Performance
- Use appropriate scopes
- Avoid expensive operations in function-scoped fixtures
- Cache expensive data

## 🎓 Exercises

1. Create fixtures for different data types (lists, dictionaries, objects)
2. Implement a fixture that creates and cleans up temporary files
3. Create a fixture factory for user objects
4. Build a fixture that depends on multiple other fixtures
5. Implement a parametrized fixture for testing different scenarios

## 📚 Real-World Examples

### Database Testing
```python
@pytest.fixture(scope="session")
def database():
    db = Database("test_db")
    db.create_tables()
    yield db
    db.drop_tables()
    db.close()

@pytest.fixture
def user_repository(database):
    return UserRepository(database)
```

### File Operations
```python
@pytest.fixture
def temp_file():
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test content")
        temp_path = f.name
    
    yield temp_path
    
    import os
    os.unlink(temp_path)
```

### API Testing
```python
@pytest.fixture
def api_client():
    client = APIClient(base_url="http://localhost:8000")
    client.authenticate("test_user", "test_pass")
    return client

@pytest.fixture
def authenticated_session(api_client):
    session = api_client.create_session()
    yield session
    session.logout()
```

## 📚 Next Steps

After completing this section, you should:
- Understand how to create and use fixtures
- Know when to use different fixture scopes
- Be able to create fixture dependencies
- Understand fixture setup and teardown
- Be familiar with advanced fixture patterns

Proceed to the next section: **03_parameterization/** to learn about test parameterization. 