import re


class DivisionRulesParser:

    last_div = None
    last_unit = None
    divisions = {}

    def __init__(self, divisions):
        self.divisions = divisions
        self.parser_methods = [
            self.parse_division,
            self.parse_unit,
            self.parse_transports,
            self.parse_number_of_units,
            self.parse_xp_multiplier
        ]

    def parse(self, line: str):
        for parser_method in self.parser_methods:
            if parser_method(line):
                break

    @property
    def parsed_data(self):
        return self.divisions

    def parse_division(self, line: str):
        if not line.startswith('~/Descriptor_Deck_Division_'):
            return False

        pattern = r'~/Descriptor_Deck_Division_(\w+)'
        matches = re.match(pattern, line)

        if matches is not None and len(matches.groups()) == 1:
            div_descriptor = matches.group(1)

            if self.find_division(div_descriptor):
                self.last_div = div_descriptor

        return True

    def parse_unit(self, line: str):
        if not line.startswith('UnitDescriptor = ~/Descriptor_Unit_'):
            return False

        pattern = r'.*~/Descriptor_Unit_(\w+)'
        matches = re.match(pattern, line)

        if matches is not None:
            self.last_unit = matches.group(1)

        return True

    def parse_transports(self, line: str):
        if not line.startswith('AvailableTransportList'):
            return False

        parts = line.split('=')
        transport_list = parts[1].strip().strip('[]')
        pattern = r'(~/Descriptor_Unit_(\w+))(, )?'
        transports = re.findall(pattern, transport_list)
        if transports is not None:
            div = self.find_division(self.last_div)
            unit_pack = self.find_unit_pack(div, self.last_unit)

            if unit_pack and 'transports' not in unit_pack.keys():
                unit_pack['transports'] = []

                for transport in transports:
                    unit_pack['transports'].append(transport[1])

        return True

    def parse_number_of_units(self, line: str):
        if not line.startswith('NumberOfUnitInPackByPhase'):
            return False

        parts = line.split('=')
        amount_str = parts[1].strip().strip('[]').split(',')

        div = self.find_division(self.last_div)
        unit_pack = self.find_unit_pack(div, self.last_unit)

        if unit_pack and 'amount' not in unit_pack.keys():
            unit_pack['amount'] = []
            for amount in amount_str:
                unit_pack['amount'].append(int(amount))

        return True

    def parse_xp_multiplier(self, line: str):
        if not line.startswith('NumberOfUnitInPackXPMultiplier'):
            return False

        parts = line.split('=')
        amount_str = parts[1].strip().strip('[]').split(',')

        div = self.find_division(self.last_div)
        unit_pack = self.find_unit_pack(div, self.last_unit)

        if unit_pack and 'veterancy_multiplier' not in unit_pack.keys():
            unit_pack['veterancy_multiplier'] = []
            for amount in amount_str:
                unit_pack['veterancy_multiplier'].append(float(amount))

        return True

    def find_division(self, descriptor):
        for key, val in self.divisions.items():
            if val['descriptor'] == descriptor:
                return self.divisions[key]

        return None

    def find_unit_pack(self, division, descriptor):
        for unit_pack in division['unit_packs']:
            if unit_pack['descriptor'] == descriptor:
                return unit_pack
