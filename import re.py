import re
from dataclasses import dataclass, field
from typing import List, Optional

PHONE_PATTERN = re.compile(r'^\+?[1-9][0-9]{7,14}$')

def normalize_phone(phone_number: str) -> str:
    """Нормалізує номер до міжнародного формату: видаляє пробіли, дефіси, дужки."""
    if not phone_number:
        return ""
    cleaned = re.sub(r'[^\d+]', '', phone_number)
    # Якщо без плюса, але міжнародний — додаємо +
    if cleaned and cleaned[0] != '+':
        cleaned = '+' + cleaned
    return cleaned

@dataclass
class Phone:
    number: str
    is_main: bool = False

    def __post_init__(self):
        # При ініціалізації обов’язково нормалізуємо номер
        self.number = normalize_phone(self.number)

    def is_valid(self) -> bool:
        """Валідує номер згідно шаблону ^+?[1-9][0-9]{7,14}$"""
        return PHONE_PATTERN.match(self.number) is not None

@dataclass
class Contact:
    name: str
    phones: List[Phone] = field(default_factory=list)
    # Додаткові поля: email, адреса, народження і т.д.

    def add_phone(self, phone_number: str, main: bool = False) -> str:
        phone = Phone(number=phone_number, is_main=main)
        if not phone.is_valid():
            return f"Некоректний номер: {phone_number}"
        if phone.is_main:
            self.reset_main()
        self.phones.append(phone)
        return f"Телефон {phone.number} додано до контакту {self.name}."

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
        if found:
            return f"Основний номер встановлено: {normalized}"
        else:
            return f"Номер {normalized} не знайдено серед номерів контакту."

    def list_phones(self) -> str:
        out = []
        for p in self.phones:
            label = "[основний]" if p.is_main else ""
            out.append(f"{label} {p.number}".strip())
        return "; ".join(out)

# --- Приклад використання ---
contact = Contact(name="Ivan Petrenko")
print(contact.add_phone("(+38) 0958767347", main=True))
print(contact.add_phone("380668888777"))
print(contact.list_phones())  # [основний] +380958767347; +380668888777
print(contact.set_main_phone("380668888777"))
print(contact.list_phones())
print(contact.add_phone("abc123")) # некоректний

# --- Unit-тест ---
def test_phone_dataclass():
    ph = Phone("(+38) 0958767347", is_main=True)
    assert ph.is_valid()
    assert ph.number == "+380958767347"
    bad_ph = Phone("123abc")
    assert not bad_ph.is_valid()
    c = Contact("Test User")
    assert "додано" in c.add_phone("+48600111222")
    c.set_main_phone("+48600111222")
    assert c.phones[0].is_main