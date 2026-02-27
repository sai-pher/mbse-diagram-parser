# Development Standards for AI Agents

This document provides detailed development standards and best practices for AI agents working on the `mbse-diagram-parser` project.

## Code Style and Quality

### Python Style Guide

1. **PEP 8 Compliance**
   - Follow PEP 8 style guide for Python code
   - Use `black` for automatic formatting (88 character line length)
   - Use `ruff` for comprehensive linting

2. **Type Hints**
   - Use type hints for all function parameters and return values
   - Use `typing` module types where appropriate (`List`, `Dict`, `Optional`, etc.)
   - Example:
     ```python
     from typing import List, Optional

     def parse_diagram(content: str, validate: bool = True) -> Optional[List[str]]:
         """Parse diagram content and return list of elements."""
         pass
     ```

3. **Docstrings**
   - Use Google-style docstrings for all public modules, classes, and functions
   - Include: description, Args, Returns, Raises, Examples
   - Example:
     ```python
     def parse_block(text: str) -> Block:
         """Parse a block definition from text.

         Args:
             text: The text containing the block definition.

         Returns:
             A Block object representing the parsed block.

         Raises:
             ParseError: If the text cannot be parsed as a valid block.

         Example:
             >>> block = parse_block("block MySystem {}")
             >>> block.name
             'MySystem'
         """
         pass
     ```

### Code Organization

1. **Module Structure**
   - One class per file for major classes
   - Group related utility functions in utility modules
   - Use `__init__.py` to expose public APIs

2. **Import Order**
   - Standard library imports
   - Third-party imports
   - Local application imports
   - Separate each group with a blank line

