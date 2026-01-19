# Testing Guide

This directory contains automated tests for the GDG Backend API.

## Setup

### Install Test Dependencies

```bash
# Install development dependencies
pip install -r requirements-dev.txt
```

This will install:
- `pytest-cov` - Code coverage reporting
- `faker` - Generate realistic test data

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test Files

```bash
# Repository tests only
pytest tests/repositories/test_events.py -v

# API tests only
pytest tests/api/test_events.py -v
```

### Run Specific Test Functions

```bash
pytest tests/api/test_events.py::test_create_event_as_admin -v
```

### Run Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run all except slow tests
pytest -m "not slow"
```

## Code Coverage

### Generate Coverage Report

```bash
# Terminal report
pytest --cov=app --cov-report=term-missing

# HTML report (opens in browser)
pytest --cov=app --cov-report=html
open htmlcov/index.html  # On macOS/Linux
start htmlcov/index.html  # On Windows
```

### Coverage Goals

- **Overall**: 80-90% code coverage
- **Critical paths**: 100% coverage (auth, data integrity)
- **Edge cases**: All covered

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── api/
│   ├── __init__.py
│   └── test_events.py       # Event endpoint integration tests
└── repositories/
    ├── __init__.py
    └── test_events.py       # Event repository unit tests
```

## Available Fixtures

### Database Fixtures
- `test_db` - Test database session with automatic rollback
- `test_client` - FastAPI test client

### User Fixtures
- `admin_user` - Admin user for testing
- `regular_user` - Non-admin user for testing
- `admin_headers` - Authentication headers for admin
- `regular_user_headers` - Authentication headers for regular user

### Data Fixtures
- `sample_event_data` - Sample event creation data
- `sample_event_update_data` - Sample event update data

## Writing New Tests

### Repository Tests (Unit Tests)

```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.events import create_event
from app.schemas.event import EventCreate

@pytest.mark.unit
@pytest.mark.asyncio
async def test_my_repository_function(test_db: AsyncSession, admin_user):
    # Arrange
    event_data = EventCreate(...)
    
    # Act
    result = await create_event(test_db, event_data, admin_user.id)
    
    # Assert
    assert result.title == "Expected Title"
```

### API Tests (Integration Tests)

```python
import pytest
from httpx import AsyncClient

@pytest.mark.integration
@pytest.mark.asyncio
async def test_my_endpoint(test_client: AsyncClient, admin_headers: dict):
    # Act
    response = await test_client.post(
        "/events/",
        json={"title": "Test"},
        headers=admin_headers,
    )
    
    # Assert
    assert response.status_code == 201
    assert response.json()["title"] == "Test"
```

## Best Practices

1. **Use descriptive test names** - Test names should clearly describe what is being tested
2. **Follow AAA pattern** - Arrange, Act, Assert
3. **One assertion per test** - Or closely related assertions
4. **Use fixtures** - Reuse common setup code
5. **Test edge cases** - Don't just test happy paths
6. **Keep tests isolated** - Each test should be independent
7. **Use markers** - Tag tests as `unit`, `integration`, or `slow`

## Continuous Integration

Tests should be run:
- **Locally** - Before committing code
- **Pre-commit** - Via git hooks
- **CI/CD** - On every PR/push
- **Before deployment** - Final verification

## Troubleshooting

### Database Connection Errors

If you see database connection errors, ensure:
1. PostgreSQL is running
2. `.env` file has correct `DATABASE_URL`
3. Test database exists and is accessible

### Import Errors

If you see import errors:
1. Ensure you're in the project root directory
2. Activate your virtual environment
3. Install all dependencies: `pip install -r requirements.txt -r requirements-dev.txt`

### Async Warnings

If you see warnings about async event loops:
- Ensure `pytest-asyncio` is installed
- Check that `pytest.ini` has `asyncio_mode = auto`

## Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio documentation](https://pytest-asyncio.readthedocs.io/)
- [FastAPI testing guide](https://fastapi.tiangolo.com/tutorial/testing/)
