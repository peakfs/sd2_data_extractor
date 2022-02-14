from sqlalchemy import Column, String, Integer, Numeric, Boolean
from extractor.database.base import Base


class DeckUnit(Base):
    __tablename__ = 'deck_unit'

    id = Column(Integer, primary_key=True)

    deck_export_name = Column(String(100))
    unit_export_name = Column(String(100))
    is_available_without_transport = Column(Boolean)
    max_cards = Column(Integer)
    units_phase_a = Column(Integer)
    units_phase_b = Column(Integer)
    units_phase_c = Column(Integer)
    vet_multiplier_phase_a = Column(Numeric)
    vet_multiplier_phase_b = Column(Numeric)
    vet_multiplier_phase_c = Column(Numeric)
