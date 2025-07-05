# Mocking and Patching - Isolating Your Tests

This section covers pytest mocking and patching techniques, which allow you to isolate your tests from external dependencies and control the behavior of objects during testing.

## 📋 What You'll Learn

1. **Basic Mocking**
   - Creating mock objects
   - Setting return values
   - Verifying calls

2. **Advanced Mocking**
   - Mock side effects
   - Mock exceptions
   - Mock context managers

3. **Patching**
   - Patching functions and methods
   - Patching classes
   - Patching modules

4. **Real-World Scenarios**
   - API calls
   - Database operations
   - File system operations
   - External services

## 🚀 Step-by-Step Guide

### Step 1: Basic Mock Objects

Create simple mock objects with predefined behavior:

```python
import pytest
from unittest.mock import Mock

def test_basic_mock():
    # Create a mock object
    mock_obj = Mock()
    
    # Set return value
    mock_obj.some_method.return_value = "Hello, World!"
    
    # Call the method
    result = mock_obj.some_method()
    
    # Verify the result
    assert result == "Hello, World!"
    
    # Verify the method was called
    mock_obj.some_method.assert_called_once()
```

### Step 2: Mock with Parameters

Test functions that depend on external objects:

```python
def test_mock_with_parameters():
    # Create a mock calculator
    calculator = Mock()
    calculator.add.return_value = 5
    
    # Test our function that uses the calculator
    result = perform_calculation(calculator, 2, 3)
    
    # Verify the calculator was used correctly
    calculator.add.assert_called_once_with(2, 3)
    assert result == 5
```

### Step 3: Mock Side Effects

Simulate different behaviors or exceptions:

```python
def test_mock_side_effects():
    mock_service = Mock()
    
    # Simulate different return values
    mock_service.get_data.side_effect = [1, 2, 3, ValueError("No data")]
    
    # First three calls return values
    assert mock_service.get_data() == 1
    assert mock_service.get_data() == 2
    assert mock_service.get_data() == 3
    
    # Fourth call raises an exception
    with pytest.raises(ValueError):
        mock_service.get_data()
```

### Step 4: Patching Functions

Replace real functions with mocks:

```python
from unittest.mock import patch

def test_patch_function():
    with patch('module.function_to_patch') as mock_func:
        mock_func.return_value = "mocked result"
        
        # Call the function that uses the patched function
        result = some_function()
        
        # Verify the patch worked
        assert result == "mocked result"
        mock_func.assert_called_once()
```

## 📁 File Structure

```
04_mocking/
├── README.md
├── test_basic_mocking.py
├── test_advanced_mocking.py
├── test_patching.py
├── test_api_mocking.py
├── test_database_mocking.py
├── test_file_mocking.py
├── conftest.py
├── sample_module.py
└── external_services.py
```

## 🎯 Key Concepts

### 1. Mock Objects
- Replace real objects with controlled substitutes
- Set predefined return values and behaviors
- Track method calls and parameters

### 2. Patching
- Temporarily replace functions, methods, or classes
- Control external dependencies
- Isolate units under test

### 3. Side Effects
- Simulate different behaviors
- Raise exceptions
- Return different values on subsequent calls

### 4. Verification
- Check if methods were called
- Verify call parameters
- Ensure correct interaction patterns

## 🔧 Advanced Patterns

### Mock Context Managers
```python
def test_mock_context_manager():
    with patch('builtins.open', mock_open(read_data='test content')):
        with open('test.txt') as f:
            content = f.read()
        assert content == 'test content'
```

### Mock Decorators
```python
@patch('module.external_function')
def test_with_decorator(mock_func):
    mock_func.return_value = "mocked"
    result = function_under_test()
    assert result == "mocked"
```

### Mock Properties
```python
def test_mock_property():
    mock_obj = Mock()
    type(mock_obj).property_name = PropertyMock(return_value="mocked_value")
    
    assert mock_obj.property_name == "mocked_value"
```

### Mock Async Functions
```python
@pytest.mark.asyncio
async def test_mock_async():
    with patch('module.async_function') as mock_async:
        mock_async.return_value = "async_result"
        
        result = await some_async_function()
        assert result == "async_result"
```

## 📊 Best Practices

### 1. Mock at the Right Level
- Mock at the boundary of your system
- Don't over-mock internal implementation details
- Focus on external dependencies

### 2. Use Descriptive Names
- Name mocks clearly to indicate their purpose
- Use meaningful return values
- Document complex mock setups

### 3. Verify Interactions
- Always verify that mocks were called correctly
- Check call parameters and counts
- Ensure proper cleanup

### 4. Keep Tests Focused
- Mock only what's necessary
- Avoid complex mock hierarchies
- Make tests readable and maintainable

## 🎓 Exercises

1. Create mocks for a simple calculator service
2. Mock API calls and test response handling
3. Patch file operations and test file processing
4. Mock database connections and test data access
5. Create mocks for external service integrations

## 📚 Real-World Examples

### API Service Mocking
```python
def test_api_service():
    with patch('requests.get') as mock_get:
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Test the service
        service = APIService()
        result = service.fetch_data("https://api.example.com/data")
        
        # Verify the result
        assert result == {"data": "test"}
        mock_get.assert_called_once_with("https://api.example.com/data")
```

### Database Mocking
```python
def test_database_operations():
    with patch('sqlite3.connect') as mock_connect:
        # Setup mock database
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [{"id": 1, "name": "Alice"}]
        
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        # Test database operations
        db = Database()
        users = db.get_users()
        
        # Verify the result
        assert users == [{"id": 1, "name": "Alice"}]
        mock_cursor.execute.assert_called_once()
```

### File System Mocking
```python
def test_file_operations():
    with patch('builtins.open', mock_open(read_data='file content')):
        with patch('os.path.exists', return_value=True):
            # Test file reading
            file_processor = FileProcessor()
            content = file_processor.read_file('test.txt')
            
            # Verify the result
            assert content == 'file content'
```

### External Service Mocking
```python
def test_external_service():
    with patch('external_service.ExternalAPI') as mock_api:
        # Setup mock service
        mock_instance = mock_api.return_value
        mock_instance.get_data.return_value = {"status": "success"}
        mock_instance.process_data.return_value = "processed"
        
        # Test service integration
        service = ServiceIntegration()
        result = service.process_external_data()
        
        # Verify interactions
        assert result == "processed"
        mock_instance.get_data.assert_called_once()
        mock_instance.process_data.assert_called_once()
```

## 📚 Next Steps

After completing this section, you should:
- Understand how to create and use mock objects
- Know how to patch functions and methods
- Be able to simulate different behaviors and exceptions
- Understand when and how to use mocking effectively
- Be familiar with real-world mocking scenarios

Proceed to the next section: **05_database_testing/** to learn about database testing. 