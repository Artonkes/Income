from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.DataBase.config_db import URL_DATABASE

class Base(DeclarativeBase):
    pass

engine = create_async_engine(url=URL_DATABASE, echo=True)

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session

SessionDepend = Annotated[AsyncSession, Depends(get_session)]
