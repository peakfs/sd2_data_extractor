from distutils.util import strtobool
from abc import ABC, abstractmethod
from typing import Any, Match

from .storage import BaseStorage

METER = 0.2
PARSE_PATTERN_PROPERTY = r'^(\w+)\s+=\s+(.+)$'
PARSE_PATTERN_EXPORT = r'^export (\w+) is \w+$'


class SkipLineError(TypeError):
    pass


class Handler(ABC):
    _pattern = None

    def __init__(self, pattern=None):
        self._pattern = pattern

    @property
    def pattern(self):
        return self._pattern

    @abstractmethod
    def handle(self, matches: Match, storage: Any):
        pass


class ExportParser(Handler):
    def __init__(self):
        super().__init__(PARSE_PATTERN_EXPORT)

    def handle(self, matches: Match, storage: BaseStorage):
        export_name = matches.group(1)
        storage.data[export_name] = {}
        storage.last_item = export_name


class PropertyParser(Handler):
    def __init__(self):
        super().__init__(PARSE_PATTERN_PROPERTY)

    @abstractmethod
    def transform_property(self, matches: Match, storage: BaseStorage):
        raise NotImplementedError('Parser not implemented!')

    def handle(self, matches: Match, storage: BaseStorage):
        self.transform_property(matches, storage)


class StringPropertyParser(PropertyParser):

    def __init__(self, field_name: str):
        pattern = fr'^({field_name})\s+=\s+(.+)$'
        super(PropertyParser, self).__init__(pattern)

    def transform_property(self, matches, storage: BaseStorage):
        if matches.group(2).startswith('\'') or matches.group(2).startswith('"'):
            storage.data[storage.last_item][matches.group(1)] = matches.group(2).strip('\'').strip('"')


class IntPropertyParser(PropertyParser):

    def __init__(self, field_name: str):
        pattern = fr'^({field_name})\s+=\s+(.+)$'
        super(PropertyParser, self).__init__(pattern)

    def transform_property(self, matches: Match, storage: BaseStorage):
        try:
            val = int(matches.group(2))
            storage.data[storage.last_item][matches.group(1)] = val
        except ValueError:
            pass


class FloatPropertyParser(PropertyParser):

    def __init__(self, field_name: str):
        pattern = fr'^({field_name})\s+=\s+(.+)$'
        super(PropertyParser, self).__init__(pattern)

    def transform_property(self, matches: Match, storage: BaseStorage):
        try:
            val = float(matches.group(2))
            storage.data[storage.last_item][matches.group(1)] = val
        except ValueError:
            pass


class BoolPropertyParser(PropertyParser):

    def __init__(self, field_name: str):
        pattern = fr'^({field_name})\s+=\s+(.+)$'
        super(PropertyParser, self).__init__(pattern)

    def transform_property(self, matches: Match, storage: BaseStorage):
        try:
            val = bool(strtobool(matches.group(2)))
            storage.data[storage.last_item][matches.group(1)] = val
        except ValueError:
            pass


class FormulaParser(PropertyParser):
    def __init__(self, field_name: str):
        pattern = fr'^({field_name})\s+=.+\((\d+)\).+$'
        super(PropertyParser, self).__init__(pattern)

    def transform_property(self, matches: Match, storage: BaseStorage):
        try:
            val = int(matches.group(2))
            storage.data[storage.last_item][matches.group(1)] = val
        except ValueError:
            pass
