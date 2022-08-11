from fastapi import Depends, FastAPI
from database import get_db, engine
from sqlalchemy.orm import Session
from typing import List
from dao.summary import Dao
from models import Base, PlaceModel
from dao.schema import Place
from sqlalchemy.ext.asyncio import AsyncSession
import csv

app = FastAPI(title="Temper Assignment")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        # with open("/data/places.csv") as csv_file:
        #     reader = csv.reader(csv_file)
        #     headers = next(reader)
        #     for i, row in enumerate(reader):
        #         record = Place(id=i, **{header: value for (header, value) in zip(headers, row)})
        #         await conn.execute(PlaceModel.__table__.insert(), record.dict())

    async with AsyncSession(engine) as session:
        async with session.begin():
            with open("/data/places.csv") as csv_file:
                reader = csv.reader(csv_file)
                headers = next(reader)
                session.add_all(
                    [
                        PlaceModel(**{header: value for (header, value) in zip(headers, row)})
                        for row in reader
                    ]
                    )

        await session.commit()


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
