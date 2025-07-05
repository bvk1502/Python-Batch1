# Parameterization - Testing Multiple Scenarios

This section covers pytest parameterization, which allows you to run the same test with different inputs, making your tests more comprehensive and reducing code duplication.

## 📋 What You'll Learn

1. **Basic Parameterization**
   - Using `@pytest.mark.parametrize`
   - Simple parameter lists
   - Multiple parameters

2. **Advanced Parameterization**
   - Parameterized fixtures
   - Dynamic parameterization
   - Custom parameterization functions

3. **Complex Scenarios**
   - Testing with different data types
   - Edge cases and boundary testing
   - Error condition testing

4. **Real-World Applications**
   - API endpoint testing
   - Database query testing
   - File format testing

## 🚀 Step-by-Step Guide

### Step 1: Basic Parameterization

Use `@pytest.mark.parametrize` to test multiple inputs:

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (0, 0),
])
def test_double(input, expected):
    assert input * 2 == expected
```

### Step 2: Multiple Parameters

Test functions with multiple parameters:

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (5, 3, 8),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_addition(a, b, expected):
    assert a + b == expected
```

### Step 3: String Parameters

Test with string inputs:

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
    ("Python", "PYTHON"),
])
def test_uppercase(input, expected):
    assert input.upper() == expected
```

### Step 4: Complex Data Structures

Test with lists, dictionaries, and objects:

```python
@pytest.mark.parametrize("input_list,expected", [
    ([1, 2, 3], 6),
    ([], 0),
    ([5], 5),
    ([1, -1, 0], 0),
])
def test_sum_list(input_list, expected):
    assert sum(input_list) == expected
```

## 📁 File Structure

```
03_parameterization/
├── README.md
├── test_basic_parameterization.py
├── test_advanced_parameterization.py
├── test_complex_scenarios.py
├── test_api_parameterization.py
├── test_database_parameterization.py
├── test_file_parameterization.py
├── conftest.py
├── sample_data.json
└── test_files/
```

## 🎯 Key Concepts

### 1. Parameterization Syntax
```python
@pytest.mark.parametrize("param_name", [value1, value2, value3])
def test_function(param_name):
    # Test logic here
```

### 2. Multiple Parameters
```python
@pytest.mark.parametrize("param1,param2", [
    (value1a, value1b),
    (value2a, value2b),
])
```

### 3. Parameter IDs
```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
], ids=["one_doubled", "two_doubled"])
```

### 4. Conditional Parameterization
```python
@pytest.mark.parametrize("input,expected", [
    pytest.param(1, 2, id="positive"),
    pytest.param(0, 0, id="zero"),
    pytest.param(-1, -2, id="negative", marks=pytest.mark.xfail),
])
```

## 🔧 Advanced Patterns

### Parametrized Fixtures
```python
@pytest.fixture(params=[1, 2, 3])
def number_fixture(request):
    return request.param

def test_with_parametrized_fixture(number_fixture):
    assert number_fixture > 0
```

### Dynamic Parameterization
```python
def generate_test_data():
    return [(i, i * 2) for i in range(10)]

@pytest.mark.parametrize("input,expected", generate_test_data())
def test_dynamic_parameterization(input, expected):
    assert input * 2 == expected
```

### Custom Parameterization
```python
def custom_parametrize(func):
    test_cases = [
        (1, "one"),
        (2, "two"),
        (3, "three"),
    ]
    return pytest.mark.parametrize("number,word", test_cases)(func)

@custom_parametrize
def test_number_to_word(number, word):
    # Test logic here
    pass
```

## 📊 Best Practices

### 1. Parameter Naming
- Use descriptive parameter names
- Make test cases self-documenting
- Use meaningful IDs for complex parameters

### 2. Test Data Organization
- Group related test cases
- Use constants for repeated values
- Separate positive and negative test cases

### 3. Edge Cases
- Always test boundary conditions
- Include empty/null values
- Test error conditions

### 4. Performance
- Avoid expensive operations in parameter generation
- Use appropriate fixture scopes
- Consider test execution time

## 🎓 Exercises

1. Create parameterized tests for mathematical operations
2. Test string manipulation functions with various inputs
3. Parameterize tests for list and dictionary operations
4. Create tests for edge cases and error conditions
5. Build parameterized tests for a simple calculator

## 📚 Real-World Examples

### API Testing
```python
@pytest.mark.parametrize("endpoint,method,expected_status", [
    ("/users", "GET", 200),
    ("/users", "POST", 201),
    ("/users/1", "GET", 200),
    ("/users/999", "GET", 404),
])
def test_api_endpoints(api_client, endpoint, method, expected_status):
    response = api_client.request(method, endpoint)
    assert response.status_code == expected_status
```

### Database Testing
```python
@pytest.mark.parametrize("user_data,expected_result", [
    ({"name": "Alice", "age": 25}, True),
    ({"name": "Bob", "age": 17}, False),
    ({"name": "", "age": 30}, False),
    ({"name": "Charlie", "age": -5}, False),
])
def test_user_validation(database, user_data, expected_result):
    result = database.validate_user(user_data)
    assert result == expected_result
```

### File Format Testing
```python
@pytest.mark.parametrize("file_format,content,expected", [
    ("json", '{"key": "value"}', True),
    ("json", '{"key": value}', False),
    ("csv", "name,age\nJohn,30", True),
    ("csv", "name,age\nJohn", False),
])
def test_file_validation(file_format, content, expected):
    result = validate_file_format(file_format, content)
    assert result == expected
```

## 📚 Next Steps

After completing this section, you should:
- Understand how to use `@pytest.mark.parametrize`
- Be able to create parameterized tests with multiple parameters
- Know how to use parameterized fixtures
- Understand advanced parameterization patterns
- Be familiar with real-world parameterization scenarios

Proceed to the next section: **04_mocking/** to learn about mocking and patching. 