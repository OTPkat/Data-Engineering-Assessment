import datetime
import typing

from pydantic import BaseModel


class People(BaseModel):
    given_name: str
    family_name: str
    date_of_birth: datetime.date
    place_id_of_birth: int

    class Config:
        orm_mode = True


class Place(BaseModel):
    city: str
    county: str
    country: str
    id: typing.Optional[int] = None

    class Config:
        orm_mode = True
