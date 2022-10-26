from fastapi import FastAPI

from database.base import Base
from database.session import engine
from routers import auth, message, user

Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(message.router)
