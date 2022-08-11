from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
from models import PlaceModel
from loader import CsvLoader


async def async_load():
    """
    :param engine:
    :return:
    """
    engine = create_async_engine(
        "postgresql+asyncpg://test_user:test_password@database/test_db",
        future=True,
        echo=True
    )

    csv_loader = CsvLoader(engine=engine)
    await csv_loader.load_csv(file_path="/data/places.csv", model=PlaceModel)


if __name__ == '__main__':
    asyncio.run(async_load())
