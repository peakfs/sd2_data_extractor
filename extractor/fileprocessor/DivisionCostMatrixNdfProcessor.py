from lineparser.storage import BaseStorage
from .NdfExportProcessor import NdfExportProcessor
from lineparser.divisioncostmatrix_fields import MatrixNameParser, UnitCategorySlotsParser


class DivisionCostMatrixNdfProcessor(NdfExportProcessor):

    CATEGORY_NAME_MAP = {
        'EDefaultFactories/reco': 'recon',
        'EDefaultFactories/infanterie': 'infantry',
        'EDefaultFactories/tank': 'tank',
        'EDefaultFactories/support': 'support',
        'EDefaultFactories/at': 'anti-tank',
        'EDefaultFactories/dca': 'anti-air',
        'EDefaultFactories/art': 'artillery',
        'EDefaultFactories/air': 'air',
        'EDefaultFactories/defense': 'defense',
    }

    def __init__(self):
        super().__init__(BaseStorage())

        self.handlers = [
            MatrixNameParser(),
            UnitCategorySlotsParser()
        ]
