from sqlalchemy.orm import Session
from sqlalchemy.future import select


class Dao:

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
