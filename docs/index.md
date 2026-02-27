# MBSE Diagram Parser Documentation

`mbse-diagram-parser` is a Python library for parsing MBSE text notation and generating Draw.io diagram files.

## Overview

This library provides a simple, text-based notation for defining Model-Based Systems Engineering (MBSE) diagrams. The text notation can be version-controlled like code, making it easy to review changes, collaborate, and maintain system diagrams.

## Installation

```bash
pip install mbse-diagram-parser
```

For development:

```bash
git clone https://github.com/sai-pher/mbse-diagram-parser.git
cd mbse-diagram-parser
pip install -e ".[dev]"
```

## Quick Start

```python
from mbse_diagram_parser import MBSEParser

notation = """
{calculator}-O(execute operations)->[results]
{calculator}-∆{keypad}, {screen}
"""

parser = MBSEParser()
diagram = parser.parse(notation)

# Access elements and connections
print(f"Elements: {len(diagram.elements)}")
print(f"Connections: {len(diagram.connections)}")
```

## Notation Syntax

### Elements

- `{component}` - System component (rectangle)
- `(process)` - Process or operation (oval)
- `[data]` - Data object (rounded rectangle)

### Connections

- `->` - Data flow
- `-O` - Process connection
- `-∆` - Composition relationship

### Comments

Lines starting with `#` are treated as comments.

## Examples

See the [examples/](https://github.com/sai-pher/mbse-diagram-parser/tree/main/examples) directory for complete examples:

- `calculator.mbse` - Calculator system
- `simple_flow.mbse` - Data processing pipeline
- `web_app.mbse` - Web application architecture

## API Reference

### MBSEParser

Main parser class for MBSE text notation.

**Methods:**

- `parse(notation: str) -> ParsedDiagram` - Parse text notation
- `to_dict() -> dict` - Convert parsed diagram to dictionary

### Element

Represents a diagram element.

**Attributes:**

- `type: ElementType` - Element type (COMPONENT, PROCESS, DATA)
- `name: str` - Element name
- `id: str` - Generated element ID

### Connection

Represents a connection between elements.

**Attributes:**

- `type: ConnectionType` - Connection type
- `source: str` - Source element ID
- `target: str` - Target element ID
- `label: Optional[str]` - Connection label

### ParsedDiagram

Container for parsed elements and connections.

**Methods:**

- `add_element(element: Element) -> Element`
- `add_connection(connection: Connection)`
- `get_element_by_name(name: str) -> Optional[Element]`
