# address.py
from __future__ import annotations

import json
import re
import sys
import webbrowser
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple

from urllib.parse import quote_plus
import pickle

#  Шляхи до файлів БД
DB_JSON = Path(__file__).with_name("addresses.json")
DB_PKL = Path(__file__).with_name("addresses.pkl")

#  Модель адресної картки
ZIP_RE = re.compile(r"^[\w\- ]{3,10}$", re.IGNORECASE)


@dataclass
class AddressCard:
    first_name: str
    last_name: str
    phone: str
    country: str
    city: str
    street_address: str
    zip_code: str

    # Нормалізація + валідація
    def __post_init__(self) -> None:
        for f in (
                "first_name",
                "last_name",
                "phone",
                "country",
                "city",
                "street_address",
                "zip_code",
        ):
            val = getattr(self, f)
            if not isinstance(val, str):
                raise TypeError(f"Поле '{f}' має бути рядком.")
            val = val.strip()
            if not val:
                raise ValueError(f"Поле '{f}' не може бути порожнім.")
            setattr(self, f, val)

        if not ZIP_RE.match(self.zip_code):
            raise ValueError("Невалідний поштовий індекс (zip_code).")

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def to_google_maps_url(self) -> str:
        query = f"{self.street_address}, {self.city}, {self.zip_code}, {self.country}"
        return f"https://www.google.com/maps/search/?api=1&query={quote_plus(query)}"

    def pretty(self) -> str:
        return (
            f"{self.full_name()} | tel: {self.phone} | "
            f"{self.street_address}, {self.city}, {self.zip_code}, {self.country}"
        )


# Ключ у БД — стабільний, щоб легко оновлювати/видаляти:
def make_key(card: AddressCard) -> str:
    # Наприклад: "Olga Kosa|0674300702"
    return f"{card.full_name()}|{card.phone}"


#  Завантаження / збереження
def load_db() -> Dict[str, AddressCard]:
    # 1) Читаємо JSON
    if DB_JSON.exists():
        try:
            data = json.loads(DB_JSON.read_text(encoding="utf-8"))
            return {k: AddressCard(**v) for k, v in data.items()}
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            # пошкоджений JSON, невірні типи або проблеми з файлом — пробуємо PKL
            pass

    # 2) Читаємо PKL
    if DB_PKL.exists():
        try:
            raw = DB_PKL.read_bytes()
            data = pickle.loads(raw)
            if isinstance(data, dict):
                out: Dict[str, AddressCard] = {}
                for k, v in data.items():
                    if isinstance(v, AddressCard):
                        out[k] = v
                    else:
                        out[k] = AddressCard(**v)  # type: ignore[arg-type]
                return out
        except (pickle.UnpicklingError, OSError, AttributeError, TypeError, ValueError):
            # пошкоджений pkl або невідповідні дані — повернемо порожню БД
            pass

    return {}


def save_db(db: Dict[str, AddressCard]) -> None:
    # JSON
    as_json = {k: asdict(v) for k, v in db.items()}
    DB_JSON.write_text(json.dumps(as_json, ensure_ascii=False, indent=2), encoding="utf-8")

    # PKL (одночасно)
    DB_PKL.write_bytes(pickle.dumps(db))


#  Допоміжні I/O
def prompt(label: str) -> str:
    return input(label).strip()


def print_help() -> None:
    print(
        "Команди:\n"
        "  add            — додати нову адресу\n"
        "  update         — оновити існуючу адресу (за ПІБ + телефон)\n"
        "  delete         — видалити запис (за ПІБ + телефон)\n"
        "  list           — показати всі записи\n"
        "  find           — пошук за ім'ям/прізвищем і (за бажанням) відкриття на мапі\n"
        "  help           — довідка\n"
        "  exit / close   — вихід і збереження\n"
    )


#  Команди
def add_cmd(db: Dict[str, AddressCard]) -> None:
    print("\n=== Додавання адреси ===")
    first = prompt("Ім'я: ")
    last = prompt("Прізвище: ")
    phone = prompt("Телефон: ")
    country = prompt("Країна: ")
    city = prompt("Місто: ")
    street = prompt("Вулиця + будинок: ")
    zip_code = prompt("Поштовий індекс: ")

    try:
        card = AddressCard(
            first_name=first,
            last_name=last,
            phone=phone,
            country=country,
            city=city,
            street_address=street,
            zip_code=zip_code,
        )
    except Exception as e:
        print(f" {e}")
        return

    key = make_key(card)
    if key in db:
        print(" Такий запис уже існує — буде перезаписано.")
    db[key] = card
    save_db(db)
    print(" Збережено.")


