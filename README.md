# MBSE Diagram Parser

[![Build Status](https://github.com/sai-pher/mbse-diagram-parser/actions/workflows/ci.yml/badge.svg)](https://github.com/sai-pher/mbse-diagram-parser/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/mbse-diagram-parser.svg)](https://pypi.org/project/mbse-diagram-parser/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python library for parsing MBSE text notation and generating Draw.io diagram files.

## Overview

`mbse-diagram-parser` provides a simple, text-based notation for defining Model-Based Systems Engineering (MBSE) diagrams and automatically generates Draw.io (diagrams.net) XML files. This enables version-controlled, code-like diagram definitions that can be easily reviewed, merged, and maintained.

## Installation

```bash
pip install mbse-diagram-parser
```

For development installation:

```bash
git clone https://github.com/sai-pher/mbse-diagram-parser.git
cd mbse-diagram-parser
pip install -e ".[dev]"
```

## Quick Start

```python
from mbse_diagram_parser import MBSEParser

# Define your system using text notation
notation = """
{calculator}-O(execute numerical operations)->[numerical results]
{calculator}-∆{keypad}, {screen}, {processing chip}
"""

# Parse the notation
parser = MBSEParser()
diagram = parser.parse(notation)

# Access parsed elements
for element in diagram.elements:
    print(f"{element.type.value}: {element.name}")

# Access connections
for connection in diagram.connections:
    print(f"{connection.source} --{connection.type.value}--> {connection.target}")

# Export to dictionary format
data = parser.to_dict()
```

## Notation Reference

The MBSE text notation uses simple symbols to define diagram elements and their relationships:

### Elements

- `{component}` - Component (rectangle)
- `(process)` - Process (oval)
- `[data]` - Data object (rounded rectangle)

### Connections

- `->` - Data flow arrow
- `-O` - Process connection
- `-∆` - Composition (sub-components)

### Examples

**Simple data flow:**
```
(read input)->[raw data]->(validate data)->[clean data]
```

**Component composition:**
```
{web application}-∆{frontend}, {backend}, {database}
```

**Complex system:**
```
{calculator}-O(execute numerical operations)->[numerical results]
{calculator}-∆{keypad}, {screen}, {processing chip}
{keypad}-O(input numbers)->[numbers]->(sum numbers)
```

See the [examples/](examples/) directory for more complete examples.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- **Documentation:** https://sai-pher.github.io/mbse-diagram-parser
- **Source Code:** https://github.com/sai-pher/mbse-diagram-parser
- **Issue Tracker:** https://github.com/sai-pher/mbse-diagram-parser/issues
