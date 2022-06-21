from fastapi import APIRouter, Depends, Request, status, Query, Path, status
from sqlalchemy.orm import Session
from datetime import date

from core.settings.database import get_db
from core.utils.permissions import get_admin_user_from_session, get_auth_user_from_session
from v1.auth.schema import ResponseSuccess
from v1.user.schema import UserSession

from .controller import ( 
    create_contractor_controller, 
    get_contractors_controller, 
    get_contractor_by_id_controller, 
    create_contractor_product_association_controller, 
    delete_contractor_product_association_controller,
    set_contractor_bank_account_controller
)
from .schema import CreateContractor, Contractor


router = APIRouter(prefix='/contractors', tags=['contractors'])

@router.post(
    path='',
    summary='Cоздать нового поставщика',
    response_model=ResponseSuccess,
    status_code=status.HTTP_201_CREATED
)
async def create_contractor(
    body: CreateContractor,
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await create_contractor_controller(db, body)


@router.get(
    path='',
    summary='получить всех поставщиков',
    response_model=list[Contractor],
    status_code=status.HTTP_200_OK
)
async def get_contractors(
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await get_contractors_controller(db)


@router.get(
    path='/{id}',
    summary='получить поставщика по его id',
    response_model=Contractor,
    status_code=status.HTTP_200_OK
)
async def get_contractor_by_id(
    id: int = Path(default=1, description='Идентификатор поставщика', ge=1),
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await get_contractor_by_id_controller(db, id)


@router.post(
    path='/{contractorId}/product/{productId}',
    summary='привязать что поставщик поставляет этот товар',
    response_model=ResponseSuccess,
    status_code=status.HTTP_200_OK
)
async def create_contractor_product_association(
    contractorId: int = Path(default=1, description='Идентификатор поставщика', ge=1),
    productId: int = Path(default=1, description='Идентификатор продукта', ge=1),
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await create_contractor_product_association_controller(db, contractorId, productId)


@router.delete(
    path='/{contractorId}/product/{productId}',
    summary='отвязать поставщика от товара',
    response_model=ResponseSuccess,
    status_code=status.HTTP_200_OK
)
async def delete_contractor_product_association(
    contractorId: int = Path(default=1, description='Идентификатор поставщика', ge=1),
    productId: int = Path(default=1, description='Идентификатор продукта', ge=1),
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await delete_contractor_product_association_controller(db, contractorId, productId)


@router.post(
    path='/{contractorId}/bank/{bankId}',
    summary='привязать банковский счет к поставщику',
    response_model=ResponseSuccess,
    status_code=status.HTTP_200_OK
)
async def set_contractor_bank_account(
    contractorId: int = Path(default=1, description='Идентификатор поставщика', ge=1),
    bankId: int = Path(default=1, description='Идентификатор банковского счета', ge=1),
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await set_contractor_bank_account_controller(db, contractorId, bankId)