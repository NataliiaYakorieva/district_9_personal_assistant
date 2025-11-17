import re
from dataclasses import dataclass

from src.district_9_personal_assistant.field import BaseField

PHONE_PATTERN = re.compile(r'^\+[1-9][0-9]{7,14}$')


def normalize_phone(phone_number: str) -> str:
    """
    Normalizes the number to international format:
    removes spaces, dashes, brackets.
    Adds '+' prefix if not present to ensure international format.
    """
    if not phone_number:
        return ""
    cleaned = re.sub(r'[^\d+]', '', phone_number)
    if cleaned and cleaned[0] != '+':
        cleaned = '+' + cleaned
    return cleaned


@dataclass
class Phone(BaseField):
    """
    Represents a phone number for a contact.
    """
    number: str
    is_main: bool = False

    def __post_init__(self) -> None:
        """
        Normalize the phone number after initialization.
        """
        self.number = normalize_phone(self.number)
        super().__post_init__()

    def validate(self) -> None:
        """
        Validates the phone number format.
        Raises ValueError if invalid.
        """
        if not PHONE_PATTERN.match(self.number):
            raise ValueError(f"Invalid phone number format: {self.number}")

    @classmethod
    def from_dict(cls, data: dict) -> "Phone":
        """
        Create a Phone instance from a dictionary.
        """
        return cls(**data)

    def __str__(self) -> str:
        return self.number
