"""
Tests for the calculator module.
"""
import pytest
from calculator import Calculator, validate_number, calculate_average, is_prime, fibonacci


class TestCalculator:
    """Test cases for the Calculator class."""
    
    def test_calculator_initialization(self):
        """Test calculator initialization."""
        calc = Calculator()
        assert calc.history == []
    
    def test_add_positive_numbers(self):
        """Test addition with positive numbers."""
        calc = Calculator()
        result = calc.add(5, 3)
        assert result == 8
        assert calc.history == ["5 + 3 = 8"]
    
    def test_add_negative_numbers(self):
        """Test addition with negative numbers."""
        calc = Calculator()
        result = calc.add(-5, -3)
        assert result == -8
        assert calc.history == ["-5 + -3 = -8"]
    
    def test_add_zero(self):
        """Test addition with zero."""
        calc = Calculator()
        result = calc.add(5, 0)
        assert result == 5
        assert calc.history == ["5 + 0 = 5"]
    
    def test_subtract_positive_numbers(self):
        """Test subtraction with positive numbers."""
        calc = Calculator()
        result = calc.subtract(10, 4)
        assert result == 6
        assert calc.history == ["10 - 4 = 6"]
    
    def test_subtract_negative_result(self):
        """Test subtraction that results in negative number."""
        calc = Calculator()
        result = calc.subtract(3, 8)
        assert result == -5
        assert calc.history == ["3 - 8 = -5"]
    
    def test_multiply_positive_numbers(self):
        """Test multiplication with positive numbers."""
        calc = Calculator()
        result = calc.multiply(6, 7)
        assert result == 42
        assert calc.history == ["6 * 7 = 42"]
    
    def test_multiply_by_zero(self):
        """Test multiplication by zero."""
        calc = Calculator()
        result = calc.multiply(5, 0)
        assert result == 0
        assert calc.history == ["5 * 0 = 0"]
    
    def test_divide_positive_numbers(self):
        """Test division with positive numbers."""
        calc = Calculator()
        result = calc.divide(10, 2)
        assert result == 5.0
        assert calc.history == ["10 / 2 = 5.0"]
    
    def test_divide_by_zero(self):
        """Test division by zero raises exception."""
        calc = Calculator()
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calc.divide(10, 0)
        assert calc.history == []  # No history entry for failed operation
    
    def test_power_positive_numbers(self):
        """Test power operation with positive numbers."""
        calc = Calculator()
        result = calc.power(2, 3)
        assert result == 8
        assert calc.history == ["2 ^ 3 = 8"]
    
    def test_power_zero_exponent(self):
        """Test power operation with zero exponent."""
        calc = Calculator()
        result = calc.power(5, 0)
        assert result == 1
        assert calc.history == ["5 ^ 0 = 1"]
    
    def test_get_history(self):
        """Test getting calculation history."""
        calc = Calculator()
        calc.add(1, 2)
        calc.subtract(5, 3)
        history = calc.get_history()
        expected = ["1 + 2 = 3", "5 - 3 = 2"]
        assert history == expected
        # Test that history is a copy, not a reference
        history.append("test")
        assert calc.history != history
    
    def test_clear_history(self):
        """Test clearing calculation history."""
        calc = Calculator()
        calc.add(1, 2)
        calc.subtract(5, 3)
        assert len(calc.history) == 2
        calc.clear_history()
        assert calc.history == []


class TestValidateNumber:
    """Test cases for the validate_number function."""
    
    def test_valid_integer(self):
        """Test validation with valid integer."""
        result = validate_number(42)
        assert result == 42
    
    def test_valid_float(self):
        """Test validation with valid float."""
        result = validate_number(3.14)
        assert result == 3.14
    
    def test_invalid_string(self):
        """Test validation with invalid string."""
        with pytest.raises(TypeError, match="Value must be a number"):
            validate_number("42")
    
    def test_invalid_list(self):
        """Test validation with invalid list."""
        with pytest.raises(TypeError, match="Value must be a number"):
            validate_number([1, 2, 3])


class TestCalculateAverage:
    """Test cases for the calculate_average function."""
    
    def test_average_positive_numbers(self):
        """Test average calculation with positive numbers."""
        result = calculate_average([1, 2, 3, 4, 5])
        assert result == 3.0
    
    def test_average_mixed_numbers(self):
        """Test average calculation with mixed positive and negative numbers."""
        result = calculate_average([1, -2, 3, -4, 5])
        assert result == 0.6
    
    def test_average_single_number(self):
        """Test average calculation with single number."""
        result = calculate_average([42])
        assert result == 42.0
    
    def test_average_empty_list(self):
        """Test average calculation with empty list raises exception."""
        with pytest.raises(ValueError, match="Cannot calculate average of empty list"):
            calculate_average([])
    
    def test_average_with_invalid_input(self):
        """Test average calculation with invalid input raises exception."""
        with pytest.raises(TypeError, match="Value must be a number"):
            calculate_average([1, 2, "3", 4])


class TestIsPrime:
    """Test cases for the is_prime function."""
    
    @pytest.mark.parametrize("number,expected", [
        (2, True),
        (3, True),
        (5, True),
        (7, True),
        (11, True),
        (13, True),
        (17, True),
        (19, True),
        (23, True),
        (29, True),
    ])
    def test_prime_numbers(self, number, expected):
        """Test that known prime numbers return True."""
        assert is_prime(number) == expected
    
    @pytest.mark.parametrize("number", [0, 1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20])
    def test_non_prime_numbers(self, number):
        """Test that known non-prime numbers return False."""
        assert is_prime(number) == False
    
    def test_negative_numbers(self):
        """Test that negative numbers return False."""
        assert is_prime(-1) == False
        assert is_prime(-5) == False


class TestFibonacci:
    """Test cases for the fibonacci function."""
    
    @pytest.mark.parametrize("n,expected", [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (6, 8),
        (7, 13),
        (8, 21),
        (9, 34),
        (10, 55),
    ])
    def test_fibonacci_numbers(self, n, expected):
        """Test that fibonacci function returns correct values."""
        assert fibonacci(n) == expected
    
    def test_negative_numbers(self):
        """Test that negative numbers raise exception."""
        with pytest.raises(ValueError, match="Fibonacci is not defined for negative numbers"):
            fibonacci(-1)
        with pytest.raises(ValueError, match="Fibonacci is not defined for negative numbers"):
            fibonacci(-5)
    
    def test_large_numbers(self):
        """Test fibonacci with larger numbers."""
        assert fibonacci(20) == 6765
        assert fibonacci(25) == 75025 