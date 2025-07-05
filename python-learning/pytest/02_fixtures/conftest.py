"""
Shared fixtures for the fixtures tutorial section.
This file is automatically discovered by pytest and fixtures defined here
are available to all test files in this directory and subdirectories.
"""
import pytest
import tempfile
import os
import json
from typing import Dict, List, Any


@pytest.fixture
def sample_numbers():
    """Basic fixture returning a list of numbers."""
    return [1, 2, 3, 4, 5]


@pytest.fixture
def sample_strings():
    """Fixture returning a list of strings."""
    return ["apple", "banana", "cherry", "date", "elderberry"]


@pytest.fixture
def sample_dict():
    """Fixture returning a dictionary."""
    return {
        "name": "John Doe",
        "age": 30,
        "city": "New York",
        "skills": ["Python", "JavaScript", "SQL"]
    }


@pytest.fixture
def sample_user():
    """Fixture returning a user object."""
    class User:
        def __init__(self, name, age, email):
            self.name = name
            self.age = age
            self.email = email
        
        def get_info(self):
            return f"{self.name} ({self.age}) - {self.email}"
    
    return User("Alice", 25, "alice@example.com")


@pytest.fixture(scope="session")
def session_data():
    """Session-scoped fixture that persists throughout the test session."""
    return {
        "session_id": "test_session_123",
        "start_time": "2024-01-01T00:00:00Z",
        "config": {
            "environment": "test",
            "debug": True
        }
    }


@pytest.fixture(scope="module")
def module_data():
    """Module-scoped fixture that persists throughout the test module."""
    return {
        "module_name": "test_module",
        "test_count": 0
    }


@pytest.fixture(scope="class")
def class_data():
    """Class-scoped fixture that persists throughout the test class."""
    return {
        "class_name": "TestClass",
        "setup_complete": False
    }


@pytest.fixture
def temp_file():
    """Fixture that creates a temporary file and cleans it up."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("This is a temporary test file.\n")
        f.write("It will be automatically cleaned up.\n")
        temp_path = f.name
    
    # Provide the file path to the test
    yield temp_path
    
    # Cleanup: remove the file after the test
    try:
        os.unlink(temp_path)
    except FileNotFoundError:
        pass  # File might already be deleted


@pytest.fixture
def temp_json_file():
    """Fixture that creates a temporary JSON file with sample data."""
    data = {
        "users": [
            {"id": 1, "name": "Alice", "age": 25},
            {"id": 2, "name": "Bob", "age": 30},
            {"id": 3, "name": "Charlie", "age": 35}
        ],
        "settings": {
            "theme": "dark",
            "language": "en"
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(data, f)
        temp_path = f.name
    
    yield temp_path
    
    try:
        os.unlink(temp_path)
    except FileNotFoundError:
        pass


@pytest.fixture
def database_connection():
    """Mock database connection fixture."""
    class MockConnection:
        def __init__(self):
            self.connected = True
            self.transactions = []
        
        def execute(self, query):
            self.transactions.append(query)
            return {"rows_affected": 1}
        
        def commit(self):
            pass
        
        def rollback(self):
            self.transactions.clear()
        
        def close(self):
            self.connected = False
    
    connection = MockConnection()
    yield connection
    connection.close()


@pytest.fixture
def api_client():
    """Mock API client fixture."""
    class MockAPIClient:
        def __init__(self):
            self.base_url = "https://api.example.com"
            self.authenticated = False
            self.requests = []
        
        def authenticate(self, username, password):
            self.authenticated = True
            self.username = username
            return {"token": "mock_token_123"}
        
        def get(self, endpoint):
            self.requests.append(("GET", endpoint))
            return {"status": 200, "data": {"message": "Success"}}
        
        def post(self, endpoint, data):
            self.requests.append(("POST", endpoint, data))
            return {"status": 201, "data": data}
        
        def logout(self):
            self.authenticated = False
    
    client = MockAPIClient()
    yield client
    client.logout()


@pytest.fixture
def user_factory():
    """Fixture factory for creating user objects."""
    class User:
        def __init__(self, name, age, email, role="user"):
            self.name = name
            self.age = age
            self.email = email
            self.role = role
        
        def is_adult(self):
            return self.age >= 18
        
        def get_display_name(self):
            return f"{self.name} ({self.role})"
    
    def create_user(name="John", age=30, email="john@example.com", role="user"):
        return User(name=name, age=age, email=email, role=role)
    
    return create_user


@pytest.fixture(params=[1, 2, 3, 5, 8, 13])
def fibonacci_number(request):
    """Parametrized fixture providing Fibonacci numbers."""
    return request.param


@pytest.fixture(params=["admin", "user", "guest"])
def user_role(request):
    """Parametrized fixture providing different user roles."""
    return request.param


@pytest.fixture
def complex_data_structure():
    """Fixture providing a complex nested data structure."""
    return {
        "company": {
            "name": "TechCorp",
            "employees": [
                {
                    "id": 1,
                    "name": "Alice",
                    "department": "Engineering",
                    "skills": ["Python", "JavaScript"],
                    "projects": [
                        {"name": "Project A", "status": "active"},
                        {"name": "Project B", "status": "completed"}
                    ]
                },
                {
                    "id": 2,
                    "name": "Bob",
                    "department": "Marketing",
                    "skills": ["SEO", "Content"],
                    "projects": [
                        {"name": "Campaign X", "status": "active"}
                    ]
                }
            ],
            "departments": {
                "Engineering": {"head": "Alice", "budget": 100000},
                "Marketing": {"head": "Bob", "budget": 50000}
            }
        }
    }


@pytest.fixture
def mock_external_service():
    """Fixture that mocks an external service."""
    class MockExternalService:
        def __init__(self):
            self.calls = []
            self.responses = {}
        
        def set_response(self, method, endpoint, response):
            self.responses[(method, endpoint)] = response
        
        def get(self, endpoint):
            self.calls.append(("GET", endpoint))
            return self.responses.get(("GET", endpoint), {"status": "success"})
        
        def post(self, endpoint, data):
            self.calls.append(("POST", endpoint, data))
            return self.responses.get(("POST", endpoint), {"status": "created"})
        
        def get_call_count(self):
            return len(self.calls)
    
    service = MockExternalService()
    yield service
    # Cleanup if needed
    service.calls.clear()
    service.responses.clear() 