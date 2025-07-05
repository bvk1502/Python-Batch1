"""
Docker integration tests demonstrating container-based testing.
"""
import pytest
import docker
import time
import requests
import subprocess
import os
from unittest.mock import patch, Mock


class TestDockerContainerIntegration:
    """Test applications running in Docker containers."""
    
    @pytest.fixture(scope="session")
    def docker_client(self):
        """Create Docker client for testing."""
        try:
            return docker.from_env()
        except docker.errors.DockerException:
            pytest.skip("Docker is not available")
    
    @pytest.fixture(scope="session")
    def test_app_container(self, docker_client):
        """Start test application in Docker container."""
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
            
            # Start container
            container = docker_client.containers.run(
                "test-app:latest",
                detach=True,
                ports={'8000/tcp': 8000},
                environment={
                    'DATABASE_URL': 'postgresql://test:test@localhost:5432/testdb',
                    'REDIS_URL': 'redis://localhost:6379/0',
                    'ENVIRONMENT': 'test'
                },
                name="test-app-container"
            )
            
            # Wait for container to be ready
            time.sleep(10)
            
            yield container
            
            # Cleanup
            try:
                container.stop(timeout=10)
                container.remove()
            except docker.errors.NotFound:
                pass  # Container already removed
                
        except Exception as e:
            pytest.skip(f"Docker container setup failed: {e}")
    
    def test_application_health_check(self, test_app_container):
        """Test application health check endpoint."""
        try:
            response = requests.get("http://localhost:8000/health", timeout=10)
            assert response.status_code == 200
            
            health_data = response.json()
            assert health_data["status"] == "healthy"
            assert "version" in health_data
            assert "timestamp" in health_data
            
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Health check failed: {e}")
    
    def test_application_api_endpoints(self, test_app_container):
        """Test application API endpoints in container."""
        try:
            # Test users endpoint
            response = requests.get("http://localhost:8000/api/users", timeout=10)
            assert response.status_code == 200
            
            users = response.json()
            assert isinstance(users, list)
            
            # Test user creation
            user_data = {
                "name": "Test User",
                "email": "test@example.com"
            }
            
            response = requests.post(
                "http://localhost:8000/api/users",
                json=user_data,
                timeout=10
            )
            assert response.status_code == 201
            
            created_user = response.json()
            assert created_user["name"] == user_data["name"]
            assert created_user["email"] == user_data["email"]
            assert "id" in created_user
            
        except requests.exceptions.RequestException as e:
            pytest.fail(f"API test failed: {e}")
    
    def test_container_logs(self, test_app_container):
        """Test container logs and monitoring."""
        # Get container logs
        logs = test_app_container.logs().decode('utf-8')
        
        # Verify application started successfully
        assert "Application startup complete" in logs or "Server started" in logs
        
        # Check for any error messages
        assert "ERROR" not in logs or "CRITICAL" not in logs
    
    def test_container_resource_usage(self, test_app_container):
        """Test container resource usage."""
        # Get container stats
        stats = test_app_container.stats(stream=False)
        
        # Verify container is running
        assert stats["memory_stats"]["usage"] > 0
        assert stats["cpu_stats"]["cpu_usage"]["total_usage"] > 0
        
        # Check memory usage is reasonable (less than 1GB)
        memory_usage_mb = stats["memory_stats"]["usage"] / (1024 * 1024)
        assert memory_usage_mb < 1024, f"Memory usage too high: {memory_usage_mb}MB"


