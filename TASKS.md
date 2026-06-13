# Task Distribution - Part A: CI Pipeline

This document outlines how the Part A assignment work is distributed equally among all four team members.

## Team Members

1. **marwanaly** - CI Pipeline Configuration
2. **manarelabsi** - Code Quality & Type Safety
3. **MohamedOthman** - Testing & Coverage
4. **ayaabdelmonem** - Containerization & Build

## Task Breakdown

### marwanaly: CI Pipeline Configuration
- Complete `.gitea/workflows/ci.yml`
- Set up jobs for: lint, type-check, test, build-and-push, sbom
- Configure registry and environment variables
- Update README with CI documentation

### manarelabsi: Code Quality & Type Safety
- Fix mypy type annotation errors in `src/preprocess.py`
- Fix mypy type annotation errors in `src/inference.py`
- Ensure ruff linting passes
- Update pyproject.toml if needed

### MohamedOthman: Testing & Coverage
- Add additional edge case tests in `tests/test_model.py`
- Add integration tests in `tests/test_inference.py`
- Maintain 100% code coverage
- Ensure pytest configuration is optimal

### ayaabdelmonem: Containerization & Build
- Complete multi-stage `Dockerfile`
- Remove `Dockerfile.template`
- Add `.dockerignore`
- Ensure non-root user and proper port exposure

## Verification Order

1. Lint: `ruff check src/ tests/`
2. Type Check: `mypy src/`
3. Test: `pytest`
4. Build: `docker build -t ml-sentiment-app .`
