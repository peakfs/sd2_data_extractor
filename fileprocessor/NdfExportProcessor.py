from parser.common import *
from parser.storage import BaseStorage
from abc import abstractmethod
import re


class NdfExportProcessor:
    handlers = []
    _storage = None

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    @property
    def storage(self):
        return self._storage

    @storage.setter
    def storage(self, storage: BaseStorage):
        self._storage = storage

    @abstractmethod
    def finalize(self):
        raise NotImplementedError('finalize must be implemented!')

    def parse_file(self, file):

        if not file:
            raise FileNotFoundError

        with open(file, 'r') as infile:
            for line in self._clean_lines(infile):
                for handler in self.handlers:
                    try:
                        matches = re.fullmatch(handler.pattern, line)

                        if matches is None:
                            raise SkipLineError()

                        handler.handle(matches, self.storage)
                    except SkipLineError:
                        continue

        self.finalize()

    def _clean_lines(self, file) -> str:
        for line in file:
            line = line.strip()

            if len(line) == 0 or line.startswith('//'):
                continue

            yield line
