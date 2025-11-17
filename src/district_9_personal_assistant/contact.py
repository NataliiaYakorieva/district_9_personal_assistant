from dataclasses import dataclass, field
from typing import List, Optional, Callable

import questionary

from src.district_9_personal_assistant.phone import Phone
from src.district_9_personal_assistant.note import Note
from src.district_9_personal_assistant.email import Email
from src.district_9_personal_assistant.address import Address
from src.district_9_personal_assistant.field import BaseField
from src.district_9_personal_assistant.name import Name
from src.district_9_personal_assistant.selection import Selection
from src.district_9_personal_assistant.helpers.message import fail_message, success_message
from src.district_9_personal_assistant.birthday import Birthday


@dataclass
class Contact(Selection):
    """
    Represents a contact with fields for name, phones, notes, emails, addresses, and birthday.
    """
    name: Name
    phones: List[Phone] = field(default_factory=list)
    notes: List[Note] = field(default_factory=list)
    emails: List[Email] = field(default_factory=list)
    addresses: List[Address] = field(default_factory=list)
    birthday: Optional[Birthday] = None

    def add_field(self, field_instance: BaseField) -> str:
        """
        Adds a field (Phone, Email, Address, Note) to the contact.
        Returns a success or failure message.
        """
        try:
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
            return success_message(f"{field_instance.__class__.__name__} added successfully.")
        except (ValueError, TypeError) as e:
            return fail_message(f"Error adding field: {e}")

    @staticmethod
    def _require_note(func: Callable) -> Callable:
        """
        Decorator to ensure a note is selected before proceeding.
        """

        def wrapper(self, *args, **kwargs):
            note = self.find_note(True)
            if note is None:
                return fail_message("No matching note found.")
            return func(self, note, *args, **kwargs)
        return wrapper

    @staticmethod
    def _require_phone(func: Callable) -> Callable:
        """
        Decorator to ensure a phone is selected before proceeding.
        """

        def wrapper(self, *args, **kwargs):
            phone = self.find_phone()
            if phone is None:
                return fail_message("No matching phone found.")
            return func(self, phone, *args, **kwargs)
        return wrapper

    def find_phone(self) -> Optional[Phone]:
        """
        Find a phone number interactively (with selection).
        """
        return self.select_item_interactively(
            self.phones,
            lambda p: p.number,
            "Select phone:",
        )

    @_require_phone
    def edit_phone(self, phone: Phone) -> str:
        """
        Edit the selected phone.
        """
        new_number = questionary.text("New phone number:", default=phone.number).ask()
        try:
            phone.update({"number": new_number})
            return success_message(f"Phone number updated to {phone.number}.")
        except ValueError as e:
            return fail_message(f"Error: {e}")

    @_require_phone
    def delete_phone(self, phone: Phone) -> str:
        """
        Delete the selected phone.
        """
        self.phones.remove(phone)
        return success_message(f"Phone {phone.number} deleted from contact {self.name}.")

    def add_phone(self) -> str:
        """
        Add a phone number to the contact.
        """
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
            return success_message(f"Phone {phone.number} added to contact {self.name}.")
        except ValueError as e:
            return fail_message(f"Error adding phone: {e}")

    def _reset_main_phone(self) -> None:
        """
        Reset the main phone flag for all phones.
        """
        for p in self.phones:
            p.is_main = False

    @_require_phone
    def set_main_phone(self, phone: Phone) -> str:
        """
        Set a phone number as the main phone.
        """
        self._reset_main_phone()
        phone.is_main = True
        return success_message(f"Main number is set to: {phone.number}")

    def show_phones(self) -> str:
        """
        Show all phone numbers for the contact.
        """
        if not self.phones:
            return fail_message("No phones found.")
        out = []
        for p in self.phones:
            label = "[main]" if p.is_main else ""
            out.append(f"{label} {p.number}".strip())
        return "; ".join(out)

    @staticmethod
    def _require_email(func: Callable) -> Callable:
        """
        Decorator to ensure an email is selected before proceeding.
        """

        def wrapper(self, *args, **kwargs):
            email = self.find_email()
            if email is None:
                return fail_message("No matching email found.")
            return func(self, email, *args, **kwargs)
        return wrapper

    def find_email(self) -> Optional[Email]:
        """
        Find an email address interactively (with selection).
        """
        return self.select_item_interactively(
            self.emails,
            lambda e: e.address,
            "Select email:",
        )

    @_require_email
    def edit_email(self, email: Email) -> str:
        """
        Edit the selected email.
        """
        new_address = questionary.text("New email address:", default=email.address).ask()
        try:
            email.update({"address": new_address})
            return success_message(f"Email updated to {email.address}.")
        except ValueError as e:
            return fail_message(f"Error: {e}")

    @_require_email
    def delete_email(self, email: Email) -> str:
        """
        Delete the selected email.
        """
        self.emails.remove(email)
        return success_message(f"Email {email.address} deleted from contact {self.name}.")

    def add_email(self) -> str:
        """
        Add an email address to the contact.
        """
        email_address = questionary.text("Email address:").ask().lower()
        try:
            email = Email(address=email_address)
            self.emails.append(email)
            return success_message(f"Email {email.address} added to contact {self.name}.")
        except ValueError as e:
            return fail_message(f"Error adding email: {e}")

    def show_emails(self) -> str:
        """
        Show all email addresses for the contact.
        """
        if not self.emails:
            return fail_message("No emails found.")
        return "; ".join(email.address for email in self.emails)

    @_require_email
    def set_main_email(self, email: Email) -> str:
        """
        Set an email address as the main email for the contact.
        """
        for e in self.emails:
            e.is_main = False
        email.is_main = True
        return success_message(f"Main email set to {email.address} for contact {self.name}.")

    def show_notes(self) -> str:
        """
        Show all notes for the contact.
        """
        if not self.notes:
            return fail_message("No notes available.")
        out = []
        for note in self.notes:
            out.append(f"\n{note}\n")
        return "All notes:\n".join(out)

    def add_note(self) -> str:
        """
        Add a note to the contact.
        """
        title = questionary.text("Title:").ask()
        content = questionary.text("Content:").ask()
        tags = questionary.text("Tags (comma separated):").ask()
        try:
            note = Note(content, title, tags)
            self.notes.append(note)
            return success_message("Note added.")
        except ValueError as e:
            return fail_message(f"Error adding note: {e}")

    def find_note(self, used_for_selection: bool = False) -> Optional[Note]:
        """
        Find a note interactively (with selection).
        """
        if not self.notes and not used_for_selection:
            return fail_message("No notes available.")

        def display_note(note: Note) -> str:
            return note.title or note.content[:20]
        return self.select_item_interactively(
            self.notes,
            display_note,
            "Select note:",
        )

    @_require_note
    def edit_note(self, note: Note) -> str:
        """
        Edit the selected note.
        """
        new_data = {
            "title": questionary.text("New title:", default=note.title).ask(),
            "content": questionary.text("New content:", default=note.content).ask(),
            "tags_string": questionary.text(
                "New tags (comma-separated):", default=note.tags_string).ask(),
        }
        try:
            note.update_note(**new_data)
            return success_message("Note updated successfully.")
        except ValueError as e:
            return fail_message(f"Error: {e}")

    @_require_note
    def delete_note(self, note: Note) -> str:
        """
        Delete the selected note.
        """
        self.notes.remove(note)
        return success_message("Note deleted.")

    def find_by_tag(self) -> str:
        """
        Prompt for a tag and find notes containing the specified tag (case-insensitive).
        Returns a message if nothing is found.
        """
        tag = questionary.text(
            "Enter tag to search for:").ask().lower().strip()
        if not tag:
            return fail_message("No tag entered.")
        elif not self.notes:
            return fail_message("No notes available.")

        found_notes = [
            note for note in self.notes if tag in [
                t.lower() for t in note.get_tags_list()]]
        if not found_notes:
            return fail_message("No notes found with this tag.")
        return "\n".join(f"{str(note)}\n" for note in found_notes)

    @staticmethod
    def _require_address(func: Callable) -> Callable:
        """
        Decorator to ensure an address is selected before proceeding.
        """

        def wrapper(self, *args, **kwargs):
            address = self.find_address()
            if address is None:
                return fail_message("No matching address found.")
            return func(self, address, *args, **kwargs)
        return wrapper

    def find_address(self) -> Optional[Address]:
        """
        Find an address interactively (with selection).
        """
        return self.select_item_interactively(
            self.addresses,
            str,
            "Select address:",
        )

    @_require_address
    def edit_address(self, address: Address) -> str:
        """
        Edit the selected address.
        """
        new_data = {
            "country": questionary.text("New country:", default=address.country).ask(),
            "city": questionary.text("New city:", default=address.city).ask(),
            "street_address": questionary.text(
                "New street address:", default=address.street_address).ask(),
            "zip_code": questionary.text("New zip code:", default=address.zip_code).ask(),
        }
        try:
            address.update(new_data)
            return success_message(f"Address updated to {address}.")
        except ValueError as e:
            return fail_message(f"Error: {e}")

    @_require_address
    def delete_address(self, address: Address) -> str:
        """
        Delete the selected address.
        """
        self.addresses.remove(address)
        return success_message(f"Address '{address}' deleted from contact {self.name}.")

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
            return success_message(f"Address '{address}' added to contact {self.name}.")
        except ValueError as e:
            return fail_message(f"Error adding address: {e}")

    def show_addresses(self) -> str:
        """
        Show all addresses for the contact.
        """
        if not self.addresses:
            return fail_message("No addresses found.")
        return "; ".join(str(address) for address in self.addresses)

    @_require_address
    def set_main_address(self, address: Address) -> str:
        """
        Set an address as the main address for the contact.
        """
        for a in self.addresses:
            a.is_main = False
        address.is_main = True
        return success_message(f"Main address set to {address} for contact {self.name}.")

    def add_birthday(self) -> str:
        """
        Add or update the birthday for this contact.
        """
        bday = questionary.text(
            "Set Birthday:",
            instruction="[Format: DD.MM.YYYY, e.g., 15.03.1990]"
        ).ask()
        try:
            birthday_obj = Birthday(value=bday)
            self.birthday = birthday_obj
            return success_message(
                f"Birthday set to {
                    birthday_obj.birthday.strftime(
                        Birthday.DATE_FORMAT)} for contact {
                    self.name.value}.")
        except ValueError as e:
            return fail_message(f"Cannot add birthday: {e}")

    def show_birthday(self) -> str:
        """
        Display the birthday and age for this contact.
        """
        if not self.birthday:
            return fail_message("No birthday set for this contact.")

        birthday_date = self.birthday.birthday.strftime(Birthday.DATE_FORMAT)
        age = self.birthday.age
        return success_message(f"{self.name.value}'s birthday is {birthday_date} (Age: {age})")

    @_require_address
    def open_in_google_maps(self, address: Address) -> None:
        """
        Open the main address in Google Maps.
        """
        address.open_in_google_maps()

    def __str__(self) -> str:
        lines = [
            f"Contact: {self.name.value}",
            f"Phones: {', '.join([str(p) for p in self.phones]) if self.phones else 'No phones'}",
            f"Emails: {', '.join([str(e) for e in self.emails]) if self.emails else 'No emails'}",
            (
                "Addresses: "
                + (", ".join(str(a) for a in self.addresses)
                   if self.addresses else "No addresses")
            ),
            (
                "Birthday: "
                + (self.birthday.birthday.strftime(self.birthday.DATE_FORMAT)
                   if self.birthday else "No birthday")
            ),
            f"Notes: {len(self.notes)} note(s)" if self.notes else "Notes: No notes"
        ]
        return "\n".join(lines)
