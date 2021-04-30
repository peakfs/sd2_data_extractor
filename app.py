#! /usr/bin/python3

from pathlib import Path
from pprint import pprint

from division_parser import DivisionParser
from ndf_parser import parse

APP_DIR = Path(__file__).parent

files = [
    'assets/GameData/Generated/Gameplay/Decks/Divisions.ndf',
]

parser = DivisionParser()

if __name__ == '__main__':
    for file_path in files:
        parse(APP_DIR / file_path, parser.parse)
        pprint(parser.divisions, width=200)
