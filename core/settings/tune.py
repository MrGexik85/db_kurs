from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from v1 import authRouter, productRouter

def set_routers(app: FastAPI):
    app.include_router(authRouter)
    app.include_router(productRouter)


def use_session(app: FastAPI):
    app.add_middleware(
        SessionMiddleware,
        secret_key="Supersecret_key",
    )