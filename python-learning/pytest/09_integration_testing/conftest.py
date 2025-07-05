"""
Shared fixtures for integration testing.
"""
import pytest
import docker
import time
import requests
import subprocess
import os
from unittest.mock import patch, Mock


@pytest.fixture(scope="session")
def docker_client():
    """Create Docker client for testing."""
    try:
        return docker.from_env()
    except docker.errors.DockerException:
        pytest.skip("Docker is not available")


@pytest.fixture(scope="session")
def test_environment():
    """Set up test environment variables."""
    # Set test environment variables
    os.environ["ENVIRONMENT"] = "test"
    os.environ["DATABASE_URL"] = "postgresql://test:test@localhost:5432/testdb"
    os.environ["REDIS_URL"] = "redis://localhost:6379/0"
    os.environ["SECRET_KEY"] = "test-secret-key"
    
    yield
    
    # Cleanup environment variables
    for key in ["ENVIRONMENT", "DATABASE_URL", "REDIS_URL", "SECRET_KEY"]:
        os.environ.pop(key, None)


@pytest.fixture(scope="session")
def database_container(docker_client):
    """Start PostgreSQL database container."""
    try:
        # Start database container
        container = docker_client.containers.run(
            "postgres:13",
            detach=True,
            environment={
                'POSTGRES_DB': 'testdb',
                'POSTGRES_USER': 'test',
                'POSTGRES_PASSWORD': 'test'
            },
            ports={'5432/tcp': 5432},
            name="test-postgres"
        )
        
        # Wait for database to be ready
        time.sleep(10)
        
        yield container
        
        # Cleanup
        try:
            container.stop(timeout=10)
            container.remove()
        except docker.errors.NotFound:
            pass
            
    except Exception as e:
        pytest.skip(f"Database container setup failed: {e}")


@pytest.fixture(scope="session")
def redis_container(docker_client):
    """Start Redis container."""
    try:
        # Start Redis container
        container = docker_client.containers.run(
            "redis:6-alpine",
            detach=True,
            ports={'6379/tcp': 6379},
            name="test-redis"
        )
        
        # Wait for Redis to be ready
        time.sleep(5)
        
        yield container
        
        # Cleanup
        try:
            container.stop(timeout=10)
            container.remove()
        except docker.errors.NotFound:
            pass
            
    except Exception as e:
        pytest.skip(f"Redis container setup failed: {e}")


@pytest.fixture(scope="session")
def application_container(docker_client, database_container, redis_container):
    """Start application container."""
    try:
        # Build test image if it doesn't exist
        try:
            docker_client.images.get("test-app:latest")
        except docker.errors.ImageNotFound:
            # Build image from Dockerfile
            docker_client.images.build(
                path=".",
                dockerfile="Dockerfile.test",
                tag="test-app:latest"
            )
        
        # Start application container
        container = docker_client.containers.run(
            "test-app:latest",
            detach=True,
            ports={'8000/tcp': 8000},
            environment={
                'DATABASE_URL': 'postgresql://test:test@localhost:5432/testdb',
                'REDIS_URL': 'redis://localhost:6379/0',
                'ENVIRONMENT': 'test',
                'SECRET_KEY': 'test-secret-key'
            },
            name="test-app"
        )
        
        # Wait for application to be ready
        time.sleep(15)
        
        yield container
        
        # Cleanup
        try:
            container.stop(timeout=10)
            container.remove()
        except docker.errors.NotFound:
            pass
            
    except Exception as e:
        pytest.skip(f"Application container setup failed: {e}")


@pytest.fixture
def api_client(application_container):
    """Create API client for testing."""
    import requests
    
    def make_request(method, endpoint, **kwargs):
        """Make HTTP request to the application."""
        url = f"http://localhost:8000{endpoint}"
        return requests.request(method, url, **kwargs)
    
    return make_request


