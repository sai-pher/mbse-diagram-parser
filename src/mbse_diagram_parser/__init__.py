"""
MBSE Diagram Parser

A Python library for parsing MBSE text notation and generating Draw.io diagram files.
"""

from mbse_diagram_parser.parser import (
    MBSEParser,
    Element,
    ElementType,
    Connection,
    ConnectionType,
    ParsedDiagram,
)

# Optional: Import generator if drawpyo is available
try:
    from mbse_diagram_parser.generator import (
        MBSEDiagramGenerator,
        OutputFormat,
    )

    _GENERATOR_AVAILABLE = True
except ImportError:
    _GENERATOR_AVAILABLE = False
    MBSEDiagramGenerator = None
    OutputFormat = None

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "MBSEParser",
    "Element",
    "ElementType",
    "Connection",
    "ConnectionType",
    "ParsedDiagram",
]

# Add generator classes to __all__ if available
if _GENERATOR_AVAILABLE:
    __all__.extend(["MBSEDiagramGenerator", "OutputFormat"])
