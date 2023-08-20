from abc import ABC, abstractmethod
from sqlalchemy import select, delete, update
from app.db.base import async_session


class AbstractRepository(ABC):
    model = None

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def add_one(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, id):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id, data):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository, ABC):
    model = None

    async def find_all(self):
        async with async_session() as session:
            query = select(self.model)
            res = await session.execute(query)
            res = [row[0].to_read_model() for row in res.all()]
            return res

    async def add_one(self, data):
        async with async_session() as session:
            instance = self.model(**data)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance.to_read_model()

    async def find_one(self, id):
        async with async_session() as session:
            query = select(self.model).where(self.model.id == id)
            res = await session.execute(query)
            instance = res.scalar()
            if instance:
                return instance.to_read_model()
            return None

    async def update_one(self, id, data):
        async with async_session() as session:
            query = (
                update(self.model)
                .where(self.model.id == id)
                .values(**data)
                .returning(self.model)
            )
            res = await session.execute(query)
            instance = res.scalar()
            if instance:
                await session.commit()
                await session.refresh(instance)
                return instance.to_read_model()
            return None

    async def delete_one(self, id):
        async with async_session() as session:
            query = delete(self.model).where(self.model.id == id)
            await session.execute(query)
            await session.commit()
