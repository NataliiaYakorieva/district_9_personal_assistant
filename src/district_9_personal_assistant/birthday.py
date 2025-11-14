from datetime import datetime, date, timedelta
import random


class Birthday:

    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, birthday_str: str):
        self._birthday = None
        if birthday_str:
            self._birthday = self._validate_date(birthday_str)

    @property
    def birthday(self) -> date:
        return self._birthday

    def _validate_date(self, date_str: str) -> date:
        try:
            birth_date = datetime.strptime(date_str, self.DATE_FORMAT).date()

            if birth_date > date.today():
                raise ValueError("Birthday cannot be in future.")
            return birth_date
        except ValueError as e:
            raise ValueError(
                f"Data format is incorrect: '{date_str}'. "
                "Please use the next format DD.MM.YYYY. "
                f"{e}"
            )

    @property
    def age(self) -> int:
        today = date.today()
        age = today.year - self.birthday.year
        if today < self.birthday.replace(year=today.year):
            age -= 1
        return age

    @property
    def has_had_birthday_this_year(self) -> bool:
        today = date.today()
        this_year_bday = self.birthday.replace(year=today.year)
        return today >= this_year_bday

    @classmethod
    def find_birthdays_this_week(cls, contacts: dict[str, str]) -> dict[str, date]:
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        birthdays_this_week = {}

        for name, bday_str in contacts.items():
            try:
                bday_obj = datetime.strptime(bday_str, cls.DATE_FORMAT).date()
                next_bday = bday_obj.replace(year=today.year)
                if next_bday < today:
                    next_bday = bday_obj.replace(year=today.year + 1)

                if start_of_week <= next_bday <= end_of_week:
                    birthdays_this_week[name] = next_bday

            except ValueError:
                print(
                    f"Invalid date format for {name}: '{bday_str}'. "
                    "Expected format: DD.MM.YYYY"
                )
                continue

        return birthdays_this_week

    @classmethod
    def add_birthday(cls, contacts: dict[str, str], name: str, birthday_str: str) -> None:
        try:
            birth_date = datetime.strptime(
                birthday_str, cls.DATE_FORMAT).date()
            if birth_date > date.today():
                raise ValueError("Birthday cannot be in future.")
            contacts[name] = birthday_str
        except ValueError as e:
            raise ValueError(
                f"Cannot add birthday for '{name}': {e}"
            )

    @classmethod
    def find_birthdays_this_day(
            cls,
            contacts: dict[str, str],
            filepath: str = "greetings.txt"
    ) -> dict[str, date]:
        today = date.today()
        birthdays_today = {}

        for name, bday_str in contacts.items():
            try:
                bday_obj = datetime.strptime(bday_str, cls.DATE_FORMAT).date()
                today_bday = bday_obj.replace(year=today.year)

                if today_bday == today:
                    birthdays_today[name] = today_bday

                greetings_sug = input(
                    f"Do you want that I suggest some greetings for {name}?").lower()
                if greetings_sug == "yes":

                    with open(filepath, "r", encoding="utf-8") as file:
                        greetings = [line.strip()
                                     for line in file if line.strip()]

                    if not greetings:
                        print("File is empty.")
                        return

                    for i, greeting in enumerate(
                        random.sample(greetings, min(3, len(greetings))), 1
                    ):
                        print(f"{i}. {greeting.replace('{name}', name)}")
                else:
                    continue

            except ValueError:
                print(
                    f"Invalid date format for {name}: '{bday_str}'. "
                    "Expected format: DD.MM.YYYY"
                )
                continue

        return birthdays_today
