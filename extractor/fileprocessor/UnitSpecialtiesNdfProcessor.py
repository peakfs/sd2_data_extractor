from extractor.fileprocessor.NdfExportProcessor import NdfExportProcessor
from extractor.lineparser.common import StringPropertyParser
from extractor.lineparser.storage import BaseStorage
from extractor.lineparser.unit_specialties_fields import SpecialtyKeyParser


class UnitSpecialtiesNdfProcessor(NdfExportProcessor):

    def __init__(self):
        super().__init__(BaseStorage())

        self.handlers = [
            SpecialtyKeyParser(),
            StringPropertyParser('SpecialtyHintTitleToken', 'title'),
            StringPropertyParser('SpecialtyHintBodyToken', 'description'),
        ]
