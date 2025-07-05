# Best Practices - Writing Effective Tests

This section covers pytest best practices, including test organization, naming conventions, test data management, and documentation to help you write maintainable and effective tests.

## 📋 What You'll Learn

1. **Test Organization**
   - Directory structure
   - Test file organization
   - Test class organization

2. **Naming Conventions**
   - Test function names
   - Fixture names
   - File names

3. **Test Data Management**
   - Test data factories
   - Data cleanup
   - Test isolation

4. **Documentation and Maintenance**
   - Test documentation
   - Code comments
   - Test maintenance

## 🚀 Step-by-Step Guide

### Step 1: Test Organization

Organize your tests in a logical structure:

```
project/
├── src/
│   ├── myapp/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── services.py
│   │   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_utils.py
│   ├── integration/
│   │   ├── test_api.py
│   │   └── test_database.py
│   └── e2e/
│       └── test_user_workflow.py
├── pytest.ini
└── requirements.txt
```

### Step 2: Naming Conventions

Use clear and descriptive names:

```python
# Good test names
def test_user_creation_with_valid_data():
    """Test that a user can be created with valid data."""
    pass

def test_user_creation_fails_with_invalid_email():
    """Test that user creation fails with invalid email format."""
    pass

def test_user_update_changes_only_specified_fields():
    """Test that user update only changes specified fields."""
    pass

# Good fixture names
@pytest.fixture
def valid_user_data():
    """Fixture providing valid user data for testing."""
    return {"name": "John Doe", "email": "john@example.com"}

@pytest.fixture
def authenticated_client():
    """Fixture providing an authenticated API client."""
    pass
```

### Step 3: Test Data Management

Use factories and fixtures for test data:

```python
import factory
from faker import Faker

fake = Faker()

class UserFactory(factory.Factory):
    class Meta:
        model = dict
    
    name = factory.LazyFunction(fake.name)
    email = factory.LazyFunction(fake.email)
    age = factory.LazyFunction(lambda: fake.random_int(min=18, max=80))

@pytest.fixture
def user_factory():
    """Factory for creating test users."""
    return UserFactory

def test_user_creation(user_factory):
    """Test user creation with factory-generated data."""
    user_data = user_factory()
    user = create_user(user_data)
    
    assert user.name == user_data["name"]
    assert user.email == user_data["email"]
```

### Step 4: Test Documentation

Document your tests effectively:

```python
class TestUserService:
    """Test cases for the UserService class."""
    
    def test_create_user_success(self, user_factory):
        """
        Test successful user creation.
        
        Given: Valid user data
        When: Creating a new user
        Then: User should be created successfully with correct data
        """
        # Arrange
        user_data = user_factory()
        
        # Act
        user = user_service.create_user(user_data)
        
        # Assert
        assert user.id is not None
        assert user.name == user_data["name"]
        assert user.email == user_data["email"]
    
    def test_create_user_duplicate_email(self, user_factory):
        """
        Test user creation with duplicate email.
        
        Given: User data with existing email
        When: Creating a new user
        Then: Should raise DuplicateEmailError
        """
        # Arrange
        existing_user = user_factory()
        user_service.create_user(existing_user)
        
        duplicate_user = user_factory()
        duplicate_user["email"] = existing_user["email"]
        
        # Act & Assert
        with pytest.raises(DuplicateEmailError):
            user_service.create_user(duplicate_user)
```

## 📁 File Structure

```
10_best_practices/
├── README.md
├── test_organization_examples/
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── test_naming_examples.py
├── test_data_management.py
├── test_documentation.py
├── pytest.ini
└── requirements.txt
```

## 🎯 Key Concepts

### 1. Test Organization Principles
- Group related tests together
- Separate unit, integration, and e2e tests
- Use descriptive directory names
- Keep test files focused and manageable

### 2. Naming Best Practices
- Use descriptive test names that explain the scenario
- Follow consistent naming patterns
- Include expected outcome in test names
- Use snake_case for Python conventions

### 3. Test Data Management
- Use factories for generating test data
- Keep test data minimal and focused
- Clean up test data after tests
- Use fixtures for shared test data

### 4. Documentation Standards
- Document complex test scenarios
- Use docstrings for test functions
- Include setup, action, and assertion comments
- Document test data requirements

## 🔧 Advanced Patterns

