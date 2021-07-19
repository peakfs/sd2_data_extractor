from typing import Match

from .common import Handler, StringIntTupleParser
from .storage import BaseStorage


class UnitWeaponParser(Handler):

    PATTERN = r'Default\s+=\s+\$/GFX/Everything/(\w+)$'

    parsed_field_name = 'weapon_export_name'

    def __init__(self, parsed_field_name: str = None):
        super().__init__(self.PATTERN)

        if parsed_field_name:
            self.parsed_field_name = parsed_field_name

    def handle(self, matches: Match, storage: BaseStorage):
        storage.data[storage.last_item][self.parsed_field_name] = matches.group(1)


class CommandPointsCostParser(StringIntTupleParser):
    def parse_matches(self, matches: Match):
        return int(matches.group(2))
