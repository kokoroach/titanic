import pytest
from app.domain.passenger import Passenger, DataValidationError


def test_passenger_from_dict_valid():
    details = {
        "PassengerId": "1",
        "Survived": "0",
        "Pclass": "3",
        "Name": 'Braund, Mr. Owen Harris    ("Alias")',
        "Sex": "male",
        "Age": "22",
        "SibSp": "1",
        "Parch": "0",
        "Ticket": "A/5 21171",
        "Fare": "7.25",
        "Cabin": "",
        "Embarked": "S",
    }

    passenger = Passenger.from_dict(details)

    assert passenger.passenger_id == 1
    assert passenger.survived is False
    assert passenger.first_name == "Owen Harris"
    assert passenger.last_name == "Braund"
    assert passenger.alias == "Alias"
    assert passenger.age == 22.0
    assert passenger.sex == "m"


def test_passenger_from_dict_invalid():
    details = {
        "PassengerId": "1",
        "Survived": "0",
        # Missing 'Pclass' key
        "Name": 'Braund, Mr. Owen Harris',
        "Sex": "male",
        "Age": "22",
        "SibSp": "1",
        "Parch": "0",
        "Ticket": "A/5 21171",
        "Fare": "7.25",
        "Cabin": "",
        "Embarked": "S",
    }

    with pytest.raises(DataValidationError):
        Passenger.from_dict(details)
