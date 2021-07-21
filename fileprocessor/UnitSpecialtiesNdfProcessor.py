from .NdfExportProcessor import NdfExportProcessor
from parser.storage import BaseStorage
from parser.unit_specialties_fields import SpecialtyKeyParser
from parser.common import StringPropertyParser
from config import ASSETS_DIR
import csv


class UnitSpecialtiesNdfProcessor(NdfExportProcessor):

    def __init__(self):
        super().__init__(BaseStorage())

        self.handlers = [
            SpecialtyKeyParser(),
            StringPropertyParser('SpecialtyHintTitleToken', 'title'),
            StringPropertyParser('SpecialtyHintBodyToken', 'description'),
        ]

    def finalize(self):

        localisation = {}

        with open(ASSETS_DIR / 'Utils/LocalisationEntries/Entries.csv', 'r') as locfile:
            reader = csv.reader(locfile, delimiter=';')
            for row in reader:
                localisation[row[2]] = row[3]

        for key, specialty_data in self.storage.data.items():
            self.storage.data[key] = {
                'title': localisation[specialty_data['title']],
                'description': localisation[specialty_data['description']]
            }

        return self.storage.data
