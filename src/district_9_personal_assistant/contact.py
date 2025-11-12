from dataclasses import dataclass, field
from typing import List
from .phone import Phone, normalize_phone
from .note import Note
import readchar
from datetime import datetime, date, timedelta


@dataclass
class Contact:
    name: str
    phones: List[Phone] = field(default_factory=list)
    notes: List[Note] = field(default_factory=list)

    def add_phone(self, phone_number: str, main: bool = False) -> str:
        phone = Phone(number=phone_number, is_main=main)
        if not phone.is_valid():
            return f"Invalid phone number: {phone_number}"
        if phone.is_main:
            self.reset_main_phone()
        self.phones.append(phone)
        return f"Phone {phone.number} added to contact {self.name}."

    def reset_main_phone(self):
        for p in self.phones:
            p.is_main = False

    def set_main_phone(self, phone_number: str) -> str:
        normalized = normalize_phone(phone_number)
        found = False
        for p in self.phones:
            if p.number == normalized:
                self.reset_main_phone()
                p.is_main = True
                found = True
                break
        if found:
            return f"Main number is set to: {normalized}"
        else:
            return f"Number {normalized} is not found in contact {self.name}."

    def show_phones(self) -> str:
        out = []
        for p in self.phones:
            label = "[main]" if p.is_main else ""
            out.append(f"{label} {p.number}".strip())
        return "; ".join(out)

    def show_notes(self) -> str:
        if not self.notes:
            return "No notes available."
        out = []
        for note in self.notes:
            out.append(f"All notes:\n{note}\n")
        return "\n".join(out)

    @staticmethod
    def require_note(func):
        def wrapper(self, *args, **kwargs):
            note = self.find_note()
            if note is None:
                return "No matching note found."
            return func(self, note, *args, **kwargs)
        return wrapper

    @staticmethod
    def select_note_interactively(matches):
        print("Use ↑/↓ arrows to navigate, SPACE to select a note.")
        selected = 0
        while True:
            for i, (idx, note) in enumerate(matches):
                prefix = "-> " if i == selected else "   "
                print(f"{prefix}{i}: [{idx}] {note}")
            key = readchar.readkey()
            if key == readchar.key.UP:
                selected = (selected - 1) % len(matches)
            elif key == readchar.key.DOWN:
                selected = (selected + 1) % len(matches)
            elif key == readchar.key.SPACE:
                # Move cursor up to overwrite
                print("\033[F" * (len(matches) + 1))
                return matches[selected][1]
            print("\033[F" * (len(matches) + 1))  # Move cursor up to overwrite

    def add_note(self):
        title = input("Note title: ")
        content = input("Note content: ")
        tags = input("Tags (comma separated): ")
        note = Note(content, title, tags)
        self.notes.append(note)
        return "Note added."

    def list_notes(self):
        notes = self.notes
        if not notes:
            return "No notes found."
        return "\n".join(str(note) for note in notes)

    def find_note(self):
        query = input(
            "Enter search query (text, tag, or title): ").strip().lower()
        matches = []
        for idx, note in enumerate(self.notes):
            if (
                    query in note.content.lower()
                    or query in note.title.lower()
                    or any(query in tag for tag in note.get_tags_list())
            ):
                matches.append((idx, note))
        if not matches:
            return None
        if len(matches) == 1:
            return matches[0][1]

        return self.select_note_interactively(matches)

    @require_note
    def edit_note(self, note):
        print('Title:\n')
        new_title = input(note.title)
        print('Content:\n')
        new_content = input(note.content)
        print('Tags (comma separated):\n')
        new_tags = input(', '.join(note.tags_list))

        note.edit_content(new_content)
        note.edit_title(new_title)
        note.add_tags(new_tags)

        return "Note updated."

    @require_note
    def delete_note(self, note):
        self.notes.remove(note)
        return "Note deleted."


class Birthday:
   
    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, birthday_str: str):
        self._birthday = None
        if birthday_str:
            self._birthday = self._validate_date(birthday_str)

    def _validate_date(self, date_str: str) -> date:
        try:
            birth_date = datetime.datetime.strptime(date_str, self.DATE_FORMAT).date()
            
            if birth_date > date.today():
                raise ValueError("Birthday cannot be in future.")
            return birth_date
        except ValueError as e:
            raise ValueError (f"Data format is incorrect: '{date_str}'. Please use the next format DD.MM.YYYY. {e}")

    @property
    def age(self) -> int:
        today = date.today()
        age = today.year - self.birthday.year
        if today < self.birthday.replace(year=today.year):
            age -= 1
        return age

    @property
    def has_had_birthday_this_year(self) -> bool:
        today = date.today()
        this_year_bday = self.birthday.replace(year=today.year)
        return today >= this_year_bday

    def find_birthdays_this_week(contacts: dict[str, str]) -> dict[str, date]:
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        birthdays_this_week = {}
        
        for name, bday_str in contacts.items():
            try:
                bday_obj = datetime.datetime.strptime(bday_str, Birthday.DATE_FORMAT).date()
                next_bday = bday_obj.replace(year=today.year)
                if next_bday < today:
                    next_bday = bday_obj.replace(year=today.year + 1)
                
                if start_of_week <= next_bday <= end_of_week:
                    birthdays_this_week[name] = next_bday

            except ValueError:
                print(f"Exeption: The format date is incorrect {name}: {bday_str}")
                continue

        return birthdays_this_week
    
    def add_birthday(contacts: dict[str, str], name: str, birthday_str: str) -> None:
        try:
            birth_date = datetime.datetime.strptime(birthday_str, Birthday.DATE_FORMAT).date()
            if birth_date > date.today():
                raise ValueError("Birthday cannot be in future.")
            contacts[name] = birthday_str
        except ValueError as e:
            raise ValueError(f"Cannot add birthday for '{name}': {e}")