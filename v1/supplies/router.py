from fastapi import APIRouter, Depends, Request, status, Query, Path, status
from sqlalchemy.orm import Session
from datetime import date

from core.settings.database import get_db
from core.utils.permissions import get_admin_user_from_session, get_auth_user_from_session
from v1.auth.schema import ResponseSuccess
from v1.user.schema import UserSession

from .controller import get_supplies_controller, get_supplies_by_product_id_controller, create_supply_controller
from .schema import SupplyResponse, CreateSupply


router = APIRouter(prefix='/supplies', tags=['supplies'])


@router.get(
    path='',
    summary='поставки всех товаров (+ фильтры по дате)',
    response_model=list[SupplyResponse],
    status_code=status.HTTP_200_OK
)
async def get_supplies(
    period_from: date | None = Query(default=None, description='От какого дня (можно не указывать эти фильтры, тогда покажет все поставки)', example='2022-05-20'),
    period_to: date | None = Query(default=None, description='До какого дня', example='2022-05-25'),
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await get_supplies_controller(db, period_from, period_to)


@router.get(
    path='/{productId}',
    summary='поставки одного товара (+ фильтры по дате)',
    response_model=list[SupplyResponse],
    status_code=status.HTTP_200_OK
)
async def get_supplies_by_product_id(
    productId: int = Path(default=1, description='Идентификатор товара', ge=1),
    period_from: date | None = Query(default=None, description='От какого дня (можно не указывать эти фильтры, тогда покажет все поставки)', example='2022-05-20'),
    period_to: date | None = Query(default=None, description='До какого дня', example='2022-05-25'),
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await get_supplies_by_product_id_controller(db, productId, period_from, period_to)


@router.post(
    path='',
    summary='добавить новую поставку',
    response_model=ResponseSuccess,
    status_code=status.HTTP_201_CREATED
)
async def create_supply(
    body: CreateSupply,
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await create_supply_controller(db, body)