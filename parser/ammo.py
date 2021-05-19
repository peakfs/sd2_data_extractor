import re
from distutils.util import strtobool

from .common import METER


class AmmunitionParser:
    last_ammo = None

    def __init__(self):
        self.ammunition = {}
        self.parser_methods = [
            self.parse_ammo,
            self.parse_ammo_type,
            self.parse_ammo_category,
            self.parse_caliber,
            self.parse_is_apcr,
            self.parse_projectile_type,
            self.parse_power,
            self.parse_max_range,
            self.parse_min_range,
            self.parse_range_ha,
            self.parse_dispersion_at_min_range,
            self.parse_dispersion_at_max_range,
            self.parse_damage,
            self.parse_suppression_damage,
            self.parse_is_indirect_fire,
            self.parse_is_direct_fire,
            self.parse_shot_per_burst,
            self.parse_time_between_shots,
            self.parse_time_between_bursts,
            self.parse_cause_friendly_fire,
            self.parse_is_armor_piercing,
            self.parse_aiming_time,
            self.parse_supply_used_per_burst,
            self.parse_stationary_accuracy,
            self.parse_moving_accuracy,
            self.parse_penetration_descriptor
        ]

    @property
    def parsed_data(self):
        return self.ammunition

    def parse(self, line: str):
        for parser_method in self.parser_methods:
            if parser_method(line):
                break

    def find_ammunition(self, descriptor):
        if descriptor in self.ammunition.keys():
            return self.ammunition[descriptor]

        return None

    def parse_ammo(self, line: str):
        if not line.startswith('export'):
            return False

        pattern = r'export (\w+)'
        matches = re.match(pattern, line)

        if matches:
            ammo = matches.group(1)

            new_ammo = {
                'descriptor': ammo,
                'amount': 1
            }

            amount_match = re.match(r'.*_x([0-9]+)', ammo)
            if amount_match:
                new_ammo['amount'] = int(amount_match.group(1))

            self.ammunition[ammo] = new_ammo

            self.last_ammo = ammo

        return True

    def parse_caliber(self, line: str):
        if not line.startswith('Caliber'):
            return False

        self.ammunition[self.last_ammo]['caliber'] = line.split('=')[1].strip().strip('\'')
        return True

    def parse_ammo_type(self, line: str):
        if not line.startswith('Arme'):
            return False

        self.ammunition[self.last_ammo]['type'] = line.split('=')[1].strip()
        return True

    def parse_ammo_category(self, line: str):
        if not line.startswith('TypeArme'):
            return False

        self.ammunition[self.last_ammo]['category'] = line.split('=')[1].strip().strip('\'').lower()
        return True

    def parse_is_apcr(self, line: str):
        if not line.startswith('IsAPCR'):
            return False

        self.ammunition[self.last_ammo]['is_apcr'] = bool(strtobool(line.split('=')[1].strip().lower()))
        return True

    def parse_projectile_type(self, line: str):
        if not line.startswith('ProjectileType'):
            return False

        self.ammunition[self.last_ammo]['projectile_type'] = line.split('=')[1].strip()
        return True

    def parse_power(self, line: str):
        if not line.startswith('Puissance'):
            return False

        self.ammunition[self.last_ammo]['power'] = float(line.split('=')[1].strip())
        return True

    def parse_max_range(self, line: str):

        line_matches = re.match(r'^PorteeMaximale +=.*', line)
        if not line_matches:
            return False

        matches = re.findall(r'\d+', line)

        if matches:
            max_range = int(matches[0]) * METER

            self.ammunition[self.last_ammo]['max_range'] = max_range
        return True

    def parse_min_range(self, line: str):

        line_matches = re.match(r'^PorteeMinimale +=.*', line)
        if not line_matches:
            return False

        matches = re.findall(r'\d+', line)

        if matches:
            max_range = int(matches[0]) * METER

            self.ammunition[self.last_ammo]['min_range'] = max_range
        return True

    def parse_range_ha(self, line: str):

        line_matches = re.match(r'^PorteeMaximaleHA +=.*', line)
        if not line_matches:
            return False

        matches = re.findall(r'\d+', line)

        if matches:
            max_range = int(matches[0]) * METER

            self.ammunition[self.last_ammo]['max_range_ha'] = max_range
        return True

    def parse_dispersion_at_min_range(self, line: str):
        if not line.startswith('DispersionAtMinRange'):
            return False

        matches = re.findall(r'\d+', line)

        if matches:
            dispersion_at_max_range = int(matches[0]) * METER
            self.ammunition[self.last_ammo]['dispersion_at_min_range'] = dispersion_at_max_range
        return True

    def parse_dispersion_at_max_range(self, line: str):
        if not line.startswith('DispersionAtMaxRange'):
            return False

        matches = re.findall(r'\d+', line)

        if matches:
            dispersion_at_max_range = int(matches[0]) * METER
            self.ammunition[self.last_ammo]['dispersion_at_max_range'] = dispersion_at_max_range
        return True

    def parse_damage(self, line: str):
        if not line.startswith('PhysicalDamages'):
            return False

        self.ammunition[self.last_ammo]['damage'] = float(line.split('=')[1].strip())
        return True

    def parse_suppression_damage(self, line: str):
        if not line.startswith('SuppressDamages'):
            return False

        self.ammunition[self.last_ammo]['suppression_damage'] = float(line.split('=')[1].strip())
        return True

    def parse_is_indirect_fire(self, line: str):
        if not line.startswith('TirIndirect'):
            return False

        self.ammunition[self.last_ammo]['indirect_fire'] = bool(strtobool(line.split('=')[1].strip().lower()))
        return True

    def parse_is_direct_fire(self, line: str):
        if not line.startswith('TirReflexe'):
            return False

        self.ammunition[self.last_ammo]['direct_fire'] = bool(strtobool(line.split('=')[1].strip().lower()))
        return True

    def parse_shot_per_burst(self, line: str):
        if not line.startswith('NbTirParSalves'):
            return False

        self.ammunition[self.last_ammo]['shot_per_burst'] = int(line.split('=')[1].strip())
        return True

    def parse_time_between_shots(self, line: str):
        line_matches = re.match(r'^TempsEntreDeuxTirs +=.*', line)
        if not line_matches:
            return False

        self.ammunition[self.last_ammo]['time_between_shots'] = float(line.split('=')[1].strip())
        return True

    def parse_time_between_bursts(self, line: str):
        line_matches = re.match(r'^TempsEntreDeuxSalves +=.*', line)
        if not line_matches:
            return False

        self.ammunition[self.last_ammo]['time_between_bursts'] = float(line.split('=')[1].strip())
        return True

    def parse_cause_friendly_fire(self, line: str):
        if not line.startswith('IsHarmlessForAllies'):
            return False

        self.ammunition[self.last_ammo]['friendly_fire'] = not bool(strtobool(line.split('=')[1].strip().lower()))
        return True

    def parse_is_armor_piercing(self, line: str):
        if not line.startswith('PiercingWeapon'):
            return False

        self.ammunition[self.last_ammo]['armor_piercing'] = bool(strtobool(line.split('=')[1].strip().lower()))
        return True

    def parse_aiming_time(self, line: str):
        if not line.startswith('TempsDeVisee'):
            return False

        self.ammunition[self.last_ammo]['aiming_time'] = float(line.split('=')[1].strip())
        return True

    def parse_supply_used_per_burst(self, line: str):
        if not line.startswith('AffichageMunitionParSalve'):
            return False

        self.ammunition[self.last_ammo]['supply_used_per_burst'] = float(line.split('=')[1].strip())
        return True

    def parse_stationary_accuracy(self, line: str):
        matches = re.findall(r'\(EBaseHitValueModifier/Idling, (\d+(.\d+)?)\),?', line)
        if not matches or len(matches) == 0:
            return False

        if 'stationary_accuracy' not in self.ammunition[self.last_ammo].keys():
            self.ammunition[self.last_ammo]['stationary_accuracy'] = float(matches[0][0])

        return True

    def parse_moving_accuracy(self, line: str):
        matches = re.findall(r'\(EBaseHitValueModifier/Moving, (\d+(.\d+)?)\),?', line)
        if not matches or len(matches) == 0:
            return False

        if 'moving_accuracy' not in self.ammunition[self.last_ammo].keys():
            self.ammunition[self.last_ammo]['moving_accuracy'] = float(matches[0][0])

        return True

    def parse_penetration_descriptor(self, line: str):
        if not line.startswith('DamageTypeEvolutionOverRangeDescriptor'):
            return False

        pen_descriptor = line.split('=')[1].strip().lstrip('~/')

        self.ammunition[self.last_ammo]['penetration_descriptor'] = pen_descriptor if pen_descriptor != 'nil' else None
        return True
