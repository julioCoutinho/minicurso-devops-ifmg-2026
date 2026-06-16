"""
Unit tests for the FastAPI application
Tests cover all main endpoints and utility functions
"""

import pytest
from fastapi.testclient import TestClient
from main import app, calculate_discount, get_item_by_name, get_user_by_username, Item, User

# Create a test client
client = TestClient(app)

# ==================== Health Check Tests ====================

def test_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to DevOps Demo API"
    assert response.json()["status"] == "healthy"

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["version"] == "1.0.0"

# ==================== Items Endpoints Tests ====================

def test_get_items():
    """Test getting all items"""
    response = client.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) > 0

def test_get_items_with_pagination():
    """Test getting items with pagination"""
    response = client.get("/items?skip=0&limit=2")
    assert response.status_code == 200
    items = response.json()
    assert len(items) <= 2

def test_get_item_by_id():
    """Test getting a specific item by ID"""
    response = client.get("/items/1")
    assert response.status_code == 200
    item = response.json()
    assert item["id"] == 1
    assert item["name"] == "Laptop"

def test_get_item_by_name():
    """Test getting a specific item by name"""
    response = client.get("/items/Laptop")
    assert response.status_code == 200
    item = response.json()
    assert item["id"] == 1
    assert item["name"] == "Laptop"

def test_get_item_not_found():
    """Test getting a non-existent item"""
    response = client.get("/items/9999")
    assert response.status_code == 404
    assert "Item not found" in response.json()["detail"]

def test_create_item():
    """Test creating a new item"""
    new_item = {
        "name": "Monitor",
        "description": "4K Monitor",
        "price": 399.99,
        "in_stock": True
    }
    response = client.post("/items", json=new_item)
    assert response.status_code == 200
    created_item = response.json()
    assert created_item["name"] == "Monitor"
    assert created_item["id"] is not None

def test_update_item():
    """Test updating an item"""
    updated_item = {
        "name": "Updated Laptop",
        "description": "Updated description",
        "price": 1099.99,
        "in_stock": False
    }
    response = client.put("/items/1", json=updated_item)
    assert response.status_code == 200
    item = response.json()
    assert item["name"] == "Updated Laptop"
    assert item["price"] == 1099.99

def test_delete_item():
    """Test deleting an item"""
    # First create an item to delete
    new_item = {
        "name": "Temporary Item",
        "description": "To be deleted",
        "price": 10.00,
        "in_stock": True
    }
    create_response = client.post("/items", json=new_item)
    item_id = create_response.json()["id"]
    
    # Now delete it
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    assert "Item deleted successfully" in response.json()["message"]
    
    # Verify it's deleted
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404

# ==================== Users Endpoints Tests ====================

def test_get_users():
    """Test getting all users"""
    response = client.get("/users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) > 0

def test_get_users_with_pagination():
    """Test getting users with pagination"""
    response = client.get("/users?skip=0&limit=1")
    assert response.status_code == 200
    users = response.json()
    assert len(users) <= 1

def test_get_user_by_id():
    """Test getting a specific user by ID"""
    response = client.get("/users/1")
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == 1
    assert user["username"] == "john_doe"

def test_get_user_not_found():
    """Test getting a non-existent user"""
    response = client.get("/users/9999")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

def test_create_user():
    """Test creating a new user"""
    new_user = {
        "username": "alice_wonder",
        "email": "alice@example.com",
        "full_name": "Alice Wonder"
    }
    response = client.post("/users", json=new_user)
    assert response.status_code == 200
    created_user = response.json()
    assert created_user["username"] == "alice_wonder"
    assert created_user["id"] is not None

# ==================== Statistics Endpoint Tests ====================

def test_get_stats():
    """Test getting statistics"""
    response = client.get("/stats")
    assert response.status_code == 200
    stats = response.json()
    assert "total_items" in stats
    assert "items_in_stock" in stats
    assert "total_users" in stats
    assert "total_inventory_value" in stats
    assert stats["total_items"] > 0
    assert stats["total_users"] > 0

# ==================== Utility Function Tests ====================

def test_calculate_discount():
    """Test the calculate_discount function"""
    # Test 10% discount
    result = calculate_discount(100, 10)
    assert result == 90.0
    
    # Test 50% discount
    result = calculate_discount(100, 50)
    assert result == 50.0
    
    # Test no discount
    result = calculate_discount(100, 0)
    assert result == 100.0

def test_calculate_discount_invalid():
    """Test calculate_discount with invalid input"""
    with pytest.raises(ValueError):
        calculate_discount(100, -10)
    
    with pytest.raises(ValueError):
        calculate_discount(100, 150)

def test_get_item_by_name():
    """Test the get_item_by_name function"""
    item = get_item_by_name("Laptop")
    assert item is not None
    assert item.name == "Laptop"
    
    # Test non-existent item
    item = get_item_by_name("NonExistent")
    assert item is None

def teste_get_item_by_id():
    """Test the get_item_by_id function"""
    item = get_item_by_id(1)
    assert item is not None
    assert item.id == 1
    assert item.name == "Laptop"

    # Test non-existent item
    item = get_item_by_id(9999)
    assert item is None

def test_get_user_by_username():
    """Test the get_user_by_username function"""
    user = get_user_by_username("john_doe")
    assert user is not None
    assert user.username == "john_doe"
    
    # Test non-existent user
    user = get_user_by_username("nonexistent_user")
    assert user is None

# ==================== Integration Tests ====================

def test_create_and_retrieve_item():
    """Integration test: create an item and retrieve it"""
    new_item = {
        "name": "Integration Test Item",
        "description": "Testing create and retrieve",
        "price": 50.00,
        "in_stock": True
    }
    
    # Create
    create_response = client.post("/items", json=new_item)
    assert create_response.status_code == 200
    created_item = create_response.json()
    item_id = created_item["id"]
    
    # Retrieve
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 200
    retrieved_item = get_response.json()
    assert retrieved_item["name"] == "Integration Test Item"
    assert retrieved_item["price"] == 50.00

def test_create_and_retrieve_user():
    """Integration test: create a user and retrieve it"""
    new_user = {
        "username": "integration_test_user",
        "email": "integration@test.com",
        "full_name": "Integration Test"
    }
    
    # Create
    create_response = client.post("/users", json=new_user)
    assert create_response.status_code == 200
    created_user = create_response.json()
    user_id = created_user["id"]
    
    # Retrieve
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    retrieved_user = get_response.json()
    assert retrieved_user["username"] == "integration_test_user"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
