# Testing Infrastructure

This document describes the comprehensive testing infrastructure for the Broken Vowels project.

## Overview

The project implements a production-ready testing infrastructure with:
- **Python**: 99.75% code coverage with 131 tests
- **Node.js**: 86% code coverage with 14 tests
- Automated CI/CD with quality gates
- Performance and load testing
- Security scanning
- Pre-commit hooks for code quality

## Quick Start

### Python Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests with coverage
pytest

# Run specific test categories
pytest tests/test_core_directive.py -v
pytest tests/test_performance.py -v
pytest -m "not slow"  # Skip slow tests

# Generate HTML coverage report
pytest --cov-report=html
open htmlcov/index.html
```

### Node.js Tests

```bash
# Install dependencies
npm install

# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch

# Lint code
npm run lint
npm run lint:fix
```

## Test Structure

### Python Tests (`tests/`)

1. **test_core_directive.py** - Core Directive module tests
   - Basic functionality tests
   - Edge case handling
   - Adversarial input testing (SQL injection, XSS, prompt injection)
   - Unicode and special character handling

2. **test_evaluator.py** - Detailed evaluation engine tests
   - All impact category detection
   - All conflict type detection
   - Score calculation and clamping
   - Recommendation generation

3. **test_gateway.py** - Gateway processing tests
   - Request/response handling
   - Middleware functionality
   - Audit logging
   - Route management
   - Integration scenarios

4. **test_ai_client.py** - AI client tests
   - Model integration
   - Pre/post processing hooks
   - Directive evaluation
   - Statistics tracking

5. **test_performance.py** - Performance and load tests
   - Throughput benchmarks (>1000 req/s for Core Directive)
   - Response time tests (<1ms average)
   - Concurrency tests (multi-threaded)
   - Scalability tests (large inputs, batch processing)
   - Memory stability tests

6. **test_governance.py** - Original comprehensive tests
   - Module-level function tests
   - Integration tests
   - Middleware tests

7. **test_main.py** - FastAPI application tests
   - API endpoint tests
   - Core Directive injection tests

### Node.js Tests (`tests/`)

1. **gateway.test.js** - LLM Gateway tests
   - Health check endpoint
   - Models endpoint
   - Core Directive injection
   - Chat completions endpoint
   - Legacy completions endpoint
   - Streaming response handling
   - Error handling (malformed JSON, missing fields, network errors)
   - OpenAI API integration (success and error cases)

## Coverage Requirements

### Python
- **Minimum**: 95% (enforced by pytest.ini)
- **Current**: 99.75%
- **Target**: 100%

Coverage by module:
- `core_directive.py`: 100%
- `evaluator.py`: 100%
- `gateway.py`: 100%
- `ai_client.py`: 98.41%

### Node.js
- **Minimum**: 80% (enforced by package.json)
- **Current**: 86%
- **Target**: 95%

Coverage by file:
- `gateway.js`: 86% (statements), 81% (branches), 88% (functions)

## Performance Benchmarks

All benchmarks are validated in CI:

| Component | Throughput | Avg Response Time | P95 Response Time |
|-----------|-----------|-------------------|-------------------|
| Core Directive | >1000 req/s | <1ms | <2ms |
| Detailed Evaluator | >500 req/s | <5ms | <10ms |
| Gateway | >500 req/s | - | - |
| AI Client | >300 req/s | - | - |

## CI/CD Workflows

### Python Tests Workflow
- Matrix testing: Python 3.10, 3.11, 3.12
- Linting: flake8, black
- Security: bandit
- Coverage reporting to Codecov
- PR comment with coverage report
- Artifacts: HTML coverage report

### Node.js Tests Workflow
- Matrix testing: Node 18.x, 20.x, 22.x
- Linting: eslint
- Security: npm audit
- Coverage reporting to Codecov
- Artifacts: Coverage report

### Auto-merge Workflow
- Auto-approves Dependabot PRs
- Auto-merges when all tests pass
- Squash merge strategy

## Quality Gates

### Pre-commit Hooks

Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

Hooks configured:
- Trailing whitespace removal
- End-of-file fixer
- YAML/JSON/TOML validation
- Large file check
- Merge conflict detection
- Private key detection
- **Python**: black, flake8, isort, mypy, bandit
- **JavaScript**: eslint
- **Documentation**: mdformat

### Type Checking

Python type checking with mypy:
```bash
mypy core_directive.py evaluator.py gateway.py ai_client.py
```

Configuration in `mypy.ini`.

## Security Scanning

### Python
- **bandit**: Static security analysis
- **safety**: Dependency vulnerability scanning

```bash
bandit -r . -ll --skip B404,B603 --exclude ./tests/
safety check
```

### Node.js
- **npm audit**: Dependency vulnerability scanning

```bash
npm audit
npm audit fix
```

## Configuration Files

- **pytest.ini**: Pytest configuration and coverage settings
- **.coveragerc**: Coverage reporting configuration
- **mypy.ini**: Type checking configuration
- **.pre-commit-config.yaml**: Pre-commit hooks
- **.eslintrc.json**: ESLint configuration for JavaScript
- **package.json**: Jest configuration and test scripts
- **.gitignore**: Excludes coverage reports and build artifacts

## Best Practices

1. **Write tests first**: Follow TDD when adding new features
2. **Keep tests isolated**: Each test should be independent
3. **Use descriptive names**: Test names should describe what they test
4. **Mock external dependencies**: Use mocks for OpenAI API calls
5. **Test edge cases**: Include adversarial inputs and error conditions
6. **Maintain coverage**: Keep coverage above 95%
7. **Run locally first**: Test before pushing to CI
8. **Review coverage reports**: Identify untested code paths

## Troubleshooting

### Tests fail locally but pass in CI
- Ensure you have the latest dependencies: `pip install -r requirements.txt`
- Check Python version matches CI (3.10-3.12)
- Clear pytest cache: `pytest --cache-clear`

### Coverage drops below threshold
- Run with coverage report: `pytest --cov-report=term-missing`
- Identify missing lines and add tests
- Update .coveragerc to exclude non-critical code

### Performance tests fail
- Performance tests can be environment-dependent
- Run on similar hardware to CI (Ubuntu, 2+ cores)
- Adjust thresholds if consistently failing

### Pre-commit hooks fail
- Run manually: `pre-commit run --all-files`
- Auto-fix issues: `black .` and `eslint --fix src/ tests/`
- Update hooks: `pre-commit autoupdate`

## Contributing

When adding new code:
1. Write comprehensive tests (unit, integration, edge cases)
2. Ensure coverage remains >95%
3. Add performance tests for critical paths
4. Update this documentation if adding new test categories
5. Run pre-commit hooks before committing
6. Verify CI passes before merging

## Future Improvements

- [ ] Increase Node.js coverage to 95%+
- [ ] Add mutation testing (mutmut for Python, Stryker for Node.js)
- [ ] Add visual regression tests
- [ ] Implement contract testing for API endpoints
- [ ] Add chaos engineering tests
- [ ] Performance regression detection with historical data
- [ ] Fuzzing tests for input validation
- [ ] Documentation coverage checking
