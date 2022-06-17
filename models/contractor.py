from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.settings.database import Base


class Contractor(Base):
    __tablename__ = "contractors"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    address = Column(String, nullable=False)
    director = Column(String, nullable=False)
    accountant = Column(String, nullable=False)
    bank_account_id = Column(Integer, ForeignKey('bank_accounts.id', ondelete='CASCADE'), nullable=False)