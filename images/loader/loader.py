import csv
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Type, TypeVar, Generic
from abc import ABC, abstractmethod
from models import PeopleModel, PlaceModel, Base
from schemas import Place, People, BaseModel as BaseSchema
import pandas as pd
from sqlalchemy.future import select

T = TypeVar("T", bound=Type[Base])
S = TypeVar("S", bound=Type[BaseSchema])


class FileLoader(Generic[T, S], ABC):
    model: Type[T]
    schema: Type[S]

    @classmethod
    async def load_csv(cls, engine, file_path: str) -> None:
        with open(file_path) as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader)
            await cls.load_records(
                engine=engine,
                records=[
                    cls.model(
                        **cls.schema(
                            **{header: value for (header, value) in zip(headers, row)}
                        ).dict()
                    )
                    for row in reader
                ],
            )

    @staticmethod
    async def load_records(engine, records: List[T]) -> None:
        async with AsyncSession(engine) as session:
            async with session.begin():
                session.add_all(records)

    @abstractmethod
    async def load_file(self, file_path: str, engine) -> None:
        ...


class PlaceLoader(FileLoader[PlaceModel, Place]):
    model = PlaceModel
    schema = Place

    @classmethod
    async def load_file(cls, file_path: str, engine) -> None:
        await cls.load_csv(file_path=file_path, engine=engine)


class PeopleLoader(FileLoader[PeopleModel, People]):
    model = PeopleModel
    schema = People

    @classmethod
    async def load_file(cls, file_path: str, engine) -> None:
        # Below I use pandas as I didn't get the time to properly
        # do everything with sqlalchemy, but in practice the join
        # made below would be made in SQL using temp table if data volume
        # is big, otherwise a with statement can work.
        async with AsyncSession(engine) as session:
            async with session.begin():
                statement = select(PlaceModel.id, PlaceModel.city)
                places = await session.execute(statement)
                df_places = pd.DataFrame(
                    places.all(), columns=["place_id_of_birth", "city"]
                )
        df_people = pd.read_csv("/data/people.csv")
        await cls.load_records(
            engine=engine,
            records=[
                PeopleModel(**People(**x).dict())
                for x in pd.merge(
                    df_people,
                    df_places,
                    right_on="city",
                    left_on="place_of_birth",
                )[
                    [
                        "place_id_of_birth",
                        "date_of_birth",
                        "family_name",
                        "given_name",
                    ]
                ].to_dict(
                    "records"
                )
            ],
        )
