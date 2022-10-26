from database.base import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, text


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    to = Column(String, nullable=False)
    content = Column(String, nullable=False)
    by = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("(DATETIME('now'))")
    )

    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
