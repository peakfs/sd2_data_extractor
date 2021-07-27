from typing import Match

from .common import Handler
from .storage import BaseStorage


class DeckParser(Handler):

    PATTERN = r'^\s*\(~/(\w+),?\s?(\d+)\).*$'
    KEY = 'decks'

    def __init__(self, field_name: str = None):

        super().__init__(self.PATTERN)

        if field_name:
            self.field_name = field_name
        else:
            self.field_name = self.KEY

    def handle(self, matches: Match, storage: BaseStorage):

        if self.field_name not in storage.data[storage.last_item].keys():
            storage.data[storage.last_item][self.field_name] = []

        storage.data[storage.last_item][self.field_name].append(matches.group(1))
