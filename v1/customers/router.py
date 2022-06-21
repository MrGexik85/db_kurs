from fastapi import APIRouter, Depends, Request, status, Query, Path, status
from sqlalchemy.orm import Session
from datetime import date

from core.settings.database import get_db
from core.utils.permissions import get_admin_user_from_session, get_auth_user_from_session
from v1.auth.schema import ResponseSuccess
from v1.user.schema import UserSession

from .controller import set_customer_bank_account_controller
from .schema import *


router = APIRouter(prefix='/customers', tags=['customers'])


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