from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
import sqlalchemy as sa

from app.db.base import Base
from app.utils.datetime import utcnow


class User(SQLAlchemyBaseUserTable[int], Base):
    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String, nullable=False)
    username = sa.Column(sa.String, nullable=False)
    registered_at = sa.Column(sa.TIMESTAMP, default=utcnow)
    hashed_password: str = sa.Column(sa.String(length=1024), nullable=False)
    is_active: bool = sa.Column(sa.Boolean, default=True, nullable=False)
    is_superuser: bool = sa.Column(sa.Boolean, default=False, nullable=False)
    is_verified: bool = sa.Column(sa.Boolean, default=False, nullable=False)