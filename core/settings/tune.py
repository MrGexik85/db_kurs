from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

def set_routers(app: FastAPI):
    pass


def use_session(app: FastAPI):
    app.add_middleware(
        SessionMiddleware,
        secret_key="Supersecret_key",
    )