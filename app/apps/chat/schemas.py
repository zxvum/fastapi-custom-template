from datetime import datetime
from typing import List

from app.utils.schema import Base


class MessageBase(Base):
    text: str


class Message(MessageBase):
    id: int
    created_at: datetime
    updated_at: datetime


class Messages(Base):
    items: List[Message]
