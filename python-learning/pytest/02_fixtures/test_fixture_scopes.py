"""
Tests demonstrating different fixture scopes and their behavior.
"""
import pytest


# Track fixture creation to demonstrate scope behavior
_scope_tracker = {
    "function": [],
    "class": [],
    "module": [],
    "session": []
}


@pytest.fixture(scope="function")
def function_scope_fixture():
    """Function-scoped fixture - created for each test function."""
    fixture_id = f"function_{len(_scope_tracker['function']) + 1}"
    _scope_tracker["function"].append(fixture_id)
    print(f"\nCreated function fixture: {fixture_id}")
    yield fixture_id
    print(f"Tearing down function fixture: {fixture_id}")


@pytest.fixture(scope="class")
def class_scope_fixture():
    """Class-scoped fixture - created once per test class."""
    fixture_id = f"class_{len(_scope_tracker['class']) + 1}"
    _scope_tracker["class"].append(fixture_id)
    print(f"\nCreated class fixture: {fixture_id}")
    yield fixture_id
    print(f"Tearing down class fixture: {fixture_id}")


@pytest.fixture(scope="module")
def module_scope_fixture():
    """Module-scoped fixture - created once per test module."""
    fixture_id = f"module_{len(_scope_tracker['module']) + 1}"
    _scope_tracker["module"].append(fixture_id)
    print(f"\nCreated module fixture: {fixture_id}")
    yield fixture_id
    print(f"Tearing down module fixture: {fixture_id}")


@pytest.fixture(scope="session")
def session_scope_fixture():
    """Session-scoped fixture - created once per test session."""
    fixture_id = f"session_{len(_scope_tracker['session']) + 1}"
    _scope_tracker["session"].append(fixture_id)
    print(f"\nCreated session fixture: {fixture_id}")
    yield fixture_id
    print(f"Tearing down session fixture: {fixture_id}")


def test_function_scope_1(function_scope_fixture):
    """First test using function-scoped fixture."""
    assert function_scope_fixture.startswith("function_")
    print(f"Using function fixture: {function_scope_fixture}")


def test_function_scope_2(function_scope_fixture):
    """Second test using function-scoped fixture."""
    assert function_scope_fixture.startswith("function_")
    print(f"Using function fixture: {function_scope_fixture}")


def test_function_scope_3(function_scope_fixture):
    """Third test using function-scoped fixture."""
    assert function_scope_fixture.startswith("function_")
    print(f"Using function fixture: {function_scope_fixture}")


class TestClassScope:
    """Test class to demonstrate class-scoped fixtures."""
    
    def test_class_scope_1(self, class_scope_fixture):
        """First test in class using class-scoped fixture."""
        assert class_scope_fixture.startswith("class_")
        print(f"Using class fixture: {class_scope_fixture}")
    
    def test_class_scope_2(self, class_scope_fixture):
        """Second test in class using class-scoped fixture."""
        assert class_scope_fixture.startswith("class_")
        print(f"Using class fixture: {class_scope_fixture}")
    
    def test_class_scope_3(self, class_scope_fixture):
        """Third test in class using class-scoped fixture."""
        assert class_scope_fixture.startswith("class_")
        print(f"Using class fixture: {class_scope_fixture}")


class TestClassScope2:
    """Another test class to demonstrate class-scoped fixtures."""
    
    def test_class_scope_another_1(self, class_scope_fixture):
        """First test in second class using class-scoped fixture."""
        assert class_scope_fixture.startswith("class_")
        print(f"Using class fixture: {class_scope_fixture}")
    
    def test_class_scope_another_2(self, class_scope_fixture):
        """Second test in second class using class-scoped fixture."""
        assert class_scope_fixture.startswith("class_")
        print(f"Using class fixture: {class_scope_fixture}")


def test_module_scope_1(module_scope_fixture):
    """First test using module-scoped fixture."""
    assert module_scope_fixture.startswith("module_")
    print(f"Using module fixture: {module_scope_fixture}")


