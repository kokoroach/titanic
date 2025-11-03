from csv import DictReader
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Passenger:
    passenger_id: int
    survived: bool
    p_class: int
    name: str
    sex: str
    age: float
    sib_sp: int
    par_ch: int
    ticket: int
    fare: float
    cabin: int
    embarked: str

    @classmethod
    async def from_csv(cls, filename: Path) -> List["Passenger"]:
        """
        Import passenger dataset from CSV and serialize to a list Passenger
        dataclass
        """
        passengers = []

        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            # Use DictReader to get each row as a dictionary
            reader = DictReader(file)
            for row in reader:
                try:
                    passenger = Passenger(
                        passenger_id=int(row['PassengerId']),
                        survived=bool(row['Survived']),
                        p_class=int(row['Pclass']),
                        name=row['Name'],
                        sex='m' if row['Sex'] == 'male' else 'f',
                        age=0 if row['Age'] == '' else float(row['Age']),
                        sib_sp=int(row['SibSp']),
                        par_ch=int(row['Parch']),
                        ticket=row['Ticket'],
                        fare=float(row['Fare']),
                        cabin=row['Cabin'],
                        embarked=row['Embarked'],
                    )
                    passengers.append(passenger)
                except (ValueError, KeyError) as e:
                    print(f"Error processing row {row}: {e}")

        return passengers
