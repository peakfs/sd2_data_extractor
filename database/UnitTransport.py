from sqlalchemy import Column, String, Integer
from .base import Base


class UnitTransport(Base):
    __tablename__ = 'unit_transport'

    id = Column(Integer, primary_key=True)

    unit_export_name = Column(String(100))
    unit_transport_name = Column(String(100))
