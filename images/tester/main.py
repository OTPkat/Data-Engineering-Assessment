import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from dao import Dao
import json


async def async_test():
    engine = create_async_engine(
        "postgresql+asyncpg://test_user:test_password@database/test_db",
        future=True,
        echo=True,
    )

    async with AsyncSession(engine) as session:
        async with session.begin():
            summary = await Dao.get_summary(db=session)
            print(f"DB summary: {summary}")
            with open("/data/sample_output1.json", "w") as fp:
                json.dump(summary, fp)


if __name__ == "__main__":
    asyncio.run(async_test())
