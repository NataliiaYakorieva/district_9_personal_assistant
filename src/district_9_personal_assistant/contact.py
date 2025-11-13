from dataclasses import dataclass, field
from typing import List

import questionary

from .phone import Phone
from .note import Note
from .email import Email
from .address import Address
from .field import BaseField
from .name import Name


@dataclass
class Contact:
    name: Name
    phones: List[Phone] = field(default_factory=list)
    notes: List[Note] = field(default_factory=list)
    emails: List[Email] = field(default_factory=list)
    addresses: List[Address] = field(default_factory=list)

    def add_field(self, field_instance: BaseField):
        """Adds a field (Phone, Email, Address, Note) to the contact."""
        try:
            field_instance.validate()
            if isinstance(field_instance, Phone):
                if field_instance.is_main:
                    self._reset_main_phone()
                self.phones.append(field_instance)
            elif isinstance(field_instance, Email):
                self.emails.append(field_instance)
            elif isinstance(field_instance, Address):
                self.addresses.append(field_instance)
            elif isinstance(field_instance, Note):
                self.notes.append(field_instance)
            else:
                raise TypeError("Unsupported field type")
            return f"{field_instance.__class__.__name__} added successfully."
        except (ValueError, TypeError) as e:
            return f"Error adding field: {e}"

    @staticmethod
    def _select_note_interactively(matches):
        choices = [
            f"{idx}: {note.title or note.content[:20]}" for idx, note in matches]
        selected = questionary.select("Select note:", choices=choices).ask()
        if not selected:
            return None
        selected_idx = int(selected.split(":")[0])
        for idx, note in matches:
            if idx == selected_idx:
                return note
        return None

    @staticmethod
    def _require_note(func):
        def wrapper(self, *args, **kwargs):
            note = self.find_note()
            if note is None:
                return "No matching note found."
            return func(self, note, *args, **kwargs)
        return wrapper

    @staticmethod
    def _select_phone_interactively(phones):
        choices = [
            f"{idx}: {
                phone.number}" for idx,
            phone in enumerate(phones)]
        selected = questionary.select("Select phone:", choices=choices).ask()
        if not selected:
            return None
        selected_idx = int(selected.split(":")[0])
        return phones[selected_idx]

    @staticmethod
    def _require_phone(func):
        def wrapper(self, *args, **kwargs):
            phone = self.find_phone()
            if phone is None:
                return "No matching phone found."
            return func(self, phone, *args, **kwargs)
        return wrapper

    def find_phone(self):
        """
        Find a phone by interactive selection.
        """
        if not self.phones:
            return None
        return self._select_phone_interactively(self.phones)

    @_require_phone
    def edit_phone(self, phone: Phone):
        """Edit the selected phone."""
        new_number = questionary.text("New phone number:", default=phone.number).ask()
        try:
            phone.update({"number": new_number})
            return f"Phone number updated to {phone.number}."
        except ValueError as e:
            return f"Error: {e}"

    @_require_phone
    def delete_phone(self, phone):
        self.phones.remove(phone)
        return f"Phone {phone.number} deleted from contact {self.name}."

    def add_phone(self) -> str:
        phone_number = questionary.text(
            "Phone number:",
            instruction="[International phone number, 8–15 digits, example: +4912345678901]"
        ).ask()
        is_main = questionary.confirm("Is this the main number?").ask()
        try:
            phone = Phone(number=phone_number, is_main=is_main)
            if phone.is_main:
                self._reset_main_phone()
            self.phones.append(phone)
            return f"Phone {phone.number} added to contact {self.name}."
        except ValueError as e:
            return f"Error adding phone: {e}"

    def _reset_main_phone(self):
        for p in self.phones:
            p.is_main = False

    @_require_phone
    def set_main_phone(self, phone):
        """
        Set a phone number as the main phone.
        """
        self._reset_main_phone()
        phone.is_main = True
        return f"Main number is set to: {phone.number}"

    def show_phones(self) -> str:
        """
        Show all phone numbers for the contact.
        """
        if not self.phones:
            return "No phones found."
        out = []
        for p in self.phones:
            label = "[main]" if p.is_main else ""
            out.append(f"{label} {p.number}".strip())
        return "; ".join(out)

    @staticmethod
    def _select_email_interactively(emails):
        choices = [
            f"{idx}: {
                email.address}" for idx,
            email in enumerate(emails)]
        selected = questionary.select("Select email:", choices=choices).ask()
        if not selected:
            return None
        selected_idx = int(selected.split(":")[0])
        return emails[selected_idx]

    @staticmethod
    def _require_email(func):
        def wrapper(self, *args, **kwargs):
            email = self.find_email()
            if email is None:
                return "No matching email found."
            return func(self, email, *args, **kwargs)
        return wrapper

    def find_email(self):
        """
        Find an email by interactive selection.
        """
        if not self.emails:
            return None
        return self._select_email_interactively(self.emails)

    @_require_email
    def edit_email(self, email: Email):
        """Edit the selected email."""
        new_address = questionary.text("New email address:", default=email.address).ask()
        try:
            email.update({"address": new_address})
            return f"Email updated to {email.address}."
        except ValueError as e:
            return f"Error: {e}"

    @_require_email
    def delete_email(self, email):
        self.emails.remove(email)
        return f"Email {email.address} deleted from contact {self.name}."

    def add_email(self) -> str:
        email_address = questionary.text("Email address:").ask().lower()
        try:
            email = Email(address=email_address)
            self.emails.append(email)
            return f"Email {email.address} added to contact {self.name}."
        except ValueError as e:
            return f"Error adding email: {e}"

    def show_emails(self) -> str:
        """
        Show all email addresses for the contact.
        """
        if not self.emails:
            return "No emails found."
        return "; ".join(email.address for email in self.emails)

    @_require_email
    def set_main_email(self, email):
        """
        Set an email address as the main email for the contact.
        """
        for e in self.emails:
            e.is_main = False
        email.is_main = True
        return f"Main email set to {email.address} for contact {self.name}."

    def show_notes(self) -> str:
        """
        Show all notes for the contact.
        """
        if not self.notes:
            return "No notes available."
        out = []
        for note in self.notes:
            out.append(f"\n{note}\n")
        return "All notes:\n".join(out)

    def add_note(self):
        title = questionary.text("Title:").ask()
        content = questionary.text("Content:").ask()
        tags = questionary.text("Tags (comma separated):").ask()
        try:
            note = Note(content, title, tags)
            self.notes.append(note)
            return "Note added."
        except ValueError as e:
            return f"Error adding note: {e}"

    def find_note(self):
        query = questionary.text(
            "Enter search query (text, tag, or title):").ask().strip().lower()
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

        note = self._select_note_interactively(matches)
        return note

    @_require_note
    def edit_note(self, note: Note):
        """Edit the selected note."""
        new_data = {
            "title": questionary.text("New title:", default=note.title).ask(),
            "content": questionary.text("New content:", default=note.content).ask(),
            "tags_string": questionary.text(
                "New tags (comma-separated):", default=note.tags_string).ask(),
        }
        try:
            note.update(new_data)
            return "Note updated successfully."
        except ValueError as e:
            return f"Error: {e}"

    @_require_note
    def delete_note(self, note):
        self.notes.remove(note)
        return "Note deleted."

    def find_by_tag(self) -> str:
        """
        Prompt for a tag and find notes containing the specified tag (case-insensitive).
        Returns a message if nothing is found.
        """
        tag = questionary.text(
            "Enter tag to search for:").ask().lower().strip()
        if not tag:
            return "No tag entered."
        found_notes = [
            note for note in self.notes if tag in [
                t.lower() for t in note.get_tags_list()]]
        if not found_notes:
            return "No notes found with this tag."
        return "\n".join(f"{str(note)}\n" for note in found_notes)

    @staticmethod
    def _select_address_interactively(addresses):
        choices = [
            f"{idx}: {address}" for idx,
            address in enumerate(addresses)]
        selected = questionary.select("Select address:", choices=choices).ask()
        if not selected:
            return None
        selected_idx = int(selected.split(":")[0])
        return addresses[selected_idx]

    @staticmethod
    def _require_address(func):
        def wrapper(self, *args, **kwargs):
            address = self.find_address()
            if address is None:
                return "No matching address found."
            return func(self, address, *args, **kwargs)
        return wrapper

    def find_address(self):
        """
        Find an address by interactive selection.
        """
        if not self.addresses:
            return None
        return self._select_address_interactively(self.addresses)

    @_require_address
    def edit_address(self, address: Address):
        """Edit the selected address."""
        new_data = {
            "country": questionary.text("New country:", default=address.country).ask(),
            "city": questionary.text("New city:", default=address.city).ask(),
            "street_address": questionary.text(
                "New street address:", default=address.street_address).ask(),
            "zip_code": questionary.text("New zip code:", default=address.zip_code).ask(),
        }
        try:
            address.update(new_data)
            return f"Address updated to {address}."
        except ValueError as e:
            return f"Error: {e}"

    @_require_address
    def delete_address(self, address):
        self.addresses.remove(address)
        return f"Address '{address}' deleted from contact {self.name}."

    def add_address(self) -> str:
        """
        Add an address to the contact.
        """
        country = questionary.text("Country:").ask()
        city = questionary.text("City:").ask()
        street_address = questionary.text("Street address:").ask()
        zip_code = questionary.text("Zip code:").ask()
        try:
            address = Address(
                country=country,
                city=city,
                street_address=street_address,
                zip_code=zip_code
            )
            self.addresses.append(address)
            return f"Address '{address}' added to contact {self.name}."
        except ValueError as e:
            return f"Error adding address: {e}"

    def show_addresses(self) -> str:
        """
        Show all addresses for the contact.
        """
        if not self.addresses:
            return "No addresses found."
        return "; ".join(str(address) for address in self.addresses)

    @_require_address
    def set_main_address(self, address):
        """
        Set an address as the main address for the contact.
        """
        for a in self.addresses:
            a.is_main = False
        address.is_main = True
        return f"Main address set to {address} for contact {self.name}."
