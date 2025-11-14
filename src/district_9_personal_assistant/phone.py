import re

# Додаємо правильний шаблон для PHONE_PATTERN:
PHONE_PATTERN = re.compile(r'^\+\d{8,15}$')


def validate(self) -> None:
    """
    Validates the phone number:
    - Must start with '+' followed by 8–15 digits
    - Detects and explains common mistakes
    """
    if not self.number:
        raise ValueError("Phone number cannot be empty.")

    if not PHONE_PATTERN.fullmatch(self.number):
        if re.search(r'[a-zA-Z]', self.number):
            raise ValueError(
                f"Phone number contains letters: '{self.number}'. "
                "Please remove any accidental text or typos."
            )
        if re.search(r'[^\d+]', self.number):
            raise ValueError(
                f"Phone number contains invalid symbols: '{self.number}'. "
                "Only digits and a leading '+' are allowed."
            )
        if not self.number.startswith('+'):
            raise ValueError(
                f"Phone number missing '+' prefix: '{self.number}'. "
                "International format should start with '+'."
            )
        raise ValueError(
            f"Invalid phone number format: '{self.number}'. "
            "Expected format: + followed by 8–15 digits, starting with non-zero."
        )
