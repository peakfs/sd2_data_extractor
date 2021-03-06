from typing import Match

import pytest

from extractor.lineparser.common import Handler
from extractor.lineparser.storage import BaseStorage


class HandlerStub(Handler):
    def handle(self, matches: Match, storage: BaseStorage):
        pass


@pytest.fixture
def get_handler_stub():
    return HandlerStub()


@pytest.fixture
def get_handler_stub_with_pattern():
    return HandlerStub('test-pattern')


class TestHandler:
    def test_can_create(self, get_handler_stub):
        assert isinstance(get_handler_stub, Handler)

    def test_pattern_is_empty_if_not_set(self, get_handler_stub):
        assert get_handler_stub.pattern is None

    def test_pattern_is_set(self, get_handler_stub_with_pattern):
        assert get_handler_stub_with_pattern.pattern == 'test-pattern'
