from extractor.fileprocessor.NdfExportProcessor import NdfExportProcessor
from extractor.lineparser.common import ExportParser, FloatTupleParser
from extractor.lineparser.storage import BaseStorage


class DTEORDNdfProcessor(NdfExportProcessor):

    def __init__(self):
        super().__init__(BaseStorage())

        self.handlers = [
            ExportParser(),
            FloatTupleParser('ranges', 'ranges')
        ]
