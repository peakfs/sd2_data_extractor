import re


class UnitParser:

    last_unit = None

    def __init__(self):
        self.units = {}
        self.parser_methods = [
        ]

    @property
    def parsed_data(self):
        return self.units

    def parse(self, line: str):
        for parser_method in self.parser_methods:
            if parser_method(line):
                break

    def parse_descriptor(self, line: str):
        pass

    def parse_type(self, line: str):
        pass

    def parse_nationale(self, line: str):
        pass

    def parse_country(self, line: str):
        pass

    def parse_tag(self, line: str):
        pass

    def parse_weapon(self, line: str):
        pass
