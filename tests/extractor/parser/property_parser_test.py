import pytest
import re

from extractor.lineparser.common import PropertyParser
from extractor.lineparser.storage import BaseStorage


class StubPropertyParser(PropertyParser):
    def transform_property(self, matches, storage):
        storage.data[self.field_name] = matches.group(2)


TEST_PATTERN = r'^\s*(Level).*=.*(\d+).*$'


@pytest.fixture
def storage():
    return BaseStorage()


@pytest.fixture
def sut():
    return StubPropertyParser


class TestPropertyParser:
    def test_sets_default_pattern(self, sut):
        parser = sut()
        expected = parser.PATTERN
        actual = parser.pattern

        assert expected == actual

    def test_handle_parses_custom_pattern(self, sut, storage):
        parser = sut(pattern=TEST_PATTERN)
        expected_property_name = 'Level'
        expected_property_value = '3'
        line = 'Level                             = 3'
        matches = re.fullmatch(parser.pattern, line)

        parser.handle(matches, storage)

        assert expected_property_name == matches.group(1)
        assert expected_property_value == matches.group(2)
        assert expected_property_name in storage.data.keys()
        assert expected_property_value == storage.data[expected_property_name]

    def test_handle_sets_property_name_to_fieldname(self, sut, storage):
        parser = sut()

        expected_property_name = 'Level'
        expected_property_value = '3'
        line = 'Level                             = 3'
        matches = re.fullmatch(parser.pattern, line)

        parser.handle(matches, storage)

        assert expected_property_name == matches.group(1)
        assert expected_property_value == matches.group(2)
        assert expected_property_name in storage.data.keys()
        assert expected_property_value == storage.data[expected_property_name]

    def test_handle_sets_parsed_field_name_to_fieldname(self, sut, storage):
        parser = sut(parsed_field_name="FIELDNAME")

        expected_property_name = 'FIELDNAME'
        expected_property_value = '3'
        line = 'Level                             = 3'
        matches = re.fullmatch(parser.pattern, line)

        parser.handle(matches, storage)

        assert expected_property_name in storage.data.keys()
        assert expected_property_value == storage.data[parser.field_name]
