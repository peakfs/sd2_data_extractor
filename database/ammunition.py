from sqlalchemy import Column, Integer, String, Numeric, Boolean
from .base import Base


class Ammunition(Base):
    __tablename__ = "ammunition"

    FIELD_EXPORT_NAME = 'export_name'
    FIELD_SHORT_NAME = 'short_name'
    FIELD_WEAPON_TYPE = 'weapon_type'
    FIELD_WEAPON_NAME = 'weapon_name'
    FIELD_WEAPON_TYPE_CATEGORY_NAME = 'weapon_type_category_name'
    FIELD_CALIBER = 'caliber'
    FIELD_POWER = 'power'
    FIELD_TIME_BETWEEN_SHOTS = 'time_between_shots'
    FIELD_TIME_BETWEEN_FX = 'time_between_fx'
    FIELD_RANGE_MIN = 'range_min'
    FIELD_RANGE_MAX = 'range_max'
    FIELD_RANGE_MIN_HA = 'range_min_ha'
    FIELD_RANGE_MAX_HA = 'range_max_ha'
    FIELD_ALTITUDE_MAX = 'altitude_max'
    FIELD_DISPERSION_AT_MIN_RANGE = 'dispersion_at_min_range'
    FIELD_DISPERSION_AT_MAX_RANGE = 'dispersion_at_max_range'
    FIELD_CORRECTED_SHOT_AIMTIME_MULTIPLIER = 'corrected_shot_aimtime_multiplier'
    FIELD_PHYSICAL_DMG = 'physical_dmg'
    FIELD_SUPPRESS_DMG = 'suppress_dmg'
    FIELD_INDIRECT_SHOT = 'indirect_shot'
    FIELD_DIRECT_SHOT = 'direct_shot'
    FIELD_SUPPLY_COST = 'supply_cost'
    FIELD_ACCURACY_IDLE = 'accuracy_idle'
    FIELD_ACCURACY_MOVING = 'accuracy_moving'
    FIELD_AIM_TIME = 'aim_time'
    FIELD_TIME_BETWEEN_BURSTS = 'time_between_bursts'
    FIELD_SHOTS_PER_BURST = 'shots_per_burst'
    FIELD_AMMUNITION_PER_BURSTS = 'ammunition_per_bursts'
    FIELD_ARMOR_PIERCING = 'armor_piercing'
    FIELD_DMG_TYPE_OVER_RANGE_DESCRIPTOR = 'dmg_type_over_range_descriptor'

    id = Column(Integer, primary_key=True)

    export_name = Column(String(100))  # export name
    short_name = Column(String(50))   # Name
    weapon_type = Column(String(50))  # TypeName
    weapon_name = Column(String(50))  # TypeArme
    weapon_type_category_name = Column(String(50))  # TypeCategoryName
    caliber = Column(String(50))  # Caliber
    power = Column(Numeric())  # Puissance
    time_between_shots = Column(Numeric())  # TempsEntreDeuxTirs
    time_between_fx = Column(Numeric())  # TempsEntreDeuxFx
    range_min = Column(Integer)  # PorteeMinimale
    range_max = Column(Integer)  # PorteeMaximale
    range_min_ha = Column(Integer)  # PorteeMinimaleHA
    range_max_ha = Column(Integer)  # PorteeMaximaleHA
    altitude_max = Column(Integer)
    dispersion_at_min_range = Column(Integer)
    dispersion_at_max_range = Column(Integer)
    corrected_shot_aimtime_multiplier = Column(Numeric())
    physical_dmg = Column(Numeric())
    suppress_dmg = Column(Numeric())
    indirect_shot = Column(Boolean())  # TirIndirect
    direct_shot = Column(Boolean())  # TirReflexe
    supply_cost = Column(Integer)
    accuracy_idle = Column(Numeric())
    accuracy_moving = Column(Numeric())
    aim_time = Column(Numeric())  # TempsDeVisee
    time_between_bursts = Column(Numeric())  # TempsEntreDeuxSalves
    shots_per_burst = Column(Integer)  # NbTirParSalves
    ammunition_per_bursts = Column(Integer)  # AffichageMunitionParSalve
    armor_piercing = Column(Boolean())  # PiercingWeapon
    dmg_type_over_range_descriptor = Column(String(120))

    def __repr__(self) -> str:
        return f"Ammunition(id={self.id}, export_name={self.export_name})"
