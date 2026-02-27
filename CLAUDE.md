# CLAUDE.md - AI Agent Context Document

This file provides context and guidelines for AI agents (like Claude) working on the `mbse-diagram-parser` project.

## Project Overview

**Purpose:** A Python library for parsing MBSE (Model-Based Systems Engineering) text notation and generating Draw.io diagram files.

**Target Users:** Systems engineers, technical architects, and developers who want to define diagrams using version-controllable text notation.

**Key Goals:**
- Provide a simple, intuitive text-based notation for MBSE diagrams
- Generate valid Draw.io XML files programmatically
- Enable diagram definitions to be version-controlled like code
- Support multiple diagram types (BDD, IBD, Sequence, State Machine)

## Architecture

### Package Structure

```
mbse-diagram-parser/
├── src/mbse_diagram_parser/
│   ├── __init__.py           # Package initialization, version export
│   ├── parser/               # Text notation parsing
│   ├── models/               # Diagram element models
│   ├── generators/           # Draw.io XML generation
│   └── cli/                  # Command-line interface
├── tests/                    # Unit and integration tests
├── docs/                     # MkDocs documentation
├── examples/                 # Example diagram definitions
└── ai/docs/                  # Development standards for AI agents
```

### Core Components (Future)

1. **Parser Module** (`parser/`)
   - Lexer/tokenizer for text notation
   - Grammar definition
   - AST (Abstract Syntax Tree) generation

2. **Models Module** (`models/`)
   - Diagram element classes (Block, Connector, Port, etc.)
   - Validation logic
   - Intermediate representation

3. **Generators Module** (`generators/`)
   - Draw.io XML template engine
   - Layout algorithms
   - Style configuration

4. **CLI Module** (`cli/`)
   - Command-line interface using Click or Typer
   - File I/O handling
   - Error reporting

## Development Standards

### Code Quality

- **Python Version:** 3.12+
- **Type Hints:** Use type hints for all function signatures
- **Docstrings:** Google-style docstrings for all public APIs
- **Testing:** Minimum 80% code coverage
- **Linting:** Use `ruff` (configured in `pyproject.toml`)
- **Formatting:** Use `black` with 88 character line length

### Testing Strategy

- **Unit Tests:** Test individual functions and classes
- **Integration Tests:** Test end-to-end parsing and generation
- **Fixture Files:** Store example notation files in `tests/fixtures/`
- **Golden Files:** Store expected XML output in `tests/golden/`

### Documentation

- **API Docs:** Auto-generated from docstrings using MkDocs
- **User Guide:** Hand-written guides in `docs/`
- **Examples:** Working examples in `examples/` directory
- **CLAUDE.md:** Keep this file updated when architecture changes

## AI Agent Guidelines

### When Making Changes

1. **Read Before Writing:** Always read existing files before modifying them
2. **Test-Driven Development:** Write tests before implementation when adding features
3. **Incremental Changes:** Make small, focused commits
4. **Documentation:** Update relevant docs when changing public APIs
5. **Type Safety:** Ensure all new code has proper type hints

### Before Committing

- [ ] Run `make lint` - ensure code passes linting
- [ ] Run `make test` - ensure all tests pass
- [ ] Run `make format` - auto-format code
- [ ] Update CLAUDE.md if architecture changed
- [ ] Update README.md if public API changed

### Common Tasks

**Adding a new diagram type:**
1. Create model classes in `models/`
2. Add parser logic in `parser/`
3. Implement generator in `generators/`
4. Write tests in `tests/`
5. Add examples in `examples/`
6. Document in `docs/`

**Fixing a bug:**
1. Write a failing test that reproduces the bug
2. Fix the bug
3. Ensure the test now passes
4. Check for similar issues elsewhere

**Improving performance:**
1. Profile first to identify bottlenecks
2. Optimize the bottleneck
3. Benchmark to verify improvement
4. Ensure tests still pass

## Notation Design Principles (Future)

1. **Readability:** Text notation should be human-readable and intuitive
2. **Simplicity:** Minimize syntax complexity
3. **Consistency:** Similar elements use similar syntax
4. **Extensibility:** Easy to add new diagram types
5. **Validation:** Catch errors early with clear messages

## External Dependencies

Keep dependencies minimal:
- **Required:** None (stdlib only for core functionality if possible)
- **Optional:** XML libraries if needed for generation
- **Dev Only:** pytest, ruff, black, mkdocs, coverage tools

## Security Considerations

- **Input Validation:** Validate all parsed input to prevent injection
- **File I/O:** Safely handle file operations, check paths
- **XML Generation:** Ensure generated XML is well-formed and safe

## Performance Targets (Future)

- Parse 1000-line notation file in < 1 second
- Generate Draw.io XML in < 2 seconds
- Handle diagrams with 100+ elements efficiently

## Versioning

- Follow [Semantic Versioning](https://semver.org/)
- Current version: `0.1.0` (initial development)
- Increment PATCH for bug fixes
- Increment MINOR for new features (backward compatible)
- Increment MAJOR for breaking changes

## Resources

- **Draw.io XML Format:** Study existing .drawio files to understand the XML structure
- **MBSE Standards:** Reference SysML and other MBSE standards for notation
- **Python Packaging:** Follow modern Python packaging best practices

## Questions for Future Development

- Which diagram types should be prioritized?
- Should we support importing existing Draw.io files?
- What layout algorithm should we use for auto-positioning?
- Should there be a GUI/web interface in addition to CLI?

---

**Last Updated:** 2026-02-27
**Maintainer:** @sai-pher
**Status:** Initial setup phase
