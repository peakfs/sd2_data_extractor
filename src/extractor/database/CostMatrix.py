from sqlalchemy import Column, Integer, String
from .base import Base


class CostMatrix(Base):
    __tablename__ = 'division_cost_matrix'

    id = Column(Integer, primary_key=True)

    export_name = Column(String(100))
    unit_category_name = Column(String(100))
    cost = Column(Integer)
