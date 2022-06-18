from fastapi import APIRouter, Depends, Path, Request, status
from sqlalchemy.orm import Session

from core.settings.database import get_db
from v1.categories.controller import (
    get_categories_controller, 
    create_category_controller, 
    get_category_by_id_controller, 
    update_category_by_id_controller, 
    delete_category_by_id_controller
)
from v1.categories.schema import CategoryResponse, CreateCategoryRequest
from core.utils.permissions import get_admin_user_from_session, get_auth_user_from_session
from v1.user.schema import UserSession
from v1.auth.schema import ResponseSuccess


router = APIRouter(prefix='/categories', tags=['categories'])


@router.get(
    path='',
    summary='Получить информация о всех существующих категориях',
    response_model=list[CategoryResponse],
    status_code=status.HTTP_200_OK
)
async def get_categories(
    db: Session = Depends(get_db)
):
    return await get_categories_controller(db)


@router.post(
    path='',
    summary='Создать новый объект категории',
    response_model=ResponseSuccess,
    status_code=status.HTTP_201_CREATED
)
async def create_category(
    body: CreateCategoryRequest,
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await create_category_controller(db, body)


@router.get(
    path='/{id}',
    summary='получить информацию о категории по id',
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK
)
async def get_category_by_id(
    id: int = Path(default=1, description='Идентификатор категории', ge=1),
    db: Session = Depends(get_db)
):
    return await get_category_by_id_controller(db, id)


@router.patch(
    path='/{id}',
    summary='Обновить данные категории',
    response_model=ResponseSuccess,
    status_code=status.HTTP_200_OK
)
async def update_category_by_id(
    body: CreateCategoryRequest,
    id: int = Path(default=1, description='Идентификатор категории', ge=1),
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await update_category_by_id_controller(db, id, body)


@router.delete(
    path='/{id}',
    summary='Удалить выбранную категорию',
    response_model=ResponseSuccess,
    status_code=status.HTTP_200_OK
)
async def delete_category_by_id(
    id: int = Path(default=1, description='Идентификатор категории', ge=1),
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await delete_category_by_id_controller(db, id)
