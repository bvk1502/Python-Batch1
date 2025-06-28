# FastAPI HTTP Methods Demonstration

This module demonstrates all the HTTP methods supported by FastAPI with practical examples and use cases.

## Overview

The `http_methods.py` endpoint provides a comprehensive demonstration of:
- All standard HTTP methods (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS)
- Request/response handling
- Data validation with Pydantic
- File uploads
- Form data processing
- Error handling
- Custom status codes

## Base URL

```
http://localhost:8000/http-methods
```

## HTTP Methods Covered

### 1. GET - Retrieve Data

#### Get All Items
```http
GET /http-methods/
```
**Description:** Retrieve all items from the database
**Response:** List of all items
**Status Code:** 200

#### Get Specific Item
```http
GET /http-methods/{item_id}
```
**Description:** Retrieve a specific item by ID
**Parameters:**
- `item_id` (path): The ID of the item to retrieve
**Response:** Single item object
**Status Code:** 200, 404 (if not found)

#### Search Items
```http
GET /http-methods/search/?name=laptop&min_price=500&max_price=1000
```
**Description:** Search items with query parameters
**Query Parameters:**
- `name` (optional): Search by item name
- `min_price` (optional): Minimum price filter
- `max_price` (optional): Maximum price filter
**Response:** Filtered list of items
**Status Code:** 200

#### Health Check
```http
GET /http-methods/health
```
**Description:** Health check endpoint
**Response:** Health status information
**Status Code:** 200

### 2. POST - Create Data

#### Create Single Item
```http
POST /http-methods/
Content-Type: application/json

{
  "id": 4,
  "name": "Tablet",
  "description": "10-inch tablet",
  "price": 299.99,
  "tags": ["electronics", "tablet"]
}
```
**Description:** Create a new item
**Request Body:** Item object
**Response:** Created item
**Status Code:** 201, 400 (if ID already exists)

#### Create Multiple Items
```http
POST /http-methods/bulk
Content-Type: application/json

[
  {
    "id": 5,
    "name": "Keyboard",
    "price": 59.99,
    "tags": ["electronics", "input"]
  },
  {
    "id": 6,
    "name": "Mouse",
    "price": 29.99,
    "tags": ["electronics", "input"]****
  }
]
```
**Description:** Create multiple items in a single request
**Request Body:** Array of item objects
**Response:** List of created items
**Status Code:** 201, 400 (if any ID already exists)

#### Form Data Submission
```http
POST /http-methods/form
Content-Type: application/x-www-form-urlencoded

name=Headphones&price=99.99&description=Wireless headphones
```
**Description:** Create item using form data
**Request Body:** Form-encoded data
**Response:** Processed form data
**Status Code:** 200

#### File Upload
```http
POST /http-methods/upload
Content-Type: multipart/form-data

file: [binary file data]
description: "Product image"
```
**Description:** Upload a single file
**Request Body:** Multipart form data
**Response:** File metadata
**Status Code:** 200

#### Multiple File Upload
```http
POST /http-methods/upload-multiple
Content-Type: multipart/form-data

files: [binary file data 1]
files: [binary file data 2]
```
**Description:** Upload multiple files
**Request Body:** Multipart form data with multiple files
**Response:** List of file metadata
**Status Code:** 200

### 3. PUT - Replace Entire Resource

```http
PUT /http-methods/{item_id}
Content-Type: application/json

{
  "id": 1,
  "name": "Updated Laptop",
  "description": "Updated description",
  "price": 1099.99,
  "tags": ["electronics", "computer", "updated"]
}
```
**Description:** Replace entire item with new data
**Parameters:**
- `item_id` (path): The ID of the item to replace
**Request Body:** Complete item object
**Response:** Updated item
**Status Code:** 200, 404 (if not found), 400 (if ID mismatch)

### 4. PATCH - Partial Update

