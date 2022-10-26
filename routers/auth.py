from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.session import get_db
from models.user import User
from oauth2.oauth2 import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from schemas.token import Token
from utils import verify

router = APIRouter(tags=["Authentification"])


@router.post("/login", response_model=Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.email == credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )

    verified = verify(credentials.password, user.password)

    if not verified:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        {"id": user.id, "email": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token}
