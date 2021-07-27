from typing import Match

from .common import Handler
from .storage import BaseStorage


class SpecialtyKeyParser(Handler):
    PATTERN = r'^\s*\"\b(Spec_\w+)\b\".*$'

    def __init__(self):
        super().__init__(self.PATTERN)

    def handle(self, matches: Match, storage: BaseStorage):
        specialty_key = matches.group(1)
        storage.last_item = specialty_key
        storage.data[specialty_key] = {}
