from extractor.fileprocessor.NdfExportProcessor import NdfExportProcessor
from extractor.lineparser.armortype_fields import ArmorTypeParser
from extractor.lineparser.storage import BaseStorage


class ArmureTypeNdfProcessor(NdfExportProcessor):

    def __init__(self):
        super().__init__(BaseStorage())

        self.handlers = [
            ArmorTypeParser()
        ]

    def finalize(self):
        return self.storage.data[ArmorTypeParser.KEY]
