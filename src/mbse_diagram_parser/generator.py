"""
MBSE Diagram Generator

Converts parsed MBSE notation into Draw.io diagrams using drawpyo.
Supports export to .drawio files and PNG images.
"""

import subprocess
import os
from enum import Enum
from typing import List, Dict

try:
    import drawpyo
except ImportError:
    drawpyo = None

from mbse_diagram_parser.parser import (
    MBSEParser,
    ElementType,
    ConnectionType,
    ParsedDiagram,
    Element,
    Connection,
)


class OutputFormat(Enum):
    """Output format options."""

    DRAWIO = "drawio"
    PNG = "png"
    BOTH = "both"


class MBSEDiagramGenerator:
    """Generate Draw.io diagrams from parsed MBSE notation."""

    # Style definitions matching MBSE notation reference
    STYLES = {
        ElementType.COMPONENT: {
            "shape": "rectangle",
            "fillColor": "#ffffff",
            "strokeColor": "#000000",
            "strokeWidth": 1,
            "fontColor": "#000000",
            "fontSize": 11,
        },
        ElementType.PROCESS: {
            "shape": "ellipse",
            "fillColor": "#ffffff",
            "strokeColor": "#000000",
            "strokeWidth": 1,
            "fontColor": "#000000",
            "fontSize": 11,
        },
        ElementType.DATA: {
            "shape": "rounded_rectangle",
            "fillColor": "#ffffff",
            "strokeColor": "#000000",
            "strokeWidth": 1,
            "fontColor": "#000000",
            "fontSize": 11,
        },
    }

    # Connection styles - matching reference design
    CONNECTION_STYLES = {
        ConnectionType.DATA_FLOW: {
            "strokeColor": "#000000",
            "strokeWidth": 1,
            "endArrow": "classic",
            "startSize": 6,
            "endSize": 6,
        },
        ConnectionType.PROCESS_CONNECTION: {
            "strokeColor": "#000000",
            "strokeWidth": 1,
            "endArrow": "classic",
            "startSize": 6,
            "endSize": 6,
        },
        ConnectionType.COMPOSITION: {
            "strokeColor": "#000000",
            "strokeWidth": 1,
            "endArrow": "block",
            "startSize": 6,
            "endSize": 6,
        },
    }

    # Layout parameters
    ELEMENT_WIDTH = 120
    ELEMENT_HEIGHT_RECT = 60
    ELEMENT_HEIGHT_OVAL = 60
    HORIZONTAL_SPACING = 150
    VERTICAL_SPACING = 100
    START_X = 50
    START_Y = 50

    def __init__(self):
        if drawpyo is None:
            raise ImportError(
                "drawpyo is required for diagram generation. "
                "Install it with: pip install drawpyo"
            )
        self.element_objects = {}  # Maps element IDs to drawpyo objects
        self.element_positions = {}  # Maps element IDs to (x, y) positions

    def generate(
        self,
        notation: str,
        filename: str = "mbse_diagram",
        output_format: OutputFormat = OutputFormat.DRAWIO,
        output_dir: str = ".",
    ) -> List[str]:
        """
        Generate a Draw.io diagram from MBSE notation.

        Args:
            notation: MBSE text notation
            filename: Output filename (without extension)
            output_format: OutputFormat.DRAWIO, OutputFormat.PNG, or OutputFormat.BOTH
            output_dir: Output directory path

        Returns:
            List of paths to generated files
        """
        # Parse the notation
        parser = MBSEParser()
        diagram = parser.parse(notation)

        # Create drawpyo file and page
        file = drawpyo.File()
        file.file_name = f"{filename}.drawio"
        file.file_path = output_dir

        page = drawpyo.Page(file=file)
        page.page_name = "MBSE Diagram"

        # Calculate layout
        self._calculate_layout(diagram)

        # Create elements
        for element in diagram.elements:
            self._create_element(page, element)

        # Create connections
        for connection in diagram.connections:
            self._create_connection(page, connection)

        # Write drawio file
        file.write()
        drawio_path = os.path.join(output_dir, f"{filename}.drawio")

        output_paths = []

        # Add drawio file to outputs if requested
        if output_format in [OutputFormat.DRAWIO, OutputFormat.BOTH]:
            output_paths.append(drawio_path)

        # Generate PNG if requested
        if output_format in [OutputFormat.PNG, OutputFormat.BOTH]:
            png_path = self._export_to_png(drawio_path, filename, output_dir)
            if png_path:
                output_paths.append(png_path)

        return output_paths

    def _calculate_layout(self, diagram: ParsedDiagram):
        """
        Calculate positions for all elements using a simple grid layout.

        Strategy:
        1. Identify layers (components, processes, data)
        2. Arrange elements in columns by type
        3. Try to keep connected elements close
        """
        # Separate elements by type
        components = [e for e in diagram.elements if e.type == ElementType.COMPONENT]
        processes = [e for e in diagram.elements if e.type == ElementType.PROCESS]
        data = [e for e in diagram.elements if e.type == ElementType.DATA]

        # Layout strategy: Left to right - Components, Processes, Data
        current_x = self.START_X
        current_y = self.START_Y

        # Position components (left column)
        for i, elem in enumerate(components):
            self.element_positions[elem.id] = (
                current_x,
                current_y + i * self.VERTICAL_SPACING,
            )

        # Position processes (middle column)
        current_x += self.HORIZONTAL_SPACING + self.ELEMENT_WIDTH
        current_y = self.START_Y
        for i, elem in enumerate(processes):
            self.element_positions[elem.id] = (
                current_x,
                current_y + i * self.VERTICAL_SPACING,
            )

        # Position data (right column)
        current_x += self.HORIZONTAL_SPACING + self.ELEMENT_WIDTH
        current_y = self.START_Y
        for i, elem in enumerate(data):
            self.element_positions[elem.id] = (
                current_x,
                current_y + i * self.VERTICAL_SPACING,
            )

    def _create_element(self, page, element: Element):
        """Create a drawpyo object for an element."""
        style = self.STYLES[element.type]
        position = self.element_positions[element.id]

        # Create the object
        obj = drawpyo.diagram.Object(page=page)

        # Set shape based on type
        if element.type == ElementType.PROCESS:
            # Ellipse shape
            obj.shape = "ellipse"
            height = self.ELEMENT_HEIGHT_OVAL
        elif element.type == ElementType.DATA:
            # Rounded rectangle
            obj.rounded = True
            obj.arcSize = 20  # More pronounced rounding like reference
            height = self.ELEMENT_HEIGHT_RECT
        else:
            # Regular rectangle (component)
            obj.rounded = False
            height = self.ELEMENT_HEIGHT_RECT

        # Set position and size
        obj.position = position
        obj.width = self.ELEMENT_WIDTH
        obj.height = height

        # Apply styling
        obj.fillColor = style["fillColor"]
        obj.strokeColor = style["strokeColor"]
        obj.strokeWidth = style["strokeWidth"]
        obj.fontColor = style["fontColor"]
        obj.fontSize = style.get("fontSize", 11)

        # Set label
        obj.value = element.name

        # Text alignment
        obj.align = "center"
        obj.verticalAlign = "middle"

        # Store reference
        self.element_objects[element.id] = obj

    def _create_connection(self, page, connection: Connection):
        """Create a drawpyo edge for a connection."""
        source_obj = self.element_objects.get(connection.source)
        target_obj = self.element_objects.get(connection.target)

        if not source_obj or not target_obj:
            print(
                f"Warning: Could not find objects for connection "
                f"{connection.source} -> {connection.target}"
            )
            return

        # Create edge
        edge = drawpyo.diagram.Edge(page=page, source=source_obj, target=target_obj)

        # Apply style based on connection type
        style = self.CONNECTION_STYLES.get(connection.type, {})

        if "strokeColor" in style:
            edge.strokeColor = style["strokeColor"]
        if "strokeWidth" in style:
            edge.strokeWidth = style["strokeWidth"]
        if "endArrow" in style:
            edge.target_arrow = style["endArrow"]
        if style.get("dashed"):
            edge.dashed = 1

        # Set waypoint style
        if connection.type == ConnectionType.PROCESS_CONNECTION:
            edge.waypoint_style = "orthogonal"
        else:
            edge.waypoint_style = "straight"

        # Add label if present
        if connection.label:
            edge.value = connection.label

    def _export_to_png(
        self, drawio_path: str, base_filename: str, output_dir: str
    ) -> str:
        """
        Export Draw.io file to PNG using drawio CLI or conversion.

        Args:
            drawio_path: Path to .drawio file
            base_filename: Base filename for output
            output_dir: Output directory

        Returns:
            Path to PNG file or None if export failed
        """
        png_path = os.path.join(output_dir, f"{base_filename}.png")

        try:
            # Try using drawio CLI if available
            result = subprocess.run(
                [
                    "drawio",
                    "--export",
                    "--format",
                    "png",
                    "--output",
                    png_path,
                    drawio_path,
                ],
                capture_output=True,
                timeout=30,
            )

            if result.returncode == 0 and os.path.exists(png_path):
                return png_path
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            print(f"Note: drawio CLI not available ({e}). PNG export requires Draw.io.")
            print(
                f"You can manually export by opening {drawio_path} "
                f"in Draw.io and using File > Export as > PNG"
            )

        return None


