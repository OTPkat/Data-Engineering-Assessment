import asyncio
from sqlalchemy.future import select
from sqlalchemy import func
from models import PlaceModel, PeopleModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession


async def async_test():
    engine = create_async_engine(
        "postgresql+asyncpg://test_user:test_password@database/test_db",
        future=True,
        echo=True,
    )
    async with AsyncSession(engine) as session:
        async with session.begin():
            statement = (
                select(func.count(PlaceModel.country), PlaceModel.country)
                    .join(
                    PeopleModel.place_of_birth,
                    PeopleModel.place_of_birth == PlaceModel.city,
                )
                    .group_by(PlaceModel.country)
            )
            result = await session.execute(statement)
            # todo adapt the code above to not have to do the line below
            print(result)
            print({
                record["country"]: record["count"] for record in result.all()
            })


if __name__ == "__main__":
    asyncio.run(async_test())