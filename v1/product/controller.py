from fastapi import HTTPException
from sqlalchemy.orm import Session

from v1.user.schema import UserSession




async def create_new_product_controller(db: Session, user: UserSession):
    raise HTTPException(401, 'Not implemented')
