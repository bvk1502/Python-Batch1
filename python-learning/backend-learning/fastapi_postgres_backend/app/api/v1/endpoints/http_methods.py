from fastapi import APIRouter, HTTPException, Query, Path, Body, Form, File, UploadFile
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import json

router = APIRouter(prefix="/http-methods", tags=["HTTP Methods Demo"])

# Pydantic models for request/response
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tags: List[str] = []

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tags: Optional[List[str]] = None

# Sample data store (in real app, this would be a database)
items_db = {
    1: {"id": 1, "name": "Laptop", "description": "High-performance laptop", "price": 999.99, "tags": ["electronics", "computer"]},
    2: {"id": 2, "name": "Phone", "description": "Smartphone", "price": 699.99, "tags": ["electronics", "mobile"]},
    3: {"id": 3, "name": "Book", "description": "Programming book", "price": 49.99, "tags": ["education", "programming"]}
}

# GET - Retrieve data
@router.get("/", response_model=List[Item])
async def get_all_items():
    """GET method - Retrieve all items"""
    return list(items_db.values())

@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int = Path(..., description="The ID of the item to get")):
    """GET method - Retrieve a specific item by ID"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@router.get("/search/", response_model=List[Item])
async def search_items(
    name: Optional[str] = Query(None, description="Search by name"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price")
):
    """GET method - Search items with query parameters"""
    results = []
    for item in items_db.values():
        if name and name.lower() not in item["name"].lower():
            continue
        if min_price and item["price"] < min_price:
            continue
        if max_price and item["price"] > max_price:
            continue
        results.append(item)
    return results

# POST - Create new data
@router.post("/", response_model=Item, status_code=201)
async def create_item(item: Item = Body(..., description="Item to create")):
    """POST method - Create a new item"""
    if item.id in items_db:
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items_db[item.id] = item.dict()
    return item

@router.post("/bulk", response_model=List[Item], status_code=201)
async def create_multiple_items(items: List[Item] = Body(..., description="List of items to create")):
    """POST method - Create multiple items"""
    created_items = []
    for item in items:
        if item.id in items_db:
            raise HTTPException(status_code=400, detail=f"Item with ID {item.id} already exists")
        items_db[item.id] = item.dict()
        created_items.append(item)
    return created_items

# PUT - Update/replace entire resource
@router.put("/{item_id}", response_model=Item)
async def update_item_put(
    item_id: int = Path(..., description="The ID of the item to update"),
    item: Item = Body(..., description="Complete item data")
):
    """PUT method - Replace entire item"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.id != item_id:
        raise HTTPException(status_code=400, detail="Item ID in body must match path parameter")
    items_db[item_id] = item.dict()
    return item

# PATCH - Partial update
@router.patch("/{item_id}", response_model=Item)
async def update_item_patch(
    item_id: int = Path(..., description="The ID of the item to update"),
    item_update: ItemUpdate = Body(..., description="Partial item data to update")
):
    """PATCH method - Partial update of item"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    current_item = items_db[item_id]
    update_data = item_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        current_item[field] = value
    
    items_db[item_id] = current_item
    return current_item

# DELETE - Remove data
@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int = Path(..., description="The ID of the item to delete")):
    """DELETE method - Delete an item"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return None

@router.delete("/", status_code=204)
async def delete_all_items():
    """DELETE method - Delete all items"""
    items_db.clear()
    return None

# HEAD - Get headers only (no body)
@router.head("/{item_id}")
async def head_item(item_id: int = Path(..., description="The ID of the item to check")):
    """HEAD method - Get headers only, no body"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return None

# OPTIONS - Get allowed methods
@router.options("/")
async def options_items():
    """OPTIONS method - Get allowed HTTP methods"""
    return {
        "allowed_methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
        "description": "Available operations for items"
    }

# Form data example
@router.post("/form", response_model=Dict[str, Any])
async def create_item_form(
    name: str = Form(..., description="Item name"),
    price: float = Form(..., description="Item price"),
    description: Optional[str] = Form(None, description="Item description")
):
    """POST method - Create item using form data"""
    return {
        "name": name,
        "price": price,
        "description": description,
        "method": "form_data"
    }

# File upload example
@router.post("/upload", response_model=Dict[str, Any])
async def upload_file(
    file: UploadFile = File(..., description="File to upload"),
    description: Optional[str] = Form(None, description="File description")
):
    """POST method - Upload a file"""
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(await file.read()),
        "description": description,
        "method": "file_upload"
    }

# Multiple file upload
@router.post("/upload-multiple", response_model=List[Dict[str, Any]])
async def upload_multiple_files(
    files: List[UploadFile] = File(..., description="Files to upload")
):
    """POST method - Upload multiple files"""
    results = []
    for file in files:
        content = await file.read()
        results.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content)
        })
    return results

# Custom status codes and responses
@router.get("/status-demo/{status_code}")
async def status_code_demo(status_code: int = Path(..., ge=200, le=599)):
    """GET method - Demonstrate different status codes"""
    if status_code == 200:
        return {"message": "Success", "status_code": status_code}
    elif status_code == 201:
        return {"message": "Created", "status_code": status_code}
    elif status_code == 400:
        raise HTTPException(status_code=400, detail="Bad Request")
    elif status_code == 404:
        raise HTTPException(status_code=404, detail="Not Found")
    elif status_code == 500:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    else:
        return {"message": f"Status code {status_code}", "status_code": status_code}

# Health check endpoint
@router.get("/health")
async def health_check():
    """GET method - Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0.0"
    } 