def test_module_scope_2(module_scope_fixture):
    """Second test using module-scoped fixture."""
    assert module_scope_fixture.startswith("module_")
    print(f"Using module fixture: {module_scope_fixture}")


def test_session_scope_1(session_scope_fixture):
    """First test using session-scoped fixture."""
    assert session_scope_fixture.startswith("session_")
    print(f"Using session fixture: {session_scope_fixture}")


def test_session_scope_2(session_scope_fixture):
    """Second test using session-scoped fixture."""
    assert session_scope_fixture.startswith("session_")
    print(f"Using session fixture: {session_scope_fixture}")


def test_all_scopes_together(
    function_scope_fixture,
    class_scope_fixture,
    module_scope_fixture,
    session_scope_fixture
):
    """Test using all scope types together."""
    assert function_scope_fixture.startswith("function_")
    assert class_scope_fixture.startswith("class_")
    assert module_scope_fixture.startswith("module_")
    assert session_scope_fixture.startswith("session_")
    
    print(f"Using all fixtures:")
    print(f"  Function: {function_scope_fixture}")
    print(f"  Class: {class_scope_fixture}")
    print(f"  Module: {module_scope_fixture}")
    print(f"  Session: {session_scope_fixture}")


def test_scope_tracking():
    """Test to verify fixture creation tracking."""
    # This test runs at the end to show the fixture creation pattern
    print(f"\nFixture creation summary:")
    print(f"Function fixtures created: {len(_scope_tracker['function'])}")
    print(f"Class fixtures created: {len(_scope_tracker['class'])}")
    print(f"Module fixtures created: {len(_scope_tracker['module'])}")
    print(f"Session fixtures created: {len(_scope_tracker['session'])}")
    
    # Verify that function fixtures are created for each test
    assert len(_scope_tracker['function']) >= 3
    
    # Verify that class fixtures are created for each class
    assert len(_scope_tracker['class']) >= 2
    
    # Verify that module fixtures are created once per module
    assert len(_scope_tracker['module']) == 1
    
    # Verify that session fixtures are created once per session
    assert len(_scope_tracker['session']) == 1


# Fixture to demonstrate resource management with different scopes
@pytest.fixture(scope="function")
def temp_file_function():
    """Function-scoped temporary file fixture."""
    import tempfile
    import os
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(f"Function scope file content\n")
        temp_path = f.name
    
    print(f"Created function-scoped temp file: {temp_path}")
    yield temp_path
    
    # Cleanup
    try:
        os.unlink(temp_path)
        print(f"Deleted function-scoped temp file: {temp_path}")
    except FileNotFoundError:
        pass


@pytest.fixture(scope="module")
def temp_file_module():
    """Module-scoped temporary file fixture."""
    import tempfile
    import os
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(f"Module scope file content\n")
        temp_path = f.name
    
    print(f"Created module-scoped temp file: {temp_path}")
    yield temp_path
    
    # Cleanup
    try:
        os.unlink(temp_path)
        print(f"Deleted module-scoped temp file: {temp_path}")
    except FileNotFoundError:
        pass


def test_temp_file_function_1(temp_file_function):
    """Test using function-scoped temp file."""
    import os
    assert os.path.exists(temp_file_function)
    with open(temp_file_function, 'r') as f:
        content = f.read()
    assert "Function scope" in content


def test_temp_file_function_2(temp_file_function):
    """Another test using function-scoped temp file."""
    import os
    assert os.path.exists(temp_file_function)
    with open(temp_file_function, 'r') as f:
        content = f.read()
    assert "Function scope" in content


def test_temp_file_module_1(temp_file_module):
    """Test using module-scoped temp file."""
    import os
    assert os.path.exists(temp_file_module)
    with open(temp_file_module, 'r') as f:
        content = f.read()
    assert "Module scope" in content


def test_temp_file_module_2(temp_file_module):
    """Another test using module-scoped temp file."""
    import os
    assert os.path.exists(temp_file_module)
    with open(temp_file_module, 'r') as f:
        content = f.read()
    assert "Module scope" in content 