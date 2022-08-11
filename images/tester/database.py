from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# todo : In practice put a secret ID in docker-compose that we can retrieve in secret manager and build the URI
# also using the funtion create_uri ...

engine = create_async_engine(
    "postgresql+asyncpg://test_user:test_password@database/test_db",
    future=True,
    echo=True,
)
session_local = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    db = session_local()
    try:
        yield db
    finally:
        await db.close()

