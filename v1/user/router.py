from fastapi import APIRouter, Depends, Request, status, Query, Path, status
from sqlalchemy.orm import Session
from datetime import date

from core.settings.database import get_db
from core.utils.permissions import get_admin_user_from_session, get_auth_user_from_session
from v1.auth.schema import ResponseSuccess
from v1.user.schema import UserSession
from v1.orders.schema import Order

from .controller import create_user_order_controller, get_user_orders_controller, delete_user_order_controller, get_user_order_by_id_controller
from .schema import CreateUserOrder


router = APIRouter(prefix='/user', tags=['user'])

@router.post(
    path='/order',
    summary='купить товар',
    response_model=ResponseSuccess,
    status_code=status.HTTP_200_OK
)
async def create_user_order(
    body: CreateUserOrder,
    user: UserSession = Depends(get_auth_user_from_session),
    db: Session = Depends(get_db)
):
    return await create_user_order_controller(db, user, body)


@router.get(
    path='/order',
    summary='получить все заказы',
    response_model=list[Order],
    status_code=status.HTTP_200_OK
)
async def get_user_orders(
    user: UserSession = Depends(get_auth_user_from_session),
    db: Session = Depends(get_db)
):
    return await get_user_orders_controller(db, user)


@router.get(
    path='/order/{orderId}',
    summary='получить заказ по id',
    response_model=Order,
    status_code=status.HTTP_200_OK
)
async def get_user_order_by_id(
    orderId: int = Path(default=1, description='Идентификатор заказа', ge=1),
    user: UserSession = Depends(get_auth_user_from_session),
    db: Session = Depends(get_db)
):
    return await get_user_order_by_id_controller(db, user, orderId)


@router.delete(
    path='/order/{orderId}',
    summary='отменить заказ',
    response_model=ResponseSuccess,
    status_code=status.HTTP_200_OK
)
async def delete_user_order(
    orderId: int = Path(default=1, description='Идентификатор заказа', ge=1),
    user: UserSession = Depends(get_auth_user_from_session),
    db: Session = Depends(get_db)
):
    return await delete_user_order_controller(db, user, orderId)