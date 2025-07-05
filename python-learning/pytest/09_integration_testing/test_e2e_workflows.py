"""
End-to-End workflow tests demonstrating complete system integration.
"""
import pytest
import time
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock


class TestUserWorkflow:
    """Test complete user workflows from registration to profile management."""
    
    def test_user_registration_and_login_flow(self, api_client):
        """Test complete user registration and login workflow."""
        # Step 1: Register a new user
        registration_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepass123",
            "full_name": "Test User"
        }
        
        register_response = api_client.post("/api/users/register", json=registration_data)
        assert register_response.status_code == 201
        
        user_data = register_response.json()
        assert user_data["username"] == registration_data["username"]
        assert user_data["email"] == registration_data["email"]
        assert "id" in user_data
        
        # Step 2: Login with the new user
        login_data = {
            "username": "testuser",
            "password": "securepass123"
        }
        
        login_response = api_client.post("/api/auth/login", data=login_data)
        assert login_response.status_code == 200
        
        auth_data = login_response.json()
        assert "access_token" in auth_data
        assert "token_type" in auth_data
        
        token = auth_data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Step 3: Access protected resources
        profile_response = api_client.get("/api/users/profile", headers=headers)
        assert profile_response.status_code == 200
        
        profile_data = profile_response.json()
        assert profile_data["username"] == "testuser"
        assert profile_data["email"] == "test@example.com"
        
        # Step 4: Update profile
        update_data = {"full_name": "Updated Test User"}
        update_response = api_client.put("/api/users/profile", json=update_data, headers=headers)
        assert update_response.status_code == 200
        
        # Step 5: Verify changes
        profile_response = api_client.get("/api/users/profile", headers=headers)
        updated_profile = profile_response.json()
        assert updated_profile["full_name"] == "Updated Test User"
        
        # Step 6: Test logout
        logout_response = api_client.post("/api/auth/logout", headers=headers)
        assert logout_response.status_code == 200
        
        # Step 7: Verify token is invalidated
        profile_response = api_client.get("/api/users/profile", headers=headers)
        assert profile_response.status_code == 401
    
    def test_user_password_reset_flow(self, api_client):
        """Test complete password reset workflow."""
        # Step 1: Request password reset
        reset_request_data = {"email": "test@example.com"}
        reset_response = api_client.post("/api/auth/reset-password", json=reset_request_data)
        assert reset_response.status_code == 200
        
        # Step 2: Verify reset email was sent (mock)
        with patch('app.services.email_service.send_email') as mock_send_email:
            mock_send_email.return_value = {"status": "sent"}
            
            # Simulate email sending
            email_sent = mock_send_email("test@example.com", "Password Reset", "Reset link")
            assert email_sent["status"] == "sent"
            mock_send_email.assert_called_once()
        
        # Step 3: Reset password with token (mock token)
        reset_token = "mock_reset_token_123"
        new_password_data = {
            "token": reset_token,
            "new_password": "newsecurepass456"
        }
        
        with patch('app.services.auth_service.verify_reset_token') as mock_verify:
            mock_verify.return_value = {"user_id": 1, "valid": True}
            
            reset_password_response = api_client.post("/api/auth/reset-password/confirm", json=new_password_data)
            assert reset_password_response.status_code == 200
        
        # Step 4: Login with new password
        login_data = {
            "username": "testuser",
            "password": "newsecurepass456"
        }
        
        login_response = api_client.post("/api/auth/login", data=login_data)
        assert login_response.status_code == 200


