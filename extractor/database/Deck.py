from sqlalchemy import Column, Integer, String
from extractor.database.base import Base


class Deck(Base):
    __tablename__ = 'decks'

    id = Column(Integer, primary_key=True)

    export_name = Column(String(100))
