from extractor.database.Ammunition import Ammunition
from extractor.fileprocessor.NdfExportProcessor import NdfExportProcessor
from extractor.lineparser.ammunition_fields import IdlingHitValueParser, MovingHitValueParser
from extractor.lineparser.common import ExportParser, \
    StringPropertyParser, \
    FloatPropertyParser, \
    FormulaParser, \
    BoolPropertyParser
from extractor.lineparser.storage import BaseStorage


class AmmunitionNdfProcessor(NdfExportProcessor):

    def __init__(self):
        super().__init__(BaseStorage())

        self.handlers = [
            ExportParser(),
            StringPropertyParser('Name', Ammunition.FIELD_SHORT_NAME),
            StringPropertyParser('TypeName', Ammunition.FIELD_WEAPON_TYPE),
            StringPropertyParser('TypeArme', Ammunition.FIELD_WEAPON_NAME),
            StringPropertyParser('TypeCategoryName', Ammunition.FIELD_WEAPON_TYPE_CATEGORY_NAME),
            StringPropertyParser('Caliber', Ammunition.FIELD_CALIBER),
            FloatPropertyParser('Puissance', Ammunition.FIELD_POWER),
            FloatPropertyParser('TempsEntreDeuxTirs', Ammunition.FIELD_TIME_BETWEEN_SHOTS),
            FloatPropertyParser('TempsEntreDeuxFx', Ammunition.FIELD_TIME_BETWEEN_FX),
            FormulaParser('PorteeMinimale', Ammunition.FIELD_RANGE_MIN),
            FormulaParser('PorteeMaximale', Ammunition.FIELD_RANGE_MAX),
            FormulaParser('PorteeMinimaleHA', Ammunition.FIELD_RANGE_MIN_HA),
            FormulaParser('PorteeMaximaleHA', Ammunition.FIELD_RANGE_MAX_HA),
            FormulaParser('AltitudeAPorteeMaximale', Ammunition.FIELD_ALTITUDE_MAX),
            FormulaParser('DispersionAtMinRange', Ammunition.FIELD_DISPERSION_AT_MIN_RANGE),
            FormulaParser('DispersionAtMaxRange', Ammunition.FIELD_DISPERSION_AT_MAX_RANGE),
            FloatPropertyParser('CorrectedShotAimtimeMultiplier', Ammunition.FIELD_CORRECTED_SHOT_AIMTIME_MULTIPLIER),
            FloatPropertyParser('PhysicalDamages', Ammunition.FIELD_PHYSICAL_DMG),
            FloatPropertyParser('SuppressDamages', Ammunition.FIELD_SUPPRESS_DMG),
            BoolPropertyParser('TirIndirect', Ammunition.FIELD_INDIRECT_SHOT),
            BoolPropertyParser('TirReflexe', Ammunition.FIELD_DIRECT_SHOT),
            FloatPropertyParser('SupplyCost', Ammunition.FIELD_SUPPLY_COST),
            IdlingHitValueParser(Ammunition.FIELD_ACCURACY_IDLE),
            MovingHitValueParser(Ammunition.FIELD_ACCURACY_MOVING),
            FloatPropertyParser('TempsDeVisee', Ammunition.FIELD_AIM_TIME),
            FloatPropertyParser('TempsEntreDeuxSalves', Ammunition.FIELD_TIME_BETWEEN_BURSTS),
            FloatPropertyParser('NbTirParSalves', Ammunition.FIELD_SHOTS_PER_BURST),
            FloatPropertyParser('AffichageMunitionParSalve', Ammunition.FIELD_AMMUNITION_PER_BURSTS),
            BoolPropertyParser('PiercingWeapon', Ammunition.FIELD_ARMOR_PIERCING),
            StringPropertyParser(
                'DamageTypeEvolutionOverRangeDescriptor',
                Ammunition.FIELD_DMG_TYPE_OVER_RANGE_DESCRIPTOR
            )
        ]
