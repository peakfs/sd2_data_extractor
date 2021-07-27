from lineparser.storage import BaseStorage
from .NdfExportProcessor import NdfExportProcessor
from lineparser.divisionrules_fields import DivisionParser, ReferencePropertyParser
from lineparser.common import StringPropertyParser, \
    BoolPropertyParser, \
    IntPropertyParser, \
    DescriptorListParser, \
    IntListParser, \
    FloatListParser


class DivisionRulesNdfProcessor(NdfExportProcessor):

    def __init__(self):
        super().__init__(BaseStorage())

        self.handlers = [
            DivisionParser(),
            ReferencePropertyParser('UnitDescriptor', 'unit_export_name'),
            BoolPropertyParser('AvailableWithoutTransport', 'is_available_without_transport'),
            DescriptorListParser('AvailableTransportList', 'available_transports'),
            IntPropertyParser('MaxPackNumber', 'max_cards'),
            IntListParser('NumberOfUnitInPackByPhase', 'number_of_units'),
            FloatListParser('NumberOfUnitInPackXPMultiplier', 'unit_count_exp_multiplier'),
        ]
