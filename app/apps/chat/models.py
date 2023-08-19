from app.db.models import BaseModel
import sqlalchemy as sa


class Message(BaseModel):
    __tablename__ = "message"

    text = sa.Column(sa.Text, nullable=False)

