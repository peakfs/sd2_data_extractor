from parser.common import StringPropertyParser
from parser.storage import BaseStorage
from parser.unit_specialties_fields import SpecialtyKeyParser
from .NdfExportProcessor import NdfExportProcessor


class UnitSpecialtiesNdfProcessor(NdfExportProcessor):

    def __init__(self):
        super().__init__(BaseStorage())

        self.handlers = [
            SpecialtyKeyParser(),
            StringPropertyParser('SpecialtyHintTitleToken', 'title'),
            StringPropertyParser('SpecialtyHintBodyToken', 'description'),
        ]
