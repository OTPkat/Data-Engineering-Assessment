from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
from models import PlaceModel, PeopleModel, Base
from schemas import Place, People
from loader import CsvLoader

# todo unfortunately the Table(.) use the inspect method which isn't available
# with an async engine. Hence I copied models here as well (code duplication). That put 3 possible options:
# 1) run this with conn.run_sync().
# 2) run the loading with sync engine.
# Didn't have time to do it.


async def async_load():
    """
    :param engine:
    :return:
    """
    engine = create_async_engine(
        "postgresql+asyncpg://test_user:test_password@database/test_db",
        future=True,
        echo=True,
    )

    csv_loader = CsvLoader(engine=engine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await csv_loader.load_csv(
        file_path="/data/places.csv", model=PlaceModel, schema=Place
    )
    await csv_loader.load_csv(
        file_path="/data/people.csv", model=PeopleModel, schema=People
    )


if __name__ == "__main__":
    asyncio.run(async_load())

