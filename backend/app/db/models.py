from app.db.database import Base
from sqlalchemy import (
    Column, Integer, String, Boolean, SmallInteger, Numeric, Text
)


class PassengerModel(Base):
    __tablename__ = "passengers"

    passenger_id = Column(Integer, primary_key=True, index=True)
    survived = Column(Boolean)
    p_class = Column(SmallInteger)
    title = Column(String)
    first_name = Column(String)
    maiden_name = Column(String)
    last_name = Column(String)
    nickname = Column(String)
    alias = Column(String)
    spouse = Column(String)
    sex = Column(String)
    age = Column(Numeric, nullable=True)
    sib_sp = Column(SmallInteger)
    par_ch = Column(SmallInteger)
    ticket = Column(String)
    fare = Column(Numeric)
    cabin = Column(String)
    embarked = Column(String)
