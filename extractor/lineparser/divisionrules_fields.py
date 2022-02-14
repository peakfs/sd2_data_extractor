from typing import Match

from extractor.lineparser.common import Handler
from extractor.lineparser.storage import BaseStorage


class DivisionParser(Handler):
    PATTERN = r'^\s*~/\b(\w+)\b,?.*$'

    def __init__(self):
        super().__init__(self.PATTERN)

    def handle(self, matches: Match, storage: BaseStorage):
        storage.last_item = matches.group(1)
        storage.data[matches.group(1)] = {}


class ReferencePropertyParser(Handler):

    def __init__(self, field_name: str, parsed_field_name: str = None):
        pattern = fr'^\s*\b({field_name})\b\s?=\s?~/\b(\w+)\b.*$'
        super().__init__(pattern)

        self.field_name = field_name

        if parsed_field_name:
            self.field_name = parsed_field_name

    def handle(self, matches: Match, storage: BaseStorage):
        storage.data[storage.last_item][self.field_name] = matches.group(2)
