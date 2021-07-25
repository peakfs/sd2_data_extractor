#! /usr/bin/python3
import csv
import os
from time import process_time

from config import ASSETS_DIR, MODFILES_DIR
from database.Ammunition import Ammunition
from database.DamageRange import DamageRange
from database.Deck import Deck
from database.DeckUnit import DeckUnit
from database.Division import Division
from database.DivisionDeck import DivisionDeck
from database.Specialty import Specialty
from database.Unit import Unit
from database.UnitSpecialty import UnitSpecialty
from database.UnitTransport import UnitTransport
from database.Weapon import Weapon
from database.WeaponAmmunition import WeaponAmmunition
from database.base import create_schemas, get_session
from fileprocessor.AmmunitionNdfProcessor import AmmunitionNdfProcessor
from fileprocessor.ArmureTypeNdfProcessor import ArmureTypeNdfProcessor
from fileprocessor.DTEORDNdfProcessor import DTEORDNdfProcessor
from fileprocessor.DivisionsNdfProcessor import DivisionsNdfProcessor
from fileprocessor.DivisonRulesNdfProcessor import DivisionRulesNdfProcessor
from fileprocessor.UnitSpecialtiesNdfProcessor import UnitSpecialtiesNdfProcessor
from fileprocessor.UniteNdfProcessor import UniteNdfProcessor
from fileprocessor.WeaponDescriptorNdfProcessor import WeaponDescriptorNdfProcessor

LOCALISATION_ENTRIES = {}


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

    localisation = get_localisation_entries()

    with get_session() as session:
        for key, unit_data in unit_export_data.items():

            try:
                unit_data['name'] = localisation[unit_data['localisation_key']]
            except KeyError:
                unit_data['name'] = None

            specialties = unit_data.pop('specialties', None)

            if specialties:
                for spec in specialties:
                    session.add(UnitSpecialty(unit_export_name=key, specialty_export_key=spec))

            session.add(Unit(export_name=key, **unit_data))

        session.commit()


def export_unit_specialties():
    specialty_export_data = UnitSpecialtiesNdfProcessor().parse_file(MODFILES_DIR / 'GameData/Generated/UserInterface/UnitSpecialties.ndf')

    localisation = get_localisation_entries()

    with get_session() as session:
        for key, specialty_data in specialty_export_data.items():
            session.add(
                Specialty(
                    export_key=key,
                    title=localisation[specialty_data['title']],
                    description=localisation[specialty_data['description']]
                )
            )

        session.commit()


def export_decks():
    deck_export_data = DivisionRulesNdfProcessor().parse_file(MODFILES_DIR / 'GameData/Generated/Gameplay/Decks/DivisionRules.ndf')

    with get_session() as session:

        for deck, deck_data in deck_export_data.items():

            if not deck_data:
                continue

            session.add(Deck(export_name=deck))
            session.add(
                DeckUnit(
                    deck_export_name=deck,
                    unit_export_name=deck_data['unit_export_name'],
                    is_available_without_transport=deck_data['is_available_without_transport'],
                    max_cards=deck_data['max_cards'],
                    units_phase_a=deck_data['number_of_units'][0],
                    units_phase_b=deck_data['number_of_units'][1],
                    units_phase_c=deck_data['number_of_units'][2],
                    vet_multiplier_phase_a=deck_data['unit_count_exp_multiplier'][0],
                    vet_multiplier_phase_b=deck_data['unit_count_exp_multiplier'][1],
                    vet_multiplier_phase_c=deck_data['unit_count_exp_multiplier'][2]
                )
            )

            if 'available_transports' in deck_data.keys():
                for transport in deck_data['available_transports']:
                    session.add(
                        UnitTransport(
                            unit_export_name=deck_data['unit_export_name'],
                            unit_transport_name=transport
                        )
                    )

        session.commit()


def get_armor_types():
    return ArmureTypeNdfProcessor().parse_file(MODFILES_DIR / 'CommonData/Gameplay/Constantes/Enumerations/ArmureType.ndf')


def get_localisation_entries():
    if len(LOCALISATION_ENTRIES) == 0:
        with open(ASSETS_DIR / 'Utils/LocalisationEntries/Entries.csv', 'r') as locfile:
            reader = csv.reader(locfile, delimiter=';')
            for row in reader:
                # row[2] = localisation token e.g. ASGNNLOKYC
                # row[3] = localised name e.g. 0-ya Gv. Strelkovy Divizii
                LOCALISATION_ENTRIES[row[2]] = row[3]

    return LOCALISATION_ENTRIES


def export_divisions():
    parsed_divisions = DivisionsNdfProcessor().parse_file(MODFILES_DIR / 'GameData/Generated/Gameplay/Decks/Divisions.ndf')
    localisation = get_localisation_entries()

    with get_session() as session:

        for division, division_data in parsed_divisions.items():
            if division_data['division_type'] not in DivisionsNdfProcessor.TYPE_CLASSIFICATION_MAP:
                continue

            if 'decks' in division_data.keys():
                for deck in division_data['decks']:
                    session.add(
                        DivisionDeck(
                            division_export_name=division,
                            deck_export_name=deck
                        )
                    )

            name = division_data['name']
            description = division_data['description']
            pwr_classification = DivisionsNdfProcessor.POWER_CLASSIFICATION_MAP[division_data['power_classification']]
            type_classification = DivisionsNdfProcessor.TYPE_CLASSIFICATION_MAP[division_data['division_type']]

            if division_data['name'] in localisation:
                name = localisation[division_data['name']]

            if division_data['description'] in localisation:
                description = localisation[division_data['description']]

            session.add(
                Division(
                    export_name=division,
                    name=name,
                    description=description,
                    nationality=division_data['nationality'],
                    max_activation_points=division_data['max_activation_points'],
                    country=division_data['country'],
                    power_classification=pwr_classification,
                    division_type=type_classification
                )
            )

        session.commit()

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
    export_divisions()
    export_damage_range_tables()
    export_weapons()
    export_decks()

    tend = process_time()

    print(f'Process ran for: {tend-tstart}(s)')


if __name__ == '__main__':
    main()
