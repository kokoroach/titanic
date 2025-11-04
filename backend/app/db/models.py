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

    def to_dict(self) -> dict:
        """
        Return a JSON-serializable dictionary representation of the Passenger.
        """
        return {
            "passenger_id": self.passenger_id,
            "survived": self.survived,
            "p_class": self.p_class,
            "title": self.title,
            "first_name": self.first_name,
            "maiden_name": self.maiden_name,
            "last_name": self.last_name,
            "nickname": self.nickname,
            "alias": self.alias,
            "spouse": self.spouse,
            "sex": self.sex,
            "age": float(self.age) if self.age is not None else None,
            "sib_sp": self.sib_sp,
            "par_ch": self.par_ch,
            "ticket": self.ticket,
            "fare": float(self.fare),
            "cabin": self.cabin,
            "embarked": self.embarked,
        }
