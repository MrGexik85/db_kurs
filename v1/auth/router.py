from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from v1.auth.schema import ResponseSuccess, ResponseLoginSuccess, RequestRegisterSchema, RequestLoginSchema, login_invalid_responses, register_invalid_responses
from core.settings.database import get_db
from v1.auth.controller import login_service, logout_service, register_service


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    path='/register',
    summary="Регистрация нового пользователя",
    response_model=ResponseLoginSuccess,
    responses=register_invalid_responses
)   
async def register(
    request: Request,
    registerBody: RequestRegisterSchema,
    db: Session = Depends(get_db)
):  
    return await register_service(db, request, registerBody)


@router.post(
    path='/login',
    summary='Вход в аккаунт, получение сессии',
    response_model=ResponseLoginSuccess,
    responses=login_invalid_responses
)
async def login(
    request: Request,
    loginBody: RequestLoginSchema,
    db: Session = Depends(get_db)
):
    return await login_service(db, request, loginBody)


@router.post(
    path='/logout',
    summary='Выход из аккаунта',
    response_model=ResponseSuccess
)
async def logout(
    request: Request,
    db: Session = Depends(get_db)
):
    return await logout_service(db, request)