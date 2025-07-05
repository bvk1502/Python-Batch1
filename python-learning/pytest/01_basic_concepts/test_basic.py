"""
Basic pytest examples demonstrating fundamental concepts.
"""
import pytest

def test_simple():
    """Basic test with simple assertion."""
    assert 1 + 1 == 2
    
def test_simple_execution():
    print("Hello, World!")
    assert 1 + 2 == 2


def test_string():
    """Test string operations."""
    assert "hello" + " world" == "hello world"
    assert len("python") == 6
    assert "test" in "this is a test string"


def test_list():
    """Test list operations."""
    numbers = [1, 2, 3, 4, 5]
    assert len(numbers) == 5
    assert 3 in numbers
    assert numbers[0] == 1
    assert numbers[-1] == 5


def test_dictionary():
    """Test dictionary operations."""
    person = {"name": "John", "age": 30, "city": "New York"}
    assert person["name"] == "John"
    assert "age" in person
    assert len(person) == 3


def test_boolean():
    """Test boolean operations."""
    assert True
    assert not False
    assert 5 > 3
    assert 10 >= 10
    assert 7 < 15


def test_type_checking():
    """Test type checking."""
    assert isinstance("hello", str)
    assert isinstance(42, int)
    assert isinstance(3.14, float)
    assert isinstance([1, 2, 3], list)
    assert isinstance({"key": "value"}, dict)


def test_exception():
    """Test that an exception is raised."""
    import pytest
    
    with pytest.raises(ValueError):
        int("not a number")
    
    with pytest.raises(IndexError):
        empty_list = []
        empty_list[0]


def test_exception_message():
    """Test exception with specific message."""
    import pytest
    
    with pytest.raises(ValueError, match="invalid literal"):
        int("abc")


def test_approximate():
    """Test floating point comparisons."""
    assert 0.1 + 0.2 == pytest.approx(0.3)
    assert 3.14159 == pytest.approx(3.14, rel=1e-2)


def test_custom_message():
    """Test assertions with custom messages."""
    x = 5
    y = 10
    assert x < y, f"Expected {x} to be less than {y}"
    
    name = "Alice"
    assert len(name) > 3, f"Name '{name}' should be longer than 3 characters" 