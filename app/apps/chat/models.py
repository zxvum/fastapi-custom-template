from app.db.models import BaseModel
import sqlalchemy as sa
from app.apps.chat import schemas


class Message(BaseModel):
    __tablename__ = "message"

    text = sa.Column(sa.Text, nullable=False)

    def to_read_model(self):
        return schemas.Message(
            id=self.id,
            text=self.text,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
