from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from v1 import authRouter, productRouter, categoriesRouter, bankAccountRouter, storageRouter

def set_routers(app: FastAPI):
    app.include_router(authRouter)
    app.include_router(productRouter)
    app.include_router(categoriesRouter)
    app.include_router(bankAccountRouter)
    app.include_router(storageRouter)


def use_session(app: FastAPI):
    app.add_middleware(
        SessionMiddleware,
        secret_key="Supersecret_key",
    )