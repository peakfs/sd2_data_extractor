#! /usr/bin/python3

from pathlib import Path
from fileprocessor.AmmunitionNdfProcessor import AmmunitionNdfProcessor
from parser.storage import BaseStorage

APP_DIR = Path(__file__).parent


def main():
    p = AmmunitionNdfProcessor(BaseStorage())
    p.parse_file(APP_DIR / 'assets/GameData/Generated/Gameplay/Gfx/Ammunition.ndf')


#
# def parse_divisions():
#     parser = DivisionParser()
#     parse_file(APP_DIR / 'assets/GameData/Generated/Gameplay/Decks/Divisions.ndf', parser)
#
#     return parser.parsed_data
#
#
# def parse_decks(parsed_divisions):
#     parser = DivisionRulesParser(parsed_divisions)
#     parse_file(APP_DIR / 'assets/GameData/Generated/Gameplay/Decks/DivisionRules.ndf', parser)
#
#     return parser.parsed_data
#
#
# def parse_division_cost_matrices(parsed_divisions):
#     parser = DivisionCostMatrixParser(parsed_divisions)
#     parse_file(APP_DIR / 'assets/GameData/Gameplay/Decks/DivisionCostMatrix.ndf', parser)
#
#     return parser.parsed_data
#
#
# def parse_ammunition():
#     parser = AmmunitionParser()
#     parse_file(APP_DIR / 'assets/GameData/Generated/Gameplay/Gfx/Ammunition.ndf', parser)
#
#     return parser.parsed_data
#
#
# def parse_weapons():
#     parser = WeaponParser()
#     parse_file(APP_DIR / 'assets/GameData/Generated/Gameplay/Gfx/WeaponDescriptor.ndf', parser)
#
#     return parser.parsed_data
#
#
# def parse_range_tables():
#     parser = DamageTypeOverRangeParser()
#     parse_file(APP_DIR / 'assets/GameData/Generated/Gameplay/Gfx/DamageTypeEvolutionOverRangeDescriptor.ndf', parser)
#
#     return parser.parsed_data
#
#
# def parse_units():
#     parser = UnitParser()
#     parse_file(APP_DIR / 'assets/GameData/Generated/Gameplay/Gfx/UniteDescriptor.ndf', parser)
#
#     return parser.parsed_data
#

# def calculate_rof(raw_ammo):

#     burst_length = (raw_ammo['shot_per_burst'] - 1.0) * raw_ammo['time_between_shots']

#     rof = (
#               60 / (
#                   burst_length + raw_ammo['time_between_bursts']
#                 )
#           ) * raw_ammo['shot_per_burst']

#     if raw_ammo['category'] == 'rifle' or raw_ammo['category'] == 'law':
#         rof = rof * raw_ammo['amount']

#     if raw_ammo['category'] in ['lmg', 'mmg', 'smg', 'hmg']:
#         rof = rof * raw_ammo['supply_used_per_burst'] * 0.5

#     return rof


if __name__ == '__main__':
    # divisions = parse_divisions()
    # decks = parse_decks(divisions)
    # costs = parse_division_cost_matrices(divisions)
    # ammo = parse_ammunition()
    # weapons = parse_weapons()
    # ranges = parse_range_tables()
    # units = parse_units()

    main()
