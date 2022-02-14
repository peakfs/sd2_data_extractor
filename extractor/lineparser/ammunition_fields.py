from typing import Match

from extractor.lineparser.common import Handler
from extractor.lineparser.storage import BaseStorage


class HitValueParser(Handler):
    def __init__(self):
        pattern = r'^\s+\(\w+\/(\w+),\s?(\d+(.\d+)?)\),?$'
        super().__init__(pattern)

    def handle(self, matches: Match, storage: BaseStorage):
        raise NotImplementedError('Handler not implemented!')


class IdlingHitValueParser(HitValueParser):
    parsed_field_name = None

    def __init__(self, parsed_field_name: str):
        pattern = r'^\(\w+\/(Idling),\s?(\d+(.\d+)?)\),?$'
        super(HitValueParser, self).__init__(pattern)
        self.parsed_field_name = parsed_field_name

    def handle(self, matches: Match, storage: BaseStorage):
        try:
            val = float(matches.group(2))
            storage.data[storage.last_item][self.parsed_field_name] = val
        except ValueError:
            pass


class MovingHitValueParser(HitValueParser):
    parsed_field_name = None

    def __init__(self, parsed_field_name: str):
        pattern = r'^\(\w+\/(Moving),\s?(\d+(.\d+)?)\),?$'
        super(HitValueParser, self).__init__(pattern)
        self.parsed_field_name = parsed_field_name

    def handle(self, matches: Match, storage: BaseStorage):
        try:
            val = float(matches.group(2))
            storage.data[storage.last_item][self.parsed_field_name] = val
        except ValueError:
            pass
