from extractor.fileprocessor.NdfExportProcessor import NdfExportProcessor
from extractor.lineparser.common import BoolPropertyParser, \
    FloatPropertyParser, \
    DescriptorListParser, \
    FloatListParser
from extractor.lineparser.divisionrules_fields import DivisionParser, ReferencePropertyParser
from extractor.lineparser.storage import BaseStorage


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
