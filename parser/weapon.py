import re
from distutils.util import strtobool


class WeaponParser:
    last_weapon = None
    last_ammo = None

    def __init__(self):
        self.weapons = {}
        self.parser_methods = [
            self.parse_weapon,
            self.parse_salves,
            self.parse_ammo,
            self.parse_can_fire_while_moving
        ]

    @property
    def parsed_data(self):
        return self.weapons

    def parse(self, line: str):
        for parser_method in self.parser_methods:
            if parser_method(line):
                break

    def find_weapon(self, descriptor):
        if descriptor in self.weapons.keys():
            return self.weapons[descriptor]

        return None

    def get_last_weapon(self):
        if self.last_weapon in self.weapons.keys():
            return self.weapons[self.last_weapon]

        return None

    def get_last_ammo(self):
        last_weapon = self.get_last_weapon()
        if self.last_ammo in last_weapon['ammo']:
            index = last_weapon['ammo'].index(self.last_ammo)
            return last_weapon['ammo'][index]

        return None

    def parse_weapon(self, line: str):
        if not line.startswith('export'):
            return False

        pattern = r'export WeaponDescriptor_(\w+).*'
        matches = re.match(pattern, line)

        if matches:
            weapon = matches.group(1)
            self.weapons[weapon] = {
                'descriptor': weapon
            }

            self.last_weapon = weapon

        return True

    def parse_salves(self, line: str):
        matches = re.findall(r'^-?\d+,?$', line)

        if not matches:
            return False

        weapon = self.get_last_weapon()
        salve = int(matches[0].rstrip(','))

        if salve <= 0:
            return False

        if 'salves' not in weapon:
            weapon['salves'] = []

        weapon['salves'].append(salve)

        return True

    def parse_ammo(self, line: str):
        if not line.startswith('Ammunition'):
            return False

        ammo = line.split('=')[1].strip().lstrip('~/')
        weapon = self.get_last_weapon()

        if 'ammo' not in weapon:
            weapon['ammo'] = []

        weapon['ammo'].append(ammo)

        self.last_ammo = ammo

        return True

    def parse_can_fire_while_moving(self, line: str):
        if not line.startswith('TirEnMouvement'):
            return False

        can_fire_while_moving = bool(strtobool(line.split('=')[1].strip()))
        last_ammo = self.get_last_ammo()
        last_weapon = self.get_last_weapon()

        if last_ammo:
            ammo_index = last_weapon['ammo'].index(last_ammo)
            last_weapon['ammo'][ammo_index] = {
                'descriptor': last_ammo,
                'can_fire_while_moving': can_fire_while_moving
            }

        return True