class TestEcommerceWorkflow:
    """Test complete e-commerce workflows."""
    
    def test_complete_purchase_workflow(self, api_client, authenticated_user):
        """Test complete purchase from browsing to order confirmation."""
        user_id, token = authenticated_user
        headers = {"Authorization": f"Bearer {token}"}
        
        # Step 1: Browse products
        products_response = api_client.get("/api/products", headers=headers)
        assert products_response.status_code == 200
        
        products = products_response.json()
        assert len(products) > 0
        
        product = products[0]
        product_id = product["id"]
        
        # Step 2: Add product to cart
        cart_data = {
            "product_id": product_id,
            "quantity": 2
        }
        
        cart_response = api_client.post("/api/cart/items", json=cart_data, headers=headers)
        assert cart_response.status_code == 201
        
        cart_item = cart_response.json()
        assert cart_item["product_id"] == product_id
        assert cart_item["quantity"] == 2
        
        # Step 3: View cart
        cart_response = api_client.get("/api/cart", headers=headers)
        assert cart_response.status_code == 200
        
        cart = cart_response.json()
        assert len(cart["items"]) == 1
        assert cart["total_amount"] == product["price"] * 2
        
        # Step 4: Create order
        order_data = {
            "shipping_address": "123 Main St, Anytown, USA",
            "payment_method": "card"
        }
        
        order_response = api_client.post("/api/orders", json=order_data, headers=headers)
        assert order_response.status_code == 201
        
        order = order_response.json()
        assert order["status"] == "pending"
        assert order["user_id"] == user_id
        
        order_id = order["id"]
        
        # Step 5: Process payment
        payment_data = {
            "order_id": order_id,
            "card_number": "4242424242424242",
            "expiry_month": "12",
            "expiry_year": "2025",
            "cvv": "123"
        }
        
        with patch('app.services.payment_service.process_payment') as mock_payment:
            mock_payment.return_value = {
                "transaction_id": "txn_123",
                "status": "succeeded",
                "amount": order["total_amount"]
            }
            
            payment_response = api_client.post("/api/payments", json=payment_data, headers=headers)
            assert payment_response.status_code == 200
            
            payment_result = payment_response.json()
            assert payment_result["status"] == "succeeded"
        
        # Step 6: Confirm order
        confirm_response = api_client.put(f"/api/orders/{order_id}/confirm", headers=headers)
        assert confirm_response.status_code == 200
        
        # Step 7: Verify order status
        order_response = api_client.get(f"/api/orders/{order_id}", headers=headers)
        assert order_response.status_code == 200
        
        final_order = order_response.json()
        assert final_order["status"] == "confirmed"
        
        # Step 8: Verify cart is cleared
        cart_response = api_client.get("/api/cart", headers=headers)
        assert cart_response.status_code == 200
        
        cart = cart_response.json()
        assert len(cart["items"]) == 0
    
    def test_inventory_management_workflow(self, api_client, authenticated_admin):
        """Test inventory management workflow."""
        admin_id, token = authenticated_admin
        headers = {"Authorization": f"Bearer {token}"}
        
        # Step 1: Create new product
        product_data = {
            "name": "Test Product",
            "description": "A test product for inventory management",
            "price": 29.99,
            "stock_quantity": 100,
            "category": "Electronics"
        }
        
        product_response = api_client.post("/api/admin/products", json=product_data, headers=headers)
        assert product_response.status_code == 201
        
        product = product_response.json()
        product_id = product["id"]
        
        # Step 2: Update inventory
        inventory_update = {
            "stock_quantity": 150
        }
        
        update_response = api_client.put(f"/api/admin/products/{product_id}/inventory", json=inventory_update, headers=headers)
        assert update_response.status_code == 200
        
        # Step 3: Verify inventory update
        product_response = api_client.get(f"/api/admin/products/{product_id}", headers=headers)
        assert product_response.status_code == 200
        
        updated_product = product_response.json()
        assert updated_product["stock_quantity"] == 150
        
        # Step 4: Test low stock alert
        low_stock_update = {
            "stock_quantity": 5
        }
        
        update_response = api_client.put(f"/api/admin/products/{product_id}/inventory", json=low_stock_update, headers=headers)
        assert update_response.status_code == 200
        
        # Step 5: Check low stock products
        low_stock_response = api_client.get("/api/admin/products/low-stock", headers=headers)
        assert low_stock_response.status_code == 200
        
        low_stock_products = low_stock_response.json()
        assert any(p["id"] == product_id for p in low_stock_products)


class TestNotificationWorkflow:
    """Test notification and communication workflows."""
    
    def test_email_notification_workflow(self, api_client, authenticated_user):
        """Test email notification workflow."""
        user_id, token = authenticated_user
        headers = {"Authorization": f"Bearer {token}"}
        
        # Step 1: Update notification preferences
        notification_prefs = {
            "email_notifications": True,
            "order_updates": True,
            "promotional_emails": False
        }
        
        prefs_response = api_client.put("/api/users/notification-preferences", json=notification_prefs, headers=headers)
        assert prefs_response.status_code == 200
        
        # Step 2: Create an order to trigger notification
        order_data = {
            "shipping_address": "123 Main St, Anytown, USA",
            "payment_method": "card"
        }
        
        with patch('app.services.email_service.send_order_confirmation') as mock_email:
            mock_email.return_value = {"status": "sent", "message_id": "msg_123"}
            
            order_response = api_client.post("/api/orders", json=order_data, headers=headers)
            assert order_response.status_code == 201
            
            # Verify email was sent
            mock_email.assert_called_once()
    
    def test_sms_notification_workflow(self, api_client, authenticated_user):
        """Test SMS notification workflow."""
        user_id, token = authenticated_user
        headers = {"Authorization": f"Bearer {token}"}
        
        # Step 1: Add phone number
        phone_data = {
            "phone_number": "+1234567890"
        }
        
        phone_response = api_client.put("/api/users/phone", json=phone_data, headers=headers)
        assert phone_response.status_code == 200
        
        # Step 2: Enable SMS notifications
        sms_prefs = {
            "sms_notifications": True,
            "order_updates_sms": True
        }
        
        prefs_response = api_client.put("/api/users/notification-preferences", json=sms_prefs, headers=headers)
        assert prefs_response.status_code == 200
        
        # Step 3: Test SMS sending (mock)
        with patch('app.services.sms_service.send_sms') as mock_sms:
            mock_sms.return_value = {"status": "sent", "message_id": "sms_123"}
            
            # Trigger SMS notification
            test_data = {"message": "Test SMS notification"}
            sms_response = api_client.post("/api/test/sms", json=test_data, headers=headers)
            assert sms_response.status_code == 200
            
            # Verify SMS was sent
            mock_sms.assert_called_once()


# Fixtures for integration testing
@pytest.fixture
def api_client():
    """Create API client for testing."""
    from app.main import app
    return TestClient(app)


@pytest.fixture
def authenticated_user(api_client):
    """Create an authenticated user for testing."""
    # Create user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "securepass123"
    }
    
    api_client.post("/api/users/register", json=user_data)
    
    # Login
    login_data = {
        "username": "testuser",
        "password": "securepass123"
    }
    
    login_response = api_client.post("/api/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    
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
    
    api_client.post("/api/users/register", json=admin_data)
    
    # Login
    login_data = {
        "username": "admin",
        "password": "adminpass123"
    }
    
    login_response = api_client.post("/api/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    
    return 2, token  # Assuming admin ID is 2 