from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class By(str, Enum):
    me = 'me'
    zerobot = 'zerobot'


class MessageBase(BaseModel):
    to: int
    content: str
    by: By


class MessageCreate(BaseModel):
    content: str
    by: By


# class used for response model
class Message(MessageBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
