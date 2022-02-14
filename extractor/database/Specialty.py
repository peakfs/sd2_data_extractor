from sqlalchemy import Column, String, Integer, Text
from extractor.database.base import Base


class Specialty(Base):
    __tablename__ = 'specialties'

    id = Column(Integer, primary_key=True)

    export_key = Column(String(100))
    title = Column(String(100))
    description = Column(Text)
