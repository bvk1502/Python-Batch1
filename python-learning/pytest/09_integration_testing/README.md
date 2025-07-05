# Integration Testing - Testing Complete Systems

This section covers integration testing with pytest, including end-to-end testing, external service integration, Docker container testing, and CI/CD integration to ensure your entire system works together correctly.

## 📋 What You'll Learn

1. **End-to-End Testing**
   - Complete user workflows
   - System integration testing
   - User interface testing

2. **External Service Integration**
   - Third-party API testing
   - Database integration
   - Message queue testing

3. **Docker Integration**
   - Container-based testing
   - Service orchestration
   - Environment isolation

4. **CI/CD Integration**
   - Automated testing pipelines
   - Test reporting
   - Deployment testing

## 🚀 Step-by-Step Guide

### Step 1: End-to-End Testing

Test complete user workflows from start to finish:

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test complete user registration and login flow
def test_user_registration_and_login_flow():
    """Test complete user registration and login workflow."""
    client = TestClient(app)
    
    # Step 1: Register a new user
    registration_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepass123"
    }
    
    register_response = client.post("/register", json=registration_data)
    assert register_response.status_code == 201
    
    # Step 2: Login with the new user
    login_data = {
        "username": "testuser",
        "password": "securepass123"
    }
    
    login_response = client.post("/login", data=login_data)
    assert login_response.status_code == 200
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 3: Access protected resources
    profile_response = client.get("/profile", headers=headers)
    assert profile_response.status_code == 200
    assert profile_response.json()["username"] == "testuser"
    
    # Step 4: Update profile
    update_data = {"name": "Updated Name"}
    update_response = client.put("/profile", json=update_data, headers=headers)
    assert update_response.status_code == 200
    
    # Step 5: Verify changes
    profile_response = client.get("/profile", headers=headers)
    assert profile_response.json()["name"] == "Updated Name"
```

### Step 2: Database Integration Testing

Test complete database operations with real database:

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, Order, Product

@pytest.fixture(scope="function")
def database_session():
    """Create a test database session."""
    # Use SQLite for testing
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)

def test_complete_order_workflow(database_session):
    """Test complete order creation and processing workflow."""
    # Create test data
    user = User(username="testuser", email="test@example.com")
    database_session.add(user)
    database_session.commit()
    
    product = Product(name="Test Product", price=29.99, stock=10)
    database_session.add(product)
    database_session.commit()
    
    # Create order
    order = Order(
        user_id=user.id,
        product_id=product.id,
        quantity=2,
        total_amount=59.98
    )
    database_session.add(order)
    database_session.commit()
    
    # Verify order was created
    assert order.id is not None
    assert order.status == "pending"
    
    # Process order
    order.status = "confirmed"
    product.stock -= order.quantity
    database_session.commit()
    
    # Verify order processing
    updated_order = database_session.query(Order).filter_by(id=order.id).first()
    assert updated_order.status == "confirmed"
    
    updated_product = database_session.query(Product).filter_by(id=product.id).first()
    assert updated_product.stock == 8
```

### Step 3: External Service Integration

Test integration with external services:

```python
import pytest
import httpx
from unittest.mock import patch

def test_external_api_integration():
    """Test integration with external payment service."""
    with httpx.Client() as client:
        # Test payment processing
        payment_data = {
            "amount": 100.00,
            "currency": "USD",
            "payment_method": "card",
            "card_number": "4242424242424242"
        }
        
        # Mock external payment service
        with patch('httpx.post') as mock_post:
            mock_response = httpx.Response(
                status_code=200,
                json={"transaction_id": "txn_123", "status": "succeeded"}
            )
            mock_post.return_value = mock_response
            
            response = client.post("/api/payments", json=payment_data)
            
            assert response.status_code == 200
            assert response.json()["transaction_id"] == "txn_123"
            assert response.json()["status"] == "succeeded"

def test_email_service_integration():
    """Test integration with email service."""
    with patch('smtplib.SMTP') as mock_smtp:
        mock_smtp_instance = mock_smtp.return_value
        
        # Test email sending
        email_data = {
            "to": "user@example.com",
            "subject": "Welcome!",
            "body": "Welcome to our platform!"
        }
        
        response = send_welcome_email(email_data)
        
        assert response["status"] == "sent"
        mock_smtp_instance.send_message.assert_called_once()
```

### Step 4: Docker Integration Testing

Test applications running in Docker containers:

```python
import pytest
import docker
import time
import requests

@pytest.fixture(scope="session")
def docker_client():
    """Create Docker client for testing."""
    return docker.from_env()

@pytest.fixture(scope="session")
def test_container(docker_client):
    """Start test application in Docker container."""
    # Build and run test container
    container = docker_client.containers.run(
        "myapp:test",
        detach=True,
        ports={'8000/tcp': 8000},
        environment={
            'DATABASE_URL': 'postgresql://test:test@db:5432/testdb',
            'REDIS_URL': 'redis://redis:6379/0'
        }
    )
    
    # Wait for container to be ready
    time.sleep(10)
    
    yield container
    
    # Cleanup
    container.stop()
    container.remove()

def test_application_in_container(test_container):
    """Test application running in Docker container."""
    # Test health check
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    
    # Test API endpoints
    response = requests.get("http://localhost:8000/api/users")
    assert response.status_code == 200
    
    # Test database connection
    response = requests.post("http://localhost:8000/api/users", json={
        "name": "Test User",
        "email": "test@example.com"
    })
    assert response.status_code == 201
```

## 📁 File Structure

```
09_integration_testing/
├── README.md
├── test_e2e_workflows.py
├── test_database_integration.py
├── test_external_services.py
├── test_docker_integration.py
├── test_ci_cd_integration.py
├── conftest.py
├── docker-compose.test.yml
├── Dockerfile.test
└── requirements.txt
```

## 🎯 Key Concepts

### 1. End-to-End Testing
- Test complete user workflows
- Verify system integration
- Test real user scenarios
- Validate business processes

### 2. External Service Integration
- Test third-party API integration
- Mock external dependencies
- Test service communication
- Handle service failures

### 3. Docker Integration
- Test applications in containers
- Verify container orchestration
- Test environment configuration
- Validate deployment processes

### 4. CI/CD Integration
- Automate testing in pipelines
- Generate test reports
- Test deployment processes
- Monitor test results

## 🔧 Advanced Patterns

### Multi-Service Integration Testing
```python
@pytest.fixture(scope="session")
def service_stack():
    """Start complete service stack for integration testing."""
    # Start database
    db_container = docker_client.containers.run(
        "postgres:13",
        detach=True,
        environment={
            'POSTGRES_DB': 'testdb',
            'POSTGRES_USER': 'test',
            'POSTGRES_PASSWORD': 'test'
        },
        ports={'5432/tcp': 5432}
    )
    
    # Start Redis
    redis_container = docker_client.containers.run(
        "redis:6",
        detach=True,
        ports={'6379/tcp': 6379}
    )
    
    # Start application
    app_container = docker_client.containers.run(
        "myapp:test",
        detach=True,
        ports={'8000/tcp': 8000},
        environment={
            'DATABASE_URL': 'postgresql://test:test@localhost:5432/testdb',
            'REDIS_URL': 'redis://localhost:6379/0'
        }
    )
    
    # Wait for services to be ready
    time.sleep(15)
    
    yield {
        'db': db_container,
        'redis': redis_container,
        'app': app_container
    }
    
    # Cleanup
    app_container.stop()
    redis_container.stop()
    db_container.stop()
    app_container.remove()
    redis_container.remove()
    db_container.remove()

def test_complete_service_integration(service_stack):
    """Test integration between all services."""
    # Test database connection
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200
    
    # Test user creation with database persistence
    user_data = {"name": "Test User", "email": "test@example.com"}
    response = requests.post("http://localhost:8000/api/users", json=user_data)
    assert response.status_code == 201
    
    # Test cache integration
    response = requests.get("http://localhost:8000/api/users")
    assert response.status_code == 200
    
    # Verify data persistence
    user_id = response.json()[0]["id"]
    response = requests.get(f"http://localhost:8000/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"
```

