from .NdfExportProcessor import NdfExportProcessor
from parser.storage import BaseStorage
from parser.common import ExportParser, \
    StringPropertyParser, \
    FloatPropertyParser, \
    FormulaParser, \
    BoolPropertyParser, \
    IntPropertyParser


class DivisionsNdfProcessor(NdfExportProcessor):

    def __init__(self):
        super().__init__(BaseStorage())
        self.handlers = [
            ExportParser(),
            StringPropertyParser('DivisionName'),
            StringPropertyParser('DivisionNationalite'),
        ]

    def finalize(self):
        return self.storage.data
