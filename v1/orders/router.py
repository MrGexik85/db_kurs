from fastapi import APIRouter, Depends, Request, status, Query, Path, status
from sqlalchemy.orm import Session
from datetime import date

from core.settings.database import get_db
from core.utils.permissions import get_admin_user_from_session, get_auth_user_from_session
from v1.auth.schema import ResponseSuccess
from v1.user.schema import UserSession

from .controller import set_deliver_order_controller, set_paid_order_controller, get_orders_controller
from .schema import Order


router = APIRouter(prefix='/orders', tags=['orders'])


@router.get(
    path='',
    summary='получить все заказы (+ фильтр по их состоянию и дате)',
    response_model=list[Order],
    status_code=status.HTTP_200_OK
)
async def get_orders(
    is_paid: bool | None = Query(default=None, description='Оплачен или нет'),
    is_deliver: bool | None = Query(default=None, description='Доставлен или нет'),
    period_from: date | None = Query(default=None, description='Дата от'),
    period_to: date | None = Query(default=None, description='Дата до'),
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await get_orders_controller(db, is_paid, is_deliver, period_from, period_to)


@router.post(
    path='/{id}/paid',
    summary='админ ставит отметку об оплате',
    response_model=ResponseSuccess,
    status_code=status.HTTP_200_OK
)
async def set_paid_order(
    id: int = Path(default=1, description='Индентификатор заказа', ge=1),
    db: Session = Depends(get_db)
):
    return await set_paid_order_controller(db, id)


@router.post(
    path='/{id}/deliver',
    summary='админ ставит отметку о доставке',
    response_model=ResponseSuccess,
    status_code=status.HTTP_200_OK
)
async def set_deliver_order(
    id: int = Path(default=1, description='Индентификатор заказа', ge=1),
    db: Session = Depends(get_db)
):
    return await set_deliver_order_controller(db, id)