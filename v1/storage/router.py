from fastapi import APIRouter, Depends, Request, status, Query, Path, status
from sqlalchemy.orm import Session

from core.settings.database import get_db
from core.utils.permissions import get_admin_user_from_session, get_auth_user_from_session
from v1.user.schema import UserSession

from .controller import get_storage_products_controller
from .schema import ProductStorage


router = APIRouter(prefix='/storage', tags=['storage'])

@router.get(
    path='/products',
    summary='получить информацию о товарах на складе (их остатки и тд)',
    response_model=list[ProductStorage],
    status_code=status.HTTP_200_OK
)
async def get_storage_products(
    user: UserSession = Depends(get_admin_user_from_session),
    db: Session = Depends(get_db)
):
    return await get_storage_products_controller(db)