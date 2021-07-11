import re
from collections import namedtuple

RangePenetrationValue = namedtuple('RangePenetrationValue', ['range', 'penetration'])


class DamageTypeOverRangeParser:
    last_damage_type = None

    def __init__(self):
        self.damage_type_over_range = {}
        self.parser_methods = [
            self.parse_damage_type,
            self.parse_range_penetration_value,
        ]

    @property
    def parsed_data(self):
        return self.damage_type_over_range

    def parse(self, line: str):
        for parser_method in self.parser_methods:
            if parser_method(line):
                break

    def find_last_damage_type(self):
        if self.last_damage_type in self.damage_type_over_range.keys():
            return self.damage_type_over_range[self.last_damage_type]

        return None

    def parse_damage_type(self, line: str):
        if not line.startswith('export'):
            return False

        matches = re.match(r'export (.+) is', line)
        if matches:
            descriptor = matches.group(1)
            self.last_damage_type = descriptor
            self.damage_type_over_range[descriptor] = {
                'descriptor': descriptor,
                'values': []
            }

        return True

    def parse_range_penetration_value(self, line: str):
        pattern = r'\((\d+),\s?(\d+)\),?'
        matches = re.findall(pattern, line)

        if not matches:
            return False

        gun_range = float(matches[0][0])
        penetration = int(matches[0][1])

        dmg_type = self.find_last_damage_type()
        dmg_type['values'].append(RangePenetrationValue(range=gun_range, penetration=penetration))

        return True
