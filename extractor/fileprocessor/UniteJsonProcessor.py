# Proof of concept(!) class for mapping the parsed data from the NDF files into useful compact data structures
class UniteJsonProcessor():

    def __init__(self):
        pass
        
    def mapItems(self, items):

        def moduleDefaultBaseTypeName(item, typeName):
            for module in item['Modules']:
                if isinstance(module, dict) and 'Default' in module and '_base_type_name' in module['Default'] and module['Default']['_base_type_name'] == typeName:
                    return module['Default']
            return None

        def mapper(item):
            val = {}
            if 'ClassNameForDebug' in item:
                val['debug_name'] = item['ClassNameForDebug']
            val['category'] = moduleDefaultBaseTypeName(item, 'TTypeUnitModuleDescriptor')['TypeUnitValue']
            val['side'] = moduleDefaultBaseTypeName(item, 'TTypeUnitModuleDescriptor')['Nationalite']
            val['country_code'] = moduleDefaultBaseTypeName(item, 'TTypeUnitModuleDescriptor')['MotherCountry']
            val['concealment_bonus'] = moduleDefaultBaseTypeName(item, 'TVisibilityModuleDescriptor')['UnitConcealmentBonus']
            val['weapon_export_name'] = ''
            val['armor_front'] = moduleDefaultBaseTypeName(item, 'TDamageModuleDescriptor')['CommonDamageDescriptor']['BlindageProperties']['ArmorDescriptorFront']
            val['armor_side'] = moduleDefaultBaseTypeName(item, 'TDamageModuleDescriptor')['CommonDamageDescriptor']['BlindageProperties']['ArmorDescriptorSides']
            val['armor_back'] = moduleDefaultBaseTypeName(item, 'TDamageModuleDescriptor')['CommonDamageDescriptor']['BlindageProperties']['ArmorDescriptorRear']
            val['armor_top'] = moduleDefaultBaseTypeName(item, 'TDamageModuleDescriptor')['CommonDamageDescriptor']['BlindageProperties']['ArmorDescriptorTop']
            val['health'] = moduleDefaultBaseTypeName(item, 'TDamageModuleDescriptor')['MaxDamages']
            val['morale'] = moduleDefaultBaseTypeName(item, 'TRoutModuleDescriptor')['MoralLevel']
            if var := moduleDefaultBaseTypeName(item, 'TLandMovementModuleDescriptor'):
                if 'Maxspeed' in var:
                    val['max_speed'] = var['Maxspeed']
                val['combat_speed'] = var['VitesseCombat']
                val['speed_bonus_on_road'] = var['SpeedBonusOnRoad']
                val['acceleration_max'] = var['MaxAcceleration']
                val['deceleartion_max'] = var['MaxDeceleration']
                val['half_turn_time'] = var['TempsDemiTour']
                val['vehicle_subtype'] = var['VehicleSubType']
                val['start_time'] = var['StartTime']
                val['stop_time'] = var['StopTime']
                val['turn_start_time'] = var['RotationStartTime']
                val['turn_stop_time'] = var['RotationStopTime']
            val['scope_range_tba'] = ''
            val['detection_range'] = moduleDefaultBaseTypeName(item, 'TScannerConfigurationDescriptor')['PorteeVision']
            val['scope_range'] = moduleDefaultBaseTypeName(item, 'TScannerConfigurationDescriptor')['DetectionTBA']
            val['optics_strength'] = moduleDefaultBaseTypeName(item, 'TScannerConfigurationDescriptor')['OpticalStrength']
            val['identify_base_probability'] = moduleDefaultBaseTypeName(item, 'TReverseScannerWithIdentificationDescriptor')['VisibilityRollRule']['IdentifyBaseProbability']
            val['time_between_identify_rolls'] = moduleDefaultBaseTypeName(item, 'TReverseScannerWithIdentificationDescriptor')['VisibilityRollRule']['TimeBetweenEachIdentifyRoll']
            val['is_towable'] = moduleDefaultBaseTypeName(item, 'TTransportableModuleDescriptor')['IsTowable']
            if var := moduleDefaultBaseTypeName(item, 'TModernWarfareProductionModuleDescriptor'):
                val['production_year'] = var['ProductionYear']
                val['command_points_cost'] = var['ProductionRessourcesNeeded']
            if var := moduleDefaultBaseTypeName(item, 'TWargameLabelModuleDescriptor'):
                val['is_command_unit'] = var['IsCommandementUnit']
                val['localisation_key'] = var['UnitName']
            if var := moduleDefaultBaseTypeName(item, 'TUnitUIModuleDescriptor'):
                val['real_road_speed'] = var['RealRoadSpeed']

            return val

        ret = {}
        for item in items:
            if type(item) is dict and 'Modules' in item:
                ret[item['_type_name']] = mapper(item)

        return ret


