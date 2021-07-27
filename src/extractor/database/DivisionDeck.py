from sqlalchemy import Column, Integer, String
from .base import Base


class DivisionDeck(Base):
    __tablename__ = 'division_deck'

    id = Column(Integer, primary_key=True)

    division_export_name = Column(String(100))
    deck_export_name = Column(String(100))
