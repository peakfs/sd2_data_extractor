from lineparser.common import BoolPropertyParser, \
    FloatPropertyParser, \
    DescriptorListParser, \
    FloatListParser
from lineparser.divisionrules_fields import DivisionParser, ReferencePropertyParser
from lineparser.storage import BaseStorage
from .NdfExportProcessor import NdfExportProcessor


class DivisionRulesNdfProcessor(NdfExportProcessor):

    def __init__(self):
        super().__init__(BaseStorage())

        self.handlers = [
            DivisionParser(),
            ReferencePropertyParser('UnitDescriptor', 'unit_export_name'),
            BoolPropertyParser('AvailableWithoutTransport', 'is_available_without_transport'),
            DescriptorListParser('AvailableTransportList', 'available_transports'),
            FloatPropertyParser('MaxPackNumber', 'max_cards'),
            FloatListParser('NumberOfUnitInPackByPhase', 'number_of_units'),
            FloatListParser('NumberOfUnitInPackXPMultiplier', 'unit_count_exp_multiplier'),
        ]
