from parser.common import ExportParser, IntPropertyParser, ListParser, StringPropertyParser
from parser.division_fields import DeckParser
from parser.storage import BaseStorage
from .NdfExportProcessor import NdfExportProcessor


class DivisionsNdfProcessor(NdfExportProcessor):

    POWER_CLASSIFICATION_MAP = {
        'DC_PWR1': 'A',
        'DC_PWR2': 'B',
        'DC_PWR3': 'C',
    }

    TYPE_CLASSIFICATION_MAP = {
        'Texture_Division_Type_armor': 'armored',
        'Texture_Division_Type_meca': 'mechanized',
        'Texture_Division_Type_soldier': 'infantry'
    }

    def __init__(self):
        super().__init__(BaseStorage())
        self.handlers = [
            ExportParser(),
            StringPropertyParser('DivisionName', 'name'),
            StringPropertyParser('DivisionDescription', 'description'),
            StringPropertyParser('DivisionPowerClassification', 'power_classification'),
            StringPropertyParser('DivisionNationalite', 'nationality'),
            ListParser('DivisionTags', 'tags'),
            DeckParser('decks'),
            IntPropertyParser('MaxActivationPoints', 'max_activation_points'),
            StringPropertyParser('CostMatrix', 'cost_matrix_name'),
            StringPropertyParser('CountryId', 'country'),
            StringPropertyParser('TypeTexture', 'division_type'),
        ]

    def finalize(self):
        return self.storage.data
