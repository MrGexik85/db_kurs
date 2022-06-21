from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from v1 import authRouter, productRouter, categoriesRouter, bankAccountRouter, storageRouter, suppliesRouter, customersRouter, ordersRouter, userRouter, contractorRouter

def set_routers(app: FastAPI):
    app.include_router(authRouter)
    app.include_router(productRouter)
    app.include_router(categoriesRouter)
    app.include_router(bankAccountRouter)
    app.include_router(storageRouter)
    app.include_router(suppliesRouter)
    app.include_router(customersRouter)
    app.include_router(ordersRouter)
    app.include_router(userRouter)
    app.include_router(contractorRouter)


def use_session(app: FastAPI):
    app.add_middleware(
        SessionMiddleware,
        secret_key="Supersecret_key",
    )