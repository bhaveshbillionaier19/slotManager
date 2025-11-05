# SlotSwapper Backend Testing Guide

This document provides comprehensive information about the testing framework and practices for the SlotSwapper backend API.

## 📋 Table of Contents

- [Overview](#overview)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Categories](#test-categories)
- [Coverage Requirements](#coverage-requirements)
- [Writing Tests](#writing-tests)
- [Performance Testing](#performance-testing)
- [CI/CD Integration](#cicd-integration)

## 🎯 Overview

The SlotSwapper backend uses a comprehensive testing strategy that includes:

- **Unit Tests**: Test individual functions and methods in isolation
- **Integration Tests**: Test API endpoints and database interactions
- **Performance Tests**: Test system performance under load
- **Authentication Tests**: Comprehensive security testing
- **Swap Logic Tests**: Critical business logic validation

### Testing Framework

- **pytest**: Primary testing framework
- **pytest-asyncio**: Async test support
- **pytest-cov**: Coverage reporting
- **Factory Boy**: Test data generation
- **httpx**: HTTP client testing
- **SQLite**: In-memory test database

## 🏗️ Test Structure

```
tests/
├── conftest.py              # Test configuration and fixtures
├── factories.py             # Test data factories
├── unit/                    # Unit tests
│   ├── test_auth.py        # Authentication logic tests
│   └── test_swap_logic.py  # Swap request logic tests
├── integration/             # Integration tests
│   └── test_api_endpoints.py # API endpoint tests
└── performance/             # Performance tests
    └── test_load.py        # Load and performance tests
```

## 🚀 Running Tests

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
python run_tests.py all

# Run quick tests (unit tests only)
python run_tests.py quick

# Run with coverage
python run_tests.py coverage
```

### Test Runner Options

```bash
# Unit tests only
python run_tests.py unit

# Integration tests only
python run_tests.py integration

# Performance tests
python run_tests.py performance

# Authentication tests
python run_tests.py auth

# Swap logic tests
python run_tests.py swaps

# Specific test file
python run_tests.py unit --test tests/unit/test_auth.py

# Specific test function
python run_tests.py unit --test tests/unit/test_auth.py::TestPasswordHashing::test_password_hashing
```

### Direct pytest Commands

```bash
# Run all tests with coverage
pytest tests/ --cov=. --cov-report=html

# Run unit tests only
pytest tests/unit/ -v

# Run tests with specific markers
pytest -m "auth" -v

# Run tests and stop on first failure
pytest tests/ -x

# Run tests in parallel (if pytest-xdist installed)
pytest tests/ -n auto
```

## 📊 Test Categories

### Unit Tests (`tests/unit/`)

#### Authentication Tests (`test_auth.py`)
- Password hashing and verification
- JWT token creation and validation
- User authentication logic
- Token expiration handling
- Security edge cases

**Key Test Classes:**
- `TestPasswordHashing`: Password security
- `TestJWTTokens`: Token management
- `TestUserAuthentication`: Login logic
- `TestTokenVerification`: Token validation

#### Swap Logic Tests (`test_swap_logic.py`)
- Swap request creation validation
- Swap request response handling
- Business rule enforcement
- Edge case handling
- Data integrity checks

**Key Test Classes:**
- `TestSwapRequestCreation`: Request validation
- `TestSwapRequestResponse`: Response handling
- `TestSwapRequestQueries`: Data retrieval
- `TestSwappableEventsQuery`: Event filtering
- `TestSwapLogicEdgeCases`: Edge cases

### Integration Tests (`tests/integration/`)

#### API Endpoint Tests (`test_api_endpoints.py`)
- Complete HTTP request/response cycles
- Authentication flow testing
- CRUD operations validation
- Error handling verification
- Workflow testing

**Key Test Classes:**
- `TestAuthenticationEndpoints`: Auth API
- `TestEventEndpoints`: Event management API
- `TestSwapRequestEndpoints`: Swap API
- `TestCompleteWorkflows`: End-to-end flows
- `TestErrorHandling`: Error scenarios

### Performance Tests (`tests/performance/`)

#### Load Tests (`test_load.py`)
- Database query performance
- API response times
- Concurrent access handling
- Memory usage monitoring
- Scalability testing

**Key Test Classes:**
- `TestDatabasePerformance`: Query optimization
- `TestAPIPerformance`: Response times
- `TestConcurrentAccess`: Concurrency handling
- `TestMemoryUsage`: Resource monitoring

## 📈 Coverage Requirements

### Minimum Coverage Targets

- **Overall Coverage**: 80%
- **Critical Modules**: 90%
  - Authentication (`auth.py`)
  - Swap Logic (`routers/swaps.py`)
  - Models (`models.py`)
- **API Endpoints**: 85%

### Coverage Reports

```bash
# Generate HTML coverage report
python run_tests.py coverage

# View coverage report
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html # Windows
```

### Coverage Configuration

Coverage settings are configured in `pytest.ini`:

```ini
[tool:pytest]
addopts = 
    --cov=.
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-fail-under=80
```

## ✍️ Writing Tests

### Test Naming Conventions

```python
# Test files: test_*.py
# Test classes: Test*
# Test methods: test_*

class TestSwapRequestCreation:
    def test_create_valid_swap_request(self):
        """Test creating a valid swap request."""
        pass
    
    def test_create_swap_request_with_invalid_data(self):
        """Test error handling for invalid data."""
        pass
```

### Using Fixtures

```python
def test_user_authentication(self, db_session, test_user):
    """Use fixtures for test data."""
    # test_user fixture provides a pre-created user
    assert test_user.email == "test@example.com"
```

### Using Factories

```python
from tests.factories import UserFactory, EventFactory

def test_with_factory_data(self, db_session):
    """Use factories for dynamic test data."""
    user = UserFactory(sqlalchemy_session=db_session)
    event = EventFactory(owner=user, sqlalchemy_session=db_session)
    
    assert event.owner_id == user.id
```

### Test Markers

```python
@pytest.mark.unit
def test_password_hashing():
    """Unit test marker."""
    pass

@pytest.mark.integration
def test_api_endpoint():
    """Integration test marker."""
    pass

@pytest.mark.slow
def test_performance():
    """Slow test marker."""
    pass

@pytest.mark.auth
def test_authentication():
    """Authentication test marker."""
    pass

@pytest.mark.swaps
def test_swap_logic():
    """Swap logic test marker."""
    pass
```

### Async Test Support

```python
@pytest.mark.asyncio
async def test_async_function():
    """Test async functions."""
    result = await some_async_function()
    assert result is not None
```

## ⚡ Performance Testing

### Performance Test Guidelines

1. **Mark slow tests**: Use `@pytest.mark.slow`
2. **Set reasonable thresholds**: Based on production requirements
3. **Test realistic scenarios**: Use representative data volumes
4. **Monitor resource usage**: Memory, CPU, database connections

### Performance Assertions

```python
def test_api_response_time(self, client, auth_headers):
    """Test API response time."""
    start_time = time.time()
    response = client.get("/events/", headers=auth_headers)
    response_time = time.time() - start_time
    
    assert response.status_code == 200
    assert response_time < 0.5  # Should respond within 500ms
```

### Load Testing

```python
def test_concurrent_requests(self, client):
    """Test concurrent request handling."""
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(50)]
        results = [future.result() for future in as_completed(futures)]
    
    successful_requests = [r for r in results if r.success]
    assert len(successful_requests) == 50
```

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          python run_tests.py all
      
      - name: Upload coverage
        uses: codecov/codecov-action@v1
        with:
          file: ./coverage.xml
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: tests
        name: Run tests
        entry: python run_tests.py quick
        language: system
        pass_filenames: false
```

## 🐛 Debugging Tests

### Running Tests in Debug Mode

```bash
# Run with verbose output
pytest tests/ -v -s

# Run specific test with debugging
pytest tests/unit/test_auth.py::TestPasswordHashing::test_password_hashing -v -s

# Run with pdb debugger
pytest tests/ --pdb

# Run with coverage and keep test database
pytest tests/ --cov=. --keep-db
```

### Common Issues and Solutions

1. **Database conflicts**: Use separate test database
2. **Async test issues**: Ensure proper async/await usage
3. **Factory conflicts**: Reset sequences between tests
4. **Memory leaks**: Monitor resource usage in performance tests

## 📝 Test Documentation

### Documenting Test Cases

```python
def test_swap_request_validation(self):
    """
    Test swap request validation logic.
    
    This test verifies that:
    1. Valid swap requests are accepted
    2. Invalid requests are rejected with appropriate errors
    3. Business rules are enforced correctly
    
    Covers:
    - Event ownership validation
    - Event status requirements
    - Time conflict checking
    """
    pass
```

### Test Coverage Reports

Coverage reports help identify untested code:

1. **Line coverage**: Which lines are executed
2. **Branch coverage**: Which code paths are taken
3. **Function coverage**: Which functions are called

## 🎯 Best Practices

### Test Organization

1. **One concept per test**: Each test should verify one specific behavior
2. **Descriptive names**: Test names should clearly describe what is being tested
3. **Arrange-Act-Assert**: Structure tests with clear setup, execution, and verification
4. **Independent tests**: Tests should not depend on each other

### Test Data Management

1. **Use factories**: Generate test data dynamically
2. **Minimal fixtures**: Create only the data needed for each test
3. **Clean state**: Ensure tests start with a clean database state
4. **Realistic data**: Use data that resembles production scenarios

### Performance Considerations

1. **Fast unit tests**: Keep unit tests under 100ms each
2. **Reasonable integration tests**: Aim for under 1 second per test
3. **Separate slow tests**: Mark and run performance tests separately
4. **Parallel execution**: Use pytest-xdist for faster test runs

## 🔍 Monitoring and Metrics

### Test Metrics to Track

1. **Test execution time**: Monitor for performance regressions
2. **Test success rate**: Aim for 100% pass rate
3. **Coverage percentage**: Maintain minimum coverage thresholds
4. **Test count**: Track growth of test suite

### Continuous Monitoring

```bash
# Generate test metrics
pytest tests/ --junit-xml=test-results.xml

# Track coverage over time
pytest tests/ --cov=. --cov-report=xml
```

---

## 📞 Support

For questions about testing:

1. Check this documentation
2. Review existing test examples
3. Run `python run_tests.py --help`
4. Contact the development team

**Happy Testing! 🧪**
