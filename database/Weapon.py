from sqlalchemy import Column, Integer, String

from .base import Base


class Weapon(Base):
    __tablename__ = 'weapons'

    FIELD_EXPORT_NAME = 'export_name'

    id = Column(Integer, primary_key=True)
    export_name = Column(String(100))
