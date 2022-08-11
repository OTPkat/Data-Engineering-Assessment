from fastapi import Depends, FastAPI
from database import get_db, engine
from sqlalchemy.orm import Session
from typing import List, Dict
from dao import Dao
from models import Base, PlaceModel, PeopleModel
from schema import Place, People


app = FastAPI(title="Temper Assignment")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
def welcome_to_assignment():
    return {"message": "Welcome to my solution",
            "docs": "refer to /docs to test the endpoints"}


@app.get("/places", response_model=List[Place])
async def get_places(
    db: Session = Depends(get_db)
):
    places = await Dao.get_all(db=db, model=PlaceModel)
    return places


@app.get("/people", response_model=List[People])
async def get_people(
    db: Session = Depends(get_db)
):
    people = await Dao.get_all(db=db, model=PeopleModel)
    return people


@app.get("/summary")
async def get_summary(
    db: Session = Depends(get_db)
):
    summary = await Dao.get_summary(db=db)
    return summary

