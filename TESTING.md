# Testing Guide

This document describes the testing setup for the voice connector template implementations.

## Overview

Both the Node.js/Express and Python/FastAPI implementations now include comprehensive unit test suites that validate:
- Health check endpoint functionality
- TTS endpoint request/response handling
- API authentication and validation
- Error handling
- API documentation endpoints

## Node.js/Express Tests

### Setup
```bash
cd nodejs/express
yarn install  # or npm install
```

### Running Tests
```bash
yarn test     # Run tests with coverage
```

### Test Framework
- **Jest** - Testing framework
- **Supertest** - HTTP assertion library for testing Express apps

### Test Location
- `nodejs/express/__tests__/api.test.js` - Main test suite
- `nodejs/express/jest.config.js` - Jest configuration

### Coverage
Tests cover:
- ✓ Health check endpoint returns correct response structure
- ✓ TTS endpoint authentication (API key validation)
- ✓ TTS endpoint input validation
- ✓ TTS endpoint successful responses
- ✓ Error handling for provider failures

## Python/FastAPI Tests

### Setup
```bash
cd python/fastapi
poetry install
```

### Running Tests
```bash
poetry run pytest              # Run tests
poetry run pytest -v           # Run tests with verbose output
poetry run pytest --cov        # Run tests with coverage report
```

### Test Framework
- **pytest** - Testing framework
- **FastAPI TestClient** - Testing client for FastAPI applications
- **pytest-cov** - Coverage plugin
- **pytest-asyncio** - Async test support

### Test Location
- `python/fastapi/tests/test_api.py` - Main test suite
- `python/fastapi/pytest.ini` - Pytest configuration

### Coverage
Tests cover:
- ✓ Health check endpoint returns correct response structure
- ✓ TTS endpoint authentication (API key validation)
- ✓ TTS endpoint input validation (Pydantic models)
- ✓ TTS endpoint successful responses with different inputs
- ✓ Error handling for request errors and unexpected exceptions
- ✓ API documentation endpoints (Swagger/ReDoc)

## Mocking External Services

Both test suites mock the ElevenLabs TTS integration to:
- Avoid making real API calls during tests
- Speed up test execution
- Enable deterministic test results
- Allow testing error scenarios

### Node.js Mocking
```javascript
jest.mock('../routers/voice/elevenlabs_sample', () => ({
  makeElevenlabsTtsSample: jest.fn().mockResolvedValue(Buffer.from('fake-wav-data'))
}));
```

### Python Mocking
```python
@pytest.fixture
def mock_elevenlabs():
    with patch('routers.voice.voice_handler.make_elevenlabs_tts_sample') as mock:
        mock.return_value = b'fake-wav-data'
        yield mock
```

## CI/CD Integration

### GitHub Actions CI Workflow
The `.github/workflows/ci.yml` workflow runs tests automatically on:
- Pull requests
- Pushes to main branch

**Node.js job:**
```yaml
- run: yarn install
- run: yarn test
```

**Python job:**
```yaml
- run: poetry install
- run: poetry run pytest
```

### Dependabot Review Workflow
The `.github/workflows/dependabot-review.yml` workflow now uses the test suites to validate dependency updates:

**Old approach (inefficient):**
- Started servers manually with `yarn start` / `python main.py`
- Tested endpoints with curl
- Required 25-30 turns, 10+ minutes
- Complex process management

**New approach (optimized):**
- Runs test suites: `yarn test` / `pytest`
- Validates functionality without server management
- Expected: 5-10 turns, 2-5 minutes
- Simple command execution

## Benefits of Unit Testing

1. **Faster Validation** - Tests run in seconds vs minutes for manual server testing
2. **Better Coverage** - Tests validate edge cases and error conditions
3. **Dependency Safety** - Quickly verify that updates don't break functionality
4. **Developer Experience** - Easy to run tests locally before committing
5. **CI Efficiency** - Reduced Claude Code turn usage and execution time
6. **Reliability** - Deterministic results without external dependencies

## Writing New Tests

### Node.js Example
```javascript
test('should handle new feature', async () => {
  const response = await request(app)
    .post('/endpoint')
    .send({ data: 'test' })
    .expect(200);

  expect(response.body).toHaveProperty('result');
});
```

### Python Example
```python
def test_new_feature(client, mock_elevenlabs):
    """Test new feature."""
    response = client.post(
        "/endpoint",
        json={"data": "test"}
    )
    assert response.status_code == 200
    assert "result" in response.json()
```

## Troubleshooting

### Node.js Tests Failing
- Ensure all dependencies are installed: `yarn install`
- Check that you're using Node.js 18+
- Verify Jest is installed: `yarn list jest`

### Python Tests Failing
- Ensure Poetry environment is set up: `poetry install`
- Check Python version: `python --version` (should be 3.11+)
- Activate virtual environment: `poetry shell`

### Mock Issues
- Ensure mock paths match the actual import paths
- For Node.js: Mock the module being imported, not where it's defined
- For Python: Use the full import path as it appears in the handler

## Future Improvements

Potential enhancements to the test suite:
- Add integration tests with real TTS provider (in separate CI job)
- Add load/performance testing
- Add security testing (SQL injection, XSS, etc.)
- Add contract testing for API compliance
- Expand coverage to include edge cases
