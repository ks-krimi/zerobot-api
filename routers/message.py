from typing import List

from core.chatbot import get_response, intents, predict_class
from database.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.message import Message as message_model
from oauth2.oauth2 import get_current_user
from schemas.message import By, Message, MessageCreate
from schemas.user import User
from sqlalchemy.orm import Session

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get("/", response_model=List[Message])
def get_messages(limit: int = 10, skip: int = 0, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(message_model).\
        filter(message_model.to == current_user.id).\
        limit(limit).offset(skip).all()


def create_response(to: int, content: str, by: str, db: Session):
    new_message = message_model(
        to=to, content=content, by=by, owner_id=to)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[Message])
def create_message_and_get_response(message: MessageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_message = message_model(
        **message.dict(), to=current_user.id, owner_id=current_user.id)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    ints = predict_class(message.content)
    res = get_response(ints, intents)

    new_res = create_response(
        to=current_user.id, content=res, by=By.zerobot, db=db)

    return {new_message, new_res}


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def remove_messages(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.query(message_model).delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_message(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    message = db.query(message_model).filter(message_model.id == id)
    if message.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Message with id {id} does not exist"
        )
    message.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
