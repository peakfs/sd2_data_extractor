import re

from parser.storage import BaseStorage


class NdfExportProcessor:
    handlers = []
    storage = None
    garbage_lines = [
        '(',
        ')',
        '[',
        ']',
        '),'
    ]

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
                if self.is_garbage_line(line):
                    continue

                for handler in self.handlers:
                    matches = re.fullmatch(handler.pattern, line)

                    if matches is None:
                        continue

                    handler.handle(matches, self.storage)
                    break

        return self.finalize()

    def is_garbage_line(self, line: str) -> bool:
        if len(line) == 0 or line.startswith('//') or line in self.garbage_lines:
            return True
        else:
            return False
