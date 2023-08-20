from abc import ABC

from app.utils.repository import SQLAlchemyRepository
from app.apps.chat.models import Message


class ChatRepository(SQLAlchemyRepository, ABC):
    model = Message
