"""
FastAPI Application for CI/CD Demonstration
This application demonstrates a simple API with multiple endpoints
that can be tested and deployed using GitHub Actions.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Initialize FastAPI application
app = FastAPI(
    title="DevOps Demo API",
    description="A FastAPI application for demonstrating CI/CD with GitHub Actions",
    version="1.0.0"
)

# Pydantic models for request/response validation
class Item(BaseModel):
    """Model for an item in the inventory"""
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True

class User(BaseModel):
    """Model for a user"""
    id: Optional[int] = None
    username: str
    email: str
    full_name: Optional[str] = None

# In-memory storage (for demonstration purposes)
items_db: List[Item] = [
    Item(id=1, name="Laptop", description="High-performance laptop", price=999.99, in_stock=True),
    Item(id=2, name="Mouse", description="Wireless mouse", price=29.99, in_stock=True),
    Item(id=3, name="Keyboard", description="Mechanical keyboard", price=79.99, in_stock=False),
]

users_db: List[User] = [
    User(id=1, username="john_doe", email="john@example.com", full_name="John Doe"),
    User(id=2, username="jane_smith", email="jane@example.com", full_name="Jane Smith"),
]

# Root endpoint
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - returns a welcome message"""
    return {
        "message": "Welcome to DevOps Demo API",
        "timestamp": datetime.now().isoformat(),
        "status": "healthy"
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint - returns the status of the API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Items endpoints
@app.get("/items", response_model=List[Item], tags=["Items"])
async def get_items(skip: int = 0, limit: int = 10):
    """Get all items with pagination"""
    return items_db[skip:skip + limit]

@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
async def get_item(item_id: int):
    """Get a specific item by ID"""
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items", response_model=Item, tags=["Items"])
async def create_item(item: Item):
    """Create a new item"""
    # Generate a new ID
    new_id = max([i.id for i in items_db], default=0) + 1
    item.id = new_id
    items_db.append(item)
    return item

@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
async def update_item(item_id: int, item: Item):
    """Update an existing item"""
    for i, existing_item in enumerate(items_db):
        if existing_item.id == item_id:
            item.id = item_id
            items_db[i] = item
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", tags=["Items"])
async def delete_item(item_id: int):
    """Delete an item"""
    for i, item in enumerate(items_db):
        if item.id == item_id:
            deleted_item = items_db.pop(i)
            return {"message": "Item deleted successfully", "item": deleted_item}
    raise HTTPException(status_code=404, detail="Item not found")

# Users endpoints
@app.get("/users", response_model=List[User], tags=["Users"])
async def get_users(skip: int = 0, limit: int = 10):
    """Get all users with pagination"""
    return users_db[skip:skip + limit]

@app.get("/users/{user_id}", response_model=User, tags=["Users"])
async def get_user(user_id: int):
    """Get a specific user by ID"""
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users", response_model=User, tags=["Users"])
async def create_user(user: User):
    """Create a new user"""
    # Generate a new ID
    new_id = max([u.id for u in users_db], default=0) + 1
    user.id = new_id
    users_db.append(user)
    return user

# Statistics endpoint
@app.get("/stats", tags=["Statistics"])
async def get_stats():
    """Get statistics about the API"""
    items_in_stock = sum(1 for item in items_db if item.in_stock)
    total_value = sum(item.price for item in items_db if item.in_stock)
    
    return {
        "total_items": len(items_db),
        "items_in_stock": items_in_stock,
        "total_users": len(users_db),
        "total_inventory_value": round(total_value, 2),
        "timestamp": datetime.now().isoformat()
    }

# Utility functions for testing
@app.get("/items/name={name}", response_model=Item, tags=["Items"])
def get_item_by_name(name: str) -> Optional[Item]:
    """Get an item by name"""
    for item in items_db:
        if item.name.lower() == name.lower():
            return item
    return None

@app.get("/items/id={id}", response_model=Item, tags=["Items"])
def get_item_by_id(id: int) -> Optional[Item]:
    """Get an item by ID"""
    for item in items_db:
        if item.id == id:
            return item
    return None

@app.get("/users/username={username}", response_model=User, tags=["Users"])
def get_user_by_username(username: str) -> Optional[User]:
    """Get a user by username"""
    for user in users_db:
        if user.username.lower() == username.lower():
            return user
    return None

def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate discounted price"""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount percent must be between 0 and 100")
    return round(price * (1 - discount_percent / 100), 2)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
