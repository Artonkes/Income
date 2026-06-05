# crud/base.py
from typing import TypeVar, Generic, Type, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model


    async def get_all(self, session: AsyncSession) -> List[ModelType]:
        result = await session.execute(
            select(self.model)
        )

        return result.scalars().all()


    async def get_by_id(self, session: AsyncSession, id: int, name: str) -> ModelType:

        if id and name == None:
            result = await session.execute(
                select(self.model).where(self.model.id == id)
            )

            obj = result.scalar_one_or_none()
            if obj is None:
                raise HTTPException(
                    status_code=404, detail=f"{self.model.__name__} not found"
                )
            return obj
        if name and id == None:
            result = await session.execute(
                select(self.model).where(self.model.name == name)
            )

            obj = result.scalar_one_or_none()
            if obj is None:
                raise HTTPException(
                    status_code=404, detail=f"{self.model.__name__} not found"
                )
            return obj


    async def create(self, session: AsyncSession, obj_in: dict) -> ModelType:
        obj = self.model(**obj_in)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
        


    async def update(self, session: AsyncSession, id: int, obj_in: dict) -> ModelType:
        obj = await self.get_by_id(session, id)
        for field, value in obj_in.items():
            setattr(obj, field, value)
        await session.commit()
        await session.refresh(obj)
        return obj


    async def delete(self, session: AsyncSession, id: int) -> None:
        obj = await self.get_by_id(session, id)
        await session.delete(obj)
        await session.commit()
