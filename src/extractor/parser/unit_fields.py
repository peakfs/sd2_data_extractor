from typing import Match

from .common import Handler, StringIntTupleParser
from .storage import BaseStorage


class UnitWeaponParser(Handler):

    PATTERN = r'Default\s+=\s+\$/GFX/Everything/(\w+)$'
    field_name = 'weapon_export_name'

    def __init__(self, parsed_field_name: str = None):
        super().__init__(self.PATTERN)

        if parsed_field_name:
            self.field_name = parsed_field_name

    def handle(self, matches: Match, storage: BaseStorage):
        storage.data[storage.last_item][self.field_name] = matches.group(1)


class CommandPointsCostParser(StringIntTupleParser):
    def parse_matches(self, matches: Match):
        return int(matches.group(2))


class SpecialtyParser(Handler):
    PATTERN = r'^\s*\'\b(Spec_\w+)\b\'.*$'
    KEY = 'specialties'

    def __init__(self):
        super().__init__(self.PATTERN)

    def handle(self, matches: Match, storage: BaseStorage):

        if self.KEY not in storage.data[storage.last_item].keys():
            storage.data[storage.last_item][self.KEY] = []

        storage.data[storage.last_item][self.KEY].append(matches.group(1))
