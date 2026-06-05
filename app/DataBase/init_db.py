import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.DataBase.database import Base, engine
from app.DataBase.models import UsersModel, PoetryModel

import asyncio


async def init_db():
    print(f"🔍 Модели в Base.metadata: {list(Base.metadata.tables.keys())}")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        print("✅ База данных успешно инициализирована!")
        print("📊 Созданы таблицы:", [table for table in Base.metadata.tables.keys()])


asyncio.run(init_db())
