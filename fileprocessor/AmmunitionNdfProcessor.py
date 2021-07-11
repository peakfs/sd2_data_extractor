from parser.ammunition_fields import IdlingHitValueParser, MovingHitValueParser
from parser.common import *
from parser.storage import BaseStorage
from .NdfExportProcessor import NdfExportProcessor


class AmmunitionNdfProcessor(NdfExportProcessor):

    def __init__(self, storage: BaseStorage):
        super().__init__(storage)

        self.handlers = [
            ExportParser(),
            StringPropertyParser('Name'),
            StringPropertyParser('TypeName'),
            StringPropertyParser('TypeArme'),
            StringPropertyParser('TypeCategoryName'),
            StringPropertyParser('Caliber'),
            FloatPropertyParser('Puissance'),                                   # power
            FloatPropertyParser('TempsEntreDeuxTirs'),                          # time between two shots
            FloatPropertyParser('TempsEntreDeuxFx'),                            # time between two fx
            FormulaParser('PorteeMinimale'),                                    # min range
            FormulaParser('PorteeMaximale'),                                    # max range
            FormulaParser('PorteeMinimaleHA'),                                  # high altitude min range
            FormulaParser('PorteeMaximaleHA'),                                  # high altitude max range
            FormulaParser('AltitudeAPorteeMaximale'),
            FormulaParser('DispersionAtMinRange'),
            FormulaParser('DispersionAtMaxRange'),
            FloatPropertyParser('CorrectedShotAimtimeMultiplier'),
            FloatPropertyParser('PhysicalDamages'),                             # phys damage
            FloatPropertyParser('SuppressDamages'),                             # supression damage
            BoolPropertyParser('TirIndirect'),                                  # indirect shot
            BoolPropertyParser('TirReflexe'),                                   # reflex shot
            IntPropertyParser('SupplyCost'),
            IdlingHitValueParser(),
            MovingHitValueParser(),
            FloatPropertyParser('TempsDeVisee'),                                # target time
            FloatPropertyParser('TempsEntreDeuxSalves'),                        # time between two bursts
            IntPropertyParser('NbTirParSalves'),                                # shots per burst
            IntPropertyParser('AffichageMunitionParSalve'),                     # ammunition per shots
            BoolPropertyParser('PiercingWeapon'),                               # has AP damage
            StringPropertyParser('DamageTypeEvolutionOverRangeDescriptor')
        ]

    def finalize(self):
        print(self.__class__.__name__ + ' finished')
