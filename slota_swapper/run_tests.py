#!/usr/bin/env python3
"""
Test runner script for SlotSwapper backend tests.
Provides different test execution modes and reporting options.
"""
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, description):
    """Run a command and handle output."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Command failed with exit code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False


def run_unit_tests():
    """Run unit tests only."""
    command = [
        "python", "-m", "pytest", 
        "tests/unit/", 
        "-v", 
        "--tb=short",
        "-m", "not slow"
    ]
    return run_command(command, "Unit Tests")


def run_integration_tests():
    """Run integration tests only."""
    command = [
        "python", "-m", "pytest", 
        "tests/integration/", 
        "-v", 
        "--tb=short"
    ]
    return run_command(command, "Integration Tests")


def run_performance_tests():
    """Run performance tests."""
    command = [
        "python", "-m", "pytest", 
        "tests/performance/", 
        "-v", 
        "--tb=short",
        "-m", "slow"
    ]
    return run_command(command, "Performance Tests")


def run_all_tests():
    """Run all tests with coverage."""
    command = [
        "python", "-m", "pytest", 
        "tests/", 
        "-v", 
        "--cov=.", 
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "--cov-fail-under=80"
    ]
    return run_command(command, "All Tests with Coverage")


def run_quick_tests():
    """Run quick tests (unit tests without slow markers)."""
    command = [
        "python", "-m", "pytest", 
        "tests/unit/", 
        "-v", 
        "--tb=line",
        "-m", "not slow",
        "-x"  # Stop on first failure
    ]
    return run_command(command, "Quick Tests")


def run_auth_tests():
    """Run authentication-related tests only."""
    command = [
        "python", "-m", "pytest", 
        "tests/", 
        "-v", 
        "--tb=short",
        "-m", "auth"
    ]
    return run_command(command, "Authentication Tests")


def run_swap_tests():
    """Run swap logic tests only."""
    command = [
        "python", "-m", "pytest", 
        "tests/", 
        "-v", 
        "--tb=short",
        "-m", "swaps"
    ]
    return run_command(command, "Swap Logic Tests")


def run_specific_test(test_path):
    """Run a specific test file or test function."""
    command = [
        "python", "-m", "pytest", 
        test_path, 
        "-v", 
        "--tb=short"
    ]
    return run_command(command, f"Specific Test: {test_path}")


def generate_coverage_report():
    """Generate detailed coverage report."""
    print("\nGenerating coverage report...")
    
    # Run tests with coverage
    command = [
        "python", "-m", "pytest", 
        "tests/", 
        "--cov=.", 
        "--cov-report=html:htmlcov",
        "--cov-report=xml",
        "--cov-report=term"
    ]
    
    success = run_command(command, "Coverage Report Generation")
    
    if success:
        print("\n" + "="*60)
        print("Coverage reports generated:")
        print("- HTML report: htmlcov/index.html")
        print("- XML report: coverage.xml")
        print("="*60)
    
    return success


def lint_code():
    """Run code linting."""
    commands = [
        (["python", "-m", "flake8", ".", "--max-line-length=120"], "Flake8 Linting"),
        (["python", "-m", "black", ".", "--check"], "Black Code Formatting Check"),
        (["python", "-m", "isort", ".", "--check-only"], "Import Sorting Check")
    ]
    
    all_passed = True
    for command, description in commands:
        try:
            success = run_command(command, description)
            if not success:
                all_passed = False
        except FileNotFoundError:
            print(f"Skipping {description} - tool not installed")
    
    return all_passed


def setup_test_environment():
    """Set up test environment."""
    print("Setting up test environment...")
    
    # Install test dependencies
    command = ["pip", "install", "-r", "requirements.txt"]
    success = run_command(command, "Installing Dependencies")
    
    if success:
        print("\nTest environment setup complete!")
    
    return success


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="SlotSwapper Test Runner")
    parser.add_argument(
        "mode", 
        choices=[
            "unit", "integration", "performance", "all", "quick", 
            "auth", "swaps", "coverage", "lint", "setup"
        ],
        help="Test mode to run"
    )
    parser.add_argument(
        "--test", 
        help="Specific test file or function to run (use with any mode)"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Verbose output"
    )
    parser.add_argument(
        "--fail-fast", "-x", 
        action="store_true", 
        help="Stop on first failure"
    )
    
    args = parser.parse_args()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    import os
    os.chdir(script_dir)
    
    print(f"SlotSwapper Test Runner")
    print(f"Working directory: {script_dir}")
    
    # Handle specific test
    if args.test:
        return run_specific_test(args.test)
    
    # Route to appropriate test function
    test_functions = {
        "unit": run_unit_tests,
        "integration": run_integration_tests,
        "performance": run_performance_tests,
        "all": run_all_tests,
        "quick": run_quick_tests,
        "auth": run_auth_tests,
        "swaps": run_swap_tests,
        "coverage": generate_coverage_report,
        "lint": lint_code,
        "setup": setup_test_environment
    }
    
    test_function = test_functions.get(args.mode)
    if test_function:
        success = test_function()
        
        if success:
            print(f"\n✅ {args.mode.title()} tests completed successfully!")
            return 0
        else:
            print(f"\n❌ {args.mode.title()} tests failed!")
            return 1
    else:
        print(f"Unknown test mode: {args.mode}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
