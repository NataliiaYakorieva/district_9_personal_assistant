from dataclasses import dataclass
import re
import urllib.parse
import webbrowser

# Allow letters/digits/space/dash; 2–20 chars
ZIP_PATTERN = re.compile(r"^[A-Za-z0-9\- ]{2,20}$")


def _clean_text(value: str) -> str:
    """Trim spaces and collapse internal whitespace."""
    if not value:
        return ""
    return " ".join(value.strip().split())


@dataclass
class Address:
    """Represents a postal address.

    Normalization rules:
      - street and city -> Title Case
      - country and zip -> UPPER
    """

    country: str
    city: str
    street_address: str
    zip_code: str

    def __post_init__(self) -> None:
        """Clean and validate fields."""
        self.country = _clean_text(self.country).upper()
        self.city = _clean_text(self.city).title()
        self.street_address = _clean_text(self.street_address).title()
        self.zip_code = _clean_text(self.zip_code).upper()

        if not ZIP_PATTERN.match(self.zip_code):
            raise ValueError(
                "zip_code must contain only letters, digits, spaces or dashes "
                "(2–20 characters)"
            )

    def full_address(self) -> str:
        """Return the formatted full address."""
        parts = [
            self.street_address,
            self.city,
            self.zip_code,
            self.country,
        ]
        return ", ".join(p for p in parts if p)

    def open_in_google_maps(self) -> None:
        """Open the address in Google Maps (default browser)."""
        base = "https://www.google.com/maps/search/?api=1&query="
        query = urllib.parse.quote(self.full_address())
        url = base + query
        webbrowser.open(url)

    def to_dict(self) -> dict:
        """Convert address to a plain dict for saving."""
        return {
            "country": self.country,
            "city": self.city,
            "street_address": self.street_address,
            "zip_code": self.zip_code,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Address":
        """Create Address from a plain dict."""
        return cls(
            country=data.get("country", ""),
            city=data.get("city", ""),
            street_address=data.get("street_address", ""),
            zip_code=data.get("zip_code", ""),
        )
