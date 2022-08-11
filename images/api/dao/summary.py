from sqlalchemy.orm import Session
import csv
from sqlalchemy.future import select


class Dao:

    # Using Generics would do whats below better.

    @classmethod
    async def load_csv(cls, db, file_path: str, model, schema):
        with open(file_path) as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader)
            for row in reader:
                record = schema(**{header: value for (header, value) in zip(headers, row)})
                await cls.insert(db=db, model=model, record=record)

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