3. **Naming Conventions**
   - Classes: `PascalCase` (e.g., `DiagramParser`, `BlockElement`)
   - Functions/variables: `snake_case` (e.g., `parse_diagram`, `element_count`)
   - Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_ELEMENTS`, `DEFAULT_STYLE`)
   - Private members: prefix with `_` (e.g., `_internal_method`)

## Testing Standards

### Test Structure

1. **Test Organization**
   - Mirror source structure in tests directory
   - One test file per source file: `test_<module_name>.py`
   - Group related tests in classes: `TestClassName`

2. **Test Naming**
   - Use descriptive names: `test_<function>_<scenario>_<expected>`
   - Examples:
     - `test_parse_block_valid_input_returns_block`
     - `test_parse_block_invalid_syntax_raises_error`
     - `test_generator_empty_diagram_creates_minimal_xml`

3. **Test Coverage**
   - Aim for 80%+ code coverage
   - Test edge cases and error conditions
   - Test both happy path and failure scenarios

### Test Best Practices

1. **Arrange-Act-Assert Pattern**
   ```python
   def test_parse_block_creates_correct_name():
       # Arrange
       input_text = "block MySystem {}"

       # Act
       result = parse_block(input_text)

       # Assert
       assert result.name == "MySystem"
   ```

2. **Use Fixtures**
   - Create pytest fixtures for common test data
   - Store complex test inputs in `tests/fixtures/`
   - Store expected outputs in `tests/golden/`

3. **Parametrized Tests**
   ```python
   import pytest

   @pytest.mark.parametrize("input,expected", [
       ("block A {}", "A"),
       ("block System1 {}", "System1"),
       ("block MySystem {}", "MySystem"),
   ])
   def test_parse_block_names(input, expected):
       result = parse_block(input)
       assert result.name == expected
   ```

## Git Workflow

### Commit Standards

1. **Conventional Commits**
   - Format: `<type>: <description>`
   - Types: `feat`, `fix`, `docs`, `chore`, `test`, `refactor`, `perf`
   - Keep commits atomic and focused

2. **Commit Messages**
   - First line: concise summary (50 chars max)
   - Body: explain what and why (not how)
   - Reference issues when applicable

3. **Commit Examples**
   ```
   feat: add parser for sequence diagrams

   Implements lexer and parser for sequence diagram notation.
   Supports messages, actors, and activation boxes.

   Closes #42
   ```

### Branch Strategy

1. **Branch Types**
   - `feature/*` - New features
   - `fix/*` - Bug fixes
   - `docs/*` - Documentation updates
   - `chore/*` - Maintenance tasks

2. **Branch Lifecycle**
   - Create from `main`
   - Keep up to date with `main`
   - Delete after merge

## Documentation Standards

### Code Documentation

1. **Module-Level**
   - Every module should have a docstring explaining its purpose
   - List main classes/functions

2. **Class-Level**
   - Explain the class purpose and responsibility
   - Document important attributes
   - Provide usage examples

3. **Function-Level**
   - Document all parameters and return values
   - Note any side effects
   - Include examples for complex functions

### User Documentation

1. **README.md**
   - Keep concise and focused
   - Update examples when API changes
   - Link to full documentation

2. **MkDocs Documentation**
   - Write tutorials for common use cases
   - Document all public APIs
   - Include diagrams and examples

3. **CLAUDE.md**
   - Update when architecture changes
   - Document design decisions
   - List known issues and TODOs

## Error Handling

### Exception Strategy

1. **Custom Exceptions**
   ```python
   class ParseError(Exception):
       """Raised when parsing fails."""
       pass

   class ValidationError(Exception):
       """Raised when validation fails."""
       pass
   ```

2. **Error Messages**
   - Be specific and actionable
   - Include context (line number, element name, etc.)
   - Suggest fixes when possible

3. **Error Handling**
   - Catch specific exceptions, not generic `Exception`
   - Don't silently swallow errors
   - Log errors appropriately

## Performance Considerations

1. **Profiling Before Optimizing**
   - Use `cProfile` to identify bottlenecks
   - Optimize only proven slow paths

2. **Common Optimizations**
   - Use generators for large data sets
   - Cache expensive computations
   - Use appropriate data structures

3. **Benchmarking**
   - Write performance tests for critical paths
   - Set performance targets
   - Monitor performance over time

## Security Best Practices

1. **Input Validation**
   - Validate all external input
   - Sanitize file paths
   - Limit resource consumption

2. **XML Generation**
   - Use safe XML libraries
   - Escape special characters
   - Validate generated XML

3. **File Operations**
   - Check file permissions
   - Handle file system errors
   - Use context managers for file I/O

## AI Agent Workflow

### Before Starting Work

1. Read `CLAUDE.md` for project context
2. Review existing code structure
3. Check open issues and PRs
4. Understand the user's requirements

### During Development

1. Write tests first (TDD approach)
2. Implement in small increments
3. Run tests frequently
4. Keep commits focused and atomic

### Before Committing

1. Run full test suite: `make test`
2. Check linting: `make lint`
3. Format code: `make format`
4. Update documentation
5. Review changes thoroughly

### Code Review Checklist

- [ ] Code follows style guide
- [ ] Tests are comprehensive
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance is acceptable
- [ ] Error handling is robust
- [ ] Type hints are present
- [ ] Docstrings are complete

## Common Patterns

### Parser Pattern
```python
class BaseParser:
    """Base class for all parsers."""

    def parse(self, text: str) -> Any:
        """Parse text and return structured data."""
        tokens = self.tokenize(text)
        ast = self.build_ast(tokens)
        return self.validate(ast)
```

### Generator Pattern
```python
class BaseGenerator:
    """Base class for all generators."""

    def generate(self, model: Any) -> str:
        """Generate output from model."""
        validated = self.validate(model)
        return self.render(validated)
```

### Factory Pattern
```python
class DiagramFactory:
    """Factory for creating diagram objects."""

    @staticmethod
    def create(diagram_type: str) -> Diagram:
        """Create diagram of specified type."""
        if diagram_type == "bdd":
            return BlockDefinitionDiagram()
        elif diagram_type == "ibd":
            return InternalBlockDiagram()
        else:
            raise ValueError(f"Unknown diagram type: {diagram_type}")
```

## Resources

- **Python Style Guide:** https://peps.python.org/pep-0008/
- **Google Python Style Guide:** https://google.github.io/styleguide/pyguide.html
- **Conventional Commits:** https://www.conventionalcommits.org/
- **Semantic Versioning:** https://semver.org/
- **pytest Documentation:** https://docs.pytest.org/

---

**Last Updated:** 2026-02-27
**Status:** Initial version
