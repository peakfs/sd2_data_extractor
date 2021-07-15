from .NdfExportProcessor import NdfExportProcessor
from parser.storage import BaseStorage
from parser.common import ExportParser, FloatTupleParser


class DTEORDNdfProcessor(NdfExportProcessor):

    def __init__(self):
        super().__init__(BaseStorage())

        self.handlers = [
            ExportParser(),
            FloatTupleParser('ranges')
        ]
