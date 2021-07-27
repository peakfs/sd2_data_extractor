import pytest
from src.extractor.lineparser.storage import BaseStorage


class TestBaseStorage:
    def test_can_create(self):
        actual = BaseStorage()

        assert isinstance(actual, BaseStorage)

    def test_data_default_is_empty_dict(self):
        expected = {}
        sut = BaseStorage()

        assert expected == sut.data

    def test_lat_item_default_is_none(self):
        expected = None
        sut = BaseStorage()

        assert expected == sut.last_item
