from sqlalchemy import Column, Integer, String, Boolean, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Duelist(Base):
    __tablename__ = "duelists"
    discord_user_id = Column(BigInteger, primary_key=True, index=True)
    availability = Column(Boolean)
    name = Column(String)
    message_id = Column(BigInteger, nullable=True)
    n_win = Column(Integer)
    n_loss = Column(Integer)
    n_draw = Column(Integer)