def update_cmd(db: Dict[str, AddressCard]) -> None:
    print("\n=== Оновлення адреси ===")
    query = input("Введи ім'я, прізвище або телефон (можна частково): ").strip().lower()

    if not query:
        print(" Порожній запит. Скасовано.")
        return

    # знайти збіги частково
    matches: List[Tuple[str, AddressCard]] = []
    for key, card in db.items():
        if (
                query in card.first_name.lower()
                or query in card.last_name.lower()
                or query in card.phone
        ):
            matches.append((key, card))

    if not matches:
        print(" Запис не знайдено.")
        return

    if len(matches) == 1:
        key, card = matches[0]
    else:
        print("Знайдено кілька записів:")
        for i, (_, card) in enumerate(matches, 1):
            print(f"{i}. {card.first_name} {card.last_name} | tel: {card.phone} | "
                  f"{card.street_address}, {card.city}, {card.zip_code}, {card.country}")
        choice = input("Вибери номер запису для оновлення або Enter, щоб скасувати: ").strip()
        if not choice:
            print(" Скасовано.")
            return
        try:
            index = int(choice) - 1
            if index < 0 or index >= len(matches):
                raise ValueError
        except ValueError:
            print(" Некоректний номер.")
            return
        key, card = matches[index]

    print(f"\nПоточний запис:\n{card.first_name} {card.last_name} | tel: {card.phone}\n"
          f"{card.street_address}, {card.city}, {card.zip_code}, {card.country}")

    print("\nВведи нові дані (Enter — залишити без змін):")
    new_country = input(f"Країна [{card.country}]: ").strip() or card.country
    new_city = input(f"Місто [{card.city}]: ").strip() or card.city
    new_street = input(f"Адреса [{card.street_address}]: ").strip() or card.street_address
    new_zip = input(f"Поштовий індекс [{card.zip_code}]: ").strip() or card.zip_code

    confirm = input("\nПідтвердити оновлення? (так/ні): ").strip().lower()
    if confirm not in ("так", "y", "yes"):
        print(" Скасовано.")
        return

    card.country = new_country
    card.city = new_city
    card.street_address = new_street
    card.zip_code = new_zip

    db[key] = card
    save_db(db)
    print(" Запис оновлено.")


def delete_cmd(db: Dict[str, AddressCard]) -> None:
    print("\n=== Видалення запису ===")
    query = input("Введи ім'я, прізвище або телефон (можна частково): ").strip().lower()

    if not query:
        print(" Порожній запит. Скасовано.")
        return

    # знайдемо усі збіги
    matches = []
    for key, card in db.items():
        if (
                query in card.first_name.lower()
                or query in card.last_name.lower()
                or query in card.phone
        ):
            matches.append((key, card))

    if not matches:
        print(" Запис не знайдено.")
        return

    if len(matches) == 1:
        key, card = matches[0]
        print(f"Знайдено: {card.first_name} {card.last_name} | tel: {card.phone} | "
              f"{card.street_address}, {card.city}, {card.zip_code}, {card.country}")
        confirm = input("Видалити цей запис? (так/ні): ").strip().lower()
        if confirm in ("так", "y", "yes"):
            del db[key]
            save_db(db)
            print("Запис видалено.")
        else:
            print("Скасовано.")
        return

    print("Знайдено кілька записів:")
    for i, (_, card) in enumerate(matches, 1):
        print(f"{i}. {card.first_name} {card.last_name} | tel: {card.phone} | "
              f"{card.street_address}, {card.city}, {card.zip_code}, {card.country}")

    choice = input("Введи номер запису для видалення або Enter, щоб скасувати: ").strip()
    if not choice:
        print("Скасовано.")
        return

    try:
        index = int(choice) - 1
        if index < 0 or index >= len(matches):
            raise ValueError
    except ValueError:
        print("Некоректний номер.")
        return

    key, card = matches[index]
    confirm = input(f"Підтвердити видалення '{card.first_name} {card.last_name}'? (так/ні): ").strip().lower()
    if confirm in ("так", "да", "yes"):
        del db[key]
        save_db(db)
        print(" Запис видалено.")
    else:
        print(" Скасовано.")


def list_cmd(db: Dict[str, AddressCard]) -> None:
    print("\n=== Усі записи ===")
    if not db:
        print("Поки порожньо.")
        return
    for c in db.values():
        print("-", c.pretty())


def find_cmd(db: Dict[str, AddressCard]) -> None:
    """
    Пошук лише за ім'ям/прізвищем.
    Якщо рівно 1 збіг — запит 'Відкрити на мапі? (так/ні):' і відкриття Google Maps.
    Якщо 0 — повідомлення. Якщо >1 — показ списку без вибору номерів.
    """
    print("\n=== Пошук за ім'ям/прізвищем ===")
    query = prompt("Введи ім'я та/або прізвище (можна частково): ").lower()
    if not query:
        print(" Порожній запит.")
        return

    matches: List[AddressCard] = []
    for card in db.values():
        if query in card.full_name().lower():
            matches.append(card)

    if not matches:
        print("Нічого не знайдено.")
        return

    if len(matches) > 1:
        print("Знайдено кілька записів. Уточни, будь ласка, запит:")
        for c in matches:
            print("-", c.pretty())
        return

    card = matches[0]
    print("Знайдено:")
    print(card.pretty())

    ans = prompt("Відкрити на мапі? (так/ні): ").lower()
    if ans in ("так", "taк", "да", "yes", "y"):
        url = card.to_google_maps_url()
        print("Відкриваю карту…", url)
        webbrowser.open(url)
    else:
        print("Ок, карту не відкриваю.")


#  Головний цикл
def main() -> None:
    db = load_db()
    if "--reset" in sys.argv:
        db.clear()
        save_db(db)
        print("Базу очищено.")
        return

    print("Персональний помічник адрес запущено. Введи 'help' для довідки.")
    while True:
        cmd = prompt("> ").lower()
        if cmd in ("exit", "close"):
            save_db(db)
            print("До зустрічі!")
            break
        elif cmd == "help":
            print_help()
        elif cmd == "add":
            add_cmd(db)
        elif cmd == "update":
            update_cmd(db)
        elif cmd == "delete":
            delete_cmd(db)
        elif cmd == "list":
            list_cmd(db)
        elif cmd == "find":
            find_cmd(db)
        elif cmd == "":
            continue
        else:
            print("Невідома команда. Введи 'help'.")


if __name__ == "__main__":
    main()
