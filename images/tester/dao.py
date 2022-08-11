import typing

from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import func
from models import PlaceModel, PeopleModel


class Dao(object):
    @staticmethod
    async def get_summary(db: Session) -> typing.Dict[str, int]:
        statement = (
            select(func.count(PlaceModel.country), PlaceModel.country)
            .join(
                PeopleModel.place_id_of_birth,
                PeopleModel.place_id_of_birth == PlaceModel.id,
            )
            .group_by(PlaceModel.country)
        )
        result = await db.execute(statement)
        # todo adapt the code above to not have to do the line below
        return {record["country"]: record["count"] for record in result.all()}
