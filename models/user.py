from database.base import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, text
from sqlalchemy.orm import relationship

from .message import Message


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("(DATETIME('now'))")
    )

    messages = relationship(Message)
