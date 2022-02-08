from typing import Match

import pytest

from extractor.lineparser.common import Handler
from extractor.lineparser.storage import BaseStorage


class HandlerStub(Handler):
    def handle(self, matches: Match, storage: BaseStorage):
        pass


@pytest.fixture
def sut():
    return HandlerStub


class TestHandler:
    def test_can_create(self, sut):
        actual = sut()
        assert isinstance(actual, Handler)

    def test_pattern_is_empty_if_not_set(self, sut):
        actual = sut()
        assert actual.pattern is None

    def test_pattern_is_set(self, sut):
        actual = sut('test-pattern')
        assert actual.pattern == 'test-pattern'
