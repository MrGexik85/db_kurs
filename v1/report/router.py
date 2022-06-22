from fastapi import APIRouter, Depends, Request, status, Query, Path, status
from sqlalchemy.orm import Session
from datetime import date

from core.settings.database import get_db
from core.utils.permissions import get_admin_user_from_session, get_auth_user_from_session
from v1.auth.schema import ResponseSuccess
from v1.user.schema import UserSession

from .controller import get_report_orders_controller, get_report_supplies_controller
from .schema import *


router = APIRouter(prefix='/report', tags=['report'])

@router.get(
    path='/supplies',
    summary='получить отчет по поставкам в виде csv файла (+ фильтры)',
)
async def get_report_supplies(
    period_from: date | None = Query(default=None, description='От какого дня (можно не указывать эти фильтры, тогда покажет все поставки)', example='2022-05-20'),
    period_to: date | None = Query(default=None, description='До какого дня', example='2022-05-25'),
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await get_report_supplies_controller(db, period_from, period_to)


@router.get(
    path='/orders',
    summary='получить отчет по заказам в виде csv файла (+ фильтр по их состоянию и дате)',
)
async def get_report_orders(
    is_paid: bool | None = Query(default=None, description='Оплачен или нет'),
    is_deliver: bool | None = Query(default=None, description='Доставлен или нет'),
    period_from: date | None = Query(default=None, description='Дата от'),
    period_to: date | None = Query(default=None, description='Дата до'),
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await get_report_orders_controller(db, is_paid, is_deliver, period_from, period_to)