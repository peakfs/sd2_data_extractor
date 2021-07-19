import re

from parser.storage import BaseStorage


class NdfExportProcessor:
    handlers = []
    storage = None

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def finalize(self):
        return self.storage.data

    def parse_file(self, file):
        if not file:
            raise FileNotFoundError

        with open(file, 'r') as infile:
            for line in infile:

                line = line.strip()
                if len(line) == 0 or line.startswith('//'):
                    continue

                for handler in self.handlers:
                    matches = re.fullmatch(handler.pattern, line)

                    if matches is None:
                        continue

                    handler.handle(matches, self.storage)

        return self.finalize()
