from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.base import Base
from database.session import engine
from routers import auth, message, user

Base.metadata.create_all(bind=engine)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(message.router)
