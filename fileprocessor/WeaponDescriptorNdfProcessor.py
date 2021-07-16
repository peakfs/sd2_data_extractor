from parser.storage import BaseStorage
from .NdfExportProcessor import NdfExportProcessor
from parser.weapon_fields import SalvoParser, AmmunitionParser
from parser.common import ExportParser


class WeaponDescriptorNdfProcessor(NdfExportProcessor):

    def __init__(self):
        super().__init__(BaseStorage())

        self.handlers = [
            ExportParser(),
            AmmunitionParser(),
            SalvoParser(),
        ]
