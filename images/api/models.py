from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PlaceModel(Base):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String)
    county = Column(String)
    country = Column(String)


class PeopleModel(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True, autoincrement=True)
    given_name = Column(String)
    family_name = Column(String)
    date_of_birth = Column(Date)
    place_of_birth = Column(String)
