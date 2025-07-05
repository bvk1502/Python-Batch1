# API Testing - Testing Web Services

This section covers API testing with pytest, including testing REST APIs, handling HTTP requests and responses, and testing API authentication and authorization.

## 📋 What You'll Learn

1. **Basic API Testing**
   - HTTP client setup
   - GET, POST, PUT, DELETE requests
   - Response validation

2. **Advanced API Testing**
   - Authentication testing
   - Error handling
   - Rate limiting
   - Pagination

3. **FastAPI Testing**
   - Testing FastAPI applications
   - Using TestClient
   - Database integration

4. **Real-World Scenarios**
   - External API testing
   - API mocking
   - Performance testing

## 🚀 Step-by-Step Guide

### Step 1: Basic HTTP Testing

Test simple HTTP requests using `httpx`:

```python
import pytest
import httpx

def test_get_request():
    with httpx.Client() as client:
        response = client.get("https://httpbin.org/get")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

def test_post_request():
    with httpx.Client() as client:
        data = {"name": "John", "age": 30}
        response = client.post("https://httpbin.org/post", json=data)
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["json"]["name"] == "John"
```

### Step 2: FastAPI Testing

Test FastAPI applications using TestClient:

```python
from fastapi.testclient import TestClient
from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def get_users():
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

@app.post("/users")
def create_user(user: dict):
    return {"id": 3, **user}

def test_get_users():
    client = TestClient(app)
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_create_user():
    client = TestClient(app)
    user_data = {"name": "Charlie", "email": "charlie@example.com"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Charlie"
```

### Step 3: Authentication Testing

Test APIs with authentication:

```python
def test_authenticated_request():
    client = TestClient(app)
    
    # Login to get token
    login_data = {"username": "testuser", "password": "testpass"}
    login_response = client.post("/login", data=login_data)
    token = login_response.json()["access_token"]
    
    # Use token for authenticated request
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200

def test_unauthorized_request():
    client = TestClient(app)
    response = client.get("/protected")
    assert response.status_code == 401
```

### Step 4: Error Handling

Test API error responses:

```python
def test_not_found():
    client = TestClient(app)
    response = client.get("/users/999")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

def test_validation_error():
    client = TestClient(app)
    invalid_data = {"name": ""}  # Empty name should fail validation
    response = client.post("/users", json=invalid_data)
    assert response.status_code == 422
```

## 📁 File Structure

```
06_api_testing/
├── README.md
├── test_basic_api.py
├── test_fastapi_app.py
├── test_authentication.py
├── test_error_handling.py
├── test_external_apis.py
├── test_performance.py
├── conftest.py
├── app.py
├── models.py
└── requirements.txt
```

## 🎯 Key Concepts

### 1. HTTP Client Testing
- Use `httpx` for external API testing
- Use `TestClient` for FastAPI applications
- Handle different HTTP methods and status codes

### 2. Response Validation
- Check status codes
- Validate response structure
- Test response headers
- Verify response content

### 3. Authentication
- Test token-based authentication
- Handle session management
- Test authorization levels
- Validate security headers

### 4. Error Scenarios
- Test 4xx and 5xx status codes
- Validate error response formats
- Test rate limiting
- Handle network errors

## 🔧 Advanced Patterns

### Parameterized API Testing
```python
@pytest.mark.parametrize("endpoint,method,expected_status", [
    ("/users", "GET", 200),
    ("/users", "POST", 201),
    ("/users/1", "GET", 200),
    ("/users/999", "GET", 404),
    ("/users/1", "PUT", 200),
    ("/users/1", "DELETE", 204),
])
def test_api_endpoints(client, endpoint, method, expected_status):
    response = client.request(method, endpoint)
    assert response.status_code == expected_status
```

### API Fixtures
```python
@pytest.fixture
def authenticated_client():
    client = TestClient(app)
    
    # Login and get token
    login_response = client.post("/login", data={
        "username": "testuser",
        "password": "testpass"
    })
    token = login_response.json()["access_token"]
    
    # Add token to headers
    client.headers = {"Authorization": f"Bearer {token}"}
    return client

def test_protected_endpoint(authenticated_client):
    response = authenticated_client.get("/protected")
    assert response.status_code == 200
```

