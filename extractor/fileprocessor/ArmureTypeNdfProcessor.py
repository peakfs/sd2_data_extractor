from .NdfExportProcessor import NdfExportProcessor
from lineparser.storage import BaseStorage
from lineparser.armortype_fields import ArmorTypeParser


class ArmureTypeNdfProcessor(NdfExportProcessor):

    def __init__(self):
        super().__init__(BaseStorage())

        self.handlers = [
            ArmorTypeParser()
        ]

    def finalize(self):
        return self.storage.data[ArmorTypeParser.KEY]
