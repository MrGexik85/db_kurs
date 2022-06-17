from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import relationship

from core.settings.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    note = Column(Text, nullable=True)
    delivery_terms = Column(String, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    is_paid = Column(Boolean, nullable=False, default=False)
    is_deliver = Column(Boolean, nullable=False, default=False)