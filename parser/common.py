from distutils.util import strtobool
from abc import ABC, abstractmethod
from typing import Any, Match

from .storage import BaseStorage

METER = 0.2


class Handler(ABC):
    _pattern = None

    def __init__(self, pattern=None):
        self._pattern = pattern

    @property
    def pattern(self):
        return self._pattern

    @abstractmethod
    def handle(self, matches: Match, storage: Any):
        raise NotImplementedError()


class ExportParser(Handler):
    PATTERN = r'export (\w+).*'

    def __init__(self):
        super().__init__(self.PATTERN)

    def handle(self, matches: Match, storage: BaseStorage):
        export_name = matches.group(1)
        storage.data[export_name] = {}
        storage.last_item = export_name


class PropertyParser(Handler):

    parsed_field_name = None
    PATTERN = r'^(\w+)\s+=\s+(.+)$'

    def __init__(self, pattern: str = None, parsed_field_name: str = None):
        self.parsed_field_name = parsed_field_name
        if not pattern:
            pattern = self.PATTERN

        super().__init__(pattern)

    @abstractmethod
    def transform_property(self, matches: Match, storage: BaseStorage):
        raise NotImplementedError('Parser not implemented!')

    def handle(self, matches: Match, storage: BaseStorage):
        self.transform_property(matches, storage)


class StringPropertyParser(PropertyParser):
    def __init__(self, field_name: str, parsed_field_name: str = None):
        pattern = fr'^\s*({field_name})\s*=\s*(.+)$'
        super().__init__(pattern, parsed_field_name)

    def transform_property(self, matches, storage: BaseStorage):

        if self.parsed_field_name:
            field_name = self.parsed_field_name
        else:
            field_name = matches.group(1)

        if matches.group(2) == 'nil':
            storage.data[storage.last_item][field_name] = None
        elif matches.group(2).startswith('~'):
            storage.data[storage.last_item][field_name] = matches.group(2)
        elif matches.group(2).startswith('\'') or matches.group(2).startswith('"'):
            storage.data[storage.last_item][field_name] = matches.group(2).strip('\'').strip('"')
        else:
            storage.data[storage.last_item][field_name] = matches.group(2)


class IntPropertyParser(PropertyParser):

    def __init__(self, field_name: str, parsed_field_name: str = None):
        pattern = fr'^({field_name})\s+=\s+(.+)$'
        super().__init__(pattern, parsed_field_name)

    def transform_property(self, matches: Match, storage: BaseStorage):

        if self.parsed_field_name:
            field_name = self.parsed_field_name
        else:
            field_name = matches.group(1)

        try:
            val = int(matches.group(2))
            storage.data[storage.last_item][field_name] = val
        except ValueError:
            pass


class FloatPropertyParser(PropertyParser):

    def __init__(self, field_name: str, parsed_field_name: str = None):
        pattern = fr'^({field_name})\s+=\s+(.+)$'
        super().__init__(pattern, parsed_field_name)

    def transform_property(self, matches: Match, storage: BaseStorage):

        if self.parsed_field_name:
            field_name = self.parsed_field_name
        else:
            field_name = matches.group(1)

        try:
            val = float(matches.group(2))
            storage.data[storage.last_item][field_name] = val
        except ValueError:
            pass


class BoolPropertyParser(PropertyParser):

    def __init__(self, field_name: str, parsed_field_name: str = None):
        pattern = fr'^({field_name})\s+=\s+(.+)$'
        super().__init__(pattern, parsed_field_name)

    def transform_property(self, matches: Match, storage: BaseStorage):

        if self.parsed_field_name:
            field_name = self.parsed_field_name
        else:
            field_name = matches.group(1)

        try:
            val = bool(strtobool(matches.group(2)))
            storage.data[storage.last_item][field_name] = val
        except ValueError:
            pass


class FormulaParser(PropertyParser):
    def __init__(self, field_name: str, parsed_field_name: str = None):
        pattern = fr'^\s*({field_name})\s+=.+\((\d+|\d+.\d+)\).+$'
        super().__init__(pattern, parsed_field_name)

    def transform_property(self, matches: Match, storage: BaseStorage):

        if self.parsed_field_name:
            field_name = self.parsed_field_name
        else:
            field_name = matches.group(1)

        try:
            val = int(matches.group(2))
            storage.data[storage.last_item][field_name] = val
        except ValueError:
            pass


class TupleParser(Handler):

    field_name = None
    parsed_field_name = None

    def __init__(self, field_name: str, parsed_field_name: str = None):
        pattern = r'\((\~\/?\w+|\d+|\d+\.?\d+), (\w+|\d+|\d+\.\d+)\),?'

        if field_name:
            self.field_name = field_name

        if parsed_field_name:
            self.parsed_field_name = parsed_field_name

        super().__init__(pattern)

    def parse_matches(self, matches: Match):
        return matches.group(1), matches.group(2)

    def handle(self, matches: Match, storage: BaseStorage):
        field_name = self.field_name

        if self.parsed_field_name:
            field_name = self.parsed_field_name

        storage.data[storage.last_item][field_name] = self.parse_matches(matches)


class IntTupleParser(TupleParser):
    def parse_matches(self, matches: Match):
        return int(matches.group(1)), int(matches.group(2))

class StringIntTupleParser(TupleParser):
    def parse_matches(self, matches: Match):
        return matches.group(1), int(matches.group(2))


class FloatTupleParser(TupleParser):
    def parse_matches(self, matches: Match):
        return float(matches.group(1)), float(matches.group(2))
