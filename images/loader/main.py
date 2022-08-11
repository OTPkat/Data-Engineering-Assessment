import pandas as pd
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
from models import PlaceModel, PeopleModel, Base
from schemas import Place, People
from loader import CsvLoader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


# REMARK 1:
# Unfortunately the Table(.) use the inspect method which isn't available
# with an async engine. Hence I copied models here as well (code duplication). That put 3 possible options:
# 1) run this with conn.run_sync().
# 2) run the loading with sync engine.
# Depending on needs this can be easily wrapped into a Fast API application. I didn't think it was essential here.


# basically modify the file before upload and upload to right schema. In practice wouldnt necessarily
# do that.


async def async_load():
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
    async with AsyncSession(engine) as session:
        async with session.begin():
            statement = select(PlaceModel.id, PlaceModel.city)
            places = await session.execute(statement)
            df_places = pd.DataFrame(
                places.all(), columns=["place_id_of_birth", "city"]
            )
            df_people = pd.read_csv("/data/people.csv")
            session.add_all([PeopleModel(**People(**x).dict()) for x in
                pd.merge(
                    df_people, df_places, right_on="city", left_on="place_of_birth"
                )[["place_id_of_birth", "date_of_birth", "family_name", "given_name"]].to_dict('records')
            ])



    # await csv_loader.load_csv(
    #     file_path="/data/people.csv", model=PeopleModel, schema=People
    # )
    #


if __name__ == "__main__":
    asyncio.run(async_load())
