
def parse_file(file, parser_cls):

    if not file:
        raise FileNotFoundError

    if not parser_cls:
        raise Exception('Missing parser function!')

    with open(file, 'r') as infile:
        for line in infile:
            line = clean_line(line)
            parser_cls.parse(line)


def clean_line(line: str) -> str:
    return line.strip()

