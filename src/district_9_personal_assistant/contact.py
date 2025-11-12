from dataclasses import dataclass, field
from typing import List
from .phone import Phone, normalize_phone


@dataclass
class Contact:
    name: str
    phones: List[Phone] = field(default_factory=list)

    def add_phone(self, phone_number: str, main: bool = False) -> str:
        phone = Phone(number=phone_number, is_main=main)
        if not phone.is_valid():
            return f"Inaccurate number: {phone_number}"
        if phone.is_main:
            self.reset_main()
        self.phones.append(phone)
        return f"Phone {phone.number} added to contact {self.name}."

    def reset_main(self):
        for p in self.phones:
            p.is_main = False

    def set_main_phone(self, phone_number: str) -> str:
        normalized = normalize_phone(phone_number)
        found = False
        for p in self.phones:
            if p.number == normalized:
                self.reset_main()
                p.is_main = True
                found = True
                break
        if found:
            return f"Main number is set to: {normalized}"
        else:
            return f"Number {normalized} is not found in contact {self.name}."

    def list_phones(self) -> str:
        out = []
        for p in self.phones:
            label = "[main]" if p.is_main else ""
            out.append(f"{label} {p.number}".strip())
        return "; ".join(out)
