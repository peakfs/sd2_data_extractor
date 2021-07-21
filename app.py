#! /usr/bin/python3
import os
from pathlib import Path
from time import process_time

from database.Ammunition import Ammunition
from database.DamageRange import DamageRange
from database.Weapon import Weapon
from database.WeaponAmmunition import WeaponAmmunition
from database.Unit import Unit
from database.Specialty import Specialty
from database.UnitSpecialty import UnitSpecialty
from database.base import create_schemas, get_session

from fileprocessor.AmmunitionNdfProcessor import AmmunitionNdfProcessor
from fileprocessor.DivisionsNdfProcessor import DivisionsNdfProcessor
from fileprocessor.DTEORDNdfProcessor import DTEORDNdfProcessor
from fileprocessor.WeaponDescriptorNdfProcessor import WeaponDescriptorNdfProcessor
from fileprocessor.ArmureTypeNdfProcessor import ArmureTypeNdfProcessor
from fileprocessor.UniteNdfProcessor import UniteNdfProcessor
from fileprocessor.UnitSpecialtiesNdfProcessor import UnitSpecialtiesNdfProcessor

from config import MODFILES_DIR


def export_ammunition():
    parsed_ammunition = AmmunitionNdfProcessor().parse_file(MODFILES_DIR / 'GameData/Generated/Gameplay/Gfx/Ammunition.ndf')

    with get_session() as session:
        for name, export_data in parsed_ammunition.items():
            if export_data['dmg_type_over_range_descriptor']:
                export_data['dmg_type_over_range_descriptor'] = export_data['dmg_type_over_range_descriptor'].lstrip('~/')

            session.add(Ammunition(export_name=name, **export_data))

        session.commit()


def export_damage_range_tables():
    parsed_damage_range_tables = DTEORDNdfProcessor().parse_file(MODFILES_DIR / 'GameData/Generated/Gameplay/Gfx/DamageTypeEvolutionOverRangeDescriptor.ndf')

    with get_session() as session:
        for name, export_data in parsed_damage_range_tables.items():
            if 'ranges' not in export_data.keys():
                continue

            for rng, pen in export_data['ranges']:
                session.add(
                    DamageRange(
                        export_name=name,
                        range_percentage=rng,
                        penetration_percentage=pen
                    )
                )

        session.commit()


def export_weapons():
    weapon_export_data = WeaponDescriptorNdfProcessor().parse_file(MODFILES_DIR / 'GameData/Generated/Gameplay/Gfx/WeaponDescriptor.ndf')

    with get_session() as session:
        for key, weapon_data in weapon_export_data.items():
            session.add(Weapon(export_name=key))

            plist = list(zip(weapon_data['salvos'], weapon_data['ammunition']))

            for salvo, ammunition in plist:
                session.add(
                    WeaponAmmunition(
                        weapon_export_name=key,
                        ammunition_export_name=ammunition,
                        salvos=salvo
                    )
                )
        session.commit()


def export_units():
    unit_export_data = UniteNdfProcessor().parse_file(MODFILES_DIR / 'GameData/Generated/Gameplay/Gfx/UniteDescriptor.ndf')

    with get_session() as session:
        for key, unit_data in unit_export_data.items():
            specialties = unit_data.pop('specialties', None)

            if specialties:
                for spec in specialties:
                    session.add(UnitSpecialty(unit_export_name=key, specialty_export_key=spec))

            session.add(Unit(export_name=key, **unit_data))

        session.commit()


def export_unit_specialties():
    specialty_export_data = UnitSpecialtiesNdfProcessor().parse_file(MODFILES_DIR / 'GameData/Generated/UserInterface/UnitSpecialties.ndf')

    with get_session() as session:
        for key, specialty_data in specialty_export_data.items():
            session.add(Specialty(export_key=key, **specialty_data))

        session.commit()


def get_armor_types():
    return ArmureTypeNdfProcessor().parse_file(MODFILES_DIR / 'CommonData/Gameplay/Constantes/Enumerations/ArmureType.ndf')


# def export_divisions():
#     parsed_divisions = DivisionsNdfProcessor().parse_file(APP_DIR / 'assets/GameData/Generated/Gameplay/Decks/Divisions.ndf')
#     print(parsed_divisions)
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


def main():
    os.remove('sd2.db')
    tstart = process_time()

    create_schemas()

    export_unit_specialties()
    export_units()

    export_ammunition()
    # export_divisions()
    export_damage_range_tables()
    export_weapons()

    tend = process_time()

    print(f'Process ran for: {tend-tstart}(s)')


if __name__ == '__main__':
    main()
