from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from core.settings.database import get_db
from core.utils.permissions import get_admin_user_from_session, get_auth_user_from_session
from v1.user.schema import UserSession
from v1.product.controller import create_new_product_controller


router = APIRouter(prefix='/product', tags=['product'])


@router.post(
    path='',

)
async def create_new_product(
    db: Session = Depends(get_db), 
    user: UserSession = Depends(get_admin_user_from_session)
):
    return await create_new_product_controller(db, user)