class TestDockerComposeIntegration:
    """Test applications using Docker Compose."""
    
    @pytest.fixture(scope="session")
    def docker_compose_stack(self):
        """Start complete application stack with Docker Compose."""
        try:
            # Start the stack
            subprocess.run([
                "docker-compose", "-f", "docker-compose.test.yml", "up", "-d"
            ], check=True, capture_output=True)
            
            # Wait for services to be ready
            time.sleep(15)
            
            yield
            
            # Stop the stack
            subprocess.run([
                "docker-compose", "-f", "docker-compose.test.yml", "down"
            ], check=True, capture_output=True)
            
        except subprocess.CalledProcessError as e:
            pytest.skip(f"Docker Compose setup failed: {e}")
        except FileNotFoundError:
            pytest.skip("Docker Compose not available")
    
    def test_complete_stack_health(self, docker_compose_stack):
        """Test health of all services in the stack."""
        try:
            # Test application health
            response = requests.get("http://localhost:8000/health", timeout=10)
            assert response.status_code == 200
            
            # Test database connectivity
            response = requests.get("http://localhost:8000/api/health/db", timeout=10)
            assert response.status_code == 200
            
            # Test Redis connectivity
            response = requests.get("http://localhost:8000/api/health/redis", timeout=10)
            assert response.status_code == 200
            
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Stack health check failed: {e}")
    
    def test_service_communication(self, docker_compose_stack):
        """Test communication between services."""
        try:
            # Test user creation with database persistence
            user_data = {
                "name": "Integration Test User",
                "email": "integration@test.com"
            }
            
            response = requests.post(
                "http://localhost:8000/api/users",
                json=user_data,
                timeout=10
            )
            assert response.status_code == 201
            
            user_id = response.json()["id"]
            
            # Test user retrieval (verifies database persistence)
            response = requests.get(
                f"http://localhost:8000/api/users/{user_id}",
                timeout=10
            )
            assert response.status_code == 200
            assert response.json()["name"] == user_data["name"]
            
            # Test cache functionality (verifies Redis integration)
            response = requests.get("http://localhost:8000/api/users", timeout=10)
            assert response.status_code == 200
            
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Service communication test failed: {e}")
    
    def test_database_persistence(self, docker_compose_stack):
        """Test database persistence across container restarts."""
        try:
            # Create test data
            user_data = {
                "name": "Persistence Test User",
                "email": "persistence@test.com"
            }
            
            response = requests.post(
                "http://localhost:8000/api/users",
                json=user_data,
                timeout=10
            )
            assert response.status_code == 201
            
            user_id = response.json()["id"]
            
            # Restart the application container
            subprocess.run([
                "docker-compose", "-f", "docker-compose.test.yml", "restart", "app"
            ], check=True, capture_output=True)
            
            # Wait for restart
            time.sleep(10)
            
            # Verify data persistence
            response = requests.get(
                f"http://localhost:8000/api/users/{user_id}",
                timeout=10
            )
            assert response.status_code == 200
            assert response.json()["name"] == user_data["name"]
            
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Database persistence test failed: {e}")


class TestDockerNetworkIntegration:
    """Test Docker network integration and service discovery."""
    
    @pytest.fixture(scope="session")
    def docker_network(self, docker_client):
        """Create Docker network for testing."""
        try:
            network = docker_client.networks.create(
                "test-network",
                driver="bridge"
            )
            
            yield network
            
            # Cleanup
            try:
                network.remove()
            except docker.errors.APIError:
                pass  # Network already removed
                
        except Exception as e:
            pytest.skip(f"Docker network setup failed: {e}")
    
    def test_service_discovery(self, docker_client, docker_network):
        """Test service discovery within Docker network."""
        try:
            # Start database container
            db_container = docker_client.containers.run(
                "postgres:13",
                detach=True,
                network="test-network",
                environment={
                    'POSTGRES_DB': 'testdb',
                    'POSTGRES_USER': 'test',
                    'POSTGRES_PASSWORD': 'test'
                },
                name="test-db"
            )
            
            # Start application container
            app_container = docker_client.containers.run(
                "test-app:latest",
                detach=True,
                network="test-network",
                environment={
                    'DATABASE_URL': 'postgresql://test:test@test-db:5432/testdb',
                    'ENVIRONMENT': 'test'
                },
                name="test-app-network"
            )
            
            # Wait for services to be ready
            time.sleep(15)
            
            # Test service communication
            response = requests.get("http://localhost:8000/health", timeout=10)
            assert response.status_code == 200
            
            # Cleanup
            app_container.stop()
            db_container.stop()
            app_container.remove()
            db_container.remove()
            
        except Exception as e:
            pytest.fail(f"Service discovery test failed: {e}")


class TestDockerVolumeIntegration:
    """Test Docker volume integration and data persistence."""
    
    def test_volume_mounting(self, docker_client):
        """Test volume mounting and data persistence."""
        try:
            # Create test volume
            volume = docker_client.volumes.create(name="test-volume")
            
            # Create test file
            test_data = "Test data for volume mounting"
            
            # Start container with volume mount
            container = docker_client.containers.run(
                "alpine:latest",
                command=f"sh -c 'echo \"{test_data}\" > /data/test.txt'",
                detach=True,
                volumes={
                    "test-volume": {"bind": "/data", "mode": "rw"}
                },
                name="test-volume-container"
            )
            
            # Wait for container to complete
            container.wait()
            
            # Start another container to read the data
            read_container = docker_client.containers.run(
                "alpine:latest",
                command="cat /data/test.txt",
                detach=True,
                volumes={
                    "test-volume": {"bind": "/data", "mode": "ro"}
                },
                name="test-volume-reader"
            )
            
            # Get output
            output = read_container.logs().decode('utf-8').strip()
            assert output == test_data
            
            # Cleanup
            read_container.remove()
            container.remove()
            volume.remove()
            
        except Exception as e:
            pytest.fail(f"Volume mounting test failed: {e}")


# Utility functions for Docker testing
def wait_for_container_ready(container, timeout=60):
    """Wait for container to be ready."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            container.reload()
            if container.status == "running":
                return True
        except docker.errors.NotFound:
            pass
        time.sleep(1)
    return False


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