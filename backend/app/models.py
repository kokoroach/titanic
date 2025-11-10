from dataclasses import asdict, dataclass
from re import compile


class DataValidationError(Exception): ...


@dataclass
class Passenger:
    passenger_id: int
    survived: bool
    title: str
    first_name: str
    maiden_name: str
    last_name: str
    nickname: str
    alias: str
    spouse: str
    p_class: int
    sex: str
    age: float
    sib_sp: int
    par_ch: int
    ticket: str
    fare: float
    cabin: str
    embarked: str

    @classmethod
    def _parse_name_field(cls, name) -> dict:
        """
        Parses a full name string into structured components:
        title, first name, maiden name, last name, nickname, alias, and spouse.
        """
        first_name = ""
        added_first_name = ""
        maiden_name = ""
        last_name = ""
        nickname = ""
        alias = ""
        spouse = ""

        last_name, _rest = name.split(", ")
        title, first_name = _rest.split(". ", 1)

        # Passenger has an alias
        # Form: ("Alias")
        # Example: 'Leeni, Mr. Fahim ("Philip Zenni")'
        if '("' in first_name:
            alias_pattern = compile(
                r'^(?P<first>.+?)\s*\(\s*"(?P<alias>[^"]+)"\s*\)\s*$'
            )
            m = alias_pattern.match(first_name)

            first_name = m.group("first")
            alias = m.group("alias")

        # Passenger has spouse
        # Form: (Spouse)
        # Example: 'Beane, Mrs. Edward (Ethel Clarke)'
        if "(" in first_name:
            spouse_pattern = compile(
                r"^\s*" r"(?:(?P<spouse>[^()]+?)\s*)?" r"\((?P<first>[^()]+)\).*$"
            )
            m = spouse_pattern.match(first_name)

            spouse = m.group("spouse")
            first_name = m.group("first")

            try:
                first_name, maiden_name = first_name.rsplit(" ", 1)
            except ValueError:
                # Name inside parenthesis is not a Maiden Name.
                # Usually an alias
                pass

        # Passenger has nickname
        # Form: "Nickname"
        # Example: 'O\'Brien, Mrs. Thomas (Johanna "Hannah" Godfrey)'
        if '"' in first_name:
            nickname_pattern = compile(
                r'^(?P<first>.+?)\s*"\s*(?P<nickname>[^"]+)\s*"\s*(?P<rest>.*)?$'
            )
            m = nickname_pattern.match(first_name)

            first_name = m.group("first")
            nickname = m.group("nickname")
            # The rest of the first name
            added_first_name = f" {m.group('rest').strip()}" if m.group("rest") else ""

        return {
            "title": title,
            "first": first_name + added_first_name,
            "maiden": maiden_name,
            "last": last_name,
            "nickname": nickname,
            "alias": alias,
            "spouse": spouse,
        }

    @classmethod
    def from_dict(cls, details: dict) -> "Passenger":
        """
        Create a Passenger instance from JSON-like dictionary.
        Performs validation and type conversion.
        """
        try:
            parsed_name = cls._parse_name_field(details["Name"])
            passenger = Passenger(
                passenger_id=int(details["PassengerId"]),
                survived=bool(int(details["Survived"])),
                p_class=int(details["Pclass"]),
                title=parsed_name["title"],
                first_name=parsed_name["first"],
                maiden_name=parsed_name["maiden"],
                last_name=parsed_name["last"],
                nickname=parsed_name["nickname"],
                alias=parsed_name["alias"],
                spouse=parsed_name["spouse"],
                sex="m" if details["Sex"] == "male" else "f",
                age=None if details["Age"] == "" else float(details["Age"]),
                sib_sp=int(details["SibSp"]),
                par_ch=int(details["Parch"]),
                ticket=details["Ticket"],
                fare=float(details["Fare"]),
                cabin=details["Cabin"],
                embarked=details["Embarked"],
            )
        except (ValueError, KeyError) as e:
            raise DataValidationError(
                f"Error processing passenger {details}. {e}"
            ) from e
        return passenger

    def as_json(self) -> dict:
        return asdict(self)
