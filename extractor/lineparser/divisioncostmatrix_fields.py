from typing import Match

from extractor.lineparser.common import Handler
from extractor.lineparser.storage import BaseStorage


class MatrixNameParser(Handler):
    PATTERN = r'^.*\b(\w+)\b\sis\sMAP.*$'
    KEY = 'cost_matrix_export_name'

    def __init__(self):
        super().__init__(self.PATTERN)

    def handle(self, matches: Match, storage: BaseStorage):
        storage.last_item = matches.group(1)
        storage.data[matches.group(1)] = {}


class UnitCategorySlotsParser(Handler):
    PATTERN = r'^\s*\(\s?\b(\w+\/\w+)\b,\s*\[(.*)\]\s?\).*$'

    def __init__(self):
        super().__init__(self.PATTERN)

    def handle(self, matches: Match, storage: BaseStorage):
        costs = []

        for slot_cost in matches.group(2).rstrip(',').split(','):
            costs.append(int(slot_cost))

        storage.data[storage.last_item][matches.group(1)] = costs
