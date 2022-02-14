from extractor.fileprocessor.NdfExportProcessor import NdfExportProcessor
from extractor.lineparser.common import ExportParser, \
    FormulaParser, \
    StringPropertyParser, \
    FloatPropertyParser, \
    BoolPropertyParser
from extractor.lineparser.storage import BaseStorage
from extractor.lineparser.unit_fields import UnitWeaponParser, CommandPointsCostParser, SpecialtyParser


class UniteNdfProcessor(NdfExportProcessor):

    def __init__(self):
        super().__init__(BaseStorage())

        self.handlers = [
            ExportParser(),
            FormulaParser('MaxAcceleration', 'acceleration_max'),
            StringPropertyParser('ArmorDescriptorRear', 'armor_back'),
            StringPropertyParser('ArmorDescriptorFront', 'armor_front'),
            StringPropertyParser('ArmorDescriptorSides', 'armor_side'),
            StringPropertyParser('ArmorDescriptorTop', 'armor_top'),
            StringPropertyParser('TypeUnitValue', 'category'),
            FormulaParser('VitesseCombat', 'combat_speed'),
            CommandPointsCostParser('~/Resource_CommandPoints', 'command_points_cost'),
            FloatPropertyParser('UnitConcealmentBonus', 'concealment_bonus'),
            StringPropertyParser('MotherCountry', 'country_code'),
            StringPropertyParser('ClassNameForDebug', 'debug_name'),
            FormulaParser('MaxDeceleration', 'deceleartion_max'),
            FormulaParser('DetectionTBA', 'detection_range'),
            FloatPropertyParser('TempsDemiTour', 'half_turn_time'),
            FloatPropertyParser('MaxDamages', 'health'),
            FloatPropertyParser('IdentifyBaseProbability', 'identify_base_probability'),
            BoolPropertyParser('IsCommandementUnit', 'is_command_unit'),
            StringPropertyParser('NameToken', 'localisation_key'),
            FormulaParser('Maxspeed', 'max_speed'),
            FloatPropertyParser('MoralLevel', 'morale'),
            StringPropertyParser('Nationalite', 'side'),
            FloatPropertyParser('OpticalStrength', 'optics_strength'),
            FloatPropertyParser('ProductionYear', 'production_year'),
            FormulaParser('PorteeVision', 'scope_range'),
            FormulaParser('PorteeVisionTBA', 'scope_range_tba'),
            FloatPropertyParser('SpeedBonusOnRoad', 'speed_bonus_on_road'),
            SpecialtyParser(),
            FloatPropertyParser('RealRoadSpeed', 'real_road_speed'),
            FormulaParser('StartTime', 'start_time'),
            FormulaParser('StopTime', 'stop_time'),
            FloatPropertyParser('TimeBetweenEachIdentifyRoll', 'time_between_identify_rolls'),
            BoolPropertyParser('IsTowable', 'is_towable'),
            FormulaParser('AgilityRadius', 'plane_turn_radius'),
            FormulaParser('RotationStartTime', 'turn_start_time'),
            FormulaParser('RotationStopTime', 'turn_stop_time'),
            StringPropertyParser('VehicleSubType', 'vehicle_subtype'),
            UnitWeaponParser('weapon_export_name'),
        ]
