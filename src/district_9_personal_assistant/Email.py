from dataclasses import dataclass
import re


@dataclass
class Email:
    """Email class with validation for contact information."""

    address: str

    def __post_init__(self):
        '''Validate the email address format.'''
        if not self.is_valid():
            return (f"Invalid email address: {self.address}")

    def is_valid(self) -> bool:
        """
        Validate email address format.
        Returns:
            bool: True if email is valid, False otherwise
        """
        if not self.address:
            return False

        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, self.address))

    def __str__(self) -> str:
        return self.address

    def __repr__(self) -> str:
        return f"Email(address='{self.address}')"