### Test Data Factories
```python
import factory
from faker import Faker

fake = Faker()

class UserFactory(factory.Factory):
    class Meta:
        model = dict
    
    name = factory.LazyFunction(fake.name)
    email = factory.LazyFunction(fake.email)
    age = factory.LazyFunction(lambda: fake.random_int(min=18, max=80))
    
    @factory.post_generation
    def posts(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for post in extracted:
                self["posts"].append(post)

class PostFactory(factory.Factory):
    class Meta:
        model = dict
    
    title = factory.LazyFunction(fake.sentence)
    content = factory.LazyFunction(fake.text)
    author_id = factory.SubFactory(UserFactory)

# Usage in tests
def test_user_with_posts(user_factory, post_factory):
    user = user_factory()
    posts = [post_factory() for _ in range(3)]
    
    user_with_posts = user_factory(posts=posts)
    assert len(user_with_posts["posts"]) == 3
```

### Test Configuration
```python
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    e2e: marks tests as end-to-end tests
```

### Test Categories
```python
import pytest

@pytest.mark.unit
def test_unit_test():
    """Unit test - tests individual function/class."""
    pass

@pytest.mark.integration
def test_integration_test():
    """Integration test - tests component interaction."""
    pass

@pytest.mark.e2e
def test_e2e_test():
    """End-to-end test - tests complete user workflow."""
    pass

@pytest.mark.slow
def test_slow_test():
    """Slow test - takes longer to run."""
    pass
```

### Test Isolation
```python
@pytest.fixture(autouse=True)
def clean_database():
    """Automatically clean database before each test."""
    # Setup
    yield
    # Cleanup
    database.cleanup()

@pytest.fixture
def isolated_user():
    """Create a user that gets cleaned up after test."""
    user = create_test_user()
    yield user
    delete_user(user.id)
```

## 📊 Best Practices

### 1. Test Structure (AAA Pattern)
```python
def test_user_registration():
    # Arrange - Set up test data and conditions
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "securepass123"
    }
    
    # Act - Execute the function being tested
    result = user_service.register_user(user_data)
    
    # Assert - Verify the results
    assert result.success is True
    assert result.user.name == user_data["name"]
    assert result.user.email == user_data["email"]
```

### 2. Test Independence
```python
def test_user_creation():
    """Each test should be independent and not rely on other tests."""
    user_data = {"name": "Alice", "email": "alice@example.com"}
    user = create_user(user_data)
    
    # Test should work regardless of other tests
    assert user.name == "Alice"

def test_user_update():
    """This test should not depend on test_user_creation."""
    # Create fresh user data for this test
    user_data = {"name": "Bob", "email": "bob@example.com"}
    user = create_user(user_data)
    
    # Update the user
    updated_user = update_user(user.id, {"name": "Bob Updated"})
    assert updated_user.name == "Bob Updated"
```

### 3. Meaningful Assertions
```python
def test_user_validation():
    """Use specific assertions that clearly show what's being tested."""
    user_data = {"name": "", "email": "invalid-email"}
    
    with pytest.raises(ValidationError) as exc_info:
        validate_user(user_data)
    
    # Specific assertion about the error
    assert "Name cannot be empty" in str(exc_info.value)
    assert "Invalid email format" in str(exc_info.value)

def test_user_creation_success():
    """Test the happy path with specific assertions."""
    user_data = {"name": "John", "email": "john@example.com"}
    user = create_user(user_data)
    
    # Specific assertions about the created user
    assert user.id is not None
    assert user.name == "John"
    assert user.email == "john@example.com"
    assert user.created_at is not None
    assert user.is_active is True
```

### 4. Test Data Management
```python
@pytest.fixture
def sample_users():
    """Provide consistent test data for multiple tests."""
    return [
        {"name": "Alice", "email": "alice@example.com", "age": 25},
        {"name": "Bob", "email": "bob@example.com", "age": 30},
        {"name": "Charlie", "email": "charlie@example.com", "age": 35}
    ]

def test_user_list_retrieval(sample_users):
    """Test using shared test data."""
    # Create users from sample data
    created_users = [create_user(user_data) for user_data in sample_users]
    
    # Test retrieval
    retrieved_users = get_all_users()
    
    assert len(retrieved_users) == len(sample_users)
    for i, user in enumerate(retrieved_users):
        assert user.name == sample_users[i]["name"]
```

## 🎓 Exercises

