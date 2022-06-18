from sqlalchemy.orm import Session
from .schema import CreateBankAccountRequest


async def create_bank_account_controller(db: Session, body: CreateBankAccountRequest):
    pass