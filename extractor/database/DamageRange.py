from sqlalchemy import Column, String, Numeric, Integer
from extractor.database.base import Base


class DamageRange(Base):
    __tablename__ = "damage_ranges"

    id = Column(Integer, primary_key=True)

    export_name = Column(String(100))
    range_percentage = Column(Numeric())
    penetration_percentage = Column(Numeric())
