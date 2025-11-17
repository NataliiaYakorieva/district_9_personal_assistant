from datetime import datetime, date
from dataclasses import dataclass

from src.district_9_personal_assistant.field import BaseField
from src.district_9_personal_assistant.helpers.message import fail_message


@dataclass
class Birthday(BaseField):
    """
    Represents a contact's birthday with validation and age calculation.

    Attributes:
        value: Birthday string in DD.MM.YYYY format.
    """
    value: str
    DATE_FORMAT = "%d.%m.%Y"

    def __post_init__(self) -> None:
        """
        Parse and store the date object after initialization.
        """
        self._birthday: date | None = None
        if self.value:
            self._birthday = self._parse_date(self.value)
        super().__post_init__()

    @property
    def birthday(self) -> date | None:
        """
        Returns the birthday as a date object, or None if not set.
        """
        return self._birthday

    def _parse_date(self, date_str: str) -> date:
        """
        Parse date string to date object.
        Raises ValueError if format is incorrect.
        """
        try:
            birth_date = datetime.strptime(date_str, self.DATE_FORMAT).date()
            return birth_date
        except ValueError as e:
            raise ValueError(
                fail_message(
                    f"Data format is incorrect: '{date_str}'. "
                    "Please use the next format DD.MM.YYYY. "
                    f"{e}"
                )
            )

    def validate(self) -> None:
        """
        Validates that the birthday is not in the future.
        Raises ValueError if invalid.
        """
        if self._birthday and self._birthday > date.today():
            raise ValueError(fail_message("Birthday cannot be in the future."))

    @classmethod
    def from_dict(cls, data: dict) -> "Birthday":
        """
        Create Birthday from a plain dict.

        Args:
            data: Dictionary containing birthday data.

        Returns:
            Birthday instance.
        """
        return cls(value=data.get("value", ""))

    @property
    def age(self) -> int:
        """
        Calculate the age based on the birthday.

        Returns:
            Age as integer.
        """
        if not self.birthday:
            return 0
        today = date.today()
        age = today.year - self.birthday.year
        if today < self.birthday.replace(year=today.year):
            age -= 1
        return age

    @property
    def has_had_birthday_this_year(self) -> bool:
        """
        Check if the birthday has occurred this year.

        Returns:
            True if birthday has occurred this year, False otherwise.
        """
        if not self.birthday:
            return False
        today = date.today()
        this_year_bday = self.birthday.replace(year=today.year)
        return today >= this_year_bday

    def __str__(self) -> str:
        return self.value if self.value else ""
