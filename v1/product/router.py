from fastapi import APIRouter, Depends, Request, status, Query, Path
from sqlalchemy.orm import Session

from core.settings.database import get_db
from core.utils.permissions import get_admin_user_from_session, get_auth_user_from_session
from v1.user.schema import UserSession
from v1.product.controller import (
    create_new_product_controller, 
    get_products_controller, 
    get_product_by_id_controller, 
    delete_product_by_id_controller,
    update_product_by_id_controller,
)
from v1.product.schema import CreateProduct, ProductResponse, ProductUpdateRequest
from v1.auth.schema import ResponseSuccess


router = APIRouter(prefix='/product', tags=['product'])


@router.post(
    path='',
    summary='создать новый экземпляр продукта',
    response_model=CreateProduct,
    status_code=status.HTTP_201_CREATED
)
async def create_new_product(
    body: CreateProduct,
    db: Session = Depends(get_db), 
    user: UserSession = Depends(get_admin_user_from_session)
):
    return await create_new_product_controller(db, user, body)


@router.get(
    path='',
    summary='получить информацию о всех товарах',
    response_model=list[ProductResponse],
    status_code=status.HTTP_200_OK
)
async def get_products(
    category_id: int | None = Query(default=None, ge=1),
    db: Session = Depends(get_db), 
):
    return await get_products_controller(db, category_id)


@router.get(
    path='/{id}',
    summary='получить данные об одном товаре по его id',
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK
)
async def get_product_by_id(
    id: int = Path(default=0, example=2, ge=1),
    db: Session = Depends(get_db),
):
    return await get_product_by_id_controller(db, id)


@router.delete(
    path='/{id}',
    summary='удалить выбранный товар',
    response_model=ResponseSuccess,
    status_code=status.HTTP_200_OK
)
async def delete_product_by_id(
    id: int = Path(default=0, example=2, ge=1),
    db: Session = Depends(get_db),
    user: UserSession = Depends(get_admin_user_from_session)
):
    return await delete_product_by_id_controller(db, id)


@router.patch(
    path='/{id}',
    summary='',
    response_model=ResponseSuccess,
    status_code=status.HTTP_200_OK
)
async def update_product_by_id(
    body: ProductUpdateRequest,
    id: int = Path(default=0, example=2, ge=1),
    db: Session = Depends(get_db),
    user: UserSession = Depends(get_admin_user_from_session)
):
    return await update_product_by_id_controller(db, id, body)