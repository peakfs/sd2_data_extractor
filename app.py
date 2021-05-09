#! /usr/bin/python3

from pathlib import Path
from pprint import pprint

from parser.common import parse_file
from parser.division import DivisionParser
from parser.division_cost_matrix import DivisionCostMatrixParser
from parser.division_rules import DivisionRulesParser

APP_DIR = Path(__file__).parent


def parse_divisions():
    parser = DivisionParser()
    parse_file(APP_DIR / 'assets/GameData/Generated/Gameplay/Decks/Divisions.ndf', parser)

    return parser.parsed_data


def parse_decks(parsed_divisions):
    parser = DivisionRulesParser(parsed_divisions)
    parse_file(APP_DIR / 'assets/GameData/Generated/Gameplay/Decks/DivisionRules.ndf', parser)

    return parser.parsed_data


def parse_division_cost_matrices(parsed_divisions):
    parser = DivisionCostMatrixParser(parsed_divisions)
    parse_file(APP_DIR / 'assets/GameData/Gameplay/Decks/DivisionCostMatrix.ndf', parser)

    return parser.parsed_data


if __name__ == '__main__':
    divisions = parse_divisions()
    decks = parse_decks(divisions)
    costs = parse_division_cost_matrices(divisions)

    pprint(costs)
