from sqlalchemy import Column, String, Integer
from .base import Base


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)

    tag_name = Column(String(100))

