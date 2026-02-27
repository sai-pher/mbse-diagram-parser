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

> **Note:** The library is under active development. Full examples and API documentation coming soon.

```python
from mbse_diagram_parser import parse_diagram

# Example usage will be added here
```

## Notation Reference

> **Note:** Detailed notation reference documentation is coming soon. The notation will support common MBSE diagram types including:
> - Block Definition Diagrams (BDD)
> - Internal Block Diagrams (IBD)
> - Sequence Diagrams
> - State Machine Diagrams

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- **Documentation:** https://sai-pher.github.io/mbse-diagram-parser
- **Source Code:** https://github.com/sai-pher/mbse-diagram-parser
- **Issue Tracker:** https://github.com/sai-pher/mbse-diagram-parser/issues
