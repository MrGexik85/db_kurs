from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.settings.database import Base


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String, nullable=False)
    inn = Column(String, nullable=False)
    bik = Column(String, nullable=False)
    account = Column(String, nullable=False)