
METER = 0.2


def parse_file(file, parser_cls):
    if not file:
        raise FileNotFoundError

    if not parser_cls:
        raise Exception('Missing parser function!')

    with open(file, 'r') as infile:
        for line in cleaned_lines(infile):
            parser_cls.parse(line)


def cleaned_lines(infile):
    for line in infile:
        line = line.strip()

        if len(line) == 0:
            continue

        if line.startswith('//'):
            continue

        yield line
