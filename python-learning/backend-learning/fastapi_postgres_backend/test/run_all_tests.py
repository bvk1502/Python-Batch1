"""
Consolidated Test Runner for FastAPI Backend
This module runs all test classes in a structured manner following TDD principles.
Optimized for uv package manager.
"""

import pytest
import sys
import os
import subprocess
from typing import List, Dict, Any

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSuiteRunner:
    """Consolidated test suite runner for all test classes."""
    
    def __init__(self):
        self.test_results: Dict[str, Any] = {}
        self.test_classes = [
            "TestUserCreate",
            "TestUserRead", 
            "TestUserUpdate",
            "TestUserDelete",
            "TestUserValidation",
            "TestUserIntegration",
            "TestUserErrorHandling"
        ]
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all test classes and return results."""
        print("🚀 Starting Comprehensive Test Suite with uv...")
        print("=" * 60)
        
        # Run tests using uv and pytest
        try:
            result = subprocess.run([
                "uv", "run", "pytest",
                "test/test_users.py",
                "-v",
                "--tb=short",
                "--strict-markers",
                "--disable-warnings"
            ], capture_output=True, text=True, check=False)
            
            exit_code = result.returncode
            
            # Print output
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
                
        except FileNotFoundError:
            print("❌ Error: 'uv' command not found. Please install uv first.")
            print("Install with: curl -LsSf https://astral.sh/uv/install.sh | sh")
            exit_code = 1
        
        self.test_results = {
            "exit_code": exit_code,
            "status": "PASSED" if exit_code == 0 else "FAILED",
            "test_classes": self.test_classes
        }
        
        return self.test_results
    
    def run_specific_test_class(self, test_class: str) -> Dict[str, Any]:
        """Run a specific test class."""
        if test_class not in self.test_classes:
            raise ValueError(f"Test class '{test_class}' not found")
        
        print(f"🧪 Running {test_class} with uv...")
        print("=" * 40)
        
        try:
            result = subprocess.run([
                "uv", "run", "pytest",
                f"test/test_users.py::{test_class}",
                "-v",
                "--tb=short"
            ], capture_output=True, text=True, check=False)
            
            exit_code = result.returncode
            
            # Print output
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
                
        except FileNotFoundError:
            print("❌ Error: 'uv' command not found. Please install uv first.")
            exit_code = 1
        
        return {
            "test_class": test_class,
            "exit_code": exit_code,
            "status": "PASSED" if exit_code == 0 else "FAILED"
        }
    
    def run_tdd_cycle(self) -> Dict[str, Any]:
        """Run tests in TDD cycle order."""
        print("🔄 Running TDD Cycle Tests with uv...")
        print("=" * 50)
        
        tdd_order = [
            "TestUserValidation",  # Start with validation
            "TestUserCreate",      # Then creation
            "TestUserRead",        # Then reading
            "TestUserUpdate",      # Then updating
            "TestUserDelete",      # Then deletion
            "TestUserIntegration", # Then integration
            "TestUserErrorHandling" # Finally error handling
        ]
        
        results = {}
        for test_class in tdd_order:
            result = self.run_specific_test_class(test_class)
            results[test_class] = result
            
            if result["status"] == "FAILED":
                print(f"❌ {test_class} failed. Stopping TDD cycle.")
                break
        
        return results
    
    def run_with_coverage(self) -> Dict[str, Any]:
        """Run tests with coverage reporting."""
        print(" Running tests with coverage...")
        print("=" * 50)
        
        try:
            result = subprocess.run([
                "uv", "run", "pytest",
                "test/test_users.py",
                "-v",
                "--cov=app",
                "--cov-report=term-missing",
                "--cov-report=html:htmlcov"
            ], capture_output=True, text=True, check=False)
            
            exit_code = result.returncode
            
            # Print output
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
                
        except FileNotFoundError:
            print("❌ Error: 'uv' command not found. Please install uv first.")
            exit_code = 1
        
        return {
            "exit_code": exit_code,
            "status": "PASSED" if exit_code == 0 else "FAILED",
            "coverage": True
        }


def main():
    """Main function to run the test suite."""
    runner = TestSuiteRunner()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--tdd":
            results = runner.run_tdd_cycle()
        elif sys.argv[1] == "--class" and len(sys.argv) > 2:
            results = runner.run_specific_test_class(sys.argv[2])
        elif sys.argv[1] == "--coverage":
            results = runner.run_with_coverage()
        else:
            print("Usage:")
            print("  uv run python test/run_all_tests.py          # Run all tests")
            print("  uv run python test/run_all_tests.py --tdd    # Run TDD cycle")
            print("  uv run python test/run_all_tests.py --class TestUserCreate  # Run specific class")
            print("  uv run python test/run_all_tests.py --coverage  # Run with coverage")
            return
    else:
        results = runner.run_all_tests()
    
    # Print summary
    print("\n" + "=" * 60)
    print(" TEST SUMMARY")
    print("=" * 60)
    
    if isinstance(results, dict) and "test_classes" in results:
        # All tests result
        print(f"Overall Status: {results['status']}")
        print(f"Exit Code: {results['exit_code']}")
    elif isinstance(results, dict) and "coverage" in results:
        # Coverage result
        print(f"Coverage Status: {results['status']}")
        print(f"Exit Code: {results['exit_code']}")
    else:
        # Specific test result
        for test_class, result in results.items():
            print(f"{test_class}: {result['status']}")
    
    print("=" * 60)


if __name__ == "__main__":
    main() 