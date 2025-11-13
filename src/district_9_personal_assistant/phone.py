import re
from dataclasses import dataclass

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
    # If no plus but number is in international format — add +
    if cleaned and cleaned[0] != '+':
        cleaned = '+' + cleaned
    return cleaned


@dataclass
class Phone:
    number: str
    is_main: bool = False

    def __post_init__(self):
        # Always normalize the number upon initialization
        self.number = normalize_phone(self.number)

    def is_valid(self) -> bool:
        """
        Validates the number according to the pattern `^\\+?[1-9][0-9]{7,14}$`
        """
        return PHONE_PATTERN.match(self.number) is not None
