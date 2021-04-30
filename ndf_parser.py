
def parse(file, parser_func):

    if not file:
        raise FileNotFoundError

    if not parser_func:
        raise Exception('Missing parser function!')

    with open(file, 'r') as infile:
        for line in infile:
            line = clean_line(line)
            parser_func(line)


def clean_line(line: str) -> str:
    return line.strip()

