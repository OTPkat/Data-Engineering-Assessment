from fastapi import Depends, FastAPI
from database import get_db, engine, session_local
from sqlalchemy.orm import Session
from typing import List
from dao.summary import Dao
from models import Base, PlaceModel
from dao.schema import Place
import csv

app = FastAPI(title="Temper Assignment")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        # async with session_local() as session:
        #     async with session.begin():
        #         with open("/data/places.csv") as csv_file:
        #             reader = csv.reader(csv_file)
        #             headers = next(reader)
        #             session.add_all(
        #                 [PlaceModel(**{header: value for (header, value) in zip(headers, row)})
        #                  for row in reader]
        #             )


@app.get("/places", response_model=List[Place])
async def get_places(
    db: Session = Depends(get_db)
):
    places = await Dao.get_all(db=db, model=PlaceModel)
    return places


@app.post("/load", response_model=None)
async def load(
    db: Session = Depends(get_db)
):
    await Dao.load_csv(file_path="/data/places.csv", model=PlaceModel, db=db, schema=Place)
