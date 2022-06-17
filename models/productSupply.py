from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from core.settings.database import Base


class ProductSupply(Base):
    __tablename__ = "product_supplies"

    id = Column(Integer, primary_key=True, index=True)
    contractor_id = Column(Integer, ForeignKey('contractors.id', ondelete='CASCADE'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)
    amount = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