### Mock External APIs
```python
def test_external_api_integration():
    with patch('httpx.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "external_data"}
        mock_get.return_value = mock_response
        
        result = fetch_external_data()
        assert result == {"data": "external_data"}
```

### Performance Testing
```python
def test_api_performance():
    client = TestClient(app)
    
    start_time = time.time()
    response = client.get("/users")
    end_time = time.time()
    
    assert response.status_code == 200
    assert (end_time - start_time) < 1.0  # Should respond within 1 second
```

## 📊 Best Practices

### 1. Test Structure
- Use descriptive test names
- Group related tests together
- Separate positive and negative test cases
- Use fixtures for common setup

### 2. Response Validation
- Always check status codes
- Validate response structure
- Test edge cases and error conditions
- Verify business logic

### 3. Authentication
- Test both authenticated and unauthenticated requests
- Verify token expiration
- Test different user roles
- Validate security headers

### 4. Error Handling
- Test all expected error conditions
- Validate error response formats
- Test rate limiting and timeouts
- Handle network failures gracefully

## 🎓 Exercises

1. Create tests for a simple REST API
2. Test authentication and authorization
3. Implement error handling tests
4. Create performance tests for API endpoints
5. Test external API integrations

## 📚 Real-World Examples

### User Management API
```python
def test_user_crud_operations():
    client = TestClient(app)
    
    # Create user
    user_data = {"name": "Alice", "email": "alice@example.com"}
    create_response = client.post("/users", json=user_data)
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]
    
    # Get user
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Alice"
    
    # Update user
    update_data = {"name": "Alice Updated"}
    update_response = client.put(f"/users/{user_id}", json=update_data)
    assert update_response.status_code == 200
    
    # Delete user
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204
    
    # Verify user is deleted
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404
```

### Authentication Flow
```python
def test_authentication_flow():
    client = TestClient(app)
    
    # Test registration
    register_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "securepass123"
    }
    register_response = client.post("/register", json=register_data)
    assert register_response.status_code == 201
    
    # Test login
    login_data = {
        "username": "newuser",
        "password": "securepass123"
    }
    login_response = client.post("/login", data=login_data)
    assert login_response.status_code == 200
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test protected endpoint
    protected_response = client.get("/profile", headers=headers)
    assert protected_response.status_code == 200
    
    # Test invalid token
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    invalid_response = client.get("/profile", headers=invalid_headers)
    assert invalid_response.status_code == 401
```

### Error Handling
```python
def test_comprehensive_error_handling():
    client = TestClient(app)
    
    # Test validation errors
    invalid_user = {"name": "", "email": "invalid-email"}
    response = client.post("/users", json=invalid_user)
    assert response.status_code == 422
    assert "validation error" in response.json()["detail"].lower()
    
    # Test not found
    response = client.get("/users/999999")
    assert response.status_code == 404
    
    # Test method not allowed
    response = client.patch("/users")
    assert response.status_code == 405
    
    # Test server error (if applicable)
    response = client.get("/error-endpoint")
    assert response.status_code == 500
```

### Rate Limiting
```python
def test_rate_limiting():
    client = TestClient(app)
    
    # Make multiple requests quickly
    for i in range(10):
        response = client.get("/api/endpoint")
        if response.status_code == 429:  # Rate limited
            break
        assert response.status_code == 200
    
    # Wait and try again
    time.sleep(1)
    response = client.get("/api/endpoint")
    assert response.status_code == 200
```

## 📚 Next Steps

After completing this section, you should:
- Understand how to test REST APIs with pytest
- Be able to test FastAPI applications
- Know how to handle authentication and authorization
- Understand error handling and validation
- Be familiar with performance testing techniques

Proceed to the next section: **07_advanced_patterns/** to learn about advanced pytest patterns. 