import asyncio
import json
import os
import typing

from sqlalchemy import func
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from orm import PlacesOrm, PeopleOrm


async def get_db_summary(db: Session) -> typing.Dict[str, int]:
    statement = (
        select(func.count(PlacesOrm.country), PlacesOrm.country)
        .join(
            PeopleOrm.place_id_of_birth,
            PeopleOrm.place_id_of_birth == PlacesOrm.id,
        )
        .group_by(PlacesOrm.country)
    )
    result = await db.execute(statement)
    # todo adapt the code above to not have to do the line below (pivot)
    return {record["country"]: record["count"] for record in result.all()}


async def async_test():
    # We could do an api container with FastAPI for instance
    # to contact instead of connecting directly to the database, depending
    # on what the context is
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

    async with AsyncSession(engine) as session:
        async with session.begin():
            summary = await get_db_summary(db=session)
            with open("/data/sample_output1.json", "w") as fp:
                json.dump(summary, fp)


if __name__ == "__main__":
    asyncio.run(async_test())
