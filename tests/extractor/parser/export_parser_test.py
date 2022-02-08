import pytest

from extractor.lineparser.common import ExportParser
from extractor.lineparser.storage import BaseStorage
from extractor.fileprocessor.NdfExportProcessor import NdfExportProcessor

lines_provider = [
    ('export DamageTypeEvolutionOverRangeDescriptor_Chute_Lente is TDamageTypeEvolutionOverRangeDescriptor',
     ("DamageTypeEvolutionOverRangeDescriptor_Chute_Lente")),
    ('export DamageTypeEvolutionOverRangeDescriptor_Chute_Lente_1750m is TDamageTypeEvolutionOverRangeDescriptor',
     ('DamageTypeEvolutionOverRangeDescriptor_Chute_Lente_1750m')),
    ('export WeaponDescriptor_203_H17_FIN is TWeaponManagerModuleDescriptor', ('WeaponDescriptor_203_H17_FIN')),
    ('export WeaponDescriptor_Rifle_Motor_CAN is TWeaponManagerModuleDescriptor', ('WeaponDescriptor_Rifle_Motor_CAN')),
    ('export Ammo_110mm_Rocket_x6 is TAmmunitionDescriptor', ('Ammo_110mm_Rocket_x6')),
    ('export Ammo_L2065_20mmL is TAmmunitionDescriptor', ('Ammo_L2065_20mmL')),
    ('export Descriptor_Deck_Division_CAN_3CID_Dv2 is TDeckDivisionDescriptor',
     ('Descriptor_Deck_Division_CAN_3CID_Dv2')),
    ('export Descriptor_Deck_Division_SOV_303DivChass_solo is TDeckDivisionDescriptor',
     ('Descriptor_Deck_Division_SOV_303DivChass_solo')),
    ('export Descriptor_Deck_Division_SOV_88DF_solo is TDeckDivisionDescriptor',
     ('Descriptor_Deck_Division_SOV_88DF_solo')),
]


@pytest.fixture
def parser():
    return ExportParser()


@pytest.fixture
def storage():
    return BaseStorage()


@pytest.fixture
def processor(storage):
    return NdfExportProcessor(storage)


class TestExportParser:

    @pytest.mark.parametrize('line, expected', lines_provider)
    def test_matches_line(self, processor, parser, line, expected):
        actual = processor.match_line(parser.pattern, line)

        assert actual.group(1) == expected

    def test_handle(self, processor, parser, storage):
        expected = 'Descriptor_Deck_Division_SOV_88DF_solo'
        line = 'export Descriptor_Deck_Division_SOV_88DF_solo is TDeckDivisionDescriptor'
        matches = processor.match_line(parser.pattern, line)
        parser.handle(matches, storage)

        assert expected in storage.data.keys()
        assert storage.data[expected] == {}
        assert expected == storage.last_item
