from fastapi import APIRouter, Depends, Path, Request, status
from sqlalchemy.orm import Session

from core.settings.database import get_db
from core.utils.permissions import get_admin_user_from_session, get_auth_user_from_session
from v1.user.schema import UserSession
from v1.auth.schema import ResponseSuccess

from v1.bank_account.controller import create_bank_account_controller, get_bank_account_by_id_controller, update_bank_account_by_id_controller
from v1.bank_account.schema import CreateBankAccountRequest, BankAccount, UpdateBankAccount


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


@router.get(
    path='/{id}',
    summary='Получить банковский счет',
    response_model=BankAccount,
    status_code=status.HTTP_200_OK
)
async def get_bank_account_by_id(
    id: int = Path(default=1, description='Уникальный идентификатор', ge=1),
    db: Session = Depends(get_db)
):
    return await get_bank_account_by_id_controller(db, id)


@router.patch(
    path='/{id}',
    summary='обновить банковский счет',
    response_model=ResponseSuccess,
    status_code=status.HTTP_200_OK
)
async def update_bank_account_by_id(
    body: UpdateBankAccount,
    id: int = Path(default=1, description='Уникальный идентификатор', ge=1),
    db: Session = Depends(get_db)
):
    return await update_bank_account_by_id_controller(db, id, body)