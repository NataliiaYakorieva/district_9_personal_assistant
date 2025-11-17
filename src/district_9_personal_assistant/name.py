from dataclasses import dataclass

from src.district_9_personal_assistant.field import BaseField


@dataclass
class Name(BaseField):
    """Represents a contact's name, with validation to ensure it's not empty."""
    value: str

    def validate(self) -> None:
        """
        Validates that the name is not empty or just whitespace.
        Raises ValueError if invalid.
        """
        if not self.value or not self.value.strip():
            raise ValueError("Name cannot be empty.")

    @classmethod
    def from_dict(cls, data: dict) -> "Name":
        """
        Create Name from a plain dict.

        Args:
            data: Dictionary containing name data.

        Returns:
            Name instance.
        """
        return cls(value=data.get("value", ""))

    def __str__(self) -> str:
        return self.value
