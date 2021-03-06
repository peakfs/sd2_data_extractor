"""
Contains data parsing classes that are commonly used in fileprocessors.
"""
from abc import ABC, abstractmethod
from distutils.util import strtobool
from typing import Match

from .storage import BaseStorage


class Handler(ABC):
    """Base class that provides the base for line lineparser methods."""
    _pattern = None

    def __init__(self, pattern=None):
        self._pattern = pattern

    @property
    def pattern(self) -> str:
        """
        The pattern that will be matched against the actual line from
        the processed file.

        :return pattern: The pattern that will be used in line matching.
        :type pattern: string
        """
        return self._pattern

    @abstractmethod
    def handle(self, matches: Match, storage: BaseStorage):
        """
        This method will run after a successful pattern match against
        the actual line.
        """
        raise NotImplementedError()


class ExportParser(Handler):
    """
    Class that parses every line that matches the provided pattern.

    From the matched lines we will store the matched value as the last
    item in the storage.
    """
    PATTERN = r'^.*export \b(.+)\b\sis\s.*$'

    def __init__(self):
        super().__init__(self.PATTERN)

    def handle(self, matches: Match, storage: BaseStorage):
        export_name = matches.group(1)
        storage.data[export_name] = {}
        storage.last_item = export_name


class PropertyParser(Handler):
    """
    Class that parsers property like lines.

    From the matched line we will store the property name and the
    property value.

    We define the `transform_property` method so we can transform the
    matched value types to whatever we would like.
    """

    field_name = None
    PATTERN = r'^\b(\w+)\b\s+=\s+(.+)$'

    def __init__(self, pattern: str = None, parsed_field_name: str = None):

        if parsed_field_name:
            self.field_name = parsed_field_name

        if not pattern:
            pattern = self.PATTERN

        super().__init__(pattern)

    @abstractmethod
    def transform_property(self, matches: Match, storage: BaseStorage):
        """
        Implementing this method, you can transform the output type of
        the matched property value.
        """
        raise NotImplementedError()

    def handle(self, matches: Match, storage: BaseStorage):

        if not self.field_name:
            self.field_name = matches.group(1)

        self.transform_property(matches, storage)


class StringPropertyParser(PropertyParser):
    def __init__(self, field_name: str, parsed_field_name: str = None):
        pattern = fr'^\s*\b({field_name})\b\s*=\s*(.+)$'
        super().__init__(pattern, parsed_field_name)

    def transform_property(self, matches, storage: BaseStorage):

        if matches.group(2) == 'nil':
            storage.data[storage.last_item][self.field_name] = None
        elif matches.group(2).startswith('~'):
            storage.data[storage.last_item][self.field_name] = matches.group(2)
        elif matches.group(2).startswith('\'') or matches.group(2).startswith('"'):
            storage.data[storage.last_item][self.field_name] = matches.group(2).strip('\'').strip('"')
        else:
            storage.data[storage.last_item][self.field_name] = matches.group(2)


class IntPropertyParser(PropertyParser):

    def __init__(self, field_name: str, parsed_field_name: str = None):
        pattern = fr'^\b({field_name})\b\s+=\s+(.+)$'
        super().__init__(pattern, parsed_field_name)

    def transform_property(self, matches: Match, storage: BaseStorage):
        try:
            val = int(matches.group(2))
            storage.data[storage.last_item][self.field_name] = val
        except ValueError:
            pass


class FloatPropertyParser(PropertyParser):

    def __init__(self, field_name: str, parsed_field_name: str = None):
        pattern = fr'^\b({field_name})\b\s+=\s+(.+)$'
        super().__init__(pattern, parsed_field_name)

    def transform_property(self, matches: Match, storage: BaseStorage):
        try:
            val = float(matches.group(2))
            storage.data[storage.last_item][self.field_name] = val
        except ValueError:
            pass


class BoolPropertyParser(PropertyParser):

    def __init__(self, field_name: str, parsed_field_name: str = None):
        pattern = fr'^\b({field_name})\b\s+=\s+(.+)$'
        super().__init__(pattern, parsed_field_name)

    def transform_property(self, matches: Match, storage: BaseStorage):
        try:
            val = bool(strtobool(matches.group(2)))
            storage.data[storage.last_item][self.field_name] = val
        except ValueError:
            pass


class FormulaParser(Handler):
    field_name = None

    def __init__(self, field_name: str, parsed_field_name: str = None):
        pattern = fr'^\s*\b({field_name})\b.*=.*?(\d+\.?\d*).*$'

        if parsed_field_name:
            self.field_name = parsed_field_name

        super().__init__(pattern)

    def handle(self, matches: Match, storage: BaseStorage):
        try:
            val = int(matches.group(2))
        except ValueError:
            val = float(matches.group(2))

        storage.data[storage.last_item][self.field_name] = val


class TupleParser(Handler):
    field_name = None

    def __init__(self, field_name: str, parsed_field_name: str = None):
        pattern = r'^\s*\((\~\/?\w+|\d+\.?\d*),\s(\w+|\d+\.?\d*)\),?$'

        self.field_name = field_name

        if parsed_field_name:
            self.field_name = parsed_field_name

        super().__init__(pattern)

    def parse_matches(self, matches: Match):
        return matches.group(1), matches.group(2)

    def handle(self, matches: Match, storage: BaseStorage):
        if not self.field_name:
            self.field_name = storage.last_item

        storage.data[storage.last_item][self.field_name] = self.parse_matches(matches)


class IntTupleParser(TupleParser):
    def parse_matches(self, matches: Match):
        return int(matches.group(1)), int(matches.group(2))


class StringIntTupleParser(TupleParser):
    def parse_matches(self, matches: Match):
        return matches.group(1), int(matches.group(2))


class FloatTupleParser(TupleParser):
    def parse_matches(self, matches: Match):
        return float(matches.group(1)), float(matches.group(2))


class ListParser(Handler):

    def __init__(self, field_name: str, parsed_field_name: str = None):
        pattern = fr'^\s*\b({field_name})\b\s?=\s?\[(.+)\].*$'
        super().__init__(pattern)

        self.field_name = field_name

        if parsed_field_name:
            self.field_name = parsed_field_name

    def handle(self, matches: Match, storage: BaseStorage):
        storage.data[storage.last_item][self.field_name] = matches.group(2)


class DescriptorListParser(ListParser):
    def handle(self, matches: Match, storage: BaseStorage):
        storage.data[storage.last_item][self.field_name] = []

        for descriptor in matches.group(2).split(','):
            storage.data[storage.last_item][self.field_name].append(descriptor.strip().lstrip('~/'))


class IntListParser(ListParser):
    def handle(self, matches: Match, storage: BaseStorage):
        storage.data[storage.last_item][self.field_name] = []

        for descriptor in matches.group(2).split(','):
            storage.data[storage.last_item][self.field_name].append(
                int(descriptor.strip())
            )


class FloatListParser(ListParser):
    def handle(self, matches: Match, storage: BaseStorage):
        storage.data[storage.last_item][self.field_name] = []

        for descriptor in matches.group(2).split(','):
            storage.data[storage.last_item][self.field_name].append(
                float(descriptor.strip())
            )
