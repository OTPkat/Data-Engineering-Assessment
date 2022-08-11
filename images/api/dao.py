from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import func
from models import PlaceModel, PeopleModel


class Dao(object):

    @staticmethod
    async def get_all(db: Session, model):
        records = await db.execute(select(model))
        return records.scalars().all()

    @staticmethod
    async def insert(db: Session, model, record):
        record = model(**record.dict())
        db.add(record)
        await db.commit()
        await db.refresh(record)
        return record

    @staticmethod
    async def get_summary(db: Session):
        statement = select(
            func.count(PlaceModel.country)
        ).join(
            PeopleModel.place_of_birth, PeopleModel.place_of_birth == PlaceModel.city
        ).group_by(PlaceModel.country)
        result = await db.execute(statement)
        scalar_results = result.scalars().all()
        return scalar_results