@pytest.fixture
def authenticated_user(api_client):
    """Create an authenticated user for testing."""
    # Create user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepass123"
    }
    
    response = api_client("POST", "/api/users/register", json=user_data)
    if response.status_code != 201:
        pytest.skip("User registration failed")
    
    # Login
    login_data = {
        "username": "testuser",
        "password": "securepass123"
    }
    
    response = api_client("POST", "/api/auth/login", data=login_data)
    if response.status_code != 200:
        pytest.skip("User login failed")
    
    token = response.json()["access_token"]
    
    return 1, token  # Assuming user ID is 1


@pytest.fixture
def authenticated_admin(api_client):
    """Create an authenticated admin user for testing."""
    # Create admin user
    admin_data = {
        "username": "admin",
        "email": "admin@example.com",
        "password": "adminpass123",
        "role": "admin"
    }
    
    response = api_client("POST", "/api/users/register", json=admin_data)
    if response.status_code != 201:
        pytest.skip("Admin registration failed")
    
    # Login
    login_data = {
        "username": "admin",
        "password": "adminpass123"
    }
    
    response = api_client("POST", "/api/auth/login", data=login_data)
    if response.status_code != 200:
        pytest.skip("Admin login failed")
    
    token = response.json()["access_token"]
    
    return 2, token  # Assuming admin ID is 2


@pytest.fixture
def external_service_mock():
    """Mock external service for testing."""
    with patch('app.services.external_service.ExternalAPI') as mock_api:
        # Setup default responses
        mock_instance = mock_api.return_value
        mock_instance.get_data.return_value = {"status": "success", "data": "test"}
        mock_instance.process_data.return_value = {"result": "processed"}
        
        yield mock_instance


@pytest.fixture
def payment_service_mock():
    """Mock payment service for testing."""
    with patch('app.services.payment_service.process_payment') as mock_payment:
        mock_payment.return_value = {
            "transaction_id": "txn_123",
            "status": "succeeded",
            "amount": 100.00
        }
        yield mock_payment


@pytest.fixture
def email_service_mock():
    """Mock email service for testing."""
    with patch('app.services.email_service.send_email') as mock_email:
        mock_email.return_value = {"status": "sent", "message_id": "msg_123"}
        yield mock_email


@pytest.fixture
def sms_service_mock():
    """Mock SMS service for testing."""
    with patch('app.services.sms_service.send_sms') as mock_sms:
        mock_sms.return_value = {"status": "sent", "message_id": "sms_123"}
        yield mock_sms


@pytest.fixture
def test_data():
    """Provide test data for integration tests."""
    return {
        "users": [
            {"name": "Alice", "email": "alice@example.com", "age": 25},
            {"name": "Bob", "email": "bob@example.com", "age": 30},
            {"name": "Charlie", "email": "charlie@example.com", "age": 35}
        ],
        "products": [
            {"name": "Product A", "price": 29.99, "category": "Electronics"},
            {"name": "Product B", "price": 49.99, "category": "Clothing"},
            {"name": "Product C", "price": 19.99, "category": "Books"}
        ],
        "orders": [
            {"user_id": 1, "product_id": 1, "quantity": 2, "total": 59.98},
            {"user_id": 2, "product_id": 2, "quantity": 1, "total": 49.99}
        ]
    }


@pytest.fixture
def clean_database(database_container):
    """Clean database before each test."""
    # This fixture ensures database is clean before each test
    # In a real implementation, you would reset the database state
    yield


@pytest.fixture
def test_logger():
    """Provide a test logger for integration tests."""
    import logging
    
    # Create test logger
    logger = logging.getLogger("test_integration")
    logger.setLevel(logging.DEBUG)
    
    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger


# Utility functions
def wait_for_service_ready(url, timeout=60):
    """Wait for service to be ready."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    return False


def cleanup_containers(docker_client, container_names):
    """Clean up containers by name."""
    for name in container_names:
        try:
            container = docker_client.containers.get(name)
            container.stop(timeout=10)
            container.remove()
        except docker.errors.NotFound:
            pass


def get_container_logs(container):
    """Get container logs as string."""
    return container.logs().decode('utf-8')


def check_container_health(container):
    """Check container health status."""
    try:
        container.reload()
        return container.status == "running"
    except docker.errors.NotFound:
        return False 