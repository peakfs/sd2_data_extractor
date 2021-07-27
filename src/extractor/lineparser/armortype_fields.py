from typing import Match

from .common import Handler
from .storage import BaseStorage


class ArmorTypeParser(Handler):
    PATTERN = r'(\w+_?\d?)\s+is\s(\d+)$'
    KEY = 'armor_types'

    def __init__(self):
        super().__init__(self.PATTERN)

    def handle(self, matches: Match, storage: BaseStorage):
        if self.KEY not in storage.data.keys():
            storage.data[self.KEY] = []

        storage.data[self.KEY].append(matches.group(1))
