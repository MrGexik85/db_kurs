from fastapi import HTTPException, status
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import text

from v1.auth.schema import ResponseSuccess


async def get_report_supplies_controller(db: Session):
    pass


async def get_orders_supplies_controller(db: Session):
    pass