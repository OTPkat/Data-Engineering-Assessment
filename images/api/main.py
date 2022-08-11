from fastapi import Depends, FastAPI
from database import get_db, engine
from sqlalchemy.orm import Session
from typing import List
from dao.summary import Dao
from models import Base, PlaceModel
from dao.schema import Place


app = FastAPI(title="Temper Assignment")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.get("/places", response_model=List[Place])
async def get_places(
    db: Session = Depends(get_db)
):
    places = await Dao.get_all(db=db, model=PlaceModel)
    return places
