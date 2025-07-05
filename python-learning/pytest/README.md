# Pytest Tutorial - Complete Guide

This tutorial provides a comprehensive introduction to pytest, covering from basic concepts to advanced testing scenarios.

## 📚 Table of Contents

1. **Basic Concepts** (`01_basic_concepts/`)
   - Installation and setup
   - Simple test functions
   - Assertions
   - Test discovery

2. **Fixtures** (`02_fixtures/`)
   - Basic fixtures
   - Fixture scope
   - Fixture dependencies
   - Parametrized fixtures

3. **Parameterization** (`03_parameterization/`)
   - Basic parameterization
   - Multiple parameters
   - Dynamic parameterization
   - Custom parameterization

4. **Mocking and Patching** (`04_mocking/`)
   - Mock objects
   - Patching functions and methods
   - Mock side effects
   - Mock return values

5. **Database Testing** (`05_database_testing/`)
   - SQLite testing
   - PostgreSQL testing
   - Database fixtures
   - Transaction management

6. **API Testing** (`06_api_testing/`)
   - FastAPI testing
   - HTTP client testing
   - Response validation
   - Authentication testing

7. **Advanced Patterns** (`07_advanced_patterns/`)
   - Test classes
   - Custom markers
   - Plugins
   - Hooks and conftest

8. **Performance Testing** (`08_performance_testing/`)
   - Benchmarking
   - Load testing
   - Memory profiling
   - Performance assertions

9. **Integration Testing** (`09_integration_testing/`)
   - End-to-end testing
   - External service testing
   - Docker integration
   - CI/CD integration

10. **Best Practices** (`10_best_practices/`)
    - Test organization
    - Naming conventions
    - Test data management
    - Documentation

## 🚀 Quick Start

```bash
# Install pytest
pip install pytest

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=your_module

# Run specific test file
pytest test_file.py

# Run specific test function
pytest test_file.py::test_function
```

## 📋 Prerequisites

- Python 3.7+
- pip (Python package installer)
- Basic understanding of Python

## 🛠️ Installation

```bash
# Create virtual environment
python -m venv pytest_env

# Activate virtual environment
# On Windows:
pytest_env\Scripts\activate
# On macOS/Linux:
source pytest_env/bin/activate

# Install required packages
pip install -r requirements.txt
```

## 📖 How to Use This Tutorial

1. Start with `01_basic_concepts/` to understand the fundamentals
2. Progress through each section in order
3. Read the README.md file in each section for detailed explanations
4. Run the example tests to see them in action
5. Experiment with the code examples

## 🎯 Learning Objectives

By the end of this tutorial, you will be able to:

- Write effective test cases using pytest
- Use fixtures for test setup and teardown
- Implement parameterized tests
- Mock external dependencies
- Test database operations
- Test API endpoints
- Apply advanced pytest patterns
- Follow testing best practices

## 📝 Contributing

Feel free to contribute by:
- Adding new test cases
- Improving documentation
- Fixing bugs
- Suggesting new topics

## 📄 License

This tutorial is open source and available under the MIT License. 