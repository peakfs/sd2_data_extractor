from typing import Any, Match

from .common import Handler
from .storage import BaseStorage

PARSE_PATTERN_HITVALUE = r'^\s+\(\w+\/(\w+),\s?(\d+(.\d+)?)\),?$'


class HitValueParser(Handler):
    def __init__(self):
        super().__init__(PARSE_PATTERN_HITVALUE)

    def handle(self, matches: Match, storage: BaseStorage):
        raise NotImplementedError('Handler not implemented!')


class IdlingHitValueParser(HitValueParser):

    KEY_ACCURACY_IDLING = 'accuracy_idle'

    def __init__(self):
        pattern = r'^\(\w+\/(Idling),\s?(\d+(.\d+)?)\),?$'
        super(HitValueParser, self).__init__(pattern)

    def handle(self, matches: Match, storage: BaseStorage):
        try:
            val = float(matches.group(2))
            storage.data[storage.last_item][self.KEY_ACCURACY_IDLING] = val
        except ValueError:
            pass


class MovingHitValueParser(HitValueParser):
    KEY_ACCURACY_MOVING = 'accuracy_moving'

    def __init__(self):
        pattern = r'^\(\w+\/(Moving),\s?(\d+(.\d+)?)\),?$'
        super(HitValueParser, self).__init__(pattern)

    def handle(self, matches: Match, storage: BaseStorage):
        try:
            val = float(matches.group(2))
            storage.data[storage.last_item][self.KEY_ACCURACY_MOVING] = val
        except ValueError:
            pass
