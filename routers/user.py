from database.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.user import User as model_user
from oauth2.oauth2 import get_current_user
from schemas.user import User, UserCreate
from sqlalchemy.orm import Session
from utils import hash

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # hash user's password before to save into db
    user.password = hash(user.password)

    try:
        new_user = model_user(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already used"
        )
