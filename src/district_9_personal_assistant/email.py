from dataclasses import dataclass
import re

from .field import BaseField


@dataclass
class Email(BaseField):
    """Email class with validation for contact information."""

    address: str

    def validate(self) -> None:
        """
        Validate email address format.
        Raises:
            ValueError: If the email format is invalid.
        """
        if not self.address:
            raise ValueError("Email address cannot be empty.")

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, self.address):
            raise ValueError(f"Invalid email address: {self.address}")

    @classmethod
    def from_dict(cls, data: dict) -> "Email":
        """Create Email from a plain dict."""
        return cls(**data)

    def __str__(self) -> str:
        return self.address

    def __repr__(self) -> str:
        return f"Email(address='{self.address}')"
