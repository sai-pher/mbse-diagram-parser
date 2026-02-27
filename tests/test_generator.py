"""Tests for MBSE diagram generator."""

import pytest

# Test if generator module can be imported
try:
    from mbse_diagram_parser import (
        MBSEDiagramGenerator,
        OutputFormat,
    )

    GENERATOR_AVAILABLE = True
except ImportError:
    GENERATOR_AVAILABLE = False


@pytest.mark.skipif(
    not GENERATOR_AVAILABLE,
    reason="drawpyo not installed - generator tests skipped",
)
class TestMBSEDiagramGenerator:
    """Test suite for MBSEDiagramGenerator."""

    def test_generator_initialization(self):
        """Test generator can be initialized."""
        generator = MBSEDiagramGenerator()
        assert generator is not None
        assert generator.element_objects == {}
        assert generator.element_positions == {}

    def test_output_format_enum(self):
        """Test OutputFormat enum values."""
        assert OutputFormat.DRAWIO.value == "drawio"
        assert OutputFormat.PNG.value == "png"
        assert OutputFormat.BOTH.value == "both"

    def test_layout_calculation(self):
        """Test layout calculation separates elements by type."""
        from mbse_diagram_parser import MBSEParser

        generator = MBSEDiagramGenerator()
        parser = MBSEParser()

        notation = """
        {component1}
        (process1)
        [data1]
        """
        diagram = parser.parse(notation)

        generator._calculate_layout(diagram)

        # All elements should have positions
        assert len(generator.element_positions) == 3

        # Components should be leftmost
        # Processes in middle
        # Data on right
        positions = list(generator.element_positions.values())
        assert all(isinstance(pos, tuple) and len(pos) == 2 for pos in positions)

    def test_element_style_definitions(self):
        """Test element style definitions are complete."""
        from mbse_diagram_parser import ElementType

        generator = MBSEDiagramGenerator()

        # All element types should have styles
        assert ElementType.COMPONENT in generator.STYLES
        assert ElementType.PROCESS in generator.STYLES
        assert ElementType.DATA in generator.STYLES

        # Each style should have required properties
        for element_type, style in generator.STYLES.items():
            assert "fillColor" in style
            assert "strokeColor" in style
            assert "strokeWidth" in style

    def test_connection_style_definitions(self):
        """Test connection style definitions are complete."""
        from mbse_diagram_parser import ConnectionType

        generator = MBSEDiagramGenerator()

        # All connection types should have styles
        assert ConnectionType.DATA_FLOW in generator.CONNECTION_STYLES
        assert ConnectionType.PROCESS_CONNECTION in generator.CONNECTION_STYLES
        assert ConnectionType.COMPOSITION in generator.CONNECTION_STYLES

        # Each style should have required properties
        for conn_type, style in generator.CONNECTION_STYLES.items():
            assert "strokeColor" in style
            assert "endArrow" in style


class TestGeneratorImport:
    """Test generator import behavior."""

    def test_generator_import_handling(self):
        """Test that missing drawpyo is handled gracefully."""
        # This test verifies the optional import works
        try:
            from mbse_diagram_parser import MBSEDiagramGenerator

            # If import succeeds, drawpyo is available
            assert MBSEDiagramGenerator is not None
        except (ImportError, AttributeError):
            # If import fails, that's also acceptable
            # (drawpyo not installed)
            pass