```http
PATCH /http-methods/{item_id}
Content-Type: application/json

{
  "price": 899.99,
  "tags": ["electronics", "computer", "discounted"]
}
```
**Description:** Partially update an item
**Parameters:**
- `item_id` (path): The ID of the item to update
**Request Body:** Partial item data (only fields to update)
**Response:** Updated item
**Status Code:** 200, 404 (if not found)

### 5. DELETE - Remove Data

#### Delete Specific Item
```http
DELETE /http-methods/{item_id}
```
**Description:** Delete a specific item
**Parameters:**
- `item_id` (path): The ID of the item to delete
**Response:** No content
**Status Code:** 204, 404 (if not found)

#### Delete All Items
```http
DELETE /http-methods/
```
**Description:** Delete all items
**Response:** No content
**Status Code:** 204

### 6. HEAD - Get Headers Only

```http
HEAD /http-methods/{item_id}
```
**Description:** Get headers without response body
**Parameters:**
- `item_id` (path): The ID of the item to check
**Response:** Headers only, no body
**Status Code:** 200, 404 (if not found)

### 7. OPTIONS - Get Allowed Methods

```http
OPTIONS /http-methods/
```
**Description:** Get allowed HTTP methods for the endpoint
**Response:** Allowed methods and description
**Status Code:** 200

## Data Models

### Item Model
```python
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tags: List[str] = []
```

### Item Update Model
```python
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tags: Optional[List[str]] = None
```

## Error Handling

The endpoints demonstrate proper error handling with appropriate HTTP status codes:

- **200 OK**: Successful GET, PUT, PATCH requests
- **201 Created**: Successful POST requests
- **204 No Content**: Successful DELETE requests
- **400 Bad Request**: Invalid request data
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server errors

## Testing

### Using curl

#### Get all items
```bash
curl -X GET "http://localhost:8000/http-methods/"
```

#### Create an item
```bash
curl -X POST "http://localhost:8000/http-methods/" \
  -H "Content-Type: application/json" \
  -d '{"id": 4, "name": "Tablet", "price": 299.99, "tags": ["electronics"]}'
```

#### Update an item
```bash
curl -X PATCH "http://localhost:8000/http-methods/1" \
  -H "Content-Type: application/json" \
  -d '{"price": 899.99}'
```

#### Delete an item
```bash
curl -X DELETE "http://localhost:8000/http-methods/1"
```

### Using Swagger UI

1. Start your FastAPI application
2. Navigate to `http://localhost:8000/docs`
3. Find the "HTTP Methods Demo" section
4. Test each endpoint interactively

## Key Features Demonstrated

1. **Type Safety**: Full type hints and Pydantic validation
2. **Automatic Documentation**: OpenAPI/Swagger documentation
3. **Request Validation**: Automatic validation of request data
4. **Response Models**: Structured response data
5. **Error Handling**: Proper HTTP status codes and error messages
6. **File Handling**: File upload capabilities
7. **Form Data**: Form processing
8. **Query Parameters**: URL parameter handling
9. **Path Parameters**: URL path variable handling
10. **Status Codes**: Custom status code responses

## Best Practices Shown

1. **RESTful Design**: Proper use of HTTP methods
2. **Validation**: Input validation with Pydantic
3. **Error Handling**: Comprehensive error responses
4. **Documentation**: Clear endpoint descriptions
5. **Type Safety**: Full type annotations
6. **Response Models**: Consistent response structures
7. **Status Codes**: Appropriate HTTP status codes
8. **Security**: Proper request handling

## Notes

- This is a demonstration module using in-memory storage
- In production, replace the `items_db` dictionary with a proper database
- Add authentication and authorization as needed
- Implement proper logging and monitoring
- Add rate limiting for production use
- Consider adding caching for GET requests

This README provides a comprehensive guide to understanding and using all the HTTP methods demonstrated in your FastAPI application. It includes practical examples, testing instructions, and best practices for each HTTP method.