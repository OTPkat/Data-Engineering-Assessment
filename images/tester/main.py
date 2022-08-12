import asyncio
import json
import typing

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from models import PlaceModel, PeopleModel


async def get_summary(db: Session) -> typing.Dict[str, int]:
    statement = (
        select(func.count(PlaceModel.country), PlaceModel.country)
        .join(
            PeopleModel.place_id_of_birth,
            PeopleModel.place_id_of_birth == PlaceModel.id,
        )
        .group_by(PlaceModel.country)
    )
    result = await db.execute(statement)
    # todo adapt the code above to not have to do the line below (pivot)
    return {record["country"]: record["count"] for record in result.all()}


async def async_test():
    engine = create_async_engine(
        "postgresql+asyncpg://test_user:test_password@database/test_db",
        future=True,
        echo=True,
    )

    async with AsyncSession(engine) as session:
        async with session.begin():
            summary = await get_summary(db=session)
            print(f"DB summary: {summary}")
            with open("/data/sample_output1.json", "w") as fp:
                json.dump(summary, fp)


if __name__ == "__main__":
    asyncio.run(async_test())