### CI/CD Pipeline Testing
```python
def test_ci_cd_pipeline():
    """Test CI/CD pipeline integration."""
    # Test code quality checks
    result = subprocess.run(["flake8", "src/"], capture_output=True, text=True)
    assert result.returncode == 0, f"Code quality check failed: {result.stdout}"
    
    # Test security scanning
    result = subprocess.run(["bandit", "-r", "src/"], capture_output=True, text=True)
    assert result.returncode == 0, f"Security scan failed: {result.stdout}"
    
    # Test test coverage
    result = subprocess.run([
        "pytest", "--cov=src", "--cov-report=xml", "--cov-report=html"
    ], capture_output=True, text=True)
    assert result.returncode == 0, f"Test coverage check failed: {result.stdout}"
    
    # Verify coverage threshold
    coverage_xml = ET.parse("coverage.xml")
    coverage_rate = float(coverage_xml.find(".//coverage").get("line-rate"))
    assert coverage_rate >= 0.8, f"Coverage {coverage_rate} is below 80%"

def test_deployment_validation():
    """Test deployment validation."""
    # Test configuration validation
    config = load_config("config/test.yml")
    assert config["database"]["host"] == "localhost"
    assert config["redis"]["port"] == 6379
    
    # Test environment variables
    assert os.getenv("DATABASE_URL") is not None
    assert os.getenv("SECRET_KEY") is not None
    
    # Test service connectivity
    assert can_connect_to_database()
    assert can_connect_to_redis()
```

## 📊 Best Practices

### 1. Test Environment Management
- Use isolated test environments
- Clean up test data after tests
- Use consistent environment configuration
- Document environment setup

### 2. Service Dependencies
- Mock external services when possible
- Use test doubles for expensive operations
- Test service failure scenarios
- Validate service contracts

### 3. Test Data Management
- Use realistic test data
- Clean up test data properly
- Avoid test data conflicts
- Use data factories for consistency

### 4. Performance Considerations
- Keep integration tests fast
- Use appropriate timeouts
- Parallelize tests when possible
- Monitor test execution time

## 🎓 Exercises

1. Create end-to-end tests for a user registration workflow
2. Implement database integration tests with real database
3. Test external API integration with mocking
4. Set up Docker-based integration testing
5. Create CI/CD pipeline tests

## 📚 Real-World Examples

### E-commerce Integration Testing
```python
class TestEcommerceIntegration:
    """Integration tests for e-commerce system."""
    
    def test_complete_purchase_workflow(self, database_session, payment_mock):
        """Test complete purchase from browsing to order confirmation."""
        # Create test data
        user = create_test_user(database_session)
        product = create_test_product(database_session, stock=5)
        
        # Step 1: Add product to cart
        cart_item = add_to_cart(user.id, product.id, quantity=2)
        assert cart_item.quantity == 2
        
        # Step 2: Create order
        order = create_order(user.id, [cart_item])
        assert order.status == "pending"
        assert order.total_amount == product.price * 2
        
        # Step 3: Process payment
        payment_result = process_payment(order.id, "card", "4242424242424242")
        assert payment_result["status"] == "succeeded"
        
        # Step 4: Update order status
        order.status = "confirmed"
        product.stock -= 2
        database_session.commit()
        
        # Step 5: Send confirmation email
        email_sent = send_order_confirmation(order.id)
        assert email_sent is True
        
        # Step 6: Verify final state
        updated_order = database_session.query(Order).filter_by(id=order.id).first()
        assert updated_order.status == "confirmed"
        
        updated_product = database_session.query(Product).filter_by(id=product.id).first()
        assert updated_product.stock == 3
    
    def test_inventory_management_integration(self, database_session):
        """Test inventory management integration."""
        # Create products with different stock levels
        product1 = create_test_product(database_session, stock=10)
        product2 = create_test_product(database_session, stock=0)
        
        # Test low stock alert
        low_stock_products = get_low_stock_products(threshold=5)
        assert product1 in low_stock_products
        
        # Test out of stock handling
        with pytest.raises(OutOfStockError):
            add_to_cart(1, product2.id, quantity=1)
        
        # Test stock replenishment
        replenish_stock(product1.id, 5)
        updated_product = database_session.query(Product).filter_by(id=product1.id).first()
        assert updated_product.stock == 15
```

### Microservices Integration Testing
```python
class TestMicroservicesIntegration:
    """Integration tests for microservices architecture."""
    
    def test_user_service_integration(self, user_service, auth_service):
        """Test integration between user and auth services."""
        # Create user in user service
        user_data = {"name": "Test User", "email": "test@example.com"}
        user = user_service.create_user(user_data)
        
        # Verify user creation
        assert user.id is not None
        assert user.name == user_data["name"]
        
        # Create authentication credentials
        auth_credentials = auth_service.create_credentials(
            user.id, "password123"
        )
        
        # Verify authentication
        token = auth_service.authenticate(
            user.email, "password123"
        )
        assert token is not None
        
        # Verify user can access protected resources
        user_profile = user_service.get_user_profile(token)
        assert user_profile["id"] == user.id
        assert user_profile["name"] == user.name
    
    def test_order_service_integration(self, order_service, inventory_service, payment_service):
        """Test integration between order, inventory, and payment services."""
        # Create order
        order_data = {
            "user_id": 1,
            "items": [{"product_id": 1, "quantity": 2}]
        }
        order = order_service.create_order(order_data)
        
        # Verify inventory check
        inventory_updated = inventory_service.reserve_stock(
            order.id, order_data["items"]
        )
        assert inventory_updated is True
        
        # Process payment
        payment_result = payment_service.process_payment(
            order.id, "card", "4242424242424242"
        )
        assert payment_result["status"] == "succeeded"
        
        # Confirm order
        order_confirmed = order_service.confirm_order(order.id)
        assert order_confirmed is True
        
        # Verify final state
        final_order = order_service.get_order(order.id)
        assert final_order["status"] == "confirmed"
        
        final_inventory = inventory_service.get_product_stock(1)
        assert final_inventory == 8  # Assuming initial stock was 10
```

### API Gateway Integration Testing
```python
class TestAPIGatewayIntegration:
    """Integration tests for API gateway."""
    
    def test_request_routing(self, api_gateway):
        """Test API gateway request routing."""
        # Test user service routing
        response = api_gateway.request("GET", "/api/users")
        assert response.status_code == 200
        
        # Test order service routing
        response = api_gateway.request("GET", "/api/orders")
        assert response.status_code == 200
        
        # Test payment service routing
        response = api_gateway.request("POST", "/api/payments")
        assert response.status_code == 400  # Missing required data
    
    def test_authentication_integration(self, api_gateway, auth_service):
        """Test API gateway authentication integration."""
        # Test unauthenticated request
        response = api_gateway.request("GET", "/api/protected")
        assert response.status_code == 401
        
        # Test authenticated request
        token = auth_service.create_token(user_id=1)
        headers = {"Authorization": f"Bearer {token}"}
        response = api_gateway.request("GET", "/api/protected", headers=headers)
        assert response.status_code == 200
    
    def test_rate_limiting_integration(self, api_gateway):
        """Test API gateway rate limiting."""
        # Make multiple requests quickly
        responses = []
        for _ in range(10):
            response = api_gateway.request("GET", "/api/users")
            responses.append(response.status_code)
        
        # Should hit rate limit
        assert 429 in responses
        
        # Wait and try again
        time.sleep(1)
        response = api_gateway.request("GET", "/api/users")
        assert response.status_code == 200
```

## 📚 Next Steps

After completing this section, you should:
- Understand how to test complete system workflows
- Be able to test external service integrations
- Know how to test applications in Docker containers
- Understand CI/CD pipeline testing
- Be familiar with microservices integration testing

This completes the integration testing section! You now have comprehensive knowledge of testing complete systems and integrations. 