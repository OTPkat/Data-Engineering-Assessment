import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from loader import PeopleLoader, PlaceLoader
from models import Base


async def async_load():
    engine = create_async_engine(
        f"postgresql+asyncpg://test_user:test_password@database/test_db",
        future=True,
        echo=True,
    )

    async with engine.begin() as conn:
        # depending on the context we wouldn't drop all here,
        # I let it here for test purposes.
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await PlaceLoader.load_file(file_path="/data/places.csv", engine=engine)
    await PeopleLoader.load_file(file_path="/data/places.csv", engine=engine)


if __name__ == "__main__":
    asyncio.run(async_load())
