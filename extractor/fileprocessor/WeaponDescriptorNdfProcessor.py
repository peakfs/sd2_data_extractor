from extractor.fileprocessor.NdfExportProcessor import NdfExportProcessor
from extractor.lineparser.common import ExportParser
from extractor.lineparser.storage import BaseStorage
from extractor.lineparser.weapon_fields import SalvoParser, AmmunitionParser


class WeaponDescriptorNdfProcessor(NdfExportProcessor):

    def __init__(self):
        super().__init__(BaseStorage())

        self.handlers = [
            ExportParser(),
            AmmunitionParser(),
            SalvoParser(),
        ]
