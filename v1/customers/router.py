from fastapi import APIRouter, Depends, Request, status, Query, Path, status
from sqlalchemy.orm import Session
from datetime import date

from core.settings.database import get_db
from core.utils.permissions import get_admin_user_from_session, get_auth_user_from_session
from v1.auth.schema import ResponseSuccess
from v1.user.schema import UserSession

from .controller import set_customer_bank_account_controller, get_customer_by_id_controller, get_customers_controller
from .schema import Customer


router = APIRouter(prefix='/customers', tags=['customers'])


@router.get(
    path='',
    summary='получить данные о клиентах',
    response_model=list[Customer],
    status_code=status.HTTP_200_OK
)
async def get_customers(
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await get_customers_controller(db)


@router.get(
    path='/{customerId}',
    summary='получить данные о клиенте',
    response_model=Customer,
    status_code=status.HTTP_200_OK
)
async def get_customer_by_id(
    customerId: int = Path(default=1, description='Идентификатор покупателя', ge=1),
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await get_customer_by_id_controller(db, customerId)


@router.post(
    path='/{customerId}/bank/{bankId}',
    summary='привязать банковский счет к клиенту',
    response_model=ResponseSuccess,
    status_code=status.HTTP_200_OK
)
async def set_customer_bank_account(
    customerId: int = Path(default=1, description='Идентификатор покупателя', ge=1),
    bankId: int = Path(default=1, description='Идентификатор банковского счета', ge=1),
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await set_customer_bank_account_controller(db, customerId, bankId)