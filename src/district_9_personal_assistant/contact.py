from dataclasses import dataclass, field
from typing import List
from .phone import Phone, normalize_phone
from .note import Note
from .Email import Email
import readchar


@dataclass
class Contact:
    name: str
    phones: List[Phone] = field(default_factory=list)
    notes: List[Note] = field(default_factory=list)
    emails: List[Email] = field(default_factory=list)

    def add_phone(self) -> str:
        phone_number = input("Phone number: ")
        input_main = input("Is this the main number? (y/n): ").strip().lower()
        main = input_main == 'y'
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

    def set_main_phone(self) -> str:
        phone_number = input("Phone number to set as main: ")
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

    def add_email(self) -> str:
        email_address = input("Email address: ").lower()
        email = Email(address=email_address)
        self.emails.append(email)
        return f"Email {email.address} added to contact {self.name}."

    def change_email(self) -> str:
        old_email = input("Old email address: ").lower()
        new_email = input("New email address: ").lower()
        if not self.emails:
            return f"No emails found for contact {self.name}."

        for i, email in enumerate(self.emails):
            if email.address == old_email:
                new_email_obj = Email(address=new_email)
                self.emails[i] = new_email_obj
                return (f"Email changed from {old_email} to {new_email} "
                        f"for contact {self.name}.")
        return f"Email {old_email} not found in contact {self.name}."

    def remove_email(self) -> str:
        email_address = input("Email address to remove: ").lower()
        if not self.emails:
            return f"No emails found for contact {self.name}."

        for email in self.emails:
            if email.address == email_address:
                self.emails.remove(email)
                return f"Email {email_address} removed from contact {
                    self.name}."
        return f"Email {email_address} not found in contact {self.name}."

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
