from typing import Match
from .common import Handler
from .storage import BaseStorage


class SalvoParser(Handler):

    KEY_SALVOS = 'salvos'
    PATTERN = r'(-?\d+),?'

    def __init__(self):
        super().__init__(self.PATTERN)

    def handle(self, matches: Match, storage: BaseStorage):
        try:
            val = int(matches.group(1))
            if self.KEY_SALVOS not in storage.data[storage.last_item].keys():
                storage.data[storage.last_item][self.KEY_SALVOS] = []

            if val > 0:
                storage.data[storage.last_item][self.KEY_SALVOS].append(val)
        except ValueError:
            pass


class AmmunitionParser(Handler):
    PATTERN = r'^(Ammunition)\s+=\s+(.+)$'
    KEY_AMMUNITION = 'ammunition'

    def __init__(self):
        super().__init__(self.PATTERN)

    def handle(self, matches: Match, storage: BaseStorage):

        if self.KEY_AMMUNITION not in storage.data[storage.last_item].keys():
            storage.data[storage.last_item][self.KEY_AMMUNITION] = []

        val = matches.group(2).lstrip('~/')

        storage.data[storage.last_item][self.KEY_AMMUNITION].append(val)
