#!/usr/bin/env python3
"""
Test runner script for FastAPI PostgreSQL Backend
Usage:
    python test/run_tests.py                    # Run all tests
    python test/run_tests.py --unit             # Run only unit tests
    python test/run_tests.py --integration      # Run only integration tests
    python test/run_tests.py --verbose          # Run with verbose output
    python test/run_tests.py --coverage         # Run with coverage report
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_tests(args):
    """Run pytest with the given arguments."""
    cmd = ["uv", "run", "pytest"]
    
    if args.unit:
        cmd.extend(["-m", "unit"])
    elif args.integration:
        cmd.extend(["-m", "integration"])
    
    if args.verbose:
        cmd.append("-v")
    
    if args.coverage:
        cmd.extend(["--cov=app", "--cov-report=html", "--cov-report=term"])
    
    if args.test_file:
        cmd.append(args.test_file)
    
    # Add test directory
    cmd.append("test/")
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run tests for FastAPI PostgreSQL Backend")
    parser.add_argument("--unit", action="store_true", help="Run only unit tests")
    parser.add_argument("--integration", action="store_true", help="Run only integration tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--test-file", help="Run specific test file")
    
    args = parser.parse_args()
    
    # Check if we're in the right directory
    if not Path("app").exists():
        print("Error: Please run this script from the project root directory")
        sys.exit(1)
    
    exit_code = run_tests(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main() 