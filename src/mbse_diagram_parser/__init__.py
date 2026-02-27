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
