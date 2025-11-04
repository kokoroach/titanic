from sqlalchemy import Boolean, Column, Integer, Numeric, SmallInteger, String

from app.db.database import Base


class PassengerModel(Base):
    """
    This model represents passenger information for the Titanic dataset,
    including personal details, travel details, and survival status.
    """

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

    def __repr__(self) -> str:
        return f"<Passenger(id={self.passenger_id}, name={self.first_name} {self.last_name})>"

    def to_dict(self) -> dict:
        """
        Return a JSON-serializable dictionary representation of the Passenger.
        """
        result = {}

        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, Numeric):
                float(self.age) if self.age is not None else None
            result[column.name] = value
        return result
