from fastapi import APIRouter, Depends, Request, status, Query, Path, status
from sqlalchemy.orm import Session
from datetime import date

from core.settings.database import get_db
from core.utils.permissions import get_admin_user_from_session, get_auth_user_from_session
from v1.auth.schema import ResponseSuccess
from v1.user.schema import UserSession

from .controller import get_orders_supplies_controller, get_report_supplies_controller
from .schema import *


router = APIRouter(prefix='/report', tags=['report'])

@router.get(
    path='/supplies',
    summary='получить отчет по поставкам (+ фильтры)',
)
async def get_report_supplies(
    body,
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await get_report_supplies_controller(db)


@router.get(
    path='/orders',
    summary='получить отчет по заказам (+ фильтр по их состоянию и дате)',
)
async def get_report_orders(
    body,
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await get_report_orders_controller(db)