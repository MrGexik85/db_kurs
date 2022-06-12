from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn  
from core.settings.tune import set_routers, use_session
from core.settings.environment import PORT, DEBUG
from core.settings.database import Base, engine
from models import *

Base.metadata.create_all(bind=engine)

app = FastAPI()

set_routers(app=app)
use_session(app=app)
app.mount("/public", StaticFiles(directory="public"), name="site")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=DEBUG)