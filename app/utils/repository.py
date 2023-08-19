from abc import ABC, abstractmethod

from sqlalchemy import select

from app.db.base import async_session


class AbstractRepository(ABC):
    model = None

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def add_one(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository, ABC):
    model = None

    async def find_all(self):
        async with async_session() as session:
            query = select(self.model)
            res = await session.execute(query)
            res = [row[0].to_read_model() for row in res.all()]
            return res
