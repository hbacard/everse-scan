# Contributing to everse-scan

Thanks for your interest in contributing! This document describes how to set up
the project, run checks, and submit changes. Please also read
[`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md) and the main
[`README.md`](./README.md).

## Getting started

- **Python**: 3.12–3.13
- **Package manager**: `pdm` (used by the maintainers), `uv`, or `pip` all work.

```bash
# With pdm (recommended by maintainers)
pdm install -d

# With uv
uv pip install -e ".[dev]"

# With pip
pip install -e .
```

## Development workflow

1. **Create a branch** from `main`: `git checkout -b feat/your-change`
2. **Make your change**, adding tests where appropriate.
3. **Run the checks** (see below).
4. **Open a pull request** against `main`.

## Running checks

```bash
# Lint & format
ruff check .
ruff format .

# Tests (with coverage)
pytest -v
pytest --cov=everse_scan --cov-report=term-missing

# Scan this repository itself (no regressions allowed)
everse-scan .
```

## Writing tests

- Tests live in [`tests/`](./tests) and use `pytest`.
- Fixtures are shared via [`tests/fixtures.py`](./tests/fixtures.py)
  (sample repos with good/bad practices) — reuse them when you can.
- Every new check or reporter feature should ship with at least one test.

## Documentation

- User-facing changes: update the [`README.md`](./README.md).
- API / CLI reference: update [`docs/api.md`](./docs/api.md).
- Changelog: add an entry under "Unreleased" in [`CHANGELOG.md`](./CHANGELOG.md)
  following [Keep a Changelog](https://keepachangelog.com/).

## Commit conventions

Use conventional-commit style prefixes:

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `refactor:` code change that is not a fix or feature
- `test:` tests
- `ci:` CI/tooling
- `chore:` maintenance

## Submitting a pull request

- Fill in the [pull request template](./.github/pull_request_template.md).
- Keep the diff focused: one logical change per PR.
- Ensure the CI workflow (tests, lint, build) is green.

## Questions?

Open a discussion or a [feature request](./.github/ISSUE_TEMPLATE/feature_request.yml)
before making large changes — we're happy to align on design first.