1. Organize a test suite with proper directory structure
2. Create test data factories for your domain objects
3. Write tests following the AAA pattern
4. Implement test categorization with markers
5. Create comprehensive test documentation

## 📚 Real-World Examples

### E-commerce Test Organization
```python
# tests/unit/test_product.py
class TestProduct:
    """Unit tests for Product model."""
    
    def test_product_creation(self):
        """Test product creation with valid data."""
        product_data = {
            "name": "Test Product",
            "price": 29.99,
            "category": "Electronics"
        }
        
        product = Product(**product_data)
        
        assert product.name == "Test Product"
        assert product.price == 29.99
        assert product.category == "Electronics"
    
    def test_product_price_validation(self):
        """Test that negative prices are rejected."""
        with pytest.raises(ValueError, match="Price must be positive"):
            Product(name="Test", price=-10.0, category="Test")

# tests/integration/test_order_processing.py
@pytest.mark.integration
class TestOrderProcessing:
    """Integration tests for order processing."""
    
    def test_order_creation_with_inventory(self, product_factory, user_factory):
        """Test order creation with inventory check."""
        # Arrange
        product = product_factory(stock_quantity=5)
        user = user_factory()
        
        # Act
        order = order_service.create_order(user.id, product.id, quantity=2)
        
        # Assert
        assert order.status == "confirmed"
        assert order.total_amount == product.price * 2
        
        # Verify inventory was updated
        updated_product = product_service.get_product(product.id)
        assert updated_product.stock_quantity == 3

# tests/e2e/test_purchase_workflow.py
@pytest.mark.e2e
class TestPurchaseWorkflow:
    """End-to-end tests for purchase workflow."""
    
    def test_complete_purchase_flow(self, browser):
        """Test complete purchase from browsing to confirmation."""
        # Navigate to product page
        browser.get("/products/1")
        
        # Add to cart
        browser.find_element(By.ID, "add-to-cart").click()
        
        # Proceed to checkout
        browser.get("/cart")
        browser.find_element(By.ID, "checkout").click()
        
        # Fill shipping information
        browser.find_element(By.NAME, "shipping_address").send_keys("123 Main St")
        browser.find_element(By.NAME, "city").send_keys("Anytown")
        
        # Complete purchase
        browser.find_element(By.ID, "place-order").click()
        
        # Verify confirmation
        assert "Order Confirmed" in browser.page_source
```

### API Testing Best Practices
```python
# tests/api/test_user_api.py
class TestUserAPI:
    """API tests for user endpoints."""
    
    def test_create_user_success(self, api_client):
        """Test successful user creation via API."""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "securepass123"
        }
        
        response = api_client.post("/api/users", json=user_data)
        
        assert response.status_code == 201
        assert response.json()["name"] == user_data["name"]
        assert response.json()["email"] == user_data["email"]
        assert "id" in response.json()
    
    def test_create_user_validation_error(self, api_client):
        """Test user creation with validation errors."""
        invalid_data = {
            "name": "",  # Empty name
            "email": "invalid-email",  # Invalid email
            "password": "123"  # Too short password
        }
        
        response = api_client.post("/api/users", json=invalid_data)
        
        assert response.status_code == 422
        errors = response.json()["detail"]
        
        # Check specific validation errors
        assert any("name" in error["loc"] for error in errors)
        assert any("email" in error["loc"] for error in errors)
        assert any("password" in error["loc"] for error in errors)
    
    @pytest.mark.parametrize("field,invalid_value,expected_error", [
        ("email", "not-an-email", "Invalid email format"),
        ("password", "123", "Password too short"),
        ("name", "", "Name cannot be empty"),
    ])
    def test_user_validation_fields(self, api_client, field, invalid_value, expected_error):
        """Test individual field validation."""
        user_data = {
            "name": "Valid Name",
            "email": "valid@email.com",
            "password": "validpassword123"
        }
        user_data[field] = invalid_value
        
        response = api_client.post("/api/users", json=user_data)
        
        assert response.status_code == 422
        assert expected_error in str(response.json())
```

## 📚 Next Steps

After completing this section, you should:
- Understand how to organize tests effectively
- Know how to write clear and maintainable tests
- Be able to manage test data properly
- Understand documentation best practices
- Be familiar with test categorization and configuration

This completes the comprehensive pytest tutorial! You now have a solid foundation in pytest testing with practical examples and real-world scenarios. 