import re


class DivisionCostMatrixParser:

    last_div = None

    def __init__(self, divisions):
        self.divisions = divisions
        self.parser_methods = [
            self.parse_division,
            self.parse_costs
        ]

    @property
    def parsed_data(self):
        return self.divisions

    def parse(self, line: str):
        for parser_method in self.parser_methods:
            if parser_method(line):
                break

    def parse_division(self, line: str):
        if not line.startswith('MatrixCostName_'):
            return False

        pattern = r'MatrixCostName_(\w+) is MAP'
        matches = re.match(pattern, line)

        if matches and len(matches.groups()) == 1:
            div_descriptor = matches.group(1)

            if self.find_division(div_descriptor):
                self.last_div = div_descriptor

        return True

    def parse_costs(self, line: str):
        if not line.startswith('( EDefaultFactories'):
            return False

        if self.last_div:
            pattern = r'\( EDefaultFactories/(\w+),\s+(\[.*\]) \),?.*'
            matches = re.match(pattern, line)

            if matches:
                category = matches.group(1).lower()
                raw_slots = matches.group(2).strip('[]').rstrip(',').split(',')
                slots = list(map(int, raw_slots))

                div = self.find_division(self.last_div)

                if 'costs' not in div.keys():
                    div['costs'] = {}
                div['costs'][category] = slots
        return True

    def find_division(self, descriptor):
        for key, val in self.divisions.items():
            if val['descriptor'] == descriptor:
                return self.divisions[key]

        return None
