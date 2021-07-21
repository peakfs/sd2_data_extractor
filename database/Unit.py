from sqlalchemy import Column, String, Numeric, Integer, Boolean
from .base import Base


class Unit(Base):
    __tablename__ = 'units'

    id = Column(Integer, primary_key=True)

    export_name = Column(String(100))

    acceleration_max = Column(Numeric)
    armor_back = Column(String(50))
    armor_front = Column(String(50))
    armor_side = Column(String(50))
    armor_top = Column(String(50))
    category = Column(String(50))
    combat_speed = Column(Integer)
    command_points_cost = Column(Integer)
    concealment_bonus = Column(Numeric)
    country_code = Column(String(10))
    debug_name = Column(String(100))
    deceleartion_max = Column(Numeric)
    detection_range = Column(Integer)

    half_turn_time = Column(Numeric)
    health = Column(Numeric)
    identify_base_probability = Column(Numeric)
    is_command_unit = Column(Boolean)
    localisation_key = Column(String(50))
    max_speed = Column(Integer)
    morale = Column(Integer)
    side = Column(String(50))
    optics_strength = Column(Integer)
    production_year = Column(Integer)
    scope_range = Column(Integer)
    scope_range_tba = Column(Numeric)
    speed_bonus_on_road = Column(Numeric)
    real_road_speed = Column(Integer)
    start_time = Column(Integer)
    stop_time = Column(Integer)
    time_between_identify_rolls = Column(Numeric)
    is_towable = Column(Boolean)
    plane_turn_radius = Column(Integer, nullable=True, default='NULL')
    turn_start_time = Column(Integer)
    turn_stop_time = Column(Integer)
    vehicle_subtype = Column(String(50))
    weapon_export_name = Column(String(100))
