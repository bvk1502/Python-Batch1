"""
Tests demonstrating basic fixture usage.
"""
import pytest


def test_with_sample_numbers(sample_numbers):
    """Test using the sample_numbers fixture."""
    assert len(sample_numbers) == 5
    assert sum(sample_numbers) == 15
    assert sample_numbers[0] == 1
    assert sample_numbers[-1] == 5


def test_with_sample_strings(sample_strings):
    """Test using the sample_strings fixture."""
    assert len(sample_strings) == 5
    assert "apple" in sample_strings
    assert all(isinstance(s, str) for s in sample_strings)
    assert sample_strings[0] == "apple"


def test_with_sample_dict(sample_dict):
    """Test using the sample_dict fixture."""
    assert sample_dict["name"] == "John Doe"
    assert sample_dict["age"] == 30
    assert len(sample_dict["skills"]) == 3
    assert "Python" in sample_dict["skills"]


def test_with_sample_user(sample_user):
    """Test using the sample_user fixture."""
    assert sample_user.name == "Alice"
    assert sample_user.age == 25
    assert sample_user.email == "alice@example.com"
    assert sample_user.get_info() == "Alice (25) - alice@example.com"


def test_fixture_isolation():
    """Test that fixtures are isolated between tests."""
    # This test doesn't use any fixtures, but demonstrates that
    # fixtures from other tests don't interfere
    assert True


def test_multiple_fixtures(sample_numbers, sample_strings, sample_dict):
    """Test using multiple fixtures in a single test."""
    # Test sample_numbers
    assert len(sample_numbers) == 5
    
    # Test sample_strings
    assert len(sample_strings) == 5
    
    # Test sample_dict
    assert sample_dict["name"] == "John Doe"
    
    # Test interaction between fixtures
    assert len(sample_numbers) == len(sample_strings)
    assert sample_dict["age"] > len(sample_numbers)


class TestFixtureInClasses:
    """Test class demonstrating fixture usage in test classes."""
    
    def test_fixture_in_class_method(self, sample_numbers):
        """Test that fixtures work in class methods."""
        assert len(sample_numbers) == 5
        assert sum(sample_numbers) == 15
    
    def test_another_fixture_in_class(self, sample_user):
        """Test another fixture in the same class."""
        assert sample_user.name == "Alice"
        assert sample_user.age == 25


def test_fixture_scope_demonstration(session_data, module_data, class_data):
    """Test demonstrating different fixture scopes."""
    # These fixtures have different scopes and will be created
    # at different times during the test session
    assert session_data["session_id"] == "test_session_123"
    assert module_data["module_name"] == "test_module"
    assert class_data["class_name"] == "TestClass"


def test_fixture_with_complex_data(complex_data_structure):
    """Test using a fixture with complex nested data."""
    company = complex_data_structure["company"]
    
    # Test company structure
    assert company["name"] == "TechCorp"
    assert len(company["employees"]) == 2
    
    # Test employee data
    alice = company["employees"][0]
    assert alice["name"] == "Alice"
    assert alice["department"] == "Engineering"
    assert "Python" in alice["skills"]
    
    # Test department data
    engineering_dept = company["departments"]["Engineering"]
    assert engineering_dept["head"] == "Alice"
    assert engineering_dept["budget"] == 100000


def test_fixture_factory_basic(user_factory):
    """Test using the user factory fixture."""
    # Create a user with default values
    user = user_factory()
    assert user.name == "John"
    assert user.age == 30
    assert user.role == "user"
    assert user.is_adult()
    
    # Create a user with custom values
    custom_user = user_factory(name="Alice", age=25, role="admin")
    assert custom_user.name == "Alice"
    assert custom_user.age == 25
    assert custom_user.role == "admin"
    assert custom_user.get_display_name() == "Alice (admin)"


def test_fixture_factory_multiple_users(user_factory):
    """Test creating multiple users with the factory."""
    users = [
        user_factory(name="Alice", age=25),
        user_factory(name="Bob", age=30),
        user_factory(name="Charlie", age=17, role="guest")
    ]
    
    assert len(users) == 3
    assert users[0].name == "Alice"
    assert users[1].name == "Bob"
    assert users[2].name == "Charlie"
    
    # Test adult check
    assert users[0].is_adult()  # Alice is 25
    assert users[1].is_adult()  # Bob is 30
    assert not users[2].is_adult()  # Charlie is 17 