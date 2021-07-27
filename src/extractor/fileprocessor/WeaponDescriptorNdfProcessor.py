from lineparser.storage import BaseStorage
from .NdfExportProcessor import NdfExportProcessor
from lineparser.weapon_fields import SalvoParser, AmmunitionParser
from lineparser.common import ExportParser


class WeaponDescriptorNdfProcessor(NdfExportProcessor):

    def __init__(self):
        super().__init__(BaseStorage())

        self.handlers = [
            ExportParser(),
            AmmunitionParser(),
            SalvoParser(),
        ]
