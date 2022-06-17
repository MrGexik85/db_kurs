from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from core.settings.database import Base


class ProductContractorAssociation(Base):
    __tablename__ = "product_contractor_association"

    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)
    contractor_id = Column(Integer, ForeignKey('contractors.id', ondelete='CASCADE'), primary_key=True)