from fastapi import Depends, FastAPI
from models import Base
from database import get_db, engine
from sqlalchemy.orm import Session

app = FastAPI(title="Temper Assignment")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.get("/country/", response_model=None)
async def get_duelists(
    db: Session = Depends(get_db)
):
    pass