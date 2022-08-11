from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PlaceModel(Base):
    __tablename__ = "place"
    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String)
    county = Column(String)
    country = Column(String)

