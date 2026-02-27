# Contributing to MBSE Diagram Parser

Thank you for your interest in contributing to `mbse-diagram-parser`! This document provides guidelines and instructions for contributing to the project.

## Getting Started

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/mbse-diagram-parser.git
   cd mbse-diagram-parser
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/sai-pher/mbse-diagram-parser.git
   ```

### Set Up Development Environment

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install the project in development mode with all dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Branch Naming Convention

Use clear, descriptive branch names following these prefixes:

- `feature/` - New features or enhancements
  - Example: `feature/add-sequence-diagram-support`
- `fix/` - Bug fixes
  - Example: `fix/parser-edge-case`
- `docs/` - Documentation updates
  - Example: `docs/update-installation-guide`
- `chore/` - Maintenance tasks, refactoring
  - Example: `chore/update-dependencies`

## Development Workflow

### Before Making Changes

1. Sync with upstream:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Making Changes

1. Make your changes in small, logical commits
2. Write or update tests for your changes
3. Ensure all tests pass: `make test`
4. Ensure code is properly linted: `make lint`
5. Format your code: `make format`

### Code Style

This project uses:
- **ruff** for linting (replaces flake8, isort, and more)
- **black** for code formatting

Run linting and formatting:
```bash
make lint    # Check for linting issues
make format  # Auto-format code and fix linting issues
```

Configuration is in `pyproject.toml`.

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>: <description>

[optional body]

[optional footer]
```

Types:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `chore:` - Maintenance tasks
- `test:` - Adding or updating tests
- `refactor:` - Code refactoring
- `perf:` - Performance improvements

Examples:
```
feat: add support for sequence diagrams

fix: handle empty input in parser

docs: update README with installation instructions
```

## Pull Request Requirements

Before submitting a PR, ensure:

1. ✅ All tests pass (`make test`)
2. ✅ Code is properly linted (`make lint`)
3. ✅ Code follows the project's style guidelines
4. ✅ New features include tests
5. ✅ Documentation is updated if needed
6. ✅ Commit messages follow Conventional Commits format

### Submitting a Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open a Pull Request on GitHub
3. Fill out the PR template completely
4. Wait for review and address any feedback

## Running Tests

```bash
# Run all tests
make test

# Run tests with coverage report
pytest tests/ --cov=src/mbse_diagram_parser --cov-report=html

# Run specific test file
pytest tests/test_parser.py

# Run with verbose output
pytest -v
```

## Building Documentation

```bash
# Serve documentation locally
make docs

# Build documentation for deployment
make docs-build
```

Documentation will be available at `http://127.0.0.1:8000/`.

## Project Structure

```
mbse-diagram-parser/
├── src/mbse_diagram_parser/  # Main library code
├── tests/                     # Test files
├── docs/                      # Documentation source
├── examples/                  # Example usage
└── ai/docs/                   # AI agent development docs
```

## Questions?

If you have questions or need help, please:
- Open an issue on GitHub
- Check existing issues and discussions
- Reach out to the maintainers

Thank you for contributing! 🎉
