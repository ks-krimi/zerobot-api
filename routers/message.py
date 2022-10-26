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
