import asyncio
import os

from sqlalchemy.ext.asyncio import create_async_engine
from loader import PeopleLoader, PlaceLoader
from orm import Base
from sqlalchemy.engine.url import URL


async def async_load():
    engine = create_async_engine(
        URL.create(
            drivername="postgresql+asyncpg",
            username=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            database=os.environ["POSTGRES_DB"],
            host="database",
        ),
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