def main():
    """Generate diagrams for all test examples with different output formats."""

    print("=" * 60)
    print("MBSE Diagram Generator - Creating Visual Diagrams")
    print("=" * 60)
    print("\nOutput Format Options:")
    print("  - DRAWIO: .drawio file only")
    print("  - PNG: PNG image only (requires Draw.io CLI)")
    print("  - BOTH: Both .drawio and PNG files")
    print()

    # Example 1: Calculator (DRAWIO only)
    print("\n[1] Generating Calculator Diagram (DRAWIO)...")
    notation1 = """
    {calculator}-O(execute numerical operations)->[numerical results]
    {calculator}-∆{keypad}, {screen}, {processing chip}
    {keypad}-O(input numbers)->[numbers]->(sum numbers)->[number]->(display result)O-{screen}
    """

    generator = MBSEDiagramGenerator()
    paths1 = generator.generate(notation1, "example1_calculator", OutputFormat.DRAWIO)
    for path in paths1:
        print(f"   ✓ Created: {path}")

    # Example 2: Process Flow (try PNG)
    print("\n[2] Generating Process Flow Diagram (PNG if available)...")
    notation2 = """
    (read input)->[raw data]->(validate data)->[clean data]->(process data)->[results]
    """

    generator = MBSEDiagramGenerator()
    paths2 = generator.generate(notation2, "example2_process_flow", OutputFormat.BOTH)
    for path in paths2:
        print(f"   ✓ Created: {path}")

    # Example 3: Component Composition (BOTH)
    print("\n[3] Generating Component Composition Diagram (BOTH)...")
    notation3 = """
    {web application}-∆{frontend}, {backend}, {database}
    {frontend}-O(render UI)
    {backend}-O(process requests)
    """

    generator = MBSEDiagramGenerator()
    paths3 = generator.generate(
        notation3, "example3_component_composition", OutputFormat.BOTH
    )
    for path in paths3:
        print(f"   ✓ Created: {path}")

    print("\n" + "=" * 60)
    print("Diagram generation complete!")
    print("=" * 60)
    print("\nGenerated files:")
    all_paths = paths1 + paths2 + paths3
    for i, path in enumerate(all_paths, 1):
        print(f"  {i}. {path}")

    print("\n" + "=" * 60)
    print("Usage Examples:")
    print("=" * 60)
    print(
        """
# Generate Draw.io file only
generator = MBSEDiagramGenerator()
paths = generator.generate(notation, "my_diagram", OutputFormat.DRAWIO)

# Generate PNG only (requires Draw.io CLI)
paths = generator.generate(notation, "my_diagram", OutputFormat.PNG)

# Generate both formats
paths = generator.generate(notation, "my_diagram", OutputFormat.BOTH)
"""
    )


if __name__ == "__main__":
    main()
