from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    "postgresql+asyncpg://test_user:test_password@database/test_db",
    future=True,
    echo=True
)
session_local = sessionmaker(bind=engine, class_=AsyncSession,  expire_on_commit=False)


async def get_db():
    db = session_local()
    try:
        yield db
    finally:
        await db.close()



