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


@router.get('/{id}', response_model=User)
def get_user(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(model_user).filter(model_user.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist"
        )
    return user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def remove_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.query(model_user).delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
