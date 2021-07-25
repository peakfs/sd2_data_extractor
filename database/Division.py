from sqlalchemy import Column, Integer, String, Text

from .base import Base


class Division(Base):
    __tablename__ = 'divisions'

    id = Column(Integer, primary_key=True)

    export_name = Column(String(100))
    name = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    nationality = Column(String(100))
    power_classification = Column(String(1), nullable=True)
    max_activation_points = Column(Integer)
    country = Column(String(10))
    division_type = Column(String(50))
