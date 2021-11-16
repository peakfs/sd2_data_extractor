from lineparser.common import StringPropertyParser
from lineparser.storage import BaseStorage
from lineparser.unit_specialties_fields import SpecialtyKeyParser
from .NdfExportProcessor import NdfExportProcessor


class UnitSpecialtiesNdfProcessor(NdfExportProcessor):

    def __init__(self):
        super().__init__(BaseStorage())

        self.handlers = [
            SpecialtyKeyParser(),
            StringPropertyParser('SpecialtyHintTitleToken', 'title'),
            StringPropertyParser('SpecialtyHintBodyToken', 'description'),
        ]
