import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate


@pytest.mark.asyncio
class TestUserCreate:
    """Test user creation endpoints - TDD Approach."""
    
    async def test_create_user_success(self, client: AsyncClient, test_user_data: dict):
        """Test successful user creation."""
        response = await client.post("/users/", json=test_user_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["name"] == test_user_data["name"]
        assert data["email"] == test_user_data["email"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
        assert data["is_deleted"] is False
    
    async def test_create_user_missing_name(self, client: AsyncClient):
        """Test user creation with missing name."""
        user_data = {"email": "test@example.com"}
        response = await client.post("/users/", json=user_data)
        
        assert response.status_code == 422  # Validation error
    
    async def test_create_user_missing_email(self, client: AsyncClient):
        """Test user creation with missing email."""
        user_data = {"name": "Test User"}
        response = await client.post("/users/", json=user_data)
        
        assert response.status_code == 422  # Validation error
    
    async def test_create_user_invalid_email(self, client: AsyncClient):
        """Test user creation with invalid email format."""
        user_data = {"name": "Test User", "email": "invalid-email"}
        response = await client.post("/users/", json=user_data)
        
        assert response.status_code == 422  # Validation error
    
    async def test_create_user_empty_data(self, client: AsyncClient):
        """Test user creation with empty data."""
        response = await client.post("/users/", json={})
        
        assert response.status_code == 422  # Validation error
    
    async def test_create_user_duplicate_email(self, client: AsyncClient, test_user_data: dict):
        """Test user creation with duplicate email."""
        # Create first user
        response1 = await client.post("/users/", json=test_user_data)
        assert response1.status_code == 200
        
        # Try to create second user with same email
        response2 = await client.post("/users/", json=test_user_data)
        assert response2.status_code == 400  # Bad request for duplicate


@pytest.mark.asyncio
class TestUserRead:
    """Test user retrieval endpoints - TDD Approach."""
    
    async def test_get_users_empty(self, client: AsyncClient):
        """Test getting users when database is empty."""
        response = await client.get("/users/")
        
        assert response.status_code == 200
        data = response.json()
        assert data == []
    
    async def test_get_users_with_data(self, client: AsyncClient, test_users_data: list[dict]):
        """Test getting users when database has data."""
        # Create users first
        for user_data in test_users_data:
            await client.post("/users/", json=user_data)
        
        # Get all users
        response = await client.get("/users/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) == len(test_users_data)
        
        # Check that all created users are returned
        for i, user_data in enumerate(test_users_data):
            assert data[i]["name"] == user_data["name"]
            assert data[i]["email"] == user_data["email"]
            assert "id" in data[i]
            assert "created_at" in data[i]
            assert "updated_at" in data[i]
            assert data[i]["is_deleted"] is False
    
    async def test_get_user_by_id_success(self, client: AsyncClient, test_user_data: dict):
        """Test getting a specific user by ID."""
        # Create user first
        create_response = await client.post("/users/", json=test_user_data)
        assert create_response.status_code == 200
        user_id = create_response.json()["id"]
        
        # Get user by ID
        response = await client.get(f"/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == user_id
        assert data["name"] == test_user_data["name"]
        assert data["email"] == test_user_data["email"]
    
    async def test_get_user_by_id_not_found(self, client: AsyncClient):
        """Test getting a non-existent user by ID."""
        response = await client.get("/users/999")
        
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]
    
    async def test_get_user_by_id_invalid_format(self, client: AsyncClient):
        """Test getting user with invalid ID format."""
        response = await client.get("/users/invalid")
        
        assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
class TestUserUpdate:
    """Test user update endpoints - TDD Approach."""
    
    async def test_update_user_success(self, client: AsyncClient, test_user_data: dict):
        """Test successful user update."""
        # Create a user first
        create_response = await client.post("/users/", json=test_user_data)
        assert create_response.status_code == 200
        user_id = create_response.json()["id"]
        
        # Update the user
        update_data = {"name": "Updated User", "email": "updated@example.com"}
        response = await client.put(f"/users/{user_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == user_id
        assert data["name"] == update_data["name"]
        assert data["email"] == update_data["email"]
        assert data["is_deleted"] is False
    
    async def test_update_user_not_found(self, client: AsyncClient):
        """Test updating a non-existent user."""
        update_data = {"name": "Updated User", "email": "updated@example.com"}
        response = await client.put("/users/999", json=update_data)
        
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]
    
    async def test_update_user_invalid_id(self, client: AsyncClient):
        """Test updating user with invalid ID."""
        update_data = {"name": "Updated User", "email": "updated@example.com"}
        response = await client.put("/users/invalid", json=update_data)
        
        assert response.status_code == 422  # Validation error for path parameter
    
    async def test_update_user_missing_data(self, client: AsyncClient, test_user_data: dict):
        """Test updating user with missing data."""
        # Create a user first
        create_response = await client.post("/users/", json=test_user_data)
        assert create_response.status_code == 200
        user_id = create_response.json()["id"]
        
        # Try to update with missing data
        response = await client.put(f"/users/{user_id}", json={})
        
        assert response.status_code == 422  # Validation error
    
    async def test_update_user_partial_data(self, client: AsyncClient, test_user_data: dict):
        """Test updating user with partial data."""
        # Create a user first
        create_response = await client.post("/users/", json=test_user_data)
        assert create_response.status_code == 200
        user_id = create_response.json()["id"]
        
        # Update only name
        update_data = {"name": "Updated Name Only"}
        response = await client.put(f"/users/{user_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["name"] == update_data["name"]
        assert data["email"] == test_user_data["email"]  # Email should remain unchanged


@pytest.mark.asyncio
class TestUserDelete:
    """Test user deletion endpoints - TDD Approach."""
    
    async def test_delete_user_success(self, client: AsyncClient, test_user_data: dict):
        """Test successful user deletion."""
        # Create a user first
        create_response = await client.post("/users/", json=test_user_data)
        assert create_response.status_code == 200
        user_id = create_response.json()["id"]
        
        # Delete the user
        response = await client.delete(f"/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == user_id
        assert data["is_deleted"] is True
    
    async def test_delete_user_not_found(self, client: AsyncClient):
        """Test deleting a non-existent user."""
        response = await client.delete("/users/999")
        
        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]
    
    async def test_delete_user_invalid_id(self, client: AsyncClient):
        """Test deleting user with invalid ID."""
        response = await client.delete("/users/invalid")
        
        assert response.status_code == 422  # Validation error
    
    async def test_delete_already_deleted_user(self, client: AsyncClient, test_user_data: dict):
        """Test deleting an already deleted user."""
        # Create a user first
        create_response = await client.post("/users/", json=test_user_data)
        assert create_response.status_code == 200
        user_id = create_response.json()["id"]
        
        # Delete the user first time
        delete_response1 = await client.delete(f"/users/{user_id}")
        assert delete_response1.status_code == 200
        
        # Try to delete the same user again
        delete_response2 = await client.delete(f"/users/{user_id}")
        assert delete_response2.status_code == 404  # Should not be found


@pytest.mark.asyncio
class TestUserValidation:
    """Test user validation - TDD Approach."""
    
    @pytest.mark.parametrize("invalid_email", [
        "not-an-email",
        "@example.com",
        "test@",
        "test.example.com",
        "",
        None
    ])
    async def test_invalid_email_formats(self, client: AsyncClient, invalid_email):
        """Test various invalid email formats."""
        user_data = {"name": "Test User", "email": invalid_email}
        response = await client.post("/users/", json=user_data)
        
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.parametrize("valid_email", [
        "test@example.com",
        "user.name@domain.co.uk",
        "user+tag@example.org",
        "123@numbers.com"
    ])
    async def test_valid_email_formats(self, client: AsyncClient, valid_email):
        """Test various valid email formats."""
        user_data = {"name": "Test User", "email": valid_email}
        response = await client.post("/users/", json=user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == valid_email
    
    async def test_empty_name(self, client: AsyncClient):
        """Test user creation with empty name."""
        user_data = {"name": "", "email": "test@example.com"}
        response = await client.post("/users/", json=user_data)
        
        assert response.status_code == 422  # Validation error
    
    async def test_very_long_name(self, client: AsyncClient):
        """Test user creation with very long name."""
        long_name = "a" * 256  # Assuming max length is 255
        user_data = {"name": long_name, "email": "test@example.com"}
        response = await client.post("/users/", json=user_data)
        
        assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
class TestUserIntegration:
    """Integration tests for user operations - TDD Approach."""
    
    async def test_full_user_lifecycle(self, client: AsyncClient):
        """Test complete user lifecycle: create, read, update, delete."""
        # Create user
        user_data = {"name": "Integration User", "email": "integration@example.com"}
        create_response = await client.post("/users/", json=user_data)
        assert create_response.status_code == 200
        created_user = create_response.json()
        user_id = created_user["id"]
        
        # Verify user was created
        get_response = await client.get("/users/")
        assert get_response.status_code == 200
        users = get_response.json()
        assert len(users) == 1
        assert users[0]["id"] == user_id
        assert users[0]["name"] == user_data["name"]
        assert users[0]["email"] == user_data["email"]
        
        # Update user
        update_data = {"name": "Updated Integration User", "email": "updated.integration@example.com"}
        update_response = await client.put(f"/users/{user_id}", json=update_data)
        assert update_response.status_code == 200
        updated_user = update_response.json()
        
        assert updated_user["id"] == user_id
        assert updated_user["name"] == update_data["name"]
        assert updated_user["email"] == update_data["email"]
        
        # Verify update is reflected in get all
        get_response_after_update = await client.get("/users/")
        assert get_response_after_update.status_code == 200
        users_after_update = get_response_after_update.json()
        assert len(users_after_update) == 1
        assert users_after_update[0]["name"] == update_data["name"]
        assert users_after_update[0]["email"] == update_data["email"]
        
        # Delete user
        delete_response = await client.delete(f"/users/{user_id}")
        assert delete_response.status_code == 200
        
        # Verify user is deleted
        get_response_after_delete = await client.get("/users/")
        assert get_response_after_delete.status_code == 200
        users_after_delete = get_response_after_delete.json()
        assert len(users_after_delete) == 0
    
    async def test_multiple_users_operations(self, client: AsyncClient, test_users_data: list[dict]):
        """Test operations with multiple users."""
        # Create multiple users
        created_users = []
        for user_data in test_users_data:
            response = await client.post("/users/", json=user_data)
            assert response.status_code == 200
            created_users.append(response.json())
        
        # Verify all users were created
        get_response = await client.get("/users/")
        assert get_response.status_code == 200
        users = get_response.json()
        assert len(users) == len(test_users_data)
        
        # Update each user
        for i, user in enumerate(created_users):
            update_data = {
                "name": f"Updated {test_users_data[i]['name']}",
                "email": f"updated.{test_users_data[i]['email']}"
            }
            response = await client.put(f"/users/{user['id']}", json=update_data)
            assert response.status_code == 200
            
            updated_user = response.json()
            assert updated_user["name"] == update_data["name"]
            assert updated_user["email"] == update_data["email"]
        
        # Delete all users
        for user in created_users:
            response = await client.delete(f"/users/{user['id']}")
            assert response.status_code == 200
        
        # Verify all users are deleted
        final_get_response = await client.get("/users/")
        assert final_get_response.status_code == 200
        final_users = final_get_response.json()
        assert len(final_users) == 0


@pytest.mark.asyncio
class TestUserErrorHandling:
    """Test error handling scenarios - TDD Approach."""
    
    async def test_database_connection_error(self, client: AsyncClient, test_user_data: dict):
        """Test handling of database connection errors."""
        # This would require mocking the database connection
        # For now, we'll test basic error handling
        pass
    
    async def test_concurrent_user_creation(self, client: AsyncClient, test_user_data: dict):
        """Test concurrent user creation scenarios."""
        # This would test race conditions
        pass
    
    async def test_malformed_json_request(self, client: AsyncClient):
        """Test handling of malformed JSON requests."""
        response = await client.post("/users/", data="invalid json")
        assert response.status_code == 422  # Unprocessable Entity 