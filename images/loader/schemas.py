import typing

from pydantic import BaseModel
import datetime


class People(BaseModel):
    given_name: str
    family_name: str
    date_of_birth: datetime.date
    place_of_birth: str

    class Config:
        orm_mode = True


class Place(BaseModel):
    city: str
    county: str
    country: str
    id: typing.Optional[int] = None

    class Config:
        orm_mode = True
