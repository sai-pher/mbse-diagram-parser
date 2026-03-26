"""Tests for MBSE text notation parser."""

import pytest
from mbse_diagram_parser import (
    MBSEParser,
    ElementType,
    ConnectionType,
)


class TestMBSEParser:
    """Test suite for MBSEParser."""

    def test_parse_single_component(self):
        """Parse notation with single component element."""
        parser = MBSEParser()
        result = parser.parse("{calculator}")

        assert len(result.elements) == 1
        assert result.elements[0].name == "calculator"
        assert result.elements[0].type == ElementType.COMPONENT

    def test_parse_single_process(self):
        """Parse notation with single process element."""
        parser = MBSEParser()
        result = parser.parse("(execute operations)")

        assert len(result.elements) == 1
        assert result.elements[0].name == "execute operations"
        assert result.elements[0].type == ElementType.PROCESS

    def test_parse_single_data(self):
        """Parse notation with single data element."""
        parser = MBSEParser()
        result = parser.parse("[numerical results]")

        assert len(result.elements) == 1
        assert result.elements[0].name == "numerical results"
        assert result.elements[0].type == ElementType.DATA

    def test_parse_data_flow_connection(self):
        """Parse notation with data flow connection."""
        parser = MBSEParser()
        result = parser.parse("(process)->[data]")

        assert len(result.elements) == 2
        assert len(result.connections) == 1
        assert result.connections[0].type == ConnectionType.DATA_FLOW

    def test_parse_process_connection(self):
        """Parse notation with process connection."""
        parser = MBSEParser()
        result = parser.parse("{component}-O(process)")

        assert len(result.elements) == 2
        assert len(result.connections) == 1
        assert result.connections[0].type == ConnectionType.PROCESS_CONNECTION

    def test_parse_composition(self):
        """Parse notation with composition relationship."""
        parser = MBSEParser()
        result = parser.parse("{calculator}-∆{keypad}, {screen}")

        assert len(result.elements) == 3
        assert len(result.connections) == 2
        assert result.connections[0].type == ConnectionType.COMPOSITION
        assert result.connections[1].type == ConnectionType.COMPOSITION

    def test_parse_complex_line(self):
        """Parse complex notation with multiple connections."""
        parser = MBSEParser()
        notation = "{keypad}-O(input)->[data]->(process)->[result]"
        result = parser.parse(notation)

        assert len(result.elements) == 5
        assert len(result.connections) == 4

    def test_parse_multiline_notation(self):
        """Parse multiline notation."""
        parser = MBSEParser()
        notation = """
        {calculator}-O(execute operations)
        {calculator}-∆{keypad}, {screen}
        """
        result = parser.parse(notation)

        assert len(result.elements) == 4  # calculator, execute ops, keypad, screen
        assert len(result.connections) == 3  # 1 process conn + 2 composition

    def test_ignore_empty_lines(self):
        """Parse notation ignoring empty lines."""
        parser = MBSEParser()
        notation = """
        {component1}

        {component2}
        """
        result = parser.parse(notation)

        assert len(result.elements) == 2

    def test_ignore_comment_lines(self):
        """Parse notation ignoring comment lines."""
        parser = MBSEParser()
        notation = """
        # This is a comment
        {component}
        # Another comment
        """
        result = parser.parse(notation)

        assert len(result.elements) == 1
        assert result.elements[0].name == "component"

    def test_element_id_generation(self):
        """Verify element IDs are generated correctly."""
        parser = MBSEParser()
        result = parser.parse("{My Component}")

        assert result.elements[0].id == "my_component"

    def test_duplicate_elements_not_added(self):
        """Verify duplicate elements are not added twice."""
        parser = MBSEParser()
        notation = """
        {calculator}
        {calculator}-O(process)
        """
        result = parser.parse(notation)

        # calculator should only appear once
        components = [e for e in result.elements if e.type == ElementType.COMPONENT]
        assert len(components) == 1

    def test_get_element_by_name(self):
        """Test getting element by name."""
        parser = MBSEParser()
        result = parser.parse("{calculator}")

        elem = result.get_element_by_name("calculator")
        assert elem is not None
        assert elem.name == "calculator"

    def test_get_element_by_name_not_found(self):
        """Test getting non-existent element returns None."""
        parser = MBSEParser()
        result = parser.parse("{calculator}")

        elem = result.get_element_by_name("nonexistent")
        assert elem is None

    def test_to_dict_conversion(self):
        """Test conversion of parsed diagram to dictionary."""
        parser = MBSEParser()
        result = parser.parse("{comp}-O(proc)")

        data = parser.to_dict()

        assert "elements" in data
        assert "connections" in data
        assert len(data["elements"]) == 2
        assert len(data["connections"]) == 1
        assert data["elements"][0]["type"] == "component"
        assert data["connections"][0]["type"] == "-O"

    def test_calculator_example(self):
        """Test full calculator example from documentation."""
        parser = MBSEParser()
        notation = """
        {calculator}-O(execute numerical operations)->[numerical results]
        {calculator}-∆{keypad}, {screen}, {processing chip}
        """
        result = parser.parse(notation)

        # Verify elements
        assert len(result.elements) >= 6
        component_names = [
            e.name for e in result.elements if e.type == ElementType.COMPONENT
        ]
        assert "calculator" in component_names
        assert "keypad" in component_names
        assert "screen" in component_names
        assert "processing chip" in component_names

        # Verify connections
        assert len(result.connections) >= 4  # 1 proc + 1 data + 3 composition


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_parse_empty_string(self):
        """Parse empty notation string."""
        parser = MBSEParser()
        result = parser.parse("")

        assert len(result.elements) == 0
        assert len(result.connections) == 0

    def test_parse_only_whitespace(self):
        """Parse notation with only whitespace."""
        parser = MBSEParser()
        result = parser.parse("   \n  \n  ")

        assert len(result.elements) == 0
        assert len(result.connections) == 0

    def test_parse_malformed_composition(self):
        """Parse malformed composition notation."""
        parser = MBSEParser()
        result = parser.parse("-∆{component}")  # Missing parent

        # Should handle gracefully without crashing
        assert isinstance(result.elements, list)
        assert isinstance(result.connections, list)

    def test_parse_special_characters_in_names(self):
        """Parse elements with special characters in names."""
        parser = MBSEParser()
        result = parser.parse("{My-Component_123}")

        assert len(result.elements) == 1
        assert result.elements[0].name == "My-Component_123"
        # ID should have special chars replaced
        assert result.elements[0].id == "my_component_123"
