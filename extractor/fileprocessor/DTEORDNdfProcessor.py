from .NdfExportProcessor import NdfExportProcessor
from lineparser.storage import BaseStorage
from lineparser.common import ExportParser, FloatTupleParser


class DTEORDNdfProcessor(NdfExportProcessor):

    def __init__(self):
        super().__init__(BaseStorage())

        self.handlers = [
            ExportParser(),
            FloatTupleParser('ranges', 'ranges')
        ]
