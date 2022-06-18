from fastapi import APIRouter, Depends, Path, Request, status
from sqlalchemy.orm import Session

from core.settings.database import get_db
from core.utils.permissions import get_admin_user_from_session, get_auth_user_from_session
from v1.user.schema import UserSession
from v1.auth.schema import ResponseSuccess

from v1.bank_account.controller import create_bank_account_controller
from v1.bank_account.schema import CreateBankAccountRequest


router = APIRouter(prefix='/bank_account', tags=['bank_account'])


@router.post(
    path='',
    summary='Cоздать банковский счет',
    response_model=ResponseSuccess,
    status_code=status.HTTP_201_CREATED
)
async def create_bank_account(
    body: CreateBankAccountRequest,
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await create_bank_account_controller(db, body)