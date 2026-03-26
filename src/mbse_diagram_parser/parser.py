"""
MBSE Text Notation Parser

Parses text notation into structured diagram elements.

Notation Reference:
- {component}      : Component (rectangle)
- (process)        : Process (oval)
- [data]          : Data object (rounded rectangle)
- ->              : Data flow arrow
- -O              : Process connection
- -∆              : Composition (sub-components)

Example:
{calculator}-O(execute numerical operations)->[numerical results]
{calculator}-∆{keypad}, {screen}, {processing chip}
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class ElementType(Enum):
    """Types of diagram elements."""

    COMPONENT = "component"
    PROCESS = "process"
    CORE_PROCESS = "core_process"
    DATA = "data"


class ConnectionType(Enum):
    """Types of connections between elements."""

    DATA_FLOW = "->"  # Data flow arrow
    PROCESS_CONNECTION = "-O"  # Process connection
    COMPOSITION = "-∆"  # Component composition


@dataclass
class Element:
    """Represents a diagram element."""

    type: ElementType
    name: str
    id: Optional[str] = None

    def __post_init__(self):
        if self.id is None:
            # Generate ID from name (sanitized)
            self.id = re.sub(r"[^a-zA-Z0-9_]", "_", self.name.lower())


@dataclass
class Connection:
    """Represents a connection between elements."""

    type: ConnectionType
    source: str  # Element ID or name
    target: str  # Element ID or name
    label: Optional[str] = None


@dataclass
class ParsedDiagram:
    """Container for parsed diagram elements."""

    elements: List[Element] = field(default_factory=list)
    connections: List[Connection] = field(default_factory=list)

    def add_element(self, element: Element) -> Element:
        """Add element if not already present."""
        # Check if element with same name already exists
        for existing in self.elements:
            if existing.name == element.name and existing.type == element.type:
                return existing
        self.elements.append(element)
        return element

    def add_connection(self, connection: Connection):
        """Add connection."""
        self.connections.append(connection)

    def get_element_by_name(
        self, name: str, element_type: Optional[ElementType] = None
    ) -> Optional[Element]:
        """Find element by name."""
        for elem in self.elements:
            if elem.name == name:
                if element_type is None or elem.type == element_type:
                    return elem
        return None


class MBSEParser:
    """Parser for MBSE text notation."""

    # Regex patterns for different element types
    COMPONENT_PATTERN = r"\{([^}]+)\}"
    PROCESS_PATTERN = r"\(([^)]+)\)"
    DATA_PATTERN = r"\[([^\]]+)\]"

    # Connection patterns
    DATA_FLOW_PATTERN = r"->"
    PROCESS_CONN_PATTERN = r"-O"
    COMPOSITION_PATTERN = r"-∆"

    def __init__(self):
        self.diagram = ParsedDiagram()

    def parse(self, notation: str) -> ParsedDiagram:
        """
        Parse MBSE text notation into structured diagram.

        Args:
            notation: Multi-line text notation

        Returns:
            ParsedDiagram object with elements and connections
        """
        self.diagram = ParsedDiagram()

        # Process line by line
        lines = notation.strip().split("\n")
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            self._parse_line(line)

        return self.diagram

    def _parse_line(self, line: str):
        """Parse a single line of notation."""

        # Check for composition (sub-components)
        if "-∆" in line:
            self._parse_composition(line)
            return

        # Parse complex lines with multiple connection types
        # Strategy: tokenize the line and process sequentially
        self._parse_complex_line(line)

    def _extract_elements(self, text: str) -> List[Element]:
        """Extract all elements from text."""
        elements = []

        # Extract components
        for match in re.finditer(self.COMPONENT_PATTERN, text):
            name = match.group(1).strip()
            elem = Element(ElementType.COMPONENT, name)
            elements.append(self.diagram.add_element(elem))

        # Extract processes
        for match in re.finditer(self.PROCESS_PATTERN, text):
            name = match.group(1).strip()
            elem = Element(ElementType.PROCESS, name)
            elements.append(self.diagram.add_element(elem))

        # Extract data
        for match in re.finditer(self.DATA_PATTERN, text):
            name = match.group(1).strip()
            elem = Element(ElementType.DATA, name)
            elements.append(self.diagram.add_element(elem))

        return elements

    def _parse_composition(self, line: str):
        """Parse composition relationship: {parent}-∆{child1}, {child2}."""
        parts = line.split("-∆")
        if len(parts) != 2:
            return

        # Extract parent component
        parent_match = re.search(self.COMPONENT_PATTERN, parts[0])
        if not parent_match:
            return

        parent_name = parent_match.group(1).strip()
        parent = self.diagram.add_element(Element(ElementType.COMPONENT, parent_name))

        # Extract child components (comma-separated)
        children_text = parts[1]
        for child_match in re.finditer(self.COMPONENT_PATTERN, children_text):
            child_name = child_match.group(1).strip()
            child = self.diagram.add_element(Element(ElementType.COMPONENT, child_name))

            # Add composition connection
            conn = Connection(
                type=ConnectionType.COMPOSITION, source=parent.id, target=child.id
            )
            self.diagram.add_connection(conn)

    def _parse_complex_line(self, line: str):
        """
        Parse complex lines that may have multiple connection types.

        Example: {keypad}-O(input numbers)->[numbers]->(sum numbers)
        """
        # Tokenize the line into elements and connectors
        tokens = []

        # Pattern to match elements and connectors
        pattern = r"(\{[^}]+\}|\([^)]+\)|\[[^\]]+\]|->|-O|O-)"

        for match in re.finditer(pattern, line):
            token = match.group(1)
            tokens.append(token)

        if not tokens:
            return

        # Process tokens sequentially
        i = 0
        last_element = None

        while i < len(tokens):
            token = tokens[i]

            # Check if it's an element
            if token.startswith("{") or token.startswith("(") or token.startswith("["):
                elements = self._extract_elements(token)
                if elements:
                    current_element = elements[0]

                    # If we have a previous element and a connection type, create connection
                    if last_element is not None and i > 0:
                        connector = tokens[i - 1]

                        if connector == "->":
                            conn = Connection(
                                type=ConnectionType.DATA_FLOW,
                                source=last_element.id,
                                target=current_element.id,
                            )
                            self.diagram.add_connection(conn)
                        elif connector == "-O" or connector == "O-":
                            conn = Connection(
                                type=ConnectionType.PROCESS_CONNECTION,
                                source=last_element.id,
                                target=current_element.id,
                            )
                            self.diagram.add_connection(conn)

                    last_element = current_element

            i += 1

    def to_dict(self) -> dict:
        """Convert parsed diagram to dictionary format."""
        return {
            "elements": [
                {"id": elem.id, "name": elem.name, "type": elem.type.value}
                for elem in self.diagram.elements
            ],
            "connections": [
                {
                    "type": conn.type.value,
                    "source": conn.source,
                    "target": conn.target,
                    "label": conn.label,
                }
                for conn in self.diagram.connections
            ],
        }


def main():
    """Test the parser with examples."""

    print("=" * 60)
    print("MBSE Text Notation Parser - Test Cases")
    print("=" * 60)

    # Test Case 1: Simple calculator example
    print("\n[Test 1] Calculator Example:")
    print("-" * 60)

    notation1 = """
    {calculator}-O(execute numerical operations)->[numerical results]
    {calculator}-∆{keypad}, {screen}, {processing chip}
    {keypad}-O(input numbers)->[numbers]->(sum numbers)->[number]->(display result)O-{screen}
    """

    print("Input notation:")
    print(notation1)

    parser = MBSEParser()
    result = parser.parse(notation1)

    print("\nParsed Elements:")
    for elem in result.elements:
        print(f"  [{elem.type.value}] {elem.name} (id: {elem.id})")

    print("\nParsed Connections:")
    for conn in result.connections:
        print(f"  {conn.source} --{conn.type.value}--> {conn.target}")

    # Test Case 2: Simple process flow
    print("\n" + "=" * 60)
    print("[Test 2] Simple Process Flow:")
    print("-" * 60)

    notation2 = """
    (read input)->[raw data]->(validate data)->[clean data]->(process data)->[results]
    """

    print("Input notation:")
    print(notation2)

    parser2 = MBSEParser()
    result2 = parser2.parse(notation2)

    print("\nParsed Elements:")
    for elem in result2.elements:
        print(f"  [{elem.type.value}] {elem.name} (id: {elem.id})")

    print("\nParsed Connections:")
    for conn in result2.connections:
        print(f"  {conn.source} --{conn.type.value}--> {conn.target}")

    # Test Case 3: Component with sub-components
    print("\n" + "=" * 60)
    print("[Test 3] Component Composition:")
    print("-" * 60)

    notation3 = """
    {web application}-∆{frontend}, {backend}, {database}
    {frontend}-O(render UI)
    {backend}-O(process requests)
    """

    print("Input notation:")
    print(notation3)

    parser3 = MBSEParser()
    result3 = parser3.parse(notation3)

    print("\nParsed Elements:")
    for elem in result3.elements:
        print(f"  [{elem.type.value}] {elem.name} (id: {elem.id})")

    print("\nParsed Connections:")
    for conn in result3.connections:
        print(f"  {conn.source} --{conn.type.value}--> {conn.target}")

    print("\n" + "=" * 60)
    print("Tests Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
