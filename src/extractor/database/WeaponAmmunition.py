from sqlalchemy import Column, Integer, String
from .base import Base


class WeaponAmmunition(Base):
    __tablename__ = 'weapon_ammunition'

    id = Column(Integer, primary_key=True)
    weapon_export_name = Column(String(100), nullable=False)
    ammunition_export_name = Column(String(100), nullable=False)
    salvos = Column(Integer)
