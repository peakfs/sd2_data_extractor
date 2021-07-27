from sqlalchemy import Column, String, Integer
from .base import Base


class UnitSpecialty(Base):
    __tablename__ = 'unit_specialty'

    id = Column(Integer, primary_key=True)

    unit_export_name = Column(String(100))
    specialty_export_key = Column(String(100))
