# Basic Concepts - Pytest Fundamentals

This section covers the fundamental concepts of pytest, including installation, basic test functions, assertions, and test discovery.

## 📋 What You'll Learn

1. **Installation and Setup**
   - Installing pytest
   - Basic configuration
   - Running your first test

2. **Test Functions**
   - Naming conventions
   - Test function structure
   - Basic test examples

3. **Assertions**
   - Built-in assert statement
   - Common assertion patterns
   - Assertion messages

4. **Test Discovery**
   - How pytest finds tests
   - File naming conventions
   - Directory structure

## 🚀 Step-by-Step Guide

### Step 1: Installation

```bash
# Install pytest
pip install pytest

# Verify installation
pytest --version
```

### Step 2: Your First Test

Create a file named `test_basic.py`:

```python
def test_simple():
    assert 1 + 1 == 2

def test_string():
    assert "hello" + " world" == "hello world"

def test_list():
    assert [1, 2, 3] + [4, 5] == [1, 2, 3, 4, 5]
```

### Step 3: Running Tests

```bash
# Run all tests in current directory
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test_basic.py

# Run specific test function
pytest test_basic.py::test_simple
```

### Step 4: Understanding Test Discovery

Pytest automatically discovers tests based on these rules:
- Files named `test_*.py` or `*_test.py`
- Functions named `test_*`
- Classes named `Test*` with methods named `test_*`

### Step 5: Basic Assertions

```python
def test_assertions():
    # Basic equality
    assert 5 == 5
    
    # Inequality
    assert 5 != 6
    
    # Truthiness
    assert True
    assert not False
    
    # Membership
    assert 1 in [1, 2, 3]
    assert "hello" in "hello world"
    
    # Type checking
    assert isinstance("hello", str)
    assert isinstance(42, int)
```

## 📁 File Structure

```
01_basic_concepts/
├── README.md
├── test_basic.py
├── test_assertions.py
├── test_discovery.py
├── calculator.py
└── test_calculator.py
```

## 🎯 Key Concepts

### 1. Test Function Naming
- Must start with `test_`
- Should be descriptive
- Use snake_case

### 2. Assertions
- Use Python's built-in `assert` statement
- pytest provides detailed failure information
- Can include custom messages: `assert x == y, "Custom message"`

### 3. Test Discovery
- Automatic discovery of test files and functions
- Configurable through `pytest.ini` or `pyproject.toml`
- Can be customized with markers and configuration

## 🔧 Configuration

Create `pytest.ini` for basic configuration:

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

## 📊 Running Tests

### Basic Commands
```bash
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest -s                 # Show print statements
pytest -k "test_name"     # Run tests matching pattern
pytest -x                 # Stop on first failure
pytest --maxfail=2        # Stop after 2 failures
```

### Output Options
```bash
pytest --tb=short         # Short traceback
pytest --tb=long          # Long traceback
pytest --tb=no            # No traceback
pytest -q                 # Quiet mode
```

## 🎓 Exercises

1. Create a test file with 5 different test functions
2. Test various data types (strings, lists, dictionaries)
3. Use different assertion types
4. Run tests with different verbosity levels
5. Experiment with test discovery by renaming files

## 📚 Next Steps

After completing this section, you should:
- Understand how to write basic test functions
- Know how to use assertions effectively
- Be familiar with test discovery
- Be able to run tests with different options

Proceed to the next section: **02_fixtures/** to learn about test fixtures and setup/teardown